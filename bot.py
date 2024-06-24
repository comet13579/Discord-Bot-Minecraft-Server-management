import discord
from discord.ext import commands
from RCON import python_rcon_client
import subprocess
import sys
import time

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

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def stop(ctx):
    """停止伺服器 每30秒只能使用一次"""
    await ctx.send("Trying to stop the server")
    if enable_Chinese:
        await ctx.send("正在嘗試關閉伺服器")
    with python_rcon_client.RCONClient(localhost_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
        rcon_client.command("stop")
        serveroff = rcon_client.outputs[0]
    if serveroff != "0":
        await ctx.send("Server stopping...")
        if enable_Chinese:
            await ctx.send("伺服器關閉中...")
    else:
        await ctx.send("Server is already off")
        await ctx.send(f"{ctx.author.mention} is a stupid guy")
        if enable_Chinese:
            await ctx.send("伺服器已經關閉")
            await ctx.send(f"{ctx.author.mention} 是個傻瓜")

@bot.command()
async def hello(ctx):
    """在Minecraft服务器中说hello (能夠有機會解決time out問題)"""

    with python_rcon_client.RCONClient(localhost_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
        rcon_client.command("say hello")
        print(rcon_client.outputs)

@bot.command()
async def serverexist(ctx):
    """檢查伺服器是否在線上"""

    await ctx.send("Check the server through the following link")
    if enable_Chinese:
        await ctx.send("使用以下連結檢查伺服器是否開啟")
    await ctx.send("https://mcstatus.io/status/java/" + server_ip)

@bot.command()
async def ip(ctx):
    """獲取伺服器IP地址"""

    await ctx.send(server_ip)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def start(ctx):
    """啟動伺服器 每30秒只能使用一次"""

    await ctx.send("Trying to start the server")
    if enable_Chinese:
        await ctx.send("正在嘗試啟動伺服器")
    with python_rcon_client.RCONClient(localhost_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
        rcon_client.command("say some stupid guys are trying to start the server")
        if enable_Chinese:
            rcon_client.command("say 有個傻瓜正在嘗試啟動伺服器")
        time.sleep(1)
        print(rcon_client.outputs)
        serveroff = rcon_client.outputs[0] ##take RCON status
    
    if serveroff != "0": ##indicate RCON is not off, server is on
        await ctx.send("Server is already running")
        await ctx.send(f"{ctx.author.mention} is a stupid guy")
        if enable_Chinese:
            await ctx.send("伺服器已經在運行中")
            await ctx.send(f"{ctx.author.mention} 是個傻瓜")    
        return
    

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