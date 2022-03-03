import discord
from discord.ext import commands

import time
import traceback

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
        
    @commands.command(name='feedback', help='Sends feedback on how I can improve the bot, or if there were any bugs that you encountered!')
    @commands.cooldown(3, 300.0, commands.BucketType.user)
    async def feedback(self, ctx, *message):
        f = open('feedback.txt', 'a')
        curtime = time.strftime('%H:%M:%S', time.localtime())
        output = f'\n[{curtime}] {" ".join(message)}'
        f.write(output)
        f.close()
        await ctx.send('Feedback successfully sent and recorded!')
    
    @about.error
    @invite.error
    @feedback.error
    async def err_handling(self, ctx, error: commands.CommandError):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
#             log_event('Unsucessful. Missing arg.')
            await ctx.send('You need an argument here! Try `div help <command>`')
        elif(isinstance(error, discord.ext.commands.errors.CommandOnCooldown)):
            await ctx.send(error)
        else:
            await ctx.send(f'An exception occured during your request! I have logged this error and sent it for review!\nError details here:||`{error}`||')
            f = open('err.txt', 'a')
            curtime = time.strftime('%H:%M:%S', time.localtime())
            output = f'\n\n[{curtime}]\n{traceback.format_exc()}'
            f.write(output)
            f.close()
        
#         log_event(str(ctx.author) + ': ' + str(error))


def setup(bot):
    bot.add_cog(AboutCog(bot))