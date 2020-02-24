import importlib
import importlib.util
import pathlib
from contextlib import suppress
from operator import methodcaller

from ..errors import ExtensionError


EXTENSION_NAME = 'matte_extension'


def get_extensions(directory: str = '', *, recursive: bool = False):
    path_to_extensions = pathlib.Path(directory)

    if not path_to_extensions.is_dir():
        return

    files = methodcaller('rglob' if recursive else 'glob', '*.py')

    for file in files(path_to_extensions):
        spec = importlib.util.spec_from_file_location(
            file.stem, str(file.resolve()))

        module_from_spec = importlib.util.module_from_spec(spec)

        with suppress(Exception):
            spec.loader.exec_module(module_from_spec)

        if extension := getattr(module_from_spec, EXTENSION_NAME, None):
            yield extension()


class ExtensionLoader:
    def __new__(cls, config, target='http'):
        self = super().__new__(cls)

        extension = {
            **self._base_extension,
            **self._additional_extension,
        }.get(target)

        if extension is None:
            raise ExtensionError(f'Not found {target}')

        return extension(config)

    @property
    def _additional_extension(self):
        return {}

    @property
    def _base_extension(self):
        return {
            extension.__name__: extension
            for extension in get_extensions(
                directory='extensions',
                recursive=True,
            )
        }
