# -*- coding: utf-8 -*-

# IMPORTS
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash import ButtonStyle
from logs import printLogs, getCurrentDate
import discord
import tennis
import logs
import cal
import DB


async def maj(bot):
  printLogs(logs.MAJ, logs.INFO, "Updating")
  tennis.main()
  await addNotifMatch()


async def nb(bot, ctx):
  category = DB.getChannelCategorie(ctx.channel.id)
  if category is None or category == "G":
    nb = DB.getNumberPlayers()
    message = ("Il y a {} inscrit{} dans le tournoi".format(
      nb, '' if nb < 2 else 's'))
    for cat in ["SM", "SD", "DM", "DD", "DX"]:
      message += "\n\t\t{}".format(numberPlayersByCategory(cat))
    await ctx.send(message)
  else:
    await ctx.send(numberPlayersByCategory(category))
  details = await yesOrNot(bot, ctx, "Afficher les détails des classements ?")
  if (details):
    if (category is None or category == "G"):
      await sendAllDetails(ctx)
    else:
      await sendCategoryDetails(ctx, category)


async def info(ctx, name):
  if name == None:
    await ctx.send(
      "La commande $info doit être suivi du nom d'un match (ex : $info SM27)")
    return
  name = name.upper()
  matchInfos = DB.getMatchInfosByName(name)
  if matchInfos == None:
    await ctx.send(f"Le match {name} n'a pas été trouvé en base de données")
    return
  message = generateMatchMessage(matchInfos)
  await ctx.send(message)


async def result(bot, ctx, name):
  if name == None:
    await ctx.send(
      "La commande $result doit être suivi du nom d'un match (ex : $info SM27)")
    return
  name = name.upper()
  matchInfos = DB.getMatchInfosByName(name)
  if matchInfos == None:
    await ctx.send(f"Le match {name} n'a pas été trouvé en base de données")
    return
  id, cat, name, player1Id, player2Id, day, hour, court, finish, winnerId, notif, score, calid = matchInfos
  if winnerId != None and score != None:
    res = await yesOrNot(
      bot, ctx,
      "Le vainqueur et le score de ce match sont déjà renseignés\nVoulez-vous renseigner de nouveaux résultats ?"
    )
    if res: await setResult(bot, ctx, id, name, player1Id, player2Id, True)
  elif winnerId != None:
    res = await yesOrNot(
      bot, ctx,
      "Le vainqueur de ce match est déjà renseigné\nVoulez-vous renseigner un nouveau vainqueur ?"
    )
    if not res:
      await setResult(bot, ctx, id, name, player1Id, player2Id, False)
    else:
      await setResult(bot, ctx, id, name, player1Id, player2Id, True)
  else:
    await setResult(bot, ctx, id, name, player1Id, player2Id, True)


async def modifCourt(bot, ctx, name):
  matchName = name.upper()
  matchId = DB.getMatchInfosByName(matchName)[0]
  if matchId == None:
    await ctx.send("Match non trouvé {}".format(matchName))
    return
  message = "Sur quel court voulez vous déplacer ce match ?"
  list = [("Numéro 1", "1", "green"), ("Numéro 2", "2", "blue"),
          ("Numéro 3", "3", "red")]
  court = await question(bot, ctx, message, list)
  DB.setCourt(matchId, int(court))
  cal.updateOneEvent(matchId)
  await ctx.send("Le match {} à été déplacé sur le court {}".format(
    matchName, court))


async def modifJoueur1(ctx, args):
  if len(args) < 3:
    await ctx.send("Veuillez entrer en paramètre un match, un nom, un prénom")
    return
  matchName = args[0].upper()
  matchId = DB.getMatchInfosByName(matchName)[0]
  if matchId == None:
    await ctx.send("Match non trouvé {}".format(matchName))
    return
  playerLastname = " ".join(args[1:-1]).upper()
  playerFirstname = args[-1].title()
  playerId = DB.getPlayerIdByName(playerLastname, playerFirstname)
  if playerId == None:
    await ctx.send("Joueur non trouvé : {} {}".format(
      playerLastname, playerFirstname))
    return
  DB.setPlayer1(matchId, playerId)
  message = "Le match {} à maintenant comme joueur 1 {} {}".format(
    matchName, playerLastname, playerFirstname)
  cal.updateOneEvent(matchId)
  await ctx.send(message)


async def modifJoueur2(ctx, args):
  if len(args) < 3:
    await ctx.send("Veuillez entrer en paramètre un match, un nom, prénom")
    return
  matchName = args[0].upper()
  matchId = DB.getMatchInfosByName(matchName)[0]
  if matchId == None:
    await ctx.send("Match non trouvé {}".format(matchName))
    return
  playerLastname = " ".join(args[1:-1]).upper()
  playerFirstname = args[-1].title()
  playerId = DB.getPlayerIdByName(playerLastname, playerFirstname)
  if playerId == None:
    await ctx.send("Joueur non trouvé : {} {}".format(
      playerLastname, playerFirstname))
    return
  DB.setPlayer2(matchId, playerId)
  message = "Le match {} à maintenant comme joueur 2 {} {}".format(
    matchName, playerLastname, playerFirstname)
  cal.updateOneEvent(matchId)
  await ctx.send(message)


async def modifJour(ctx, args):
  if len(args) != 2:
    await ctx.send(
      "Veuillez entrer en paramètre un match et un jour au format dd/mm")
    return
  matchName = args[0].upper()
  matchId = DB.getMatchInfosByName(matchName)[0]
  if matchId == None:
    await ctx.send("Match non trouvé {}".format(matchName))
    return
  day = args[1]
  if len(day) == 4: day = "0" + day
  if notADay(day):
    await ctx.send("Veuillez rentrer un jour au format dd/mm")
    return
  if notInTournament(day):
    await ctx.send("Le jour indiqué {} est hors du tournoi".format(day))
    return
  DB.setDay(matchId, day)
  message = "Le match {} est programmé pour le {}".format(matchName, day)
  cal.updateOneEvent(matchId)
  await ctx.send(message)


async def modifHeure(ctx, args):
  if len(args) != 2:
    await ctx.send("Veuillez entrer en paramètre un match et une heure")
    return
  matchName = args[0].upper()
  matchId = DB.getMatchInfosByName(matchName)[0]
  if matchId == None:
    await ctx.send("Match non trouvé {}".format(matchName))
    return
  hour = convertInHour(args[1])
  if hour == None:
    await ctx.send("L'heure entrée n'est pas correcte")
    return
  DB.setHour(matchId, hour)
  message = "Le match {} est programmé à {}".format(matchName, hour)
  cal.updateOneEvent(matchId)
  await ctx.send(message)

async def modifPg(ctx, args):
  if len(args) != 3 :
    await ctx.send("Veuillez entrer en paramètre un match,\
                       un jour au format dd/mm et une heure")
    return
  matchName = args[0].upper()
  matchId = DB.getMatchInfosByName(matchName)[0]
  if matchId == None :
    await ctx.send("Match non trouvé {}".format(matchName))
    return
  day = args[1]
  if len(day) == 4: day = "0" + day
  if notADay(day):
    await ctx.send("Veuillez rentrer un jour au format dd/mm")
    return
  if notInTournament(day):
    await ctx.send("Le jour indiqué {} est hors du tournoi".format(day))
    return
  hour = convertInHour(args[2])
  if hour == None:
    await ctx.send("L'heure entrée n'est pas correcte")
    return
  DB.setDay(matchId, day)
  DB.setHour(matchId, hour)
  message = "Le match {} est programmé pour le {} à {}".format(
    matchName, day, hour)
  cal.updateOneEvent(matchId)
  await ctx.send(message)


async def pg(ctx, args):
  dates = getDatesFromArgs(args)
  message = ""
  matchs = False
  for date in dates:
    matchs = DB.getMatchsByDate(date)
    if matchs == None: break
    message += "Voici la programmation du {}:\n".format(date)
    for match in matchs:
      player1 = getPlayerFromPlayerIdInDB(match[0], match[1])
      player2 = getPlayerFromPlayerIdInDB(match[0], match[2])
      message += "{} : {}, {} contre {} sur le court n°{}\n".format(
        match[3], match[0], player1, player2, match[4])
      matchs = True
    message += "\n"
  if not matchs:
    message = "Aucune programmation prévue le {}".format(dates[0])
  await ctx.send(message)


async def cmd(ctx):
  message = "Voici la liste des commandes disponibles :\n"
  message += "$maj : mettre à jour la liste des inscrits\n"
  message += "$nb : connaitre le nombre d'inscrits\n"
  message += "$info [match] : obtenir des informations sur un match ($infos)\n"
  message += "$result [match] : enregistrer le résultat d'un match ($resultat)\n"
  message += "$modifCourt [match] : modifier le court affecté à un match ($mc)'\n"
  message += "$modifJoueur1 [match] [joueur]: modifier le joueur 1 affecté à un match ($mj1)\n"
  message += "$modifJoueur2 [match] [joueur]: modifier le joueur 2 affecté à un match ($mj2)\n"
  message += "$modifJour [match] [jour] : modifier la date affectée à un match ($mj)\n"
  message += "$modifHeure [match] [heure]: modifier l'heure affectée à un match ($mh)\n"
  message += "$modifiPg [match] [jour] [heure] : modifier la programmation d'un match ($mpg)\n"
  message += "$pg {jour} : obtenir la programmation des jours données, ou du jour actuel ($program / $programmation)\n"
  message == "$updateCal : mettre à jour tout les évènements (attention, chargement assez long)\n"
  await ctx.send(message)


def getDatesFromArgs(args):
  dates = []
  for arg in args:
    if not notADay(arg) and not notInTournament(arg):
      dates.append(arg)
  if len(dates) == 0:
    return [getCurrentDate().strftime("%d/%m")]
  return dates


async def yesOrNot(bot, ctx, message):
  return await question(bot, ctx, message, [("Oui", "1", "Green"),
                                            ("Non", "0", "Red")])


async def question(bot, ctx, message, list):
  while len(list) > 0:
    questionList = list[:4]
    if len(questionList) == 4:
      questionList.append(("Afficher plus", "Next", "Blue"))
    result = await question5max(bot, ctx, message, questionList)
    if result != "Next": return result
    list = list[4:]


async def question5max(bot, ctx, message, list):

  def check(m):
    return m.author.id == ctx.author.id and m.origin_message.id == choice.id

  buttons = generateButtons(list)
  actionRow = create_actionrow(*buttons)
  choice = await ctx.send(message, components=[actionRow])
  buttonCtx = await wait_for_component(bot, components=actionRow, check=check)
  await buttonCtx.edit_origin(content=message + "(" + buttonCtx.custom_id + ")"
                              )
  if buttonCtx.custom_id.isdigit(): return int(buttonCtx.custom_id)
  return buttonCtx.custom_id


def generateButtons(list):
  buttons = []
  for (index, value) in enumerate(list):
    buttons.append(
      create_button(style=findStyle(index,
                                    value[2] if len(value) > 2 else None),
                    label=value[0],
                    custom_id=value[1]))
  return buttons


def findStyle(index, value):
  if value != None and value.lower() == "green": return ButtonStyle.green
  if value != None and value.lower() == "red": return ButtonStyle.red
  if value != None and value.lower() == "blue": return ButtonStyle.blue
  if index % 3 == 0: return ButtonStyle.green
  if index % 3 == 1: return ButtonStyle.red
  return ButtonStyle.blue


async def sendAllDetails(ctx):
  title = "Nombre d'inscrits par classement pour chaque catégorie :"
  embed = discord.Embed(title=title, color=0x9f1994)
  embed.add_field(name="Total",
                  value=rankingMessage(DB.getRankings()),
                  inline=False)
  for category in ["SM", "SD", "DM", "DD", "DX"]:
    embed.add_field(name=category,
                    value=rankingMessage(DB.getRankingsByCategory(category)),
                    inline=False)
  await ctx.send(embed=embed)


async def sendCategoryDetails(ctx, category):
  title = "Nombre d'inscrits par classements :"
  embed = discord.Embed(title=title, color=0x9f1994)
  embed.add_field(name=category,
                  value=rankingMessage(DB.getRankingsByCategory(category)),
                  inline=False)
  await ctx.send(embed=embed)


def rankingMessage(rankings):
  rankingsMessage = "\u200B"
  for ranking in [
      "NC", "40", "30/5", "30/4", "30/3", "30/2", "30/1", "30", "15/5", "15/4",
      "15/3", "15/2", "15/1", "15"
  ]:
    rankingsMessage += "    {} : {}\n".format(ranking.ljust(4),
                                              rankings.count(ranking))
  return rankingsMessage


def numberPlayersByCategory(cat):
  nb = DB.getNumberPlayersByCategory(cat)
  return ("Il y a {} inscrit{} dans la catégorie {}".format(
    nb, '' if nb < 2 else 's', cat))


async def sendMessages(bot):
  printLogs(logs.MAJ, logs.INFO, "Sending messages")
  for category in ["G", "SM", "SD", "DM", "DD", "DX", "NOTIF"]:
    await sendMessagesByCategory(bot, category)


async def sendMessagesByCategory(bot, cat):
  messages = DB.getMessages(cat)
  channelID = DB.getLogChannelID(cat)
  channel = await bot.fetch_channel(channelID)
  for message in messages:
    await channel.send(message[1])
    DB.deleteMessage(message[0])


def generateMatchMessage(matchInfos):
  id, cat, name, player1Id, player2Id, day, hour, court, finish, winnerId, notif, score, calid = matchInfos
  player1 = getPlayerFromPlayerIdInDB(cat, player1Id)
  player2 = getPlayerFromPlayerIdInDB(cat, player2Id)
  if finish:
    msg = "Le match {} à opposé {} à {}".format(name, player1, player2)
    if day != None: msg += " le {}".format(day)
    if hour != None: msg += " à {}".format(hour)
    if court != None: msg += " sur le court {}".format(court)
    msg += "."
    if winnerId != None:
      winner = player2
      if int(winnerId) == int(player1Id): winner = player1
      msg += " Il a été gagné par {}".format(winner.split("(")[0])
      if score != None:
        msg += " ({})".format(score)
      msg += "."
  else:
    if player1 != None and player2 != None:
      msg = "Le match {} opposera {} à {}".format(name, player1, player2)
    elif player1 != None:
      msg = "Le match {} opposera {} à ?".format(name, player1)
    elif player2 != None:
      msg = "Le match {} opposera {} à ?".format(name, player2)
    else:
      msg = "Le match {} se jouera".format(name)
    if day != None: msg += " le {}".format(day)
    if hour != None: msg += " à {}".format(hour)
    if court != None: msg += " sur le court {}".format(court)
    msg += "."
  return msg


def getPlayerFromPlayerIdInDB(cat, playerIdDB):
  if playerIdDB == None or playerIdDB == "null":
    return None
  if playerIdDB.startswith("VS") or playerIdDB.startswith("VD") or\
   playerIdDB.startswith("VP"):
    match = playerIdDB.lstrip("V")
    return "Le vainqueur du match {}".format(match)
  if playerIdDB.startswith("VT"):
    return "Qualifié entrant"
  if cat.startswith("S") :
    p1 = DB.getPlayerInfosById(playerIdDB)
    return "{} {} ({})".format(p1[1], p1[0], p1[2])
  return DB.getTeamInfosById(playerIdDB)


async def setResult(bot, ctx, id, name, player1Id, player2Id, winner):
  if winner:
    if player1Id == None or player1Id.startswith("V"):
      player1 = "Joueur inconnu"
    else:
      p1 = DB.getPlayerInfosById(player1Id)
      player1 = "{} {}".format(p1[1], p1[0])
    if player2Id == None or player2Id.startswith("V"):
      player2 = "Joueur inconnu"
    else:
      p2 = DB.getPlayerInfosById(player2Id)
      player2 = "{} {}".format(p2[1], p2[0])
    message = "Quel joueur a gagné le match ?"
    winner = await question(bot, ctx, message, [(player1, player1Id, "green"),
                                                (player2, player2Id, "blue")])
    DB.setWinner(id, winner)
    DB.updatePlayerId("V" + name, winner)
  set1 = await askSetResult(bot, ctx, "Quel est le résultat du premier set ?")
  set2 = await askSetResult(bot, ctx, "Quel est le résultat du deuxième set ?")
  res = set1 + " " + set2
  if thirdSet(set1, set2):
    set3 = await askSetResult(bot, ctx,
                              "Quel est le résultat du troisième set ?", False)
    res += " " + set3
  DB.setScore(id, res)
  await ctx.send(f"Le résultat du match {name} a été mis à jour")


async def askSetResult(bot, ctx, message, canLose=True):
  list = []
  win = ["7/5", "6/4", "6/3", "6/2", "6/1", "6/0"]
  for score in win:
    list.append((score, score, "green"))
  if canLose:
    lose = ["5/7", "4/6", "3/6", "2/6", "1/6", "0/6"]
    for score in lose:
      list.append((score, score, "red"))
  return await question(bot, ctx, message, list)


def thirdSet(set1, set2):
  win = 0
  for set in [set1, set2]:
    score1, score2 = set.split("/")
    if score1 > score2: win = win + 1
  return win < 2

def notADay(day):
  if len(day) !=5:
    return True
  if day[2] != "/":
    return True
  if day[0] != "0" and day[0] != "1" and day[0] != "2" and day[0] != "3":
    return True
  if not day[1].isdigit() or not day[3].isdigit() or not day[4].isdigit():
    return True
  return False


def notInTournament(day):
  if day.split("/")[1] == "06" and int(day.split("/")[0]) > 18 and\
   int(day.split("/")[1]) <31:
    return False
  if day in ["01/07", "02/07"]:
    return False
  return True


def convertInHour(hour):
  if len(hour) == 2:
    if hour[0].isdigit() and hour[1].upper() == "H":
      return hour.upper()
    return None
  if len(hour) == 3:
    if hour[0] in ["1", "2"] and hour[1].isdigit() and hour[2].upper() == "H":
      return hour.upper()
    if hour[0] == "0" and hour[1].isdigit() and hour[2].upper() == "H":
      return hour[1:].upper()
    return None
  if len(hour) == 4:
    if hour[0].isdigit() and hour[1].upper() == "H" and\
     hour[2] == "0" and hour[3] == "0":
      return hour[:2].upper()
    if hour[0].isdigit() and hour[1].upper() == "H"and\
     hour[2] in ["0", "1", "2", "3", "4", "5"] and hour[3].isdigit():
      return hour.upper()
    return None
  if len(hour) == 5:
    if hour[0] == "0" and hour[1].isdigit() and hour[2].upper() == "H" and\
     hour[3] == "0" and hour[4] == "0":
      return hour[1:3].upper()
    if hour[0] == "0" and hour[1].isdigit() and hour[2].upper() == "H" and\
     hour[3] in ["0", "1", "2", "3", "4", "5"] and hour[4].isdigit():
      return hour[:3].upper()
    if hour[0] in ["1", "2"] and hour[1].isdigit() and\
     hour[2].upper() == "H" and hour[3] == "0" and hour[4] == "0":
      return hour[:3].upper()
    if hour[0] in ["1", "2"] and hour[1].isdigit() and hour[2].upper(
     ) == "H" and hour[3] in ["0", "1", "2", "3", "4", "5"] and\
      hour[4].isdigit():
      return hour.upper()
  return None


async def addNotifMatch():
  currentDate = getCurrentDate().strftime("%d/%m")
  currentHour = int(getCurrentDate().strftime("%H"))
  currentMinutes = int(getCurrentDate().strftime("%M"))
  matchs = DB.getMatchsToPlay(currentDate)
  for match in matchs:
    matchHour = int(match[4][0:2])
    matchMinutes = int(match[4][3:])
    if ((60*matchHour + matchMinutes) -
      (60*currentHour + currentMinutes)) <= 16:
      player1 = getPlayerFromPlayerIdInDB(match[1], match[2])
      player2 = getPlayerFromPlayerIdInDB(match[1], match[3])
      DB.setNotifToSend(match[0])
      DB.addNotif(match, player1, player2)
