import discord
from discord.ext import commands

class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        await guild.system_channel.send('{member.mention} welcome to the Divvynotes server! While you\'re here, please check out and become a member of our site at https://divvynotes.com !')
    
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

        

def setup(bot):
    bot.add_cog(MembersCog(bot))