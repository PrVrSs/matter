from typing import List, Tuple, ClassVar


class BaseMatterError(Exception):
    """Base project exception. """
    project_exceptions: ClassVar[List['BaseMatterError']] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.project_exceptions.append(cls)


class ExtensionError(BaseMatterError):
    pass


ERROR_LIST: Tuple[BaseMatterError, ...] = tuple(
    BaseMatterError.project_exceptions)
