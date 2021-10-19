import logging
import re
import discord

from discord.ext import commands
from discord.ext.commands.context import Context
from psycopg2 import DataError
from sqlalchemy.orm import aliased
from sqlalchemy.orm.session import Session

from db.connection import session_scope
from db.models import OwedBeer, Member
from utils import log_command
from utils import get_beer_word


description = 'Bot dla Izby\nIn development'
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

logger = logging.getLogger('app_logger')


def update_nicknames():
    guild: discord.guild.Guild = bot.guilds[0]
    with session_scope() as session:
        session: Session
        for m in guild.members:
            member = Member(m.id, m.display_name)
            session.merge(member)


@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} logged in', extra={'sender': 'root'})
    update_nicknames()


@bot.command(name='refresh')
async def refresh_nicknames(ctx: Context):
    """Odświeżyć niknejmy"""
    update_nicknames()
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

    beer_to_search = re.search(r'<@!(\d+)>', beer_to)
    if beer_to_search:
        beer_to_id = beer_to_search.group(1)
    else:
        await ctx.send('zły format')
        return

    with session_scope() as session:
        owed_beer: OwedBeer = session.query(OwedBeer) \
            .filter_by(beer_from_id=beer_from_id, beer_to_id=beer_to_id) \
            .first()
        if not owed_beer:
            owed_beer = OwedBeer(beer_from_id, beer_to_id, amount)
            session.add(owed_beer)
        else:
            try:
                owed_beer.count += amount
            except DataError:
                return await ctx.send(f'nie wypije tyle')
    await ctx.send(f'postawione {amount} {get_beer_word(amount)}')


@bot.command(name='wypite')
@log_command
async def drink_beer(ctx: Context, beer_from: str, amount: int = 1):
    """Odebrać postawione piwo"""
    beer_to_id = ctx.author.id

    beer_from_search = re.search(r'<@!(\d+)>', beer_from)
    if beer_from_search:
        beer_from_id = beer_from_search.group(1)
    else:
        await ctx.send('zły format')
        return

    with session_scope() as session:
        owed_beer: OwedBeer = session.query(OwedBeer) \
            .filter_by(beer_from_id=beer_from_id, beer_to_id=beer_to_id) \
            .first()

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
async def beers(ctx: Context):
    """Wyświetlić wszystkie postawione piwa"""
    with session_scope() as session:
        from_alias = aliased(Member)
        to_alias = aliased(Member)

        beers = session.query(from_alias.name, to_alias.name, OwedBeer.count).\
            join(from_alias, OwedBeer.beer_from_id == from_alias.member_id).\
            join(to_alias, OwedBeer.beer_to_id == to_alias.member_id).\
            all()

        if beers:
            await ctx.send('\n'.join(
                f'{name_from} wisi {name_to} {beer_count} {get_beer_word(beer_count)}'
                for name_from, name_to, beer_count
                in beers))
        else:
            await ctx.send('brak piw')