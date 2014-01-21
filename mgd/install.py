from __future__ import print_function
import os
import inspect


try:
    input = raw_input
except:
    pass


def _get_path(filename):
    obj = inspect.currentframe()
    module = inspect.getmodule(obj)
    path, _ = os.path.split(module.__file__)
    return os.path.join(path, filename)


def _get_env_var(name):
    _ERROR_CONTENT = 'Unable to dectect {} variable in you environment.'
    var = os.environ.get(name, None)
    if var is None or not var:
        raise Exception(_ERROR_CONTENT.format(name))


def _enter_install_path(PATH):
    paths = PATH.split(':')
    while True:
        install_path = input('Please select a path for installation: ')
        if install_path in paths:
            break
        else:
            print('Invalid input.')
    return install_path


def _make_symbol_link(install_path):
    source = _get_path('interface.py')
    link = os.path.join(install_path, 'mgd')
    try:
        os.symlink(source, link)
    except:
        print('Can not make symbolic link {}'.format(link))
    print('Successfully made symbolic link {}'.format(link))


def install():
    PATH = _get_env_var('PATH')
    print('PATH: {}'.format(PATH))
    install_path = _enter_install_path(PATH)
    _make_symbol_link(install_path)
