# -*- coding: utf-8 -*-

# IMPORTS
from flask import Flask, jsonify
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


app.run(host="0.0.0.0", port=8080)
