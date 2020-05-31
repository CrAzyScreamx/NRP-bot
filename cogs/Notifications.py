import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections.abc import Sequence

class Notifications(commands.Cog):


    def __init__(self, client):
        self.client = client


    @commands.group(case_insensitive=True, aliases=['n'], invoke_without_command=True)
    async def Notify(self, ctx):
        await ctx.send("You must choose if the app is pending, accepted or rejected!")

    @Notify.command(case_insensitive=True, aliases=['p'])
    async def Pending(self, ctx, mention=None):
        connection = connect()
        if CheckC(ctx.channel.id, connection) == True:
            if mention == None or mention[0] != '<':
                await ctx.author.send("You must mention a user!")
                await ctx.message.delete()
            else:
                await Notif(self, ctx, mention, 'p', ctx.channel.id, connection)
        else: await ctx.message.delete()

    @Notify.command(case_insensitive=True, aliases=['i'])
    async def Interview(self, ctx, mention=None):
        connection = connect()
        if CheckC(ctx.channel.id, connection) == True:
            if mention == None or mention[0] != '<':
                await ctx.author.send("You must mention a user!")
                await ctx.message.delete()
            else:
                await Notif(self, ctx, mention, 'i', ctx.channel.id, connection)
        else: await ctx.message.delete()

    @Notify.command(case_insensitive=True, aliases=['a'])
    async def Accept(self, ctx, mention=None):
        connection = connect()
        if CheckC(ctx.channel.id, connection) == True:
            if mention == None or mention[0] != '<':
                await ctx.author.send("You must mention a user!")
                await ctx.message.delete()
            else:
                await Notif(self, ctx, mention, 'a', ctx.channel.id, connection)

        else: await ctx.message.delete()

    @Notify.command(case_insensitive=True, aliases=['r'])
    async def Reject(self, ctx, mention=None):
        connection = connect()
        if CheckC(ctx.channel.id, connection) == True:
            if mention == None or mention[0] != '<':
                await ctx.author.send("You must mention a user!")
                await ctx.message.delete()
            else:
                await Notif(self, ctx, mention, 'r', ctx.channel.id, connection)
        else: await ctx.message.delete()


def setup(client):
    client.add_cog(Notifications(client))

async def Notif(self, ctx, mention, type, channel_id, connection):
    verifier = False
    name = CheckChannel(ctx.channel.id, connection)
    sheet = connection.worksheet(str(name))
    clean_id = clean(mention)
    verify = CheckActiveUser(clean_id, sheet)
    if verify == True:
        user = self.client.get_user(int(clean_id))
        msg = await ctx.send("Are you sure you want to notify {0}?".format(user.display_name))
        await msg.add_reaction('❌')
        await msg.add_reaction('✅')
        re = await self.client.wait_for('reaction_add', check = lambda r, u: r.emoji in ['❌', '✅'] and r.message.id == msg.id and u == ctx.author)
        if str(re[0]) == str('✅'):
            await ctx.message.delete()
            await msg.delete()
            if type == 'p': pending = sheet.get("D2:E")
            elif type == 'i': pending = sheet.get("F2:G")
            elif type == 'a': pending = sheet.get("H2:I")
            elif type == 'r': pending = sheet.get("J2:K")
            pending = str(pending[0][0]).strip()
            pending = MessageTo(pending, user.display_name)
            embed = discord.Embed(
                description = pending,
                colour = discord.Colour.blue()
            )
            await user.send(embed=embed)
            if type == 'a' or type == 'r': await RemoveUser(clean(mention), sheet, self, channel_id)
        else:
            await ctx.message.delete()
            await msg.delete()
            await ctx.author.send("Notification has been cancelled")
    else:
        await ctx.author.send(verify)
        await ctx.message.delete()

async def RemoveUser(id, worksheet, self, cid):
    line = 0
    list = worksheet.get("L2:L")
    for i in range(len(list)):
        if str(id) == str(list[i][0]):
            line = str(i+2)
            break
    channel = self.client.get_channel(int(cid))
    msg = await channel.fetch_message(worksheet.acell("M{0}".format(line)).value)
    await msg.delete()
    worksheet.update("L{0}".format(line), "")
    worksheet.update("M{0}".format(line), "")

def listmaker(data):
    sentence = ""
    for i in range(len(data)):
        sentence += str(i+1) + ". " + str(data[i][0]) + "\n"
    return sentence

def CheckChannel(id, connection):
    ws = connection.worksheet("Data Puller")
    facs = ws.get("A1:A")
    for i in range(len(facs)):
        if str(id) == str(facs[i][0]):
            cell = "B{0}".format(str(i+1))
            name = ws.acell(cell).value
            return name
            break

def CheckActiveUser(id, worksheet):
    check = False
    try:
        list = worksheet.get("L2:L")
        for i in range(len(list)):
            if str(id) == str(list[i][0]):
                check = True
                break
            else: check = "This user did not apply for this position ¯\_(ツ)_/¯"
    except Exception:
        check = "This user did not apply for this position ¯\_(ツ)_/¯"
    return check

def clean(a):
    a = a.replace("<","")
    a = a.replace(">","")
    a = a.replace("@","")
    a = a.replace("!","")
    return a

def MessageTo(a, name):
    a = a.replace("<name>", name)
    return a

def connect():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("ImportentFiles/DriveAPIcreds.json", scope)

    gc = gspread.authorize(creds)

    sheet = gc.open_by_key('1p_v4ofnd5_oBbRIM6i47skC5rhPdWd_BsWrKUM7QHKM')
    return sheet

def CheckC(id, connection):
    check = False
    ws = connection.worksheet("Data Puller")
    line = ws.get("A1:A")
    for i in range(len(line)):
        if str(line[i][0]) == str(id):
            check = True
            break
    return check
