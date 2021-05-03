#AUTHOR: duhack
#GITHUB: https://github.com/duhack

import discord
from discord.ext import commands, tasks
from discord.utils import get

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents) #W MIEJSCU '!' USTAW PREFIX BOTA

extensions = ['commands', 'events']

for extension in extensions:
    bot.load_extension(extension)

bot.run('') #TUTAJ WPISZ TOKEN BOTA