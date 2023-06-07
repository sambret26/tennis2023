# -*- coding: utf-8 -*-

# IMPORTS
from flask import Flask, jsonify, request
import sqlite3

# CONST
DBNAME = "DB.db"

app = Flask('app')


# Returns a connection object to the database
def connect():
  return sqlite3.connect(DBNAME)

  ### EXPORT


@app.route('/channels', methods=['GET'])
def exportChannels():
  connection = connect()
  cursor = connection.cursor()
  channels = cursor.execute("SELECT * FROM Channels").fetchall()
  connection.close()
  return jsonify(channels)


@app.route('/matchs', methods=['GET'])
def exportMatchs():
  connection = connect()
  cursor = connection.cursor()
  matchs = cursor.execute("SELECT * FROM Matchs").fetchall()
  connection.close()
  return jsonify(matchs)


@app.route('/players', methods=['GET'])
def exportPlayers():
  connection = connect()
  cursor = connection.cursor()
  players = cursor.execute("SELECT * FROM Players").fetchall()
  connection.close()
  return jsonify(players)


@app.route('/privateDatas', methods=['GET'])
def exportPrivateDatas():
  connection = connect()
  cursor = connection.cursor()
  privateDatas = cursor.execute("SELECT * FROM PrivateDatas").fetchall()
  connection.close()
  return jsonify(privateDatas)


@app.route('/playersInfos', methods=['GET'])
def getPlayersInfo():
  connection = connect()
  cursor = connection.cursor()
  players = cursor.execute(
    "SELECT Firstname, Lastname, Ranking FROM Players").fetchall()
  connection.close()
  return jsonify(players)


@app.route('/teamsInfos', methods=['GET'])
def getTeamsInfos():
  result = []
  connection = connect()
  cursor = connection.cursor()
  teams = cursor.execute(
    "SELECT Player1, Player2, Ranking FROM Teams").fetchall()
  for team in teams:
    query = "SELECT Lastname FROM Players WHERE Id = ?"
    player1 = cursor.execute(query, (team[0], )).fetchone()[0]
    player2 = cursor.execute(query, (team[1], )).fetchone()[0]
    result.append((player1.upper(), player2.upper(), team[2]))
  connection.close()
  return jsonify(result)


@app.route('/playerIdByName/<name>', methods=['GET'])
def getPlayerIdByName(name):
  split = name.split(" ")
  lastname = " ".join(split[0:-1]).upper()
  firstname = name.split(" ")[-1].title()
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Id FROM Players WHERE Firstname = ? AND Lastname = ?"
  values = (firstname, lastname)
  id = cursor.execute(query, values).fetchone()[0]
  connection.close()
  return jsonify(id)


@app.route('/teamIdByName/<name>', methods=['GET'])
def getTeamIdByName(name):
  player1Name = name.split("--")[0].upper()
  player2Name = name.split("--")[1].upper()
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Id FROM Players WHERE Lastname = ?"
  values = (player1Name, )
  cursor.execute(query, values)
  players1 = [row[0] for row in cursor.fetchall()]
  if len(players1) == 1:
    players1 = (players1[0], players1[0])
  else:
    players1 = tuple(players1)
  values = (player2Name, )
  cursor.execute(query, values)
  players2 = [row[0] for row in cursor.fetchall()]
  if len(players2) == 1:
    players2 = (players2[0], players2[0])
  else:
    players2 = tuple(players2)
  placeholders1 = ",".join(["?"] * len(players1))
  placeholders2 = ",".join(["?"] * len(players2))
  query = f"SELECT Id FROM Teams WHERE Player1 IN ({placeholders1}) AND Player2 IN ({placeholders2})"
  values = (players1 + players2)
  id = cursor.execute(query, values).fetchone()[0]
  connection.close()
  return jsonify(id)


@app.route('/playerNameById/<id>', methods=['GET'])
def getPlayerNameById(id):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Firstname, Lastname FROM Players WHERE Id = ?"
  values = (id, )
  player = cursor.execute(query, values).fetchone()
  name = player[1].upper() + " " + player[0].title()
  connection.close()
  return jsonify(name)


@app.route('/playersName', methods=['GET'])
def getAllPlayersName():
  players = {}
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Id, Firstname, Lastname FROM Players"
  results = cursor.execute(query).fetchall()
  connection.close()
  for player in results:
    players[player[0]] = player[2].upper() + " " + player[1].title()
  return jsonify(players)


@app.route('/teamNameById/<id>', methods=['GET'])
def getTeamNameById(id):
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Player1, Player2 FROM Teams WHERE Id = ?"
  values = (id, )
  (id1, id2) = cursor.execute(query, values).fetchone()
  query = "SELECT Lastname FROM Players WHERE Id = ?"
  values = (id1, )
  player1 = cursor.execute(query, values).fetchone()[0]
  values = (id2, )
  player2 = cursor.execute(query, values).fetchone()[0]
  name = player1.upper() + "--" + player2.upper()
  connection.close()
  return jsonify(name)


@app.route('/teamsName', methods=["GET"])
def getAllTeams():
  teams = {}
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Id, Player1, Player2 FROM Teams"
  results = cursor.execute(query).fetchall()
  for team in results:
    (idTeam, idPlayer1, idPlayer2) = team
    query = "SELECT Lastname FROM Players WHERE Id = ?"
    player1 = cursor.execute(query, (idPlayer1, )).fetchone()[0]
    player2 = cursor.execute(query, (idPlayer2, )).fetchone()[0]
    teams[idTeam] = player1.upper() + "--" + player2.upper()
  connection.close()
  return jsonify(teams)


@app.route('/matchsInfos', methods=['GET'])
def getMatchsInfo():
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Name, Player1, Player2, Day, Hour, Court, Finish, Winner, Score FROM Matchs"
  matchs = cursor.execute(query).fetchall()
  connection.close()
  return jsonify(matchs)


@app.route('/deleteMatchs', methods=['Post'])
def deleteMatchs():
  connection = connect()
  cursor = connection.cursor()
  cursor.execute("DELETE FROM Matchs")
  connection.commit()
  connection.close()
  response = {"status": 201}
  return response


@app.route('/insertMatch', methods=['Post'])
def insertMatch():
  match = request.args.to_dict()
  connection = connect()
  cursor = connection.cursor()
  query = "INSERT INTO Matchs (Category, Name, Player1, Player2, Day, Hour, Court, Finish, Winner, Score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
  values = []
  for value in match.values():
    if (value == "NULL"):
      values.append(None)
    else:
      values.append(value)
  values = tuple(values)
  cursor.execute(query, values)
  connection.commit()
  connection.close()
  response = {"status": 201}
  return response


def main():
  app.run(host="0.0.0.0", port=8070)
