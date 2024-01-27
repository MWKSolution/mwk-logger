from mwk_logger import MwkLogger

from mwk_traceback import compact_tb

compact_tb.activate()


class TestError(Exception):
    pass

def main():
    log = MwkLogger(name='mwk',
                    stream_level='DEBUG',
                    time=False)
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