#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme_file = os.path.join(here, 'README.md')
changes_file = os.path.join(here, 'CHANGES.md')

long_description = '\n\n'.join((
    open(readme_file).read(),
    open(changes_file).read(),
))


setup(
    name = 'django_channel',
    version = '0.4.5',
    url = 'http://github.com/duanhongyi/django-channel',
    license = 'BSD',
    description = 'channel support for django.',
    long_description = long_description,
    author = "duanhongyi",
    author_email = 'duanhongyi@doopai.com',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    zip_safe = True,
    install_requires = ['setuptools',],
)
