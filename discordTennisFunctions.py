# -*- coding: utf-8 -*-

# IMPORTS
from discord_slash.utils.manage_components import create_button,create_actionrow,wait_for_component
from discord_slash import ButtonStyle
import discord
import tennis
import DB


async def maj(bot, void = False):
    tennis.main()
    await sendMessages(bot, void)

async def nb(bot, ctx):
    category = DB.getChannelCategorie(ctx.channel.id)
    if category is None or category == "G" :
        nb = DB.getNumberPlayers()
        message = ("Il y a {} inscrit{} dans le tournoi".format(nb, '' if nb <2 else 's'))
        for cat in ["SM", "SD", "DM", "DD", "DX"]:
            message += "\n\t\t{}".format(numberPlayersByCategory(cat))
        await ctx.send(message)
    else :
        await ctx.send(numberPlayersByCategory(category))
    details = await askDetails(bot, ctx)
    if (details):
        if (category is None or category == "G") :
            await sendAllDetails(ctx)
        else :
            await sendCategoryDetails(ctx, category)

async def askDetails(bot, ctx):
    def check(m):
        return m.author.id == ctx.author.id and m.origin_message.id == choice.id
    buttons = [create_button(style = ButtonStyle.green, label = "Oui", custom_id = "1"),
               create_button(style = ButtonStyle.red,   label = "Non", custom_id = "0")]
    actionRow = create_actionrow(*buttons)
    choice = await ctx.send("Afficher les détails des classements ?", components = [actionRow])
    buttonCtx = await wait_for_component(bot, components = actionRow, check = check)
    await buttonCtx.edit_origin(content= "Afficher les détails des classements ? ("+buttonCtx.custom_id+")")
    return int(buttonCtx.custom_id)

async def sendAllDetails(ctx):
    title = "Nombre d'inscrits par classement pour chaque catégorie :"
    embed = discord.Embed(title = title, color = 0x9f1994)
    embed.add_field(name = "Total", value = rankingMessage(DB.getRankings()), inline=False)
    for category in ["SM", "SD", "DM", "DD", "DX"]:
        embed.add_field(name = category, value = rankingMessage(DB.getRankingsByCategory(category)), inline=False)
    await ctx.send(embed = embed)

async def sendCategoryDetails(ctx,category):
    title = "Nombre d'inscrits par classements :"
    embed = discord.Embed(title = title, color = 0x9f1994)
    embed.add_field(name = category, value = rankingMessage(DB.getRankingsByCategory(category)), inline=False)
    await ctx.send(embed = embed)

def rankingMessage(rankings):
    rankingsMessage = ""
    for ranking in ["NC", "40", "30/5", "30/4", "30/3", "30/2", "30/1", "30", "15/5", "15/4", "15/3", "15/2", "15/1", "15"]:
        rankingsMessage += "{} : {}\n".format(ranking.ljust(4), rankings.count(ranking))
    return rankingsMessage

def numberPlayersByCategory(cat):
    nb = DB.getNumberPlayersByCategory(cat)
    return ("Il y a {} inscrit{} dans la catégorie {}".format(nb, '' if nb < 2 else 's', cat))

async def sendMessages(bot, void):
    for category in ["G", "SM", "SD", "DM", "DD", "DX"]:
        await sendMessagesByCategory(bot, category, void)

async def sendMessagesByCategory(bot, cat, void):
    messages = DB.getMessages(cat)
    channelID = DB.getChannelID(cat)
    channel = await bot.fetch_channel(channelID)
    for message in messages :
        await channel.send(message[1])
        DB.deleteMessage(message[0])
    if cat == "G" and len(messages) == 0 and void :
        await channel.send("Aucune nouvelle inscription")
