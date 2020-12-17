#!/usr/bin/env python3

import discord
from discord.ext import commands
from cogs.greet import greet

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='./', case_insensitive=True, intents=intents)

with open('secret.txt', 'r') as f:
    API_KEY =  f.read()

extensions = [
            'cogs.greet'
]

for extension in extensions:
    client.load_extension(extension)

@client.event
async def on_ready():
    print(f'logged in as {client.user.name} - {client.user.id}')

client.run(API_KEY)
