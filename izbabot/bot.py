import logging
import re
import discord
import sqlalchemy

from discord.ext import commands
from discord.ext.commands.context import Context
from sqlalchemy import select
from sqlalchemy.orm import aliased

from db.connection import session_scope
from db.models import OwedBeer, Member
from utils import log_command
from utils import get_beer_word

description = 'Bot dla Izby\nIn development'
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

logger = logging.getLogger('app_logger')


async def update_nicknames():
    guild: discord.guild.Guild = bot.guilds[0]
    async with session_scope() as session:
        for m in guild.members:
            member = Member(m.id, m.display_name)
            await session.merge(member)


@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} logged in', extra={'sender': 'root'})
    await update_nicknames()


@bot.command(name='refresh')
async def refresh_nicknames(ctx: Context):
    """Odświeżyć niknejmy"""
    await update_nicknames()
    await ctx.send('odświeżone')


@bot.command()
@log_command
async def t(ctx: Context):
    """Test command"""
    await ctx.send('test')


@bot.command(name='stawiam')
@log_command
async def owe_beer(ctx: Context, beer_to: str, amount: int = 1):
    """Postawić komuś piwo"""
    beer_from_id = ctx.author.id

    if (beer_to_search := re.search(r'<@!(\d+)>', beer_to)) or (beer_to_search := re.search(r'<@(\d+)>', beer_to)):
        beer_to_id = int(beer_to_search.group(1))
    else:
        await ctx.send('zły format')
        return

    try:
        async with session_scope() as session:
            owed_beer: OwedBeer = (await session.execute(
                select(OwedBeer).
                filter_by(beer_from_id=beer_from_id, beer_to_id=beer_to_id)
            )).first()[0]

            print(owed_beer)

            if not owed_beer:
                owed_beer = OwedBeer(beer_from_id, beer_to_id, amount)
                session.add(owed_beer)
            else:
                owed_beer.count += amount
    except sqlalchemy.exc.DataError as e:  # noqa
        return await ctx.send(f'nie wypije tyle')

    await ctx.send(f'postawione {amount} {get_beer_word(amount)}')


@bot.command(name='wypite')
@log_command
async def drink_beer(ctx: Context, beer_from: str, amount: int = 1):
    """Odebrać postawione piwo"""
    beer_to_id = ctx.author.id

    if (beer_from_search := re.search(r'<@!(\d+)>', beer_from)) or \
       (beer_from_search := re.search(r'<@(\d+)>', beer_from)):
        beer_from_id = int(beer_from_search.group(1))
    else:
        await ctx.send('zły format')
        return

    async with session_scope() as session:
        owed_beer: OwedBeer = (await session.execute(
            select(OwedBeer).
            filter_by(beer_from_id=beer_from_id, beer_to_id=beer_to_id)
        )).first()[0]

        if owed_beer:
            if owed_beer.count > amount:
                owed_beer.count -= amount
                session.add(owed_beer)
                await ctx.send(f'wypite, wisi ci jeszcze {owed_beer.count}')
            else:
                session.delete(owed_beer)
                await ctx.send('wypite, już ci nic nie wisi')
        else:
            await ctx.send('i tak ci nie wisi')


@bot.command(name='piwa')
@log_command
async def list_beers(ctx: Context):
    """Wyświetlić wszystkie postawione piwa"""
    async with session_scope() as session:
        print(session)
        from_alias = aliased(Member)
        to_alias = aliased(Member)

        beers = (await session.execute(
            select(from_alias.name, to_alias.name, OwedBeer.count).
            join(from_alias, OwedBeer.beer_from_id == from_alias.member_id).
            join(to_alias, OwedBeer.beer_to_id == to_alias.member_id)
        )).all()

        if beers:
            await ctx.send('\n'.join(
                f'{name_from} wisi {name_to} {beer_count} {get_beer_word(beer_count)}'
                for name_from, name_to, beer_count
                in beers))
        else:
            await ctx.send('brak piw')
