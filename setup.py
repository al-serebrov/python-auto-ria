"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-auto-ria',
    version='0.5',
    description='Calculate average car price',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/al-serebrov/python-auto-ria',
    author='Alexander Serebrov',
    author_email='serebrov.alexandr@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='cars average price',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5',
    instal_requires=[
        'requests',
        'typing',
        'pytest',
        'pytest-greendots',
        'coverage',
        'flake8',
        'pylint',
        'mypy',
        'requests_mock',
    ]
)
