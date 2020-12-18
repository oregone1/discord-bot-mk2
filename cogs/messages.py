import discord
from discord.ext import commands
import json

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
            print(exp[0])
            exp[0] = int(exp[0]) + 1
            if int(exp[0]) > 99:
                exp[0], exp[1] = int(exp[0]), int(exp[1])
                exp[0] = 0
                exp[1] += 1
                await message.channel.send(f'{author} levelled up!')
                print(exp[0], exp[1])

            data['user-xp'][str(author)] = f'{exp[0]},{exp[1]}'
            with open('./users.json', 'w') as w:
                print(data)
                json.dump(data, w, indent=2, ensure_ascii=False)

        else:
            print('message sent was by discord-bot and was therefor ignored')

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.update_user(message)

def setup(bot):
    bot.add_cog(messages(bot))
    print('\'messages\' is loaded')
