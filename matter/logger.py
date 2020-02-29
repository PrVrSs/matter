import logging

import click


TRACE_LOG_LEVEL = 4


class matte_logger:  # pylint: disable=invalid-name
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


logging_lvl = frozenset((  # pylint: disable=invalid-name
    'INFO',
    'ERROR',
    'CRITICAL',
    'DEBUG',
    'WARNING',
))


class MatteFormatter(logging.Formatter):
    level_name_colors = {
        TRACE_LOG_LEVEL: lambda level_name: click.style(
            str(level_name), fg='blue'),
        logging.DEBUG: lambda level_name: click.style(
            str(level_name), fg='cyan'),
        logging.INFO: lambda level_name: click.style(
            str(level_name), fg='green'),
        logging.WARNING: lambda level_name: click.style(
            str(level_name), fg='yellow'),
        logging.ERROR: lambda level_name: click.style(
            str(level_name), fg='red'),
        logging.CRITICAL: lambda level_name: click.style(
            str(level_name), fg='bright_red'),
    }

    def __init__(self, fmt=None, datefmt=None, style='%', use_colors=True):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.use_colors = use_colors

    def formatMessage(self, record):
        if not self.use_colors:
            return super().formatMessage(record)

        record.__dict__['message'] = click.style(
            record.__dict__['message'], bold=True, fg='red')
        record.__dict__['asctime'] = click.style(
            f'[+] {record.__dict__["asctime"]}', bold=True, fg='cyan')
        record.__dict__['levelname'] = click.style(
            f'{record.__dict__["levelname"]}:', bold=True, fg='cyan')

        return super().formatMessage(record)
