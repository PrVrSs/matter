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

GREETING = r'''
 __    __     ______     ______   ______   ______     ______    
/\ "-./  \   /\  __ \   /\__  _\ /\__  _\ /\  ___\   /\  == \   
\ \ \-./\ \  \ \  __ \  \/_/\ \/ \/_/\ \/ \ \  __\   \ \  __<   
 \ \_\ \ \_\  \ \_\ \_\    \ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
  \/_/  \/_/   \/_/\/_/     \/_/     \/_/   \/_____/   \/_/ /_/ 
'''.lstrip()


class Config:
    pass
