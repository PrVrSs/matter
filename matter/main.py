import logging

import click

from .application import Application
from .errors import ERROR_LIST
from .extensions import ExtensionLoader
from .logger import LOG_LEVELS, configure_logging
from .utils import async_click
from .config import GREETING


class Fuzzer:
    def __init__(self, app, config=None):
        self._app = app
        self.extension = ExtensionLoader(config)

    def run(self):
        self.extension.run()


@click.command()
@click.option('--level', '-l',
              default='debug',
              type=click.Choice(LOG_LEVELS.keys()))
@async_click
async def main(level):
    print(click.style(GREETING, fg='blue', bold=True))
    configure_logging(level)

    try:
        app = Application()
        await app.startup()
        fuzzer = Fuzzer(app)
        await fuzzer.extension.create_builder()
        fuzzer.run()
    except ERROR_LIST as error:
        logging.exception(error)
        raise click.Abort
