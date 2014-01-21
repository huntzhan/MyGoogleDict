from __future__ import print_function
import os
import inspect
import platform


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
    # succeeded, print it.
    print('{}: {}'.format(name, var))
    return var


def _enter_install_path(PATH):
    paths = PATH.split(':')
    while True:
        install_path = input('Please select a path for installation: ')
        if install_path in paths:
            break
        else:
            print('Invalid input. Try Again.')
    return install_path


def _make_symbol_link(install_path):
    source = _get_path('interface.py')
    # ensure executable
    os.chmod(source, 0b111111111)
    link = os.path.join(install_path, 'mgd')
    try:
        os.symlink(source, link)
        print('Successfully made symbolic link {}'.format(link))
    except Exception as e:
        print('Can not make symbolic link {}'.format(link))
        raise e


def run():
    if platform.system() == 'Windows':
        print('Windows Not Support. Please install mgd manually.')
        return

    PATH = _get_env_var('PATH')
    install_path = _enter_install_path(PATH)
    _make_symbol_link(install_path)
