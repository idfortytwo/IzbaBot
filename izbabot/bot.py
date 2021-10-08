import discord

from discord.ext import commands
from discord.ext.commands.context import Context as Ctx

description = 'Bot dla Izby\nIn development'
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} logged in\n-----')


@bot.command()
async def t(ctx: Ctx):
    """Test command"""
    await ctx.send('test')
