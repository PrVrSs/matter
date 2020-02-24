import click

from .application import Application
from .extensions import ExtensionLoader
from .logger import logging_lvl
from .utils import async_click


class Fuzzer:
    def __init__(self, app, config=None):
        self._app = app
        self._extension = ExtensionLoader(config)

    def run(self):
        self._extension.run()


@click.command()
@click.option('--level', '-l',
              default='INFO',
              type=click.Choice(logging_lvl))
@async_click
async def main(level):
    app = Application()
    await app.startup()
    fuzzer = Fuzzer(app)
    await fuzzer._extension.create_builder()
    fuzzer.run()


if __name__ == '__main__':
    main()
