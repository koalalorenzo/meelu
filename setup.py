#!/usr/bin/env python

from distutils.core import setup

setup(name='Meelu',
    version='0.2',
    description='Meelu is a Desktop client for Meemi',
    author='Lorenzo Setale',
    author_email='koalalorenzo@gmail.com',
    url='http://www.meelu.org/',
    py_modules=['libmeelu'],
    data_files=[
                ('share/meelu/', ['meelu.png', 'gui.glade', 'main.py']),
                ('bin', ['meelu']),
                ('share/applications', ['meelu.desktop'])
                ],
    )
