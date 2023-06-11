# -*- coding: utf-8 -*-

# IMPORTS
from datetime import datetime as date
from datetime import timedelta
import os

# CONST

MAJ = "[MAJ]"
DB = "[DB ]"
CAL = "[CAL]"

INFO = "[INFO ]"
WARN = "[WARN ]"
ERROR = "[ERROR]"


# Print the date and the message on the file logs/logs.txt
def printLogs(type1, type2, message):
  printDetails(type1, type2, message)
  currentDate = str(getCurrentDate().strftime("%d/%m %Hh%M:%S"))
  formattedMessage = "{} : {} {} {}\n".format(currentDate, type1, type2,
                                              message)
  with open("./logs/logs.txt", 'a') as f:
    f.write(formattedMessage)


def printDetails(type1, type2, message):
  currentDate = str(getCurrentDate().strftime("%d/%m %Hh%M"))
  formattedMessage = "{} : {} {} {}\n".format(currentDate, type1, type2,
                                              message)
  with open("./logs/out.txt", 'a') as f:
    f.write(formattedMessage)


# Returns the current date, with an offset if necessary (c.f. jetlag)
def getCurrentDate():
  offset = 0
  if "REPLIT" in os.environ:
    offset = 2
  return date.now() + timedelta(seconds=3600 * offset)
