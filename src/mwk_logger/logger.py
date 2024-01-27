"""Custom logger with colors on terminal"""
import logging
from .sys_handler import SysLogHandlerSSL
from colorama import Fore, Back, Style
from colorama import initialise

initialise.just_fix_windows_console()

# formats for components of the log record
FMT = dict(
    LEVEL=r'[%(levelname)8s]',
    TIME=r'%(asctime)s',
    INFO=r'[%(name)s]',  # %(module)s.%(funcName)s@%(lineno)s',
    MSG=r'%(message)s')

# general date/time format
DATE_FMT = r'%y.%m.%d %H:%M'

# record definition for logging in file
FILE_FMT = ' '.join([fmt for fmt in FMT.values()])
SYS_FMT = ' '.join([fmt for key, fmt in FMT.items() if key != 'TIME'])


class MwkFormatter(logging.Formatter):
    """Custom formatter class"""

    def get_color_fmt(self, color):
        """Get coloured format of record for logging in terminal.
        It uses format components and given colors.
        <general_color> is for level and message, <info_color> is for time and info part of the record.
        Returns logging record format."""
        time_fmt = FMT['TIME'] if self.time else ''
        return color + FMT['LEVEL'] + ' ' + time_fmt + FMT['INFO'] + ' ' + FMT['MSG'] + Style.RESET_ALL

    def __init__(self, time):
        """Defining formats of logging levels and date/time format for custom logger."""
        super().__init__()
        self.date_fmt = DATE_FMT
        self.time = time
        self.FORMATS = {logging.DEBUG: self.get_color_fmt(Fore.WHITE),
                        logging.INFO: self.get_color_fmt(Fore.LIGHTWHITE_EX),
                        logging.WARNING: self.get_color_fmt(Fore.LIGHTYELLOW_EX),
                        logging.ERROR: self.get_color_fmt(Fore.LIGHTRED_EX),
                        logging.CRITICAL: self.get_color_fmt(Fore.LIGHTWHITE_EX + Back.RED), }

    def format(self, record):
        """Function needed for logging record generation according to defined formats."""
        log_fmt = self.FORMATS.get(record.levelno)
        log_date_fmt = self.date_fmt
        formatter = logging.Formatter(log_fmt, log_date_fmt)
        return formatter.format(record)


class LoggerCreationError(Exception):
    """Custom error raised when creating logger failed"""


class LogHandler:
    """Class for setting up loger handler."""

    def __init__(self, _handler, _level, _formatter):
        self.handler = _handler
        self.handler.setLevel(_level)
        self.handler.setFormatter(_formatter)


class MwkLogger:
    """Custom logger class"""

    def __new__(cls,
                name='mwk',  # name of the logger
                file=None,  # path to log file
                syslog=None,  # (host, port) for syslog
                stream_level='DEBUG',  # logging to terminal level
                file_level='INFO',  # logging to file level
                syslog_level='INFO',
                time=False,  # add timestamp to stream logging
                system=None):  # system name for syslog
        """Constructor parameters:
        name - name of the logger, by default = 'mwk',
        file - path to file to log into, by default = 'mwk.log',
        stream_level - logging level for terminal, by default = 'WARNING',
        file_level - logging level for file, by default = None,
        time - if timestamp should be added to terminal log, by default = False,

        LEVELS:
         None - no logging or:
         'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
        If both levels are set to None stream_level is changed to WARNING.

        !!! __new__ returns instance of logging.logger, no need to use .logger after the constructor """
        try:
            logger = logging.getLogger(name)

            logger.setLevel('DEBUG')
            # if both levels set to None then set stream level to DEBUG
            if not stream_level and not file_level and not syslog_level:
                stream_level = 'DEBUG'
            # set logger handlers according to settings
            if stream_level:  # for terminal
                stream = LogHandler(logging.StreamHandler(),
                                    stream_level,
                                    MwkFormatter(time))
                logger.addHandler(stream.handler)
            if file:  # and for file
                file = LogHandler(logging.FileHandler(file),
                                  file_level,
                                  logging.Formatter(fmt=FILE_FMT, datefmt=DATE_FMT))
                logger.addHandler(file.handler)

            if syslog:
                syshandler = SysLogHandlerSSL(syslog[0], syslog[1], system)
                syshandler.setFormatter(logging.Formatter(fmt=SYS_FMT, datefmt=DATE_FMT))
                syshandler.setLevel(syslog_level)
                logger.addHandler(syshandler)
            return logger
        # catch error creating handler
        except Exception as err:
            raise LoggerCreationError('ERROR creating logger:') from err
