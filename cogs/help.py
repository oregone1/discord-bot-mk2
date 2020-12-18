import discord
import asyncio
import datetime
from discord.ext import commands
from discord import Embed
import json
import os
import datetime

class help(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        with open("help.json") as f:
            data = json.load(f)

        embed = discord.Embed(color=(0x84fa), url="https://discordapp.com/", description="Help")
        for i in range(len(data["commands"])):
            embed.add_field(name=data['commands'][i]["name"], value=data["commands"][i]["functions"],inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))
    print('\'help\' is loaded')
