import discord
from discord.ext import commands
from RCON import python_rcon_client
import subprocess

#initialize bot+
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "!", intents = intents)

server_ip = "localhost"
server_RCON_port = "25575"
server_RCON_passsword = "12345678"

@bot.event
async def on_ready():
    print(bot.user)

@bot.command()
async def Hello(ctx, *, message: str):
    print(message)
    await ctx.send("Hello, world!")

@bot.command()
async def command(ctx, *, message: str):
    with python_rcon_client.RCONClient('192.168.1.248', 25575, '12345678') as rcon_client:
        rcon_client.command(message)

@bot.command()
async def start(ctx):
    subprocess.run([r"D:\Minecraft_server\minecraft server 1.19.2\start.bat"])

bot.run("MTI0NDkxMjk1ODYwMjIxNTQ2NA.GgqN5x.hLvnrJF-VMrqBJZHHkqMNv-Oc4dpleZk0xdsvA")