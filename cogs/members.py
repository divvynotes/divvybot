import discord
from discord.ext import commands

import time
import traceback

class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        await channel.send(f'{member.mention} welcome to the Divvynotes server! While you\'re here, please check out and become a member of our site at https://divvynotes.com !')
    
    @commands.command(name='fetchuser', help='Fetches a user\'s information on this server.')
    async def fetchuser(self, ctx, *, member: discord.Member=None):
        if(not member):
            member = ctx.author
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)
        embed=discord.Embed(title=f'User information in: ', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name='User id: ', value=member.id, inline=True)
        embed.add_field(name='Joined Discord at: ', value=member.created_at, inline=True)
        embed.add_field(name='Permissions: ', value=perms)
        embed.set_footer(text='From Divvybot')
        
        await ctx.send(embed=embed)
    
    @fetchuser.error
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
        

def setup(bot):
    bot.add_cog(MembersCog(bot))