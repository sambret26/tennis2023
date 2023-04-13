# -*- coding: utf-8 -*-

# IMPORTS
from bs4 import BeautifulSoup
import mechanize
import DB
import re


def getInformations(retry=5):
  br = mechanize.Browser()
  br.set_handle_robots(False)
  br.open(DB.getConnectionURL())
  br.select_form(id="kc-form")
  br["username"] = DB.getUsername()
  br["password"] = DB.getPassword()
  try:
    br.submit()
  except Exception as e:
    if retry == 0:
      raise e
    else:
      return getInformations(retry - 1)
  res = br.open(DB.getDataURL())
  content = res.read().decode("cp850")
  players = parse(content)
  return players


def parse(content):
  pattern = re.compile(r'<table[^>]*>.*?<tbody>(.*?)</tbody>.*?</table>',
                       re.DOTALL)
  tableMatch = pattern.search(content)
  if not tableMatch:
    return []
  tableHtml = tableMatch.group(1)
  soup = BeautifulSoup(tableHtml, 'html.parser')
  rows = soup.find_all('tr')
  players = []
  for row in rows:
    cells = row.find_all('td')
    if len(cells) < 5:
      continue
    lastname, firstname, _, club, ranking = (cell.text.strip()
                                             for cell in cells[:5])
    emailMatch = re.search(r'<a[^>]*?href="mailto:([^"]+)"', str(cells[8]))
    email = emailMatch.group(1) if emailMatch else None
    categories = []
    for category in ["SM", "SD", "DM", "DD", "DX"]:
      if category in cells[5].text.strip():
        categories.append(category)
    players.append({
      'Firstname': firstname.title(),
      'Lastname': lastname.title(),
      'Club': club,
      'Ranking': ranking,
      'Email': email,
      'SM': 'SM' in categories,
      'SD': 'SD' in categories,
      'DM': 'DM' in categories,
      'DD': 'DD' in categories,
      'DX': 'DX' in categories,
      'C': 'C' in categories,
    })
  return players


def updateDB(players):
  DB.setAllPlayersToZero()
  for player in players:
    id = DB.searchPlayer(player)
    if id:
      DB.setPlayerToOne(player, id)
    else:
      DB.insertPlayer(player)
      sendNotifAdd(player)
  playersToRemove = DB.getPlayersAtZero()
  for playerToRemove in playersToRemove:
    DB.deletePlayer(playerToRemove[0])
    sendNotifRemove(playerToRemove)


def sendNotifAdd(player):
  DB.addMessage("G", player)
  for category in ["SM", "SD", "DM", "DD", "DX"]:
    if player[category]: DB.addMessage(category, player)


def sendNotifRemove(player):
  DB.removeMessage("G", player)
  for (category, index) in [("SM", 6), ("SD", 7), ("DM", 8), ("DD", 9),
                            ("DX", 10)]:
    if player[index]: DB.removeMessage(category, player)


def main():
  players = getInformations()
  updateDB(players)
