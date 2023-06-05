# -*- coding: utf-8 -*-


# IMPORTS
from flask import Flask, jsonify
import sqlite3


# CONST
DBNAME = "BD.db"


app = Flask(__name__)


# Returns a connection object to the database
def connect():
  return sqlite.connect(DBNAME)


    ### EXPORT

@app.route('/channels', methods=['GET'])
def exportChanels():
  connection = connect()
  cursor = connection.cursor()
  channels = cursor.execute("SELECT * FROM Channels").fetchall()
  connection.close()
  return channels


@app.route('/matchs', methods=['GET'])
def exportMatchs():
  connection = connect()
  cursor = connection.cursor()
  channels = cursor.execute("SELECT * FROM Matchs").fetchall()
  connection.close()
  return channels

@app.route('/players', methods=['GET'])
def exportPlayers():
    connection = connect()
    cursor = connection.cursor()
    channels = cursor.execute("SELECT * FROM Players").fetchall()
    connection.close()
    return channels


@app.route('/privateDatas', methods=['GET'])
def exportPrivateDatas():
  connection = connect()
  cursor = connection.cursor()
  channels = cursor.execute("SELECT * FROM PrivateDatas").fetchall()
  connection.close()
  return channels


def main():
  app.run()


main()
