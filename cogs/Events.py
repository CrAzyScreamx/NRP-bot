import discord
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
from collections.abc import Sequence
import gspread
from discord.utils import get


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
            await ctx.author.send("You are not permitted to do this action!")
            await ctx.message.delete()

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        connection = connect()
        ws = connection.worksheet("Role List")
        next_row = next_available_row(ws)
        ws.update(f"A{next_row}", role.name)
        ws.update(f"B{next_row}", str(role.id))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        connection = connect()
        ws = connection.worksheet("Role List")
        id = str(role.id)
        ids = ws.get("B1:B")
        for i in range(0, len(ids)):
            if id == ids[i][0]:
                ws.delete_row(i+1)
                break

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        connection = connect()
        ws = connection.worksheet("Role List")
        channel = self.client.get_channel(716659354383679530)
        ids = ws.get("B1:B")
        id = str(before.id)
        for i in range(0, len(ids)):
            if id == ids[i][0]:
                ws.update(f"A{i+1}", after.name)
                break

def setup(client):
    client.add_cog(Events(client))

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def connect():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("ImportentFiles/DriveAPIcreds.json", scope)

    gc = gspread.authorize(creds)
    with open('ImportentFiles/SheetID.txt', 'r') as f:
        ids = f.readlines()
        id = ids[0].strip()
    sheet = gc.open_by_key(id)
    return sheet
