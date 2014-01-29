import inspect
from functools import wraps
from pprint import pprint


SENTENCES = 'sentences'
TRANS = 'trans'
DICT = 'dict'
TERMS = 'terms'
POS = 'pos'


def assemble_senteces_from_json(json):
    sentences = map(
        lambda x: x[TRANS],
        json[SENTENCES],
    )
    return ''.join(sentences)


def convert_dict_to_key_value_pairs(json):
    for entity in json.get(DICT):
        pos = entity[POS] or 'error_pos'
        vals = [val for val in entity[TERMS]]
        yield pos, vals


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
