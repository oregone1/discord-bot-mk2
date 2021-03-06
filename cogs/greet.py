import discord
import datetime
import asyncio
import json
from discord.ext import commands
from discord import Embed

class greet(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('./users.json', 'r') as jsonfile:
            data = json.load(jsonfile)
        embed = discord.Embed(color=(0x84fa), url="https://discordapp.com",
        description=f"Welcome to the server, {member.mention}!")

        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        channel = self.bot.get_channel(id=789043746255536169)

        await channel.send(embed=embed)
        data['users'][str(member.id)] = json.loads('{"username": "'+str(member)+'", "warns": [], "level": 0, "prog-to-next-level": 0}')
        with open('./users.json', 'w') as w:
            json.dump(data, w, indent=2, ensure_ascii=False)

        role = discord.utils.get(member.guild.roles, name="Cool Person")
        await member.add_roles(role)

        print(f'{member} joined the server, was given {role}, and was registered to the json file')

def setup(bot):
    bot.add_cog(greet(bot))
    print('\'greet\' is loaded')
