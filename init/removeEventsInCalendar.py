# -*- coding: utf-8 -*-

# IMPORTS
import sys
sys.path.append("modules")

from google_auth_oauthlib.flow import InstalledAppFlow as IAF
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from discordTennisFunctions import getPlayerFromPlayerIdInDB
from logs import printDetails
import os.path as path
import pickle
import logs
import cal
import DB



def deleteCal():
  creds = cal.findCreds()
  calendarId = DB.getCalendarID()
  service = build('calendar', 'v3', credentials=creds)
  eventsResult = service.events().list(calendarId=calendarId, singleEvents=True, orderBy='startTime').execute()
  events = eventsResult.get('items', [])
  for event in events :
    service.events().delete(calendarId=calendarId, eventId=event['id']).execute()


def deleteDB():
  connection = DB.connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET CalId = NULL"
  cursor.execute(query)
  connection.commit()
  connection.close()


def main():
  deleteCal()
  deleteDB()


main()
