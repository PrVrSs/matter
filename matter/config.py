LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'matter.logger.MatteFormatter',
            'fmt': '%(asctime)s %(levelname)s %(message)s',
            'datefmt': '%H:%M:%S',
            'use_colors': True,
        },
    },
    'handlers': {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        '': {'handlers': ['default'], 'level': 'ERROR'},
        'matte.error': {'level': 'INFO'},
    },
}


class Config:
    pass
