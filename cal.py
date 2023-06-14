# -*- coding: utf-8 -*-

# IMPORTS
from google_auth_oauthlib.flow import InstalledAppFlow as IAF
from discordTennisFunctions import getPlayerFromPlayerIdInDB
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from logs import printDetails, printLogs
import os.path as path
import schedule
import asyncio
import pickle
import logs
import DB


def getEvent(eventId):
  calendarId = DB.getCalendarID()
  service = build('calendar', 'v3', credentials=findCreds())
  event = service.events().get(calendarId=calendarId, eventId=eventId).execute()
  return event


def compare(eventInDB, eventInCal): #TODO
  event = generateEvent(eventInDB)
  if event['summary'] != eventInCal['summary'] or\
     event['description'] != eventInCal['description'] or\
     event['colorId'] != int(eventInCal['colorId']) or\
     event['start']['dateTime'] != eventInCal['start']['dateTime'][0:19] or\
     event['end']['dateTime'] != eventInCal['end']['dateTime'][0:19]:
    return True
  return False


def deleteEvent(eventId):
  calendarId = DB.getCalendarID()
  service = build('calendar', 'v3', credentials=findCreds())
  service.events().delete(calendarId=calendarId, eventId=eventId).execute()


def createEvent(event):
  calendarId = DB.getCalendarID()
  service = build('calendar', 'v3', credentials=findCreds())
  id = service.events().insert(calendarId=calendarId,
                               body=generateEvent(event),
                               sendNotifications=True).execute()["id"]
  return id


def generateEvent(event):
  player1 = getPlayerFromPlayerIdInDB(event[3])
  player2 = getPlayerFromPlayerIdInDB(event[4])
  timezone = "Europe/Paris"
  newEvent = {
    "summary": event[2],
    "description": "{} contre {} sur le terrain n°{}".format(
      player1, player2, event[7]),
    "colorId": getColor(event[1]),
    "start": {
      "dateTime": getStart(event[5], event[6]),
      "timeZone": timezone,
    },
    "end": {
      "dateTime": getEnd(event[5], event[6]),
      "timeZone": timezone,
    },
  }
  return newEvent


def getColor(category):
  if category == "SM": return 9
  if category == "SD": return 3
  if category == "DM": return 10
  if category == "DD": return 11
  if category == "DX": return 5
  return 8


def getStart(day, hour):
 d, m = day.split("/")
 h, min = hour.lower().split("h")
 if min == '' : min = "00"
 if len(h) == 1 : h = "0" + h
 return "2023-{}-{}T{}:{}:00".format(m, d, h, min)


def getEnd(day, hour):
 d, m = day.split("/")
 h, min = hour.lower().split("h")
 if min == '' : min = "00"
 h = int(h) + 1
 min = int(min) + 30
 if min > 59:
   h = h + 1
   min = min - 60
 h = str(h)
 min = str(min)
 if len(h) == 1 : h = "0" + h
 if len(min) == 1 : min = "0" + min
 return "2023-{}-{}T{}:{}:00".format(m, d, h, min)


def load(name):
  with open('DB/' + name + '.pkl', 'rb') as f:
    return pickle.load(f)


def findCreds():
  creds = None
  fileName = "tokenCalendar"
  if path.exists("DB/" + fileName + ".pkl"):
    creds = load(fileName)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      scopes = ['https://www.googleapis.com/auth/calendar']
      flow = IAF.from_client_secrets_file('DB/credentials.json', scopes)
      creds = flow.run_local_server(port=0)
    with open("DB/" + fileName + ".pkl", 'wb') as token:
      pickle.dump(creds, token)
  return creds


def update():
  printLogs(logs.CAL, logs.INFO, "Updating calendar")
  DB.setCalendarStatus(1)
  eventsInDB = DB.getMatchs()
  for eventInDB in eventsInDB:
    id = eventInDB[0]
    idCal = eventInDB[12]
    if(idCal != None):
      eventInCal = getEvent(idCal)
      diff = compare(eventInDB, eventInCal)
      if (diff):
        printDetails(logs.CAL, logs.INFO,
          "Modification in calendar of match {}".format(id))
        try:
          deleteEvent(idCal)
          idCal = createEvent(eventInDB)
          DB.updateEvent(id, idCal)
        except:
          printDetails(logs.CAL, logs.ERROR,
            "Error modificating in calendar match {}".format(id))
    else:
      printDetails(logs.CAL, logs.INFO,
        "Creation in calendar of match {}".format(id))
      #try:
      idCal = createEvent(eventInDB)
      DB.updateEvent(id, idCal)
      #except:
        #printDetails(logs.CAL, logs.ERROR,
         # "Error creating in calendar match {}".format(id))
  printDetails(logs.CAL, logs.INFO, "End of calendar update")
  DB.setCalendarStatus(0)


def launch_update():
  printDetails(logs.CAL, logs.INFO,
    "Launching calendar update")
  if(DB.getCalendarStatus() in [0, "0"]):
    update()
  else:
    printDetails(logs.CAL, logs.WARN,
      "Updating already running...")

def main():
  schedule.every().minute.at(":00").do(launch_update)
