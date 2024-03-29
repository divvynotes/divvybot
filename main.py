import discord
from discord.ext import commands

import time
import traceback
import os
from dotenv import load_dotenv

def get_prefix(bot, message):
    prefixes = ['div ', 'divvy ', 'obama', '\\']
    return commands.when_mentioned_or(*prefixes)(bot, message)

def log_event(string):
    f = open('logs.txt', 'a')
    t = time.localtime()
    cur_t = time.strftime('%H:%M:%S', t)
    eventstr = '\n[' + cur_t + ']' + string
    print(eventstr)
    f.write(eventstr)
    f.close()


init_ext = ['cogs.members', 'cogs.about', 'cogs.owner', 'cogs.moderation']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, owner_id = 656727549681860658, description='The Divvynotes Discord bot', intents=intents)


if __name__ == '__main__':
    for ext in init_ext:
        bot.load_extension(ext)

@bot.event
async def on_ready():
    log_event('Bot is ready!')
    await bot.change_presence(activity=discord.Game(name='https://divvynotes.com', type=1, url='https://divvynotes.com'))

bot.run(TOKEN, bot=True, reconnect=True)