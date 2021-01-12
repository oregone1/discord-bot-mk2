import discord
import time
import random
import datetime
import json
from discord.ext import commands
from discord.ext.commands import MemberConverter
converter = MemberConverter()

class admin(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            await ctx.send(f'{cog} reloaded')
        except Exception as e:
            await ctx.send('error')
            if e == 'discord.ext.commands.errors.MissingPermissions: You are missing Administrator permission(s) to run this command.':
                await ctx.send('your must have admin permissions to run this command.')
            elif 'discord.ext.commands.errors.MissingRequiredArgument: cog is a required argument that is missing.' in e:
                await ctx.send('you must specify a cog to reload')
            else:
                await ctx.send('unkown error, check the log for details')
                print(e)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
            await ctx.send(f'{cog} loaded')
        except Exception as e:
            await ctx.send('error')
            if e == 'discord.ext.commands.errors.MissingPermissions: You are missing Administrator permission(s) to run this command.':
                await ctx.send('your must have admin permissions to run this command.')
            elif 'discord.ext.commands.errors.MissingRequiredArgument: cog is a required argument that is missing.' in e:
                await ctx.send('you must specify a co🇵g to load')
            else:
                await ctx.send('unkown error, check the log for details')
                print(e)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            await ctx.send(f'{cog} unloaded')
        except Exception as e:
            await ctx.send('error')
            if e == 'discord.ext.commands.errors.MissingPermissions: You are missing Administrator permission(s) to run this command.':
                await ctx.send('your must have admin permissions to run this command.')
            elif 'discord.ext.commands.errors.MissingRequiredArgument: cog is a required argument that is missing.' in e:
                await ctx.send('you must specify a cog to unload')
            else:
                await ctx.send('unkown error, check the log for details')
                print(e)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        time.sleep(.3)
        await ctx.channel.purge(limit = limit + 1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} was kicked by {ctx.message.author} for {reason}')

    @commands.Cog.listener()
    async def on_message(self, message):
        reaction_list = ['🇵','🇴','🇰','🇮','🇲','🇦','🇳','🇪']
        if random.randint(0, 100) == 27:
            for reaction in reaction_list:
                await message.add_reaction(reaction)

    @commands.command()
    async def setup(self, ctx, autoreg: bool):
        persons = {}
        people = {} # huh
        if str(ctx.author) == 'justsomelasagna#0847':
            embed = discord.Embed(color=(0x84fa), url="https://discordapp.com",
            description="unregistered members")
            with open("users.json", "r") as f:
                data = json.load(f)

            for person in ctx.author.guild.members:
                persons[person.name+'#'+person.discriminator] = person.id

            for user in data["users"]:
                people[data["users"][user]["username"]] = user

            for person in people:
                try:
                    persons.pop(person)
                except:
                    print(person)

            for person in persons:
                person = await converter.convert(ctx, person)
                embed.add_field(name=str(person), value=person.id, inline=True)
                if autoreg:
                    data['users'][str(person.id)] = json.loads('{"username": "'+str(person)+'", "warns": [], "level": 0, "prog-to-next-level": 0}')
                    await ctx.send(f'{person} was registered')
                    with open('./users.json', 'w') as w:
                        json.dump(data, w, indent=2, ensure_ascii=False)

            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command()
    async def test(self, ctx):
        await ctx.send('working')

def setup(bot):
    bot.add_cog(admin(bot))
    print('\'admin\' is loaded')
