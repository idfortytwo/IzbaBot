import logging
import re
import discord

from discord.ext import commands
from discord.ext.commands.context import Context
from sqlalchemy.orm import aliased
from sqlalchemy.orm.session import Session

from db.connection import session_scope
from db.models import OwnedBeer, Member
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
        owned_beer: OwnedBeer = session.query(OwnedBeer) \
            .filter_by(beer_from_id=beer_from_id, beer_to_id=beer_to_id) \
            .first()
        if not owned_beer:
            owned_beer = OwnedBeer(beer_from_id, beer_to_id, amount)
            session.add(owned_beer)
        else:
            owned_beer.count += amount
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
        owned_beer: OwnedBeer = session.query(OwnedBeer) \
            .filter_by(beer_from_id=beer_from_id, beer_to_id=beer_to_id) \
            .first()

        if owned_beer:
            if owned_beer.count > amount:
                owned_beer.count -= amount
                session.add(owned_beer)
                await ctx.send(f'wypite, wisi ci jeszcze {owned_beer.count}')
            else:
                session.delete(owned_beer)
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

        beers = session.query(from_alias.name, to_alias.name, OwnedBeer.count).\
            join(from_alias, OwnedBeer.beer_from_id == from_alias.member_id).\
            join(to_alias, OwnedBeer.beer_to_id == to_alias.member_id).\
            all()

        if beers:
            await ctx.send('\n'.join(
                f'{name_from} wisi {name_to} {beer_count} {get_beer_word(beer_count)}'
                for name_from, name_to, beer_count
                in beers))
        else:
            await ctx.send('brak piw')