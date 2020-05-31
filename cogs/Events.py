import discord
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    #events:
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='%h'))
        print("Bot is ready!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.author.send(error)
            await ctx.message.delete()



def setup(client):
    client.add_cog(Events(client))
