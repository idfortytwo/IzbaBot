import discord

from discord.ext import commands
from discord.ext.commands.context import Context

from db.connection import session_scope
from db.models import OwnedBeer

description = 'Bot dla Izby\nIn development'
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} logged in\n-----')


@bot.command()
async def t(ctx: Context):
    """Test command"""
    await ctx.send('test')


@bot.command(name='stawiam')
async def owe_beer(ctx: Context, beer_to: str):
    beer_from_id = ctx.author.id
    beer_to_id = beer_to[3:-1]

    with session_scope() as session:
        owned_beer: OwnedBeer = session.query(OwnedBeer) \
            .filter_by(beer_from_id=beer_from_id, beer_to_id=beer_to_id) \
            .first()
        if not owned_beer:
            owned_beer = OwnedBeer(beer_from_id, beer_to_id, 1)
            session.add(owned_beer)
        else:
            owned_beer.count += 1
    await ctx.send(f'postawione')


@bot.command(name='wypite')
async def drink_beer(ctx: Context, beer_from: str):
    beer_to_id = ctx.author.id
    beer_from_id = beer_from[3:-1]

    with session_scope() as session:
        owned_beer: OwnedBeer = session.query(OwnedBeer) \
            .filter_by(beer_from_id=beer_from_id, beer_to_id=beer_to_id) \
            .first()

        if owned_beer:
            if owned_beer.count > 1:
                owned_beer.count -= 1
                session.add(owned_beer)
                await ctx.send(f'wypite, wisi ci jeszcze {owned_beer.count}')
            else:
                session.delete(owned_beer)
                await ctx.send('wypite, już ci nic nie wisi')
        else:
            await ctx.send('i tak ci nie wisi')


@bot.command(name='piwa')
async def beers(ctx: Context):
    with session_scope() as session:
        beers: [OwnedBeer] = session.query(OwnedBeer).all()
        if beers:
            await ctx.send('\n'.join(str(beer) for beer in beers))
        else:
            await ctx.send('brak piw')