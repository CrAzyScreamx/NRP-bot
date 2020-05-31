import discord
from discord.ext import commands


class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(case_insensitive=True, aliases=['h'], invoke_without_command=True)
    async def help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title = '__**Application Bot Help System**__',
            description = "This command is used to know all the commands of the bot!\n\n__**Application commands**__\n%apply\n\n**Instructions**\n1. Choose the faction you wish to apply to\n2. Answer the questions given to you via Direct Messages in discord.\n3. Press wether or not you want your application to be sent to command.\n\n__**Restricted Commands**__\n%help a - Only do this if you're an admin (won't work for normal players!)\n%help f - Only do this if you're a faction member (won't work for normal players)",
            colour=discord.Colour.blue()
        )
        await ctx.author.send(embed=embed)

    @help.command(case_insensitive=True, aliases=['a'])
    async def Admin(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title = '__**Application Bot Help System (Admin Page)**__',
            description = "This admin page is for admins only!\n\n__**Commands**__\n%setgch - Sets a channel to be a general application channel\n%setfch - Sets a faction channel by the faction you pick (once typed you'll get a list of what channel you want to set it to)",
            colour = discord.Colour.blue()
        )
        await ctx.author.send(embed=embed)

    @help.command(case_insensitive=True, aliases=['f'])
    async def Faction(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title = '__**Application Bot Help System (Faction Page)**__',
            description = "This faction page is for faction commands ONLY!\n\n__**Commands**__\n➨ %n p [user] - Notifies the user his application is on pending state\n➨ %n i [user] - Notifies the user his application has moved to the interview phase\n➨ %n a [user] - Notifies the user his application has been accepted\n➨ %n r [user] - Notifies the user his application has been rejected\n**User**\nThe user is applied by mentioning someone.\nIn order to mention someone you must type his full DISPLAYED NAME in order to notify him. the script won't respond without a mention.",
            colour = discord.Colour.blue()
        )
        await ctx.author.send(embed=embed)




def setup(client):
    client.add_cog(help(client))
