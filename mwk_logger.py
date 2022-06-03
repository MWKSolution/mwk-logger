"""Custom logger with colors"""
import logging

# escape codes for changing colors in terminal
NORMAL = '\x1b[37m'
WHITE = '\x1b[97m'
GREEN = '\x1b[92m'
YELLOW = '\x1b[93m'
RED = '\x1b[91m'
CRITICAL = '\x1b[30;1;101m'
RESET = '\x1b[0;0;0m'

# used logging formats
LEVEL_FMT = r'[%(levelname)8s]'
TIME_FMT = r' %(asctime)s'
INFO_FMT = r' %(name)s %(module)s.%(funcName)s%(lineno)4s '
MSG_FMT = r'%(message)s'

DATE_FMT = r'%y.%m.%d %H:%M'

# record definition for logging in file
FILE_FMT = LEVEL_FMT + TIME_FMT + INFO_FMT + MSG_FMT

class CustomFormatter(logging.Formatter):
    """Custom formatter class"""

    @staticmethod
    def get_color_fmt(color):
        """Get coloured format of record for logging in terminal"""
        if color == CRITICAL:
            mid = RESET
        else:
            mid = NORMAL
        return color + LEVEL_FMT + mid  + INFO_FMT + color + MSG_FMT + RESET

    def __init__(self):
        """Defining levels logging formats and date time format for custom logger."""
        super().__init__()
        self.date_fmt = DATE_FMT
        self.FORMATS = {logging.DEBUG   :self.get_color_fmt(NORMAL),
                        logging.INFO    :self.get_color_fmt(WHITE),
                        logging.WARNING :self.get_color_fmt(YELLOW),
                        logging.ERROR   :self.get_color_fmt(RED),
                        logging.CRITICAL:self.get_color_fmt(CRITICAL)}

    def format(self, record):
        """Function needed for logging record generation according to defined formats."""
        log_fmt = self.FORMATS.get(record.levelno)
        log_date_fmt = self.date_fmt
        formatter = logging.Formatter(log_fmt, log_date_fmt)
        return formatter.format(record)


class CustomLoggerCreationError(Exception):
    """Custom error raised when creating logger failed"""
    def __init__(self, value, prev):
        self.value = value
        self.prev = prev

    def __str__(self):
        """Error info + info on source error"""
        return repr(self.value) + '\n\tbecause of: ' + repr(self.prev)


class CustomLogger:
    """Custom logger class with default parameters"""
    def __init__(self,
                 name='>',            # = name of the logger
                 file='mwk_log.log',        # = default log file
                 stream_level='DEBUG',   # ='' if no logging to terminal
                 file_level=None):     # ='' if no logging to file
        try:
            self.log_NAME = name
            self.log_FILE = file
            self.log_STREAM_LEVEL = stream_level
            self.log_FILE_LEVEL = file_level

            self.logger = logging.getLogger(self.log_NAME)
            self.logger.setLevel(logging.DEBUG)
            if not self.log_STREAM_LEVEL and not self.log_FILE_LEVEL:
                self.log_STREAM_LEVEL = 'DEBUG'

            if self.log_STREAM_LEVEL:
                self.stream_handler = logging.StreamHandler()
                self.stream_handler.setLevel(self.log_STREAM_LEVEL)
                self.stream_handler.setFormatter(CustomFormatter())
                self.logger.addHandler(self.stream_handler)
            if self.log_FILE_LEVEL:
                self.file_handler = logging.FileHandler(self.log_FILE)
                self.file_handler.setLevel(self.log_FILE_LEVEL)
                self.file_handler.setFormatter(logging.Formatter(fmt=FILE_FMT, datefmt=DATE_FMT))
                self.logger.addHandler(self.file_handler)
        except Exception as err:
            raise CustomLoggerCreationError('ERROR creating logger', err) from None


if __name__ == '__main__':
    #Testing custom logger
    # new logger referred by variable 'log'
    log = CustomLogger(stream_level=None, file_level='CRITICAL').logger
    # some log records...
    log.debug('This is a debug message')
    log.info('This is an info message')
    log.warning('This is a warning message')
    log.error('This is an error message')
    log.critical('This is a critical message')
    try:
        raise ZeroDivisionError('Some error')
    except Exception:
        log.exception('Some other error!')
