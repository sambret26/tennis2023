# -*- coding: utf-8 -*-

# IMPORTS
import sqlite3

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


def getGuildID():
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT ChannelID FROM Channels WHERE Category = 'GuildID'"
  data = cursor.execute(query).fetchone()[0]
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


def getPlayerInfosById(id):
  connection = connect()
  cursor = connection.cursor()
  query = f"SELECT Firstname, Lastname, Ranking FROM Players WHERE id = {id}"
  result = cursor.execute(query).fetchone()
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


def setAllPlayersToZero():
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Players SET state = 0"
  cursor.execute(query)
  connection.commit()
  connection.close()


def setPlayerToOne(player, id):
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Players SET state = 1, SM = ?, SD = ?, DM = ?, DD = ?, DX = ?, C = ? WHERE id = ?"
  values = (player["SM"], player["SD"], player["DM"], player["DD"],
            player["DX"], player["C"], id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setWinner(id, playerId):
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Winner = ?, Finish = 1 WHERE id = ?"
  values = (playerId, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def setScore(id, score):
  connection = connect()
  cursor = connection.cursor()
  query = "UPDATE Matchs SET Score = ?, Finish = 1 WHERE id = ?"
  values = (score, id)
  cursor.execute(query, values)
  connection.commit()
  connection.close()

  ### INSERT


def insertPlayer(player):
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
  connection = connect()
  cursor = connection.cursor()
  query = "INSERT INTO Messages (category, message) VALUES (?, ?)"
  message = "Nouvelle inscription : {} {} ({}) classé(e) {}".format(
    player["Firstname"], player["Lastname"], player["Club"], player["Ranking"])
  values = (category, message)
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def removeMessage(category, player):
  connection = connect()
  cursor = connection.cursor()
  query = "INSERT INTO Messages (category, message) VALUES (?, ?)"
  message = "Désinscription de {} {} ({}) classé(e) {}".format(
    player[1], player[2], player[4], player[3])
  values = (category, message)
  cursor.execute(query, values)
  connection.commit()
  connection.close()

  ### DELETE


def deletePlayer(id):
  connection = connect()
  cursor = connection.cursor()
  query = "DELETE FROM Players WHERE id = ?"
  values = (id, )
  cursor.execute(query, values)
  connection.commit()
  connection.close()


def deleteMessage(id):
  connection = connect()
  cursor = connection.cursor()
  query = "DELETE FROM Messages WHERE id = ?"
  values = (id, )
  cursor.execute(query, values)
  connection.commit()
  connection.close()
