from ..base_builder import create_builder


class MetaExtension(type):
    def __new__(mcs, name, bases, dct):
        if not bases:
            return super().__new__(mcs, name, bases, dct)

        if implement := dct.get('__implements__', None):
            dct['__implements__'] = mcs.prepare_implements(implement)

        if algorithm := dct.get('__mutations_alg__', None):
            dct['__mutations_alg__'] = mcs.prepare_algorithm(algorithm)

        if scheme := dct.get('__mutations_scheme__', None):
            dct['__mutations_scheme__'] = mcs.prepare_scheme(scheme)

        if __init__ := dct.get('__init__', None):
            dct['__init__'] = mcs.decorating_function(__init__)

        cls = super().__new__(mcs, name, bases, dct)
        cls.__name__ = cls.__name__.lower()

        return cls

    @staticmethod
    def decorating_function(user_function):
        def wrapper(__obj__, *args, **kwargs):
            return user_function(__obj__, *args, **kwargs)

        return wrapper

    @staticmethod
    def prepare_scheme(target):
        return target()

    @staticmethod
    def prepare_algorithm(target):
        return target()

    @staticmethod
    def prepare_implements(target):
        return target()


class BaseExtension(metaclass=MetaExtension):
    __implements__ = None
    __mutations_alg__ = None
    __mutations_scheme__ = None
    __files__ = ()

    def __init__(self):
        self.builder = None

    async def create_builder(self):
        self.builder = await create_builder(self.__files__)

    def run(self):
        while True:
            print(' '.join(self.builder.build_sentence(start_rule='http_message')))
