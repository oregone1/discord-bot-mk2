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
        embed = discord.Embed(color=(0x84fa), url="https://discordapp.com", description="level up")

        with open('./users.json', 'r') as f:
            data = json.load(f)

        if not str(message.author) == 'discord-bot-mk2#1717':

            data["users"][str(message.author.id)]["prog-to-next-level"] += 1

            if data["users"][str(message.author.id)]["prog-to-next-level"] >= 100 + 25 * data["users"][str(message.author.id)]["level"]:
                data["users"][str(message.author.id)]["prog-to-next-level"] = 0
                data["users"][str(message.author.id)]["level"] += 1
                embed.set_thumbnail(url=f"{message.author.avatar_url}")
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name=f"@{message.author.mention} leveled up!", value=f"{message.author} is now level {data['users'][str(message.author.id)]['level']}")
                await message.channel.send(embed=embed)

            # print(data["users"][str(message.author.id)]["prog-to-next-level"]/(100 + 25 * data["users"][str(message.author.id)]["level"]))

        else:
            print(f'bot said: {message.content}')

        with open('./users.json', 'w') as w:
            json.dump(data, w, indent=2, ensure_ascii=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('./log', 'a+') as f:
            f.writelines(f'{ctime()}: {message.author}: {message.content}\n')
        await self.update_user(message)
        print((f'{ctime()}: {message.author}: {message.content}'))
        print(message.channel.id)

    @commands.command()
    async def leaderboard(self, ctx, index=1):
        scores = {}
        i = 1
        fields = []
        with open('./users.json', 'r') as f:
            data = json.load(f)
        for user in data["users"]:
            scores[data["users"][user]["level"], data["users"][user]["prog-to-next-level"], len(scores)] = data["users"][user]["username"]
        print(sorted(scores.keys(), reverse=True))
        for score in sorted(scores.keys(), reverse=True):
            print(score)

            level_percent = score[1]/(100 + 25 * score[0]) * 100

            fields.append((f'{i}: {scores[score]}', f'{scores[score]} is at level {score[0]}\nand is {str(level_percent)[:4]}% to level {score[0] + 1}'))
            i += 1

        embed = discord.Embed(color=(0x84fa), url="https://discordapp.com", description="leaderboard")
        embed.timestamp = datetime.datetime.utcnow()

        if index == 1:
            for user in fields:
                embed.add_field(name=user[0], value=user[1], inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def register(self, ctx):
        with open('./users.json', 'r') as jsonfile:
            data = json.load(jsonfile)
        data['users'][str(ctx.message.author.id)] = json.loads('{"username": "'+str(ctx.message.author)+'", "warns": [], "level": 0, "prog-to-next-level": 0}')
        with open('./users.json', 'w') as w:
            json.dump(data, w, indent=2, ensure_ascii=False)
        await ctx.send(f'{ctx.message.author.mention} was registered to the scoreboard')

    @commands.command()
    async def score(self, ctx, user: discord.Member):
        embed = discord.Embed(color=(0x84fa), url="https://discordapp.com", description=f"{str(user)}s score")
        with open('./users.json', 'r') as f:
            data = json.load(f)
        embed.set_thumbnail(url=f"{user.avatar_url}")
        embed.add_field(name=f'user\'s level:', value=f'{user} is level {data["users"][str(user.id)]["level"]}', inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(messages(bot))
    print('\'messages\' is loaded')
