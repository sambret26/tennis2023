# -*- coding: utf-8 -*-

# IMPORTS
import sys

sys.path.append("modules")

import discord
from discord.ext import commands
from discord_slash import SlashCommand
import asyncio
import DB
import discordTennisFunctions as DTF
import schedule
import time
import cal

intent = discord.Intents(messages=True, members=True, guilds=True)
bot = commands.Bot(command_prefix="$", description="Sam's API", intents=intent)
slash = SlashCommand(bot, sync_commands=True)


def isAllowed(ctx):
  return int(ctx.author.id) == int(DB.getSamID())

  ### EVENTS


# @bot.event
# async def on_command_error(ctx,error):
#     if isinstance(error,commands.CheckFailure):
#         await ctx.send("Tu ne disposes pas des droits necessaires pour cette action...")
#     else :
#         await ctx.send(error)

### CMD


@bot.command()
async def maj(ctx):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.maj(bot)


@bot.command()
async def nb(ctx):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.nb(bot, ctx)


@bot.command()
async def info(ctx, name=None):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.info(ctx, name)


@bot.command()
async def infos(ctx, name=None):
  await info(ctx, name)


@bot.command()
async def result(ctx, name=None):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.result(bot, ctx, name)


@bot.command()
async def resultat(ctx, name=None):
  await result(ctx, name)


@bot.command()
async def modifCourt(ctx, name=None):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifCourt(bot, ctx, name)


@bot.command()
async def mc(ctx, name=None):
  await modifCourt(ctx, name)


@bot.command()
async def modifJoueur1(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifJoueur1(ctx, args)


@bot.command()
async def mj1(ctx, *args):
  await modifJoueur1(ctx, *args)


@bot.command()
async def modifJoueur2(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifJoueur2(ctx, args)


@bot.command()
async def mj2(ctx, *args):
  await modifJoueur2(ctx, *args)


@bot.command()
async def modifJour(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifJour(ctx, args)


@bot.command()
async def mj(ctx, *args):
  await modifJour(ctx, *args)


@bot.command()
async def modifHeure(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifHeure(ctx, args)


@bot.command()
async def mh(ctx, *args):
  await modifHeure(ctx, *args)


@bot.command()
async def modifPg(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifPg(ctx, args)


@bot.command()
async def mpg(ctx, *args):
  await modifPg(ctx, *args)


@bot.command()
async def pg(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.pg(ctx, args)


@bot.command()
async def programmation(ctx, *args):
  await pg(ctx, *args)


@bot.command()
async def program(ctx, *args):
  await pg(ctx, *args)


@bot.command()
async def updateCal(ctx):
  await cal.update(ctx)


@bot.command()
async def cmd(ctx):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.cmd(ctx)


@bot.command()
async def command(ctx):
  await cmd(ctx)


@bot.command()
async def commandes(ctx):
  await cmd(ctx)


@bot.command()
@commands.check(isAllowed)
async def clear(ctx, nombre: int = 100):
  await ctx.channel.purge(limit=nombre + 1, check=lambda msg: not msg.pinned)

  ### RECURING TASKS


async def recurring_task():
  await bot.wait_until_ready()

  while not bot.is_closed():
    schedule.run_pending()
    await asyncio.sleep(1)


def main():
  schedule.every().minute.at(":00").do(
    lambda: asyncio.create_task(DTF.sendMessages(bot)))
  schedule.every().minute.at(":30").do(
    lambda: asyncio.create_task(DTF.maj(bot)))
  bot.loop.create_task(recurring_task())
  bot.run(DB.getDiscordToken())
