#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''setup twoq'''

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = ['stuf>=0.8.9']

setup(
    name='twoq',
    version='0.4.3',
    description='iterator chaining, underscored by a two-headed queue',
    long_description=open(os.path.join(os.getcwd(), 'README.rst'), 'r').read(),
    author='L. C. Rees',
    url='https://bitbucket.org/lcrees/twoq/',
    author_email='lcrees@gmail.com',
    license='MIT',
    packages=['twoq', 'twoq.mixins', 'twoq.active', 'twoq.lazy'],
    test_suite='twoq.tests',
    zip_safe=False,
    keywords='queue generator utility iterator functional programming',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
