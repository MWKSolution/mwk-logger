from functools import wraps, partial
from time import perf_counter as pc
from inspect import signature
from logger import ESC


def color_msg(info, func, result):
    return ''.join([ESC['GREEN'], info, ESC['NORMAL'], func, ESC['GREEN'], result, ESC['RESET']])

def normal_msg(info, func, result):
    return ''.join([info, func, result])


def split_seconds(s):
    sec = s // 1
    msec = (s % 1) * 1000
    return sec, msec


def timer(func=None, *, logger=None):
    """Print the runtime of the decorated function"""
    if func is None:
        return partial(timer, logger=logger)

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = pc()
        value = func(*args, **kwargs)
        end_time = pc()
        secs, msecs = split_seconds(end_time - start_time)
        msg = color_msg(f'[Timer   ]',
                        f' {func.__module__}.{func.__name__} -- ',
                        f'{secs:.0f} sec(s) {msecs:.0f} msec(s).')
        if logger:
            logger.debug(msg)
        else:
            print(msg)
        return value
    return wrapper_timer


def debug(func=None, *, logger=None):
    """Print the function signature and return value"""
    if func is None:
        return partial(debug, logger=logger)

    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        arguments = ', '.join(args_repr + kwargs_repr)
        sig = str((signature(func)))
        call_msg = color_msg(f'[Call    ]',
                    f' {func.__module__}.{func.__name__}{sig}',
                    f'({arguments})')
        if logger:
            logger.debug(call_msg)
        else:
            print(call_msg)
        value = func(*args, **kwargs)
        return_msg = color_msg(f'[Return  ]',
                      f' {func.__module__}.{func.__name__}({arguments}) = ',
                      f'{value!r}')
        if logger:
            logger.debug(return_msg)
            print(dir(logger))
        else:
            print(return_msg)
        return value
    return wrapper_debug


if __name__ == '__main__':
    # Testing decorators
    from time import sleep
    from logger import MwkLogger

    # @timer
    # @debug
    # def function(*args, **kwargs):
    #     # ... some function ...
    #     sleep(1.531)
    #     return True
    #
    # x = function('arg', kwarg='kwarg')

    log = MwkLogger(stream_level='DEBUG', file_level='DEBUG')

    @timer(logger=log)
    @debug(logger=log)
    def function_log(*args, **kwargs):
        # ... some function to be logged...
        sleep(1.135)
        return True

    y = function_log('arg', kwarg='kwarg')