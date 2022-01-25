import discord
from discord.ext import commands

class AboutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='about', help='Displays about message!')
    async def about(self, ctx):
        await ctx.send('This is the Divvynotes bot for Discord! Currently it doesn\' do much... \nIf you haven\'t already, join us on https://divvynotes.com !')
    
    @commands.command(name='invite', help='Gives invite link to invite bot.')
    async def invite(self, ctx):
        embedVar = discord.Embed(title="Bot Invite", description="Open this [link](https://discord.com/api/oauth2/authorize?client_id=934696329559547914&permissions=8&scope=bot) to invite this bot to your server!", color=0x00ff00)
        await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(AboutCog(bot))