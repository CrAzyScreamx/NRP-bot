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



def setup(client):
    client.add_cog(Events(client))
