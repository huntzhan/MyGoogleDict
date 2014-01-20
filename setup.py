#!/usr/bin/env python

from setuptools import setup

setup(
    name='mgd',
    version='0.1',
    author='Zhan Haoxun',
    author_email='programmer.zhx@gmail.com',

    url='https://pypi.python.org/pypi/mgd',
    license='MIT',
    descrption='command-line front end of google translation serve.',

    install_requires=['docopt==0.6.1', 'goslate==1.1.2'],
    packages=['mgd'],
)
