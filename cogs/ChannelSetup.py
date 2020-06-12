import discord
import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
from collections.abc import Sequence


class ChannelSetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def is_permed(ctx):
        checker = False
        connection = connect()
        ws = connection.worksheet("Command Roles")
        roles_id = ws.get('F5:F')
        roles_id2 = ws.get("C5:C")
        roles = []
        for i in range(0, len(roles_id)):
            roles.append(str(roles_id[i][0]))
        for i in range(0, len(roles_id2)):
            roles.append(str(roles_id2[i][0]))
        aroles = ctx.author.roles
        role_names = []
        for i in range(0, len(aroles)):
            role_names.append(aroles[i].name)
        for i in range(0, len(roles)):
            if roles[i] in role_names:
                checker = True
        return checker

    @commands.command(aliases=['setfch'])
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
    async def SetGeneral(self, ctx):
        await ctx.message.delete()
        with open('ImportentFiles/GeneralFile.txt', 'w') as f:
            f.write(str(ctx.channel.id))
            f.close()
        await ctx.author.send("Channel has been set for app purposes")

    @commands.command(aliases=['sets'])
    @commands.check(is_permed)
    async def SetState(self, ctx, state=None):
        if state == None or state != 'open' != state != 'close':
            await ctx.message.delete()
            await ctx.author.send("You must provide the state ``open`` or ``close``")
        else:
            emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            connection = connect()
            facsheet = connection.worksheet("Factions")
            faclist = facsheet.get("A4:A")
            sentence = listmaker(faclist)
            embed = discord.Embed(
                description = 'Choose one of the listed factions to set the state to',
                colour = discord.Colour.blue()
            )
            embed.add_field(name = ' ‏‏‎ ', value="__**LIST**__\n{0}".format(sentence))
            msg = await ctx.send(embed=embed)
            for i in range(len(faclist)):
                await msg.add_reaction(emojis[i])
            re = await self.client.wait_for('reaction_add', check = lambda r, u: r.emoji in emojis and r.message.id == msg.id and u == ctx.author)
            for i in range(0, len(faclist)):
                if str(emojis[i]) == str(re[0]):
                    await ctx.author.send("Faction's state has been set to ``{0}``".format(state))
                    await msg.delete()
                    await ctx.message.delete()
                    ss = connection.worksheet(faclist[i][0])
                    ss.update("O2", str(state))
                    with open('ImportentFiles/GeneralFile.txt', 'r') as f:
                        ids = f.readlines()
                        channel = self.client.get_channel(int(ids[0].strip()))
                    break
            if state == 'open': await channel.send("Applications for {0} are now OPEN!".format(faclist[i][0]))
            else: await channel.send("Applications for {0} are now CLOSED!".format(faclist[i][0]))


    #Update Roles on Website:
    @commands.command(aliases=['ur'])
    @commands.has_permissions(administrator=True)
    async def UpdateRoles(self, ctx):
        await ctx.message.delete()
        connection = connect()
        ws = connection.worksheet("Role List")
        roles = ctx.guild.roles
        for i in range(1, len(roles)):
            ws.update(f"A{i}", roles[i].name)
            ws.update(f"B{i}", str(roles[i].id))


def setup(client):
    client.add_cog(ChannelSetup(client))


def connect():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("ImportentFiles/DriveAPIcreds.json", scope)

    gc = gspread.authorize(creds)
    with open('ImportentFiles/SheetID.txt', 'r') as f:
        ids = f.readlines()
        id = ids[0].strip()
    sheet = gc.open_by_key(id)
    return sheet

def listmaker(data):
    sentence = ""
    for i in range(len(data)):
        sentence += str(i+1) + ". " + str(data[i][0]) + "\n"
    return sentence
