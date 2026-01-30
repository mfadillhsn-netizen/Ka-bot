import discord
from discord.ext import commands
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

VERIFY_MESSAGE_ID = 1465292240044691522
MEMBER_ROLE_ID = 1465226826753245438
WELCOME_CHANNEL_ID = 1465293157834035233

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    if payload.message_id != VERIFY_MESSAGE_ID:
        return

    if str(payload.emoji) != "✅":
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        return

    role = guild.get_role(MEMBER_ROLE_ID)
    if role is None:
        return

    if role in member.roles:
        return

    try:
        await member.add_roles(role)
    except:
        pass

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        return

    await channel.send(f"Selamat datang {member.mention} di kachatalk")

if BOT_TOKEN is None:
    raise RuntimeError("BOT_TOKEN is not set")

bot.run(BOT_TOKEN)




