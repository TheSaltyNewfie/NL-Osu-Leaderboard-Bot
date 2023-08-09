import discord
from discord.ext import commands
from discord import SlashCommand
import os
from ossapi import Ossapi
import json
import db.sql_interaction as osudb
import redis
import utils

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
    embed.add_field(name="Rank", value=f"{rank:,}", inline=False)
    embed.add_field(name="Highest Rank", value=f"{rank_highest:,}", inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command()
async def adduser(ctx, id: str, from_nl: bool, gamemode: str):
    dev_role = discord.utils.get(ctx.guild.roles, name="Developer")
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")

    if dev_role or admin_role in ctx.author.roles:
        username = api.user(id).username
        country = api.user(id).country.name

        osudb.add_players(username, id, country, from_nl, gamemode)

        embed = discord.Embed(title="Adding User", description="Adds a user to Osu!Newfoundland Database")
        embed.add_field(name="Name", value=username, inline=True)
        embed.add_field(name="From NL?", value=from_nl, inline=True)
        embed.add_field(name="Country", value=country, inline=True)
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(title="Error!", description="Well bhys, shes gone.")
        embed.add_field(name="You must be an Admin or Developer to use this command", value="", inline=True)
        await ctx.respond(embed=embed)

@bot.slash_command()
async def listusers(ctx, gamemode:str):
    list_db = osudb.get_players(game_mode=gamemode, limit=8)
    
    embed = discord.Embed(title=f"NL {gamemode.upper()} Players", description="NL players within the db")

    index = 1

    for row in list_db:
        embed.add_field(name=f"{index}. {row[0]}", value=f"#{api.user(row[1]).rank_history.data[-1]:,}", inline=False)
        #await ctx.send(row[0])
        index = index+1

    await ctx.respond(embed=embed)

@bot.slash_command()
async def listusers_temp(ctx, gamemode: str):
    # Send a temporary message saying "Gathering users"
    temp_message = await ctx.respond("Gathering users")

    list_db = osudb.get_players(game_mode=gamemode, limit=8)

    embed = discord.Embed(title=f"NL {gamemode.upper()} Players", description="NL players within the db")
    index = 1

    for row in list_db:
        embed.add_field(name=f"{index}. {row[0]}", value=f"#{utils.get_rank(row[1]):,}", inline=False)
        index = index + 1

    # Delete the temporary message
    await temp_message.edit_original_response(f"{embed}")  # Temp fix for something.

    # Respond with the new embed
    #await ctx.respond(embed=embed)


@bot.slash_command()
async def leaderboard(ctx, gamemode:str):
    embedd=discord.Embed(title="Leaderboard will soon show", description="If the server is caching new results, it will take a minute or so to show", color=0x00ff00)
    wait_message = await ctx.respond(embed=embedd)
    testing_feature = {'std':'Standard',
                       'mania':'Mania',
                       'ctb':'Catch The Beat',
                       'taiko':'Taiko'}

    players = osudb.get_players_nl(gamemode)
    leaderboard_data = {}
    for player_name, player_id in players:
        rank = utils.get_rank(player_id)
        if rank is not None:
            leaderboard_data[player_name] = rank
    
    sorted_leaderboard = sorted(leaderboard_data.items(), key=lambda x: x[1])
    limit_list = sorted_leaderboard[:8]
    embed=discord.Embed(title="Leaderboard", description=f"Here are the top Newfies for {testing_feature[gamemode.lower()]}!", color=0x00ff00)
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/tAiyncgkMCfcsLwR7GHYL18_mm7R5F8EUMkb4VOKVK0/https/cdn.discordapp.com/icons/1109560747211620433/e77a061f86b4da5b876f705d9ff6e7ce.webp")
    for idx, (player_name, rank) in enumerate(limit_list, start=1):
        embed.add_field(name=f"{idx}. {player_name}", value=f"#{rank:,}", inline=False)
    embed.set_footer(text="Only showing top 8 because of discord problems")

    await wait_message.delete_original_response()

    await ctx.respond(embed=embed)


bot.run(os.environ.get("TOKEN"))
