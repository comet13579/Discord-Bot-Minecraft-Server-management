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
    enable_Chinese = int(lines[7].split("=")[1].strip())

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
    f"""{"Stop the server " + "關閉伺服器" * enable_Chinese}"""
    with python_rcon_client.RCONClient(localhost_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
        rcon_client.command("stop")
    await ctx.send("Server stopping...")
    if enable_Chinese:
        await ctx.send("伺服器關閉中...")

@bot.command()
async def hello(ctx):
    f"""{"Says hello (might solve time out issue) " + "在Minecraft服务器中说hello (能夠有機會解決time out問題)" * enable_Chinese}"""
    with python_rcon_client.RCONClient(localhost_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
        rcon_client.command("say hello")
        print(rcon_client.outputs)

@bot.command()
async def serverexist(ctx):
    f"""{"Check if the server is online " + "檢查伺服器是否在線上" * enable_Chinese}"""
    await ctx.send("Check the server through the following link")
    if enable_Chinese:
        await ctx.send("使用以下連結檢查伺服器是否開啟")
    await ctx.send("https://mcstatus.io/status/java/" + server_ip)

@bot.command()
async def ip(ctx):
    f"""{"Get the server ip address " + "獲取伺服器IP地址" * enable_Chinese}"""
    await ctx.send(server_ip)

@bot.command()
async def start(ctx):
    f"""{"Start the server " + "啟動伺服器" * enable_Chinese}"""
    if sys.platform == "win32":
        args = ["cmd.exe","/c ",launch_path]
    else:
        args = ["./",launch_path]
    print(args)
    print(launch_path)
    subprocess.Popen(args)
    await ctx.send("Server starting...")
    if enable_Chinese:
        await ctx.send("伺服器啟動中...")

bot.run(bot_token)