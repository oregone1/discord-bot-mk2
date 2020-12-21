import discord
import youtube_dl
import os
import shutil
import json
from discord.ext import commands
from discord.utils import get
from youtube_search import YoutubeSearch
from gtts import gTTS

class voice(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            self.voice = get(self.bot.voice_clients, guild=ctx.guild)

            if self.voice and self.voice.is_connected():
                await self.voice.move_to(channel)

            else:
                await channel.connect()
                print(f'bot connected to {channel}')

            await ctx.send(f'joined {channel}')
        except exception as e:
            print('critical error:', e)

    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            #self.voice = get(self.bot.voice_clients, guild=ctx.guild)

            if self.voice and self.voice.is_connected():
                await self.voice.disconnect()
                print('bot disconnected')
                await ctx.send('disconnecting...')
            else:
                print('could not disconnect from channel')
                await ctx.send('bot not in channel')
                await self.voice.disconnect()

        except:
            await ctx.send('cannot leave when not in a channel')
            print('leave called while not in a channel')

    @commands.command(alliases=['p'])
    async def play(self, ctx, *args):
        input = ''.join(args[:])

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            }

        if 'https://www.youtube.com' not in input:
            results = YoutubeSearch(input, max_results=1).to_dict()
            input = 'https://www.youtube.com' + str(results[0]['url_suffix'])

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([input])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        self.voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: ctx.send(name))
        self.voice.source = discord.PCMVolumeTransformer(voice.source)
        self.voice.source.volume = 0.25

        os.remove('./song.mp3') # could be problematic, maybe should be moved to self.voice.play lambda function

def setup(bot):
    bot.add_cog(voice(bot))
    print('\'voice\' is loaded')
