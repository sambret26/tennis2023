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


@app.route('/playerIdByName/<name>', methods=['GET'])
def getPlayerIdByName(name):
  print(name)
  lastname = name.split(" ")[0].title()
  firstname = name.split(" ")[1].title()
  connection = connect()
  cursor = connection.cursor()
  query = "SELECT Id FROM Players WHERE Firstname = ? AND Lastname = ?"
  values = (firstname, lastname)
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
  print("On entre")
  match = request.args.to_dict()
  print(match)
  connection = connect()
  cursor = connection.cursor()
  query = "INSERT INTO Matchs (Category, Name, Player1, Player2, Day, Hour, Court, Finish, Winner, Score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
  values = tuple(match.values())
  for value in values:
    if (value == "NULL"):
      value = None
  print(values)
  cursor.execute(query, values)
  connection.commit()
  connection.close()
  response = {"status": 201}
  return response


def main():
  app.run(host="0.0.0.0", port=8070)
