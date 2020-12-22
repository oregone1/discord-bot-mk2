#!/usr/bin/env python3

import discord
import time
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='./', case_insensitive=True, intents=intents)
client.remove_command('help')

with open('secret.txt', 'r') as f:
    API_KEY =  f.read()

extensions = [
            'cogs.greet',
            'cogs.messages',
            'cogs.admin',
            'cogs.help',
            'cogs.voice'
]

for extension in extensions:
    client.load_extension(extension)

@client.event
async def on_ready():
    print(f'logged in as {client.user.name} - {client.user.id}')

client.run(API_KEY)
