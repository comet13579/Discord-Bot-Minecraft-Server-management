import discord
from discord.ext import commands
from discord.ui import Button, View
from RCON import python_rcon_client
import subprocess
import sys
import time
import ctypes

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

def force_quit_process(pid):
    PROCESS_TERMINATE = 1
    process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
    
    if not process_handle:
        print(f"Failed to open process with PID {pid}.")
        return
    
    result = ctypes.windll.kernel32.TerminateProcess(process_handle, -1)
    
    if not result:
        print(f"Failed to terminate process with PID {pid}.")
    else:
        print(f"Process {pid} has been forcefully terminated.")
    
    ctypes.windll.kernel32.CloseHandle(process_handle)
    ##function from gpt

@bot.event
async def on_ready():
    print(bot.user)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def stop(ctx):
    """停止伺服器 每60秒只能使用一次"""
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
@commands.cooldown(1, 60, commands.BucketType.user)
async def forcequit(ctx):
    """強制關閉伺服器 每60秒只能使用一次"""
    class myView(View):
        def __init__(self,ctx):
            super().__init__(timeout=10)
            self.ctx = ctx
        async def on_timeout(self) -> None:
            await self.ctx.send("Time out " + "操作逾時" * enable_Chinese, view=None)

    yesbutton = Button(label="KILL" + "強制關閉" * enable_Chinese, style=discord.ButtonStyle.danger)
    nobutton = Button(label="NO" + "不要關閉" * enable_Chinese, style=discord.ButtonStyle.blurple)
    view = myView(ctx)
    view.add_item(yesbutton)
    view.add_item(nobutton)
    await ctx.send("Are you sure to force quit the server?" + "\n你要強制關閉伺服器嗎?" * enable_Chinese, view=view)

    async def kill_itself(interaction):
        
        if sys.platform == "win32":
            force_quit_process(jar_itself.pid)
        else:
            jar_itself.kill()
        ##kill the server
        message = "Server is forced to stop"  + "\n伺服器已被強制關閉" * enable_Chinese
        await interaction.response.edit_message(content = message, view=None)
    async def no_kill(interaction):
        message = "Force Shut is rejected" + "\n伺服器並未強制關閉" * enable_Chinese
        await interaction.response.edit_message(content = message, view=None)


    yesbutton.callback = kill_itself
    nobutton.callback = no_kill
    ##i just copy these button interactions from youtube


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def start(ctx):
    """啟動伺服器 每60秒只能使用一次"""

    await ctx.send("Trying to start the server")
    if enable_Chinese:
        await ctx.send("正在嘗試啟動伺服器")
    with python_rcon_client.RCONClient(localhost_ip, server_RCON_port, server_RCON_passsword) as rcon_client:
        rcon_client.command("say some stupid guys are trying to start the server")
        if enable_Chinese:
            rcon_client.command("say 有個傻瓜正在嘗試啟動伺服器")
        time.sleep(1)
        serveroff = rcon_client.outputs[0] ##take RCON status
    
    if serveroff != "0": ##indicate RCON is not off, server is on
        await ctx.send("Server is already running")
        await ctx.send(f"{ctx.author.mention} is a stupid guy")
        if enable_Chinese:
            await ctx.send("伺服器已經在運行中")
            await ctx.send(f"{ctx.author.mention} 是個傻瓜")    
        return
    global jar_itself
    if sys.platform == "win32":
        args = ["cmd.exe","/c ",launch_path]
    else:
        args = ["./",launch_path]
    jar_itself = subprocess.Popen(args)
    await ctx.send("Server starting...")
    if enable_Chinese:
        await ctx.send("伺服器啟動中...")

bot.run(bot_token)