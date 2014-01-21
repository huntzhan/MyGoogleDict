#!/usr/bin/env python

from setuptools import setup

setup(
    name='mgd',
    version='0.1',
    author='Zhan Haoxun',
    author_email='programmer.zhx@gmail.com',

    url='https://pypi.python.org/pypi/mgd',
    license='MIT',
    description='command-line front end of google translation serve.',
    long_description=open('README.rst').read(),

    install_requires=['docopt==0.6.1', 'goslate==1.1.2'],
    packages=['mgd'],

    entry_points = {
        'console_scripts': [
            'mgd = mgd.interface:main',
        ]
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
