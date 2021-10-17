import functools

from discord.ext.commands import Context

from logger import setup_command_logger


command_logger = setup_command_logger()


def get_beer_word(amount):
    if amount == 1:
        return 'piwo'
    elif amount in [2, 3, 4]:
        return 'piwa'
    else:
        return 'piw'


def pair_params(func_args, command_params):
    params_it = iter(command_params)
    next(params_it)
    return ', '.join(f'{k}={v}' for k, v in zip(params_it, func_args))


def log_command(f):
    @functools.wraps(f)
    async def wrapper(ctx: Context, *args, **kwargs):
        sender = ctx.author
        command = ctx.command.name
        command_kwargs = pair_params(args, ctx.command.params)
        command_logger.debug(f'{sender} called {command}({command_kwargs})')

        return await f(ctx, *args, **kwargs)

    return wrapper