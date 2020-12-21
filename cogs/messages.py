import discord
import json
import datetime
from discord.ext import commands
from discord import Embed
from time import ctime

class messages(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    async def update_user(self, message):
        author = message.author
        if not str(author) == 'discord-bot-mk2#1717':
            with open('./users.json', 'r') as f:
                data = json.load(f)
            exp = data['user-xp'][str(author)]
            exp = exp.split(',')
            print(exp[1])
            exp[1] = int(exp[1]) + 1
            if int(exp[1]) > 99:
                exp[0], exp[1] = int(exp[0]), int(exp[1])
                exp[1] = 0
                exp[0] += 1
                embed = discord.Embed(color=(0x84fa), url="https://discordapp.com", description="level up")
                embed.set_thumbnail(url=f"{author.avatar_url}")
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name='level up', value=f'{author} has reached level {exp[0]}')
                await message.channel.send(embed=embed)
                print(exp[0],':', exp[1])

            data['user-xp'][str(author)] = f'{exp[0]},{exp[1]}'
            with open('./users.json', 'w') as w:
                print(data)
                json.dump(data, w, indent=2, ensure_ascii=False)

        else:
            print('message sent was by discord-bot and was therefor ignored')

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('./log', 'a+') as f:
            f.writelines(f'{ctime()}: {message.author}: {message.content}\n  ')
        await self.update_user(message)

    @commands.command()
    async def leaderboard(self, ctx):
        leaderboard_order = {}
        value_list = []
        with open('./users.json', 'r') as f:
            data = json.load(f)
        embed = discord.Embed(color=(0x84fa), url="https://discordapp.com", description="leaderboard")

        leaderboard_order = data['user-xp']

        listofTuples = sorted(leaderboard_order.items() , reverse=True, key=lambda x: x[1])
        for i, elem in enumerate(listofTuples):
            elem_0, elem_1 = elem[1].split(',')[0], elem[1].split(',')[1]
            embed.add_field(name=f'{i + 1}: {elem[0]}', value=f'level {elem_0} \n {elem_1}% to next level', inline=False)

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(messages(bot))
    print('\'messages\' is loaded')
