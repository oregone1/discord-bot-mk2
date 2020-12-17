import discord
import asyncio
import datetime
import os
import time
from discord.ext import commands
from discord import Embed
import subprocess
import random

class admin(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, cog: str):
        if 'admin' not in cog:
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                await ctx.send(f'error {cog} not found')
                return
            await ctx.send('sucess!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'error {cog} not found')
            return
        await ctx.send('sucess!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            await ctx.send(f'reloading {cog}')
            time.sleep(1)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'error {cog} not found')
            return
        await ctx.send('sucess!')
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        time.sleep(.3)
        await ctx.channel.purge(limit = limit + 1)

def setup(bot):
    bot.add_cog(admin(bot))
    print('\'admin\' is loaded')
