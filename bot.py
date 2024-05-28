#copy from internet
import discord
from discord.ext import commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "%", intents = intents)

@bot.event
async def on_ready():
    print(bot.user)

@bot.command()
async def Hello(ctx):
    await ctx.send("Hello, world!")

bot.run("機器人的TOKEN")