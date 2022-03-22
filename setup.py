# -*- coding:utf-8 -*-
from os.path import abspath, join, dirname
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

version = {}
with open(join(this_dir, "polyhymnia", "version.py")) as fp:
    exec(fp.read(), version)

setup(
    name='polyhymnia',
    version=version['__version__'],
    description='Polyhymnia: Natual Chinese Data Augmentation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/luoy2/polyhymnia.git',
    author='yikang',
    author_email='luoy2@hotmail.com',
    license='Apache License 2.0',
    keywords='corpus,NLU,NLP',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    package_data={'': ['data/*', 'data/stopwords/*']},
    install_requires=required,
    python_requires='>=3.6',
)