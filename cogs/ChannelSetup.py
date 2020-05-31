import discord
import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
from collections.abc import Sequence


class ChannelSetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['setfch'])
    async def setChannel(self, ctx):
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        connection = connect()
        facsheet = connection.worksheet("Factions")
        faclist = facsheet.get("A4:A")
        sentence = listmaker(faclist)
        embed = discord.Embed(
            description = 'Choose one of the listed factions to set this channel to\nNOTE: Setting this channel will make it receive new applications for the selected channel',
            colour = discord.Colour.blue()
        )
        embed.add_field(name = ' ‏‏‎ ', value="__**LIST**__\n{0}".format(sentence))
        msg = await ctx.send(embed=embed)
        for i in range(len(faclist)):
            await msg.add_reaction(emojis[i])
        re = await self.client.wait_for('reaction_add', check = lambda r, u: r.emoji in emojis and r.message.id == msg.id and u == ctx.author)
        for i in range(0, len(faclist)):
            if str(emojis[i]) == str(re[0]):
                await ctx.author.send("Channel has been set for {0}".format(faclist[i][0]))
                await msg.delete()
                await ctx.message.delete()
                ss = connection.worksheet(faclist[i][0])
                ss.update("N2", str(ctx.channel.id))
                break
    @commands.command(aliases=['setgch'])
    async def SetGeneral(self, ctx):
        await ctx.message.delete()
        with open('ImportentFiles/GeneralFile.txt', 'w') as f:
            f.write(str(ctx.channel.id))
            f.close()
        await ctx.author.send("Channel has been set for app purposes")


def setup(client):
    client.add_cog(ChannelSetup(client))


def connect():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("ImportentFiles/DriveAPIcreds.json", scope)

    gc = gspread.authorize(creds)

    sheet = gc.open_by_key('1p_v4ofnd5_oBbRIM6i47skC5rhPdWd_BsWrKUM7QHKM')
    return sheet

def listmaker(data):
    sentence = ""
    for i in range(len(data)):
        sentence += str(i+1) + ". " + str(data[i][0]) + "\n"
    return sentence
