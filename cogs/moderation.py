import discord
from discord.ext import commands

import traceback

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='nickall', help='Changes everyone\'s nickname to what you choose!')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 180.0, commands.BucketType.guild)
    async def nickall(self, ctx, *newname):
        await ctx.send('Changing nicknames, please be patient with the bot...')
        changecounter = 0
        unchangeable = []
        newnamestr = ' '.join(newname)
        async for member in ctx.guild.fetch_members(limit=None):
            try:
                await member.edit(nick=newnamestr)
                changecounter += 1
            except discord.errors.Forbidden:
                unchangeable.append(str(member.name + '#' + member.discriminator))
        await ctx.send(f'Edited {changecounter} accounts to the nickname of: "{newnamestr}"\nI was unable to change the nick of: `{unchangeable}`')
        
    

    @commands.command(name='ban', help='Bans a member; does not work on members with administrator perms.')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await ctx.guild.ban(member, reason=reason)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`SUCCESS`**: Banned {str(member)}')
    
    @commands.command(name='kick', help='Kick a member; does not work on members with administrator perms.')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            if(member.guild_permissions.administrator):
                await ctx.send(f'{str(member)} has the administrator permission from at least one of their roles.')
                return
            await ctx.guild.kick(member, reason=reason)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`SUCCESS`**: Kicked {str(member)}')
    
    @ban.error
    @kick.error
    @nickall.error
    async def err_handling(self, ctx, error: commands.CommandError):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
#             log_event('Unsucessful. Missing arg.')
            await ctx.send('You need an argument here! Try `div help <command>`')
        elif(isinstance(error, discord.ext.commands.errors.CommandOnCooldown)):
            await ctx.send(error)
            
        else:
            await ctx.send('An exception occured during your request: `' + str(error) + '`')
        print(traceback.format_exc())
#         log_event(str(ctx.author) + ': ' + str(error))
    
        
def setup(bot):
    bot.add_cog(ModerationCog(bot))