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
        self.queue = []

    async def queue(self, url):
        queue.append(url)

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)

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
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.disconnect()
                print('bot disconnected')
                await ctx.send('disconnecting...')
            else:
                print('could not disconnect from channel')
                await ctx.send('bot not in channel')
                await voice.disconnect()

        except:
            await ctx.send('cannot leave when not in a channel')
            print('leave called while not in a channel')

    @commands.command()
    async def tts(self, ctx, *args):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        say = ' '.join(args[:])
        tts = gTTS(say)
        tts.save('ttssay.mp3')

        voice.play(discord.FFmpegPCMAudio("ttssay.mp3"), after=lambda e: print("tts done!"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.50

    @commands.command(aliases=['p'])
    async def play(self, ctx, *args):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
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
            await ctx.send(f'found: {results[0]["title"]}')
            input = 'https://www.youtube.com' + str(results[0]['url_suffix'])

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([input])

        if not voice.is_playing():

            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    name = file
                    print(f"Renamed File: {file}\n")
                    os.rename(file, "song.mp3")

            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: os.remove('./song.mp3'))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 2.25

        else:
            self.queue(input) # TODO: queue function
            await ctx.send('queue test')

def setup(bot):
    bot.add_cog(voice(bot))
    print('\'voice\' is loaded')
