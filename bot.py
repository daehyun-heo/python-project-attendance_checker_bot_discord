import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import db

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

if not os.path.exists("attendance.db"):
    db.init_db()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    await tree.sync()


@tree.command(name="about", description="봇 정보 표시")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(
        "attendance_checker_bot made by daehyun-heo (hyeon365@gmail.com)",
        ephemeral=True
    )


@tree.command(name="help", description="명령어 목록")
async def help_cmd(interaction: discord.Interaction):
    txt = (
        "/about : 봇 정보\n"
        "/help : 명령어 도움말\n"
        "/check_in : 출근\n"
        "/check_out : 퇴근\n"
        "/log : 특정 사용자 또는 나의 출퇴근 기록\n"
        "/log_all : 전체 출퇴근 기록"
    )
    await interaction.response.send_message(txt, ephemeral=True)


@tree.command(name="check_in", description="출근 기록")
async def check_in(interaction: discord.Interaction):
    now = db.check_in(interaction.user.name)
    await interaction.response.send_message(
        f"{interaction.user.name} checked-in. {now}",
        ephemeral=True
    )


@tree.command(name="check_out", description="퇴근 기록")
async def check_out(interaction: discord.Interaction):
    out, duration = db.check_out(interaction.user.name)
    if duration is None:
        await interaction.response.send_message("출근 기록 없음.", ephemeral=True)
        return
    await interaction.response.send_message(
        f"{interaction.user.name} checked-out. {out}\n근무시간: {duration}",
        ephemeral=True
    )



@tree.command(name="log", description="사용자 출퇴근 로그 조회")
@app_commands.describe(member="조회할 사용자 (미입력 시 본인)")
async def log_cmd(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    logs = db.get_log(target.name)

    if not logs:
        await interaction.response.send_message(
            f"{target.name} : 기록 없음",
            ephemeral=True
        )
        return

    lines = [f"{i+1}. {c[0]} → {c[1]}" for i, c in enumerate(logs)]

    await interaction.response.send_message(
        f"{target.name} 기록:\n" + "\n".join(lines),
        ephemeral=True
    )



@tree.command(name="log_all", description="모든 사용자 출퇴근 로그")
async def log_all(interaction: discord.Interaction):
    logs = db.get_logs()
    if not logs:
        await interaction.response.send_message("기록 없음.", ephemeral=True)
        return

    msg = ""
    for user, pairs in logs.items():
        msg += f"{user}:\n"
        for c in pairs:
            msg += f" - {c[0]} → {c[1]}\n"
        msg += "\n"

    await interaction.response.send_message(msg, ephemeral=True)


bot.run(os.getenv("DISCORD_TOKEN"))
