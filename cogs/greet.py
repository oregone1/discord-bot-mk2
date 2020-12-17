import discord
import datetime
import asyncio
from discord.ext import commands
from discord import Embed

class greet(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print('test')
        embed = discord.Embed(color=(0x84fa), url="https://discordapp.com",
        description=f"Welcome to the server, {member.mention}! Please go to #ip to join the server.")

        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        channel = self.bot.get_channel(id=789043746255536169)

        await channel.send(embed=embed)
        print(member)

def setup(bot):
    bot.add_cog(greet(bot))
    print('\'greet\' is loaded')
