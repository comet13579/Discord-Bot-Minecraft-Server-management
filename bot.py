import discord
from discord.ext import commands
from RCON import python_rcon_client
import subprocess
import sys

#load properties
with open("bot.properties") as properties:
    lines = properties.readlines()
    bot_token = lines[0].split("=")[1].strip()
    bot_prefix = lines[1].split("=")[1].strip()
    localhost_ip = lines[2].split("=")[1].strip()
    server_RCON_port = int(lines[3].split("=")[1].strip())
    server_RCON_passsword = lines[4].split("=")[1].strip()
    launch_path = lines[5].split("=")[1].strip()
    server_ip = lines[6].split("=")[1].strip()

#initialize bot+
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = bot_prefix, intents = intents)

@bot.event
async def on_ready():
    print(bot.user)

#@bot.command()
#async def Hello(ctx):
#    await ctx.send("Hello, world!")

#@bot.command()
#async def command(ctx, *, message: str):
#    with python_rcon_client.RCONClient(server_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
#        rcon_client.command(message)
#        for output in rcon_client.outputs:
#            await ctx.send(output)

@bot.command()
async def stop(ctx):
    with python_rcon_client.RCONClient(localhost_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
        rcon_client.command("stop")
    await ctx.send("Server stopping...")

@bot.command()
async def hello(ctx):
    with python_rcon_client.RCONClient(localhost_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
        rcon_client.command("say hello")

@bot.command()
async def serverexist(ctx):
    await ctx.send("Check the server through \n https://mcstatus.io/status/java/" + server_ip)

@bot.command()
async def ip(ctx):
    await ctx.send(server_ip)

@bot.command()
async def start(ctx):
    if sys.platform == "win32":
        args = ["cmd.exe","/c ",launch_path]
    else:
        args = ["./",launch_path]
    print(args)
    print(launch_path)
    subprocess.Popen(args)
    await ctx.send("Server starting...")

bot.run(bot_token)