#! /usr/bin/env sh

python test_goslate.py
python setup.py build_sphinx
python setup.py upload_sphinx
python setup.py bdist_egg upload
python setup.py sdist upload
