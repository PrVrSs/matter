import click

from .application import Application
from .errors import ERROR_LIST
from .extensions import ExtensionLoader
from .logger import logging_lvl
from .utils import async_click


class Fuzzer:
    def __init__(self, app, config=None):
        self._app = app
        self.extension = ExtensionLoader(config)

    def run(self):
        self.extension.run()


@click.command()
@click.option('--level', '-l',
              default='INFO',
              type=click.Choice(logging_lvl))
@async_click
async def main(level):
    print(level)
    try:
        app = Application()
        await app.startup()
        fuzzer = Fuzzer(app)
        await fuzzer.extension.create_builder()
        fuzzer.run()
    except ERROR_LIST as error:
        print(error)


if __name__ == '__main__':
    main()
