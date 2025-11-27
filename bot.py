import discord
import os
from discord.ext import commands
from discord.ext.commands.context import Context
from dotenv import load_dotenv
import db as db 

# Setting

load_dotenv() 
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

if not os.path.exists("attendance.db"):
    db.init_db()

# Function

bot.remove_command("help")
 
@bot.event
async def on_ready():
    print('Done')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command()
async def hello(ctx:Context):
    await ctx.send("Hello, I'm attendance checker bot!", silent=True)

@bot.command()
async def about(ctx:Context):
    await ctx.send(
        'attendance_checker_bot made by daehyun-heo (hyeon365@gmail.com)',
        silent=True
    )

@bot.command()
async def help(ctx:Context):
    innerTxt = (
        "모든 명령어는 !(명령어) 형식으로 입력해주세요.\n"
        "hello : 인삿말 출력\n"
        "about : bot 정보 출력\n"
        "help : 도움말 출력\n"
        "check_in : 출근 기록\n"
        "check_out : 퇴근 기록\n"
        "status @사용자명 : 특정 사용자 출근/퇴근 상태 출력\n"
        "status : 자기 자신의 출근/퇴근 상태 출력\n"
        "who_online : 현재 출근 중인 사용자 목록 출력"
    )
    await ctx.send(innerTxt, silent=True)

@bot.command()
async def check_in(ctx:Context):
    db.check_in(ctx.author.name)
    await ctx.send(f"{ctx.author.name} checked-in.", silent=True)

@bot.command()
async def check_out(ctx:Context):
    db.check_out(ctx.author.name)
    await ctx.send(f"{ctx.author.name} checked-out.", silent=True)

@bot.command()
async def status(ctx:Context, member: discord.Member = None):
    member = member or ctx.author
    res = db.get_status(member.name)
    await ctx.send(f"{member.name} is {res}.", silent=True)

@bot.command()
async def who_online(ctx:Context):
    res = db.get_online_users() 

    if not res:
        await ctx.send("출근 중인 사용자가 없습니다.", silent=True)
        return

    innerTxt = ", ".join([f"{name}({time})" for name, time in res])
    await ctx.send(innerTxt, silent=True)

bot.run(os.getenv("DISCORD_TOKEN"))
