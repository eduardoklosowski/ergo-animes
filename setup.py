# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


version = __import__('ergoanimes').__version__
with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')


setup(
    name='ergo-animes',
    version=version,
    packages=find_packages(),

    install_requires=['Pillow'],

    author='Eduardo Augusto Klosowski',
    author_email='eduardo_klosowski@yahoo.com',

    description='Animes for Ergo',
    long_description=long_description,
    license='MIT',
    url='https://github.com/eduardoklosowski/ergo-animes',

    include_package_data=True,
    zip_safe=False,
)
