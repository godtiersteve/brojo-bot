from nextcord.ext import commands
import nextcord
import sqlite3
import bot_commands as bc

bot = commands.Bot(command_prefix='!')
token = 'OTgyMDAxOTUzMDMyNzY1NTMy.GtmXM2.Z2fUMYonRhPEe8-2psD8nxWFZkPlSnWg1dnkrA'

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

@bot.command()
async def fdfull(ctx, character, command):
    embed = bc.fetchFrameDataEmbed(character, command, cursor)
    if(embed is not None):
        await ctx.send(embed = embed)
    else:
        await ctx.send("Could not locate command " + command + " or character " + character)

@bot.command()
async def fdtext(ctx, character, command):       
    message = bc.fetchFrameDataText(character, command, cursor)
    if(message is not None):            
        await ctx.send(message)
    else:
        await ctx.send("Could not locate command " + command + " or character " + character)
       
bot.run(token)