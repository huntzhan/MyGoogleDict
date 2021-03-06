from __future__ import unicode_literals

import inspect
from functools import wraps
from pprint import pprint


def ensure_decode(func):
    def utf8_decoder(text):
        UTF8 = 'UTF-8'
        try:
            decoded = text.decode(UTF8)
        except:
            # both decoded text and result(a dictionary variable contains
            # decoded information) would trigger exception. In this case, just
            # return the argument.
            decoded = text
        return decoded

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        decoded_args = map(utf8_decoder, args)
        decoded_kwargs = {k: utf8_decoder(v) for k, v in kwargs.items()}
        return func(self, *decoded_args, **decoded_kwargs)
    return wrapper


def debug_return_val(func):
    def _print_func(prefix, name):
        line = "{}: {}".format(prefix, name)
        print('*' * len(line))
        print(line)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._debug:
            _print_func('ENTER_FUNC', func.__name__)

        val = func(self, *args, **kwargs)

        if self._debug:
            _print_func('QUIT_FUNC', func.__name__)
            pprint(val)

        return val
    return wrapper


def decorate_all_methods(decorator):
    def decorate(cls):
        for attr, method in inspect.getmembers(cls, inspect.ismethod):
            if attr == '__init__':
                continue
            setattr(cls, attr, decorator(method))
        return cls
    return decorate
