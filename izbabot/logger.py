import logging


def setup_command_logger():
    command_logger = logging.getLogger('command_logger')
    command_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s: %(msg)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    command_logger.addHandler(ch)

    return command_logger


def setup_app_logger():
    app_logger = logging.getLogger('app_logger')
    app_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)-8s]: %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    app_logger.addHandler(ch)

    return app_logger