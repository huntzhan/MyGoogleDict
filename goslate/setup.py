#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''Setup script for goslate
'''

import os
import goslate as module

__author__ = 'ZHUO Qiang'
__date__ = '2013-05-14'

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = module.__name__,
    version = module.__version__,
    author = module.__author__,
    author_email = module.__email__,
    description = module.__doc__,
    license = module.__license__,
    keywords = "google translation i18n l10n",
    url = module.__download__,
    packages=[],
    py_modules=['goslate'],
    long_description=read('README.rst'),
    install_requires=['futures'],    
    test_suite='test_goslate',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Linguistic',
    ],
)
