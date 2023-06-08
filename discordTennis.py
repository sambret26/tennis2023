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
  await DTF.maj(bot, void=True)


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
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.info(ctx, name)


@bot.command()
async def result(ctx, name=None):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.result(bot, ctx, name)


@bot.command()
async def resultat(ctx, name=None):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.result(bot, ctx, name)


@bot.command()
async def modifCourt(ctx, name=None):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifCourt(bot, ctx, name)


@bot.command()
async def modifJoueur1(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifJoueur1(ctx, args)


@bot.command()
async def modifJoueur2(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifJoueur2(ctx, args)


@bot.command()
async def modifJour(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifJour(ctx, args)


@bot.command()
async def modifHeure(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifHeure(ctx, args)


@bot.command()
async def modifPg(ctx, *args):
  if ctx.message.guild.id != DB.getGuildID(): return
  await DTF.modifPg(ctx, args)


@bot.command()
@commands.check(isAllowed)
async def clear(ctx, nombre: int = 100):
  await ctx.channel.purge(limit=nombre + 1, check=lambda msg: not msg.pinned)


  ### RECURING TASKS


@bot.event
async def recurring_task():
  await bot.wait_until_ready()
  while not bot.is_closed():
    await DTF.maj(bot)
    await asyncio.sleep(60)


def main():
  bot.loop.create_task(recurring_task())
  bot.run(DB.getDiscordToken())
