#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''setup for twoq'''

from os import getcwd
from os.path import join
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = list(l.strip() for l in open(
    join(getcwd(), 'requirements.txt'), 'r',
).readlines())

setup(
    name='twoq',
    version='0.4.11',
    description='iterator chaining, underscored by a two-headed queue',
    long_description=open(join(getcwd(), 'README.rst'), 'r').read(),
    keywords='queue generator utility iterator functional programming',
    license='BSD',
    author='L. C. Rees',
    author_email='lcrees@gmail.com',
    url='https://bitbucket.org/lcrees/twoq',
    packages=[
        l.strip() for l in open(join(getcwd(), 'packages'), 'r').readlines()
    ],
    test_suite='twoq.tests',
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
