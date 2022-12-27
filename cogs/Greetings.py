import discord
from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}')

    @commands.command(aliases=['hi'])
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hi {member.name} \:)')
        else:
            await ctx.send(f'hii again {member.name} :joy:')
        self._last_member = member


async def setup(bot):
    await bot.add_cog(Greetings(bot))