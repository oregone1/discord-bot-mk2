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
        author = str(message.author)

        with open('./users.json', 'r') as f:
            data = json.load(f)

        if not author == 'discord-bot-mk2#1717':

            data["users"][author]["prog-to-next-level"] += 1

            if data["users"][author]["prog-to-next-level"] >= 100 + 25 * data["users"][author]["level"]:
                data["users"][author]["prog-to-next-level"] = 0
                data["users"][author]["level"] += 1
                embed.set_thumbnail(url=f"{message.author.avatar_url}")
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name=f"@{message.author.mention} leveled up!", value=f"{author} is now level {data['users'][author]['level']}")
                await message.channel.send(embed=embed)

        else:
            print('message sent was by discord-bot and was therefor ignored')

        with open('./users.json', 'w') as w:
            json.dump(data, w, indent=2, ensure_ascii=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('./log', 'a+') as f:
            f.writelines(f'{ctime()}: {message.author}: {message.content}\n  ')
        await self.update_user(message)

    @commands.command()
    async def leaderboard(self, ctx):
        scores = {}
        i = 1
        with open('./users.json', 'r') as f:
            data = json.load(f)
        embed = discord.Embed(color=(0x84fa), url="https://discordapp.com", description="leaderboard")
        for user in data["users"]:
            scores[data["users"][user]["level"]] = data["users"][user]["username"]
        print(sorted(scores.keys(), reverse=True))
        for score in sorted(scores.keys(), reverse=True):
            if i < 11:
                print(score)
                #print(data["users"][scores[score]]["level"])

                #percentage = data["users"][scores[score]]["prog-to-next-level"]
                #percentage_mod = 100 + 25 * score

                #print(percentage, percentage_mod, percentage/percentage_mod, percentage/percentage_mod*100)

                embed.add_field(name=f'{i}: {scores[score]}', value=f'{scores[score]} is at level {score}', inline=False)#value=f'{(data["users"][scores[score]]["prog-to-next-level"] / 100 + 25 * score) * 100}% to level {score + 1}', inline=False)
                i += 1
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    async def register(self, ctx):
        with open('./users.json', 'r') as jsonfile:
            data = json.load(jsonfile)
        data['users'][str(ctx.message.author)] = json.loads('{"username": "'+str(ctx.message.author)+'", "warns": [], "level": 0, "prog-to-next-level": 0}')
        with open('./users.json', 'w') as w:
            json.dump(data, w, indent=2, ensure_ascii=False)
        await ctx.send(f'{ctx.message.author.mention} was registered to the scoreboard')

def setup(bot):
    bot.add_cog(messages(bot))
    print('\'messages\' is loaded')
