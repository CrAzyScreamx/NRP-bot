import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = commands.when_mentioned_or("%"), case_insensitive = True)
client.remove_command('help')

def token_read():
    with open('ImportentFiles/token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()

token = token_read()

@client.command()
async def re(ctx):
    if ctx.author.id == 231405897820143616:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.load_extension(f'cogs.{filename[:-3]}')

        msg = ctx.message
        await msg.delete()
        await ctx.author.send("Extensions loaded")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
