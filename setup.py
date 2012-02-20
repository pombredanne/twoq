# -*- coding: utf-8 -*-
'''setup twoq'''

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = ['stuf>=0.8.4']
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    install_requires.extend(['ordereddict', 'unittest2'])

setup(
    name='twoq',
    version='0.1.1',
    description='''iterator manipulation, underscored by two queues''',
    long_description=open(os.path.join(os.getcwd(), 'README.rst'), 'r').read(),
    author='L. C. Rees',
    url='https://bitbucket.org/lcrees/twoq/',
    author_email='lcrees@gmail.com',
    license='MIT',
    packages=['twoq'],
    test_suite='twoq.test',
    zip_safe=False,
    keywords='queue generator utility iterator',
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
        'Topic :: Utilities',
    ],
)
