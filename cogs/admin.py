import discord
import time
from discord.ext import commands

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
                await ctx.send('you must specify a cog to load')
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

def setup(bot):
    bot.add_cog(admin(bot))
    print('\'admin\' is loaded')
