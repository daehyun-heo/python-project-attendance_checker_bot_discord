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
 
@bot.event
async def on_ready():
    print('Done')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command()
async def hello(ctx:Context):
    await ctx.send('Hello, I\' m attendance checker bot!')

@bot.command()
async def about(ctx:Context):
    await ctx.send('attendance_checker_bot made by daehyun-heo(hyeon365@gmail.com)')

@bot.command()
async def check_in(ctx:Context):
    db.check_in(ctx.author.name)
    await ctx.send(f"{ctx.author.name} checked-in.")

@bot.command()
async def check_out(ctx:Context):
    db.check_out(ctx.author.name)
    await ctx.send(f"{ctx.author.name} checked-out.")

@bot.command()
async def status(ctx:Context, member: discord.Member = None):
    member = member or ctx.author  # 인자 없으면 자기 자신
    res = db.get_status(member.name)
    await ctx.send(f"{member.name} is {res}.")

@bot.command()
async def who_online(ctx:Context):
    res = db.get_online_users() # res 가 리스트인걸 생각
    innerTxt = " , ".join(res)
    await ctx.send(f"{innerTxt}")


bot.run(os.getenv("DISCORD_TOKEN"))