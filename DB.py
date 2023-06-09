# -*- coding: utf-8 -*-

# IMPORTS
from logs import printLogs, printDetails
import sqlite3
import logs

# CONST
DBNAME = "DB.db"


# Returns a connection object to the database
def connect():
  return sqlite3.connect(DBNAME)


  ### GETTERS
def getNumberPlayers():
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT COUNT(*) FROM Players"
  number = cursor.execute(query).fetchone()[0]
  connection.close()
  return number


def getCategoriesById(id):
  connection = connect()
  cursor = connection.cursor()
  query = f"SELECT SM, SD, DM, DD, DX FROM Players WHERE id = {id}"
  categories = cursor.execute(query).fetchone()
  connection.close()
  return categories


def getNumberPlayersByCategory(category):
  connection = connect()
  cursor = connection.cursor()
  query = f"SELECT COUNT(*) FROM Players WHERE {category} = 1"
  number = cursor.execute(query).fetchone()[0]
  connection.close()
  return number


def getRankings():
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Ranking FROM Players"
  cursor.execute(query)
  rankings = [row[0] for row in cursor.fetchall()]
  connection.close()
  return rankings


def getPlayerIdByName(lastname, firstname):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Id FROM Players WHERE Lastname = ? AND Firstname = ?"
  values = (lastname, firstname)
  id = cursor.execute(query, values).fetchone()
  connection.close()
  if id != None:
    return id[0]
  return id


def getRankingsByCategory(category):
  connection = connect()
  cursor = connection.cursor()
  query = f"SELECT Ranking FROM Players WHERE {category} = 1"
  cursor.execute(query)
  rankings = [row[0] for row in cursor.fetchall()]
  connection.close()
  return rankings


def getPlayersAtZero():
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT * FROM Players WHERE State = 0"
  players = cursor.execute(query).fetchall()
  connection.close()
  return players


def getStatsPlayersByCategory(category):
  connection = connect()
  cursor = connection.cursor()
  query = f"SELECT classement FROM Players where {category} = 1"
  cursor.execute(query)
  list = [row[0] for row in cursor.fetchall()]
  connection.close()
  return list


def getPrivateData(type):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Data FROM PrivateDatas WHERE Type = ?"
  values = (type, )
  data = cursor.execute(query, values).fetchone()[0]
  connection.close()
  return data


def getConnectionURL():
  return getPrivateData("ConnectionURL")


def getDataURL():
  return getPrivateData("DataURL")


def getUsername():
  return getPrivateData("Username")


def getPassword():
  return getPrivateData("Password")


def getDiscordToken():
  return getPrivateData("DiscordToken")


def getSamID():
  return getPrivateData("SamID")


def getCalendarID():
  return getPrivateData("CalendarID")


def getCalendarStatus():
  return getPrivateData("CalendarStatus")


def getGuildID():
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT ChannelID FROM Channels WHERE Category = 'GuildID'"
  data = cursor.execute(query).fetchone()[0]
  connection.close()
  return data


def getMatchs():
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT * FROM Matchs"
  data = cursor.execute(query).fetchall()
  connection.close()
  return data


def getMessages(cat):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT id, Message FROM Messages WHERE Category = ?"
  values = (cat, )
  messages = cursor.execute(query, values).fetchall()
  connection.close()
  return messages


def getLogChannelID(cat):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT ChannelID FROM Channels WHERE Category = ? and Type = ?"
  values = (cat, "Logs")
  channelID = cursor.execute(query, values).fetchone()[0]
  connection.close()
  return channelID


def getChannelCategorie(channelId):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Category FROM Channels WHERE ChannelId = ?"
  values = (channelId, )
  result = cursor.execute(query, values).fetchone()
  if result is None:
    cat = None
  else:
    cat = result[0]
  connection.close()
  return cat


def getMatchInfosByName(name):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT * FROM Matchs WHERE Name = ?"
  values = (name, )
  result = cursor.execute(query, values).fetchone()
  connection.close()
  return result


def getMatchInfosById(id):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT * FROM Matchs WHERE Id = ?"
  values = (id, )
  result = cursor.execute(query, values).fetchone()
  connection.close()
  return result


def getPlayerInfosById(id):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Firstname, Lastname, Ranking FROM Players WHERE Id = ?"
  values = (id, )
  result = cursor.execute(query, values).fetchone()
  connection.close()
  return result


def getTeamInfosById(id):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Player1, Player2, Ranking FROM Teams WHERE Id = ?"
  values = (id, )
  (id1, id2, ranking) = cursor.execute(query, values).fetchone()
  query = "SELECT Lastname FROM Players WHERE Id = ?"
  values = (id1, )
  player1 = cursor.execute(query, values).fetchone()[0]
  values = (id2, )
  player2 = cursor.execute(query, values).fetchone()[0]
  result = "{} et {} ({})".format(player1, player2, ranking)
  connection.close()
  return result


def getMatchsByDate(date):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Name, Player1, Player2, Hour, Court FROM Matchs WHERE Day = ?"
  values = (date, )
  result = cursor.execute(query, values).fetchall()
  connection.close()
  return result


def getMatchsToPlay(date):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Id, Name, Player1, Player2, Hour, Court FROM Matchs WHERE Day = ? AND Notif = ?"
  values = (date, 0)
  result = cursor.execute(query, values).fetchall()
  connection.close()
  return result


def searchPlayer(player):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT id FROM Players WHERE (Firstname, Lastname, Club, Mail) = (?, ?, ?, ?)"
  values = (player["Firstname"], player["Lastname"], player["Club"],
            player["Email"])
  id = cursor.execute(query, values).fetchone()
  if not id: return None
  return id[0]

  ### SETTERS


def setCalendarStatus(status):
  printDetails(logs.DB, logs.INFO, f"Setting CalendarStatus to {status}")
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE PrivateDatas SET Data = ? WHERE Type = ?"
  values = (status, "CalendarStatus")
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setAllPlayersToZero():
  printDetails(logs.DB, logs.INFO, "Setting all players to unfind")
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Players SET state = 0"
  cursor.execute(query)
  connection.commit()
  connection.close()


def updateEvent(id, calId):
  printDetails(logs.DB, logs.INFO, "Setting calId to {} for {}".format(
    calId, id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET calId = ? WHERE id = ?"
  values = (calId, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setPlayerToOne(player, id):
  # printDetails(
  #   logs.DB, logs.INFO,
  #   "Setting SM = {}, SD = {}, DM = {}, DD = {}, DX = {} for {} {} ".format(
  #     player["SM"], player["SD"], player["DM"], player["DD"], player["DX"],
  #     player["Firstname"], player["Lastname"]))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Players SET state = 1, SM = ?, SD = ?, DM = ?, DD = ?, DX = ?, C = ? WHERE id = ?"
  values = (player["SM"], player["SD"], player["DM"], player["DD"],
            player["DX"], player["C"], id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setWinner(id, playerId):
  printLogs(logs.DB, logs.INFO,
            "Setting winner = {} for match {}".format(playerId, id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Winner = ?, Finish = 1 WHERE id = ?"
  values = (playerId, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setScore(id, score):
  printLogs(logs.DB, logs.INFO,
            "Setting score = {} for match = {}".format(score, id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Score = ?, Finish = 1 WHERE id = ?"
  values = (score, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setCourt(id, court):
  printLogs(logs.DB, logs.INFO,
            "Setting court = {} for match = {}".format(court, id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Court = ? WHERE id = ?"
  values = (int(court), id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setPlayer1(id, playerId):
  printLogs(logs.DB, logs.INFO,
            "Setting player1 = {} for match = {}".format(playerId, id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Player1 = ? WHERE id = ?"
  values = (playerId, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setPlayer2(id, playerId):
  printLogs(logs.DB, logs.INFO,
            "Setting player2 = {} for match = {}".format(playerId, id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Player2 = ? WHERE id = ?"
  values = (playerId, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setDay(id, day):
  printLogs(logs.DB, logs.INFO,
            "Setting day = {} for match = {}".format(day, id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Day = ? WHERE id = ?"
  values = (day, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setHour(id, hour):
  printLogs(logs.DB, logs.INFO,
            "Setting hour = {} for match = {}".format(hour, id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Hour = ? WHERE id = ?"
  values = (hour, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setNotifToSend(id):
  printLogs(logs.DB, logs.INFO,
            "Setting notif = 1 for match = {}".format(id))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Notif = ? WHERE id = ?"
  values = (1, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def updatePlayerId(name, playerId):
  printLogs(logs.DB, logs.INFO,
            "Setting player = {} where it was {}".format(playerId, name))
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Player1 = ? WHERE Player1 = ?"
  values = (playerId, name)
  cursor.execute(query, values)
  query = "UPDATE Matchs SET Player2 = ? WHERE Player2 = ?"
  values = (playerId, name)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def removeCalId():
  printLogs(logs.DB, logs.INFO,
            "Removing all events")
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET CalId = NULL"
  cursor.execute(query)
  connection.commit()
  connection.close()

  ### INSERT


def insertPlayer(player):
  printLogs(
    logs.DB, logs.INFO,
    "Adding {} {} {} {} {} SM = {} SD = {} DM = {} DD = {} DX = {}".format(
      player["Firstname"], player["Lastname"], player["Ranking"],
      player["Club"], player["Email"], player["SM"], player["SD"],
      player["DM"], player["DD"], player["DX"]))
  connection = connect()
  cursor = connection.cursor()
  query = "INSERT INTO Players (firstname, lastname, ranking, club, mail, SM, SD, DM, DD, DX, C) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
  values = (player["Firstname"], player["Lastname"], player["Ranking"],
            player["Club"], player["Email"], player["SM"], player["SD"],
            player["DM"], player["DD"], player["DX"], player["C"])
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def addMessage(category, player):
  message = "Nouvelle inscription : {} {} ({}) classé(e) {}".format(
    player["Firstname"], player["Lastname"], player["Club"], player["Ranking"])
  printLogs(logs.DB, logs.INFO,
            "Adding message {} in {}".format(message, category))
  connection = connect()
  cursor = connection.cursor()
  query = "INSERT INTO Messages (category, message) VALUES (?, ?)"
  values = (category, message)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def addNotif(match, player1, player2):
  message = "Match {} : {} contre {} prévu à {} sur le court n°{}".format(
    match[1], player1, player2, match[4], match[5])
  printLogs(logs.DB, logs.INFO,
            "Adding notification message {}".format(message))
  connection = connect()
  cursor = connection.cursor()
  query = "INSERT INTO Messages (category, message) VALUES (? ,?)"
  values = ("NOTIF", message)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def removeMessage(category, player):
  message = "Désinscription de {} {} ({}) classé(e) {}".format(
    player[1], player[2], player[4], player[3])
  printLogs(logs.DB, logs.INFO,
            "Adding message {} in {}".format(message, category))
  connection = connect()
  cursor = connection.cursor()
  query = "INSERT INTO Messages (category, message) VALUES (?, ?)"
  values = (category, message)
  cursor.execute(query, values)
  connection.commit()
  connection.close()

  ### DELETE


def deletePlayer(id):
  datas = getPlayerInfosById(id)
  printLogs(logs.DB, logs.INFO,
            "Deleting player {} {}".format(datas[0], datas[1]))
  connection = connect()
  cursor = connection.cursor()
  query = "DELETE FROM Players WHERE id = ?"
  values = (id, )
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def deleteMessage(id):
  printLogs(logs.DB, logs.INFO, "Deleting message {}".format(id))
  connection = connect()
  cursor = connection.cursor()
  query = "DELETE FROM Messages WHERE id = ?"
  values = (id, )
  cursor.execute(query, values)
  connection.commit()
  connection.close()
