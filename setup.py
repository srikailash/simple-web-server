import os
import re
from setuptools import setup, find_packages

def read_file(path):
    with open(path) as f:
        return f.read()

def get_version():
    #todo: This should be reading __version__ from __init__.py
    return "1.0.0"

setup(
    name='Araku',
    version=get_version(),
    description='Text based static blog generator',
    long_description=read_file('README.rst'),
    author='Sri Kailash',
    author_email='',
    url='http://srikailash.github.io/',
    license='BSD',
    keywords='srikailash blog',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'docutils>=0.16',
        'pygments>=2.6.1',
        'jinja2>=2.11.2',
        'watchdog>=0.10.3'
    ],
    entry_points={
        'console_scripts': [
            'araku = araku.__main__:main'
        ]
    },
    classifiers=[

    ]
)
