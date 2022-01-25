import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='nickall', help='Changes everyone\' nickname to what you choose!')
    @has_permissions()
    def nickall