import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections.abc import Sequence

class Apps(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def apply(self, ctx):
        with open('ImportentFiles/GeneralFile.txt', 'r') as f:
            id = f.readlines()
        if str(id[0]).strip() == str(ctx.channel.id).strip():
            connection = connect()
            check = False
            ss = ""
            emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            fsheet = connection.worksheet("Factions")
            try:
                list = fsheet.get("A4:A")
            except Exception:
                await ctx.message.delete()
                await ctx.author.send("No faction has been set at the moment, please contact Jordan Dep for further assistance")
            embed = discord.Embed(
                title='Faction Selection (sent by {0})'.format(ctx.author.display_name),
                colour = discord.Colour.blue()
            )
            datalist = listmaker(list)
            embed.add_field(name = ' ‏‏‎ ', value=datalist)
            msg = await ctx.send(embed=embed)
            for i in range(len(list)):
                await msg.add_reaction(emojis[i])
            re = await self.client.wait_for('reaction_add', check = lambda r, u: r.emoji in emojis and r.message.id == msg.id and u == ctx.author)
            await ctx.message.delete()
            await msg.delete()
            ids = []
            for i in range(0, len(list)):
                if str(emojis[i]) == str(re[0]):
                    ss = connection.worksheet(list[i][0])
                    try:
                        ids = ss.get("L2:L")
                        for g in ids:
                            if str(g[0]) == str(ctx.author.id):
                                check = True
                                await ctx.author.send("You have already applied for this position, wait!")
                                break
                            else: check = False
                        if check == False:
                            await LaunchApp(self, ctx, ss, list[i][0])
                    except Exception:
                        await LaunchApp(self, ctx, ss, list[i][0])
                        break
        else: await ctx.message.delete()

    @commands.command()
    async def cancel(self, ctx):
        await ctx.author.send("Application process has been cancelled")




def setup(client):
    client.add_cog(Apps(client))


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

async def LaunchApp(self, ctx, worksheet, name):
    ids = []
    answers = []
    question = []
    author = ctx.author
    embed = discord.Embed(
        description = 'Application process for {0} has started. Type %cancel to cancel the process'.format(name),
        colour = discord.Colour.blue()
    )
    await author.send(embed=embed)
    questions = worksheet.get("A2:A")
    for q in questions:
        embed = discord.Embed(
            description = q[0],
            colour = discord.Colour.blue()
        )
        msg = await author.send(embed=embed)
        r = await self.client.wait_for('message', check=message_check(channel=ctx.author.dm_channel))
        if str(r.content) == '%cancel': break
        else:
            answers.append(str(r.content))
            question.append(str(q[0]))
    embed = discord.Embed(
        description = 'Are you sure you wish to apply?, check your answers before-hand',
        colour = discord.Colour.red()
    )
    if str(r.content) != "%cancel":
        msg = await ctx.author.send(embed=embed)
        await msg.add_reaction('❌')
        await msg.add_reaction('✅')
        re = await self.client.wait_for('reaction_add', check = lambda r, u: r.emoji in ['❌', '✅'] and r.message.id == msg.id and u == ctx.author)
        if str(re[0]) == str('✅'):
            embed = discord.Embed(description='Application has been sent, Good Luck!', colour = discord.Colour.blue())
            await ctx.author.send(embed=embed)
            getid = await MakeApp(self, ctx, question, answers, worksheet)
            DataPusher(ctx, ctx.author.id, worksheet, getid)
        else: await ctx.author.send("App has been cancelled")

async def MakeApp(self, ctx, questions, answers, worksheet):
    sentence = ""
    for i in range(len(answers)):
        sentence += str(questions[i]) + "\n\nAnswer: " + answers[i] + "\n\n"
    embed = discord.Embed(
        title = 'Application of {0}'.format(ctx.author.display_name),
        colour = discord.Colour.blue()
    )
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name=' ‏‏‎ ', value=sentence)
    embed.set_footer(text='Created at: {0}'.format(ctx.message.created_at))
    cid = int(worksheet.acell("N2").value)
    channel = self.client.get_channel(cid)
    msg = await channel.send(embed=embed)
    return msg.id

def DataPusher(ctx, id, worksheet, msgid):
    ids = []
    counter = 2
    try:
        ids = worksheet.get("L2:L")
    except Exception:
        worksheet.update("L2", str(id))
        worksheet.update("M2", str(msgid))
    worksheet.update("L{0}".format(len(ids)+2), str(id))
    worksheet.update("M{0}".format(len(ids)+2), str(msgid))



def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)
    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check
