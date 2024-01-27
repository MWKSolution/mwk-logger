import os
from mwk_logger import MwkLogger

from mwk_traceback import compact_tb

compact_tb.activate()


class TestError(Exception):
    pass

def main():
    # # Record format
    # print('Record format:', FILE_FMT)
    # # Test colors
    # [print(''.join([c, n]), end=' ') for n, c in MwkLogger.ESC.items()]
    # print()

    # Testing custom logger
    # new logger referred by variable: log
    # !!! v2.0.0 no need to use .logger after the constructor !!!
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    print(f'{host}:{port}')

    log = MwkLogger(name='mwk',
                    file='logger.log',
                    stream_level='DEBUG',
                    time=False,
                    syslog=(host, port),
                    syslog_level='WARNING',
                    system='server')
    # some log records...
    log.debug('This is a debug message.')
    log.info('This is an info message.')
    log.warning('This is a warning message.')
    log.error('This is an error message!')
    log.critical('This is a critical message!!!')
    try:
        raise TestError('Same like log.error but logs also traceback when error was raised!')
    except Exception:
        log.exception('This is an exception message!')

if __name__ == '__main__':
    main()