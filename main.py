import discord
from discord.ext import commands
import os
from ossapi import Ossapi
import json
import db.sql_interaction as osudb

api = Ossapi(os.environ.get("CLIENT_ID"), os.environ.get("CLIENT_SECRET"))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)

@bot.slash_command()
async def userstats(ctx, id: str):
    username = api.user(id).username
    rank_highest = api.user(id).rank_highest.rank
    rank = api.user(id).rank_history.data[-1]
    embed=discord.Embed(title="User Stats", description="Grabs a users stats")
    embed.set_thumbnail(url=api.user(id).avatar_url)
    embed.add_field(name="Username", value=username, inline=False)
    embed.add_field(name="Rank", value=rank, inline=False)
    embed.add_field(name="Highest Rank", value=rank_highest, inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command()
async def usertest(ctx):
    await ctx.respond(api.user(4916057))

@bot.slash_command()
async def adduser(ctx, id: str, from_nl: bool, gamemode: str):
    username = api.user(id).username
    country = api.user(id).country.name
    
    osudb.add_players(username, id, country, from_nl, gamemode)

    embed = discord.Embed(title="Adding User", description="Adds a user to Osu!Newfoundland Database")
    embed.add_field(name="Name", value=username, inline=True)
    embed.add_field(name="From NL?", value=from_nl, inline=True)
    embed.add_field(name="Country", value=country, inline=True)
    await ctx.respond(embed=embed)

bot.run(os.environ.get("TOKEN"))
