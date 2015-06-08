# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


version = __import__('ergoanimes').__version__
with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')


setup(
    name='ergo-animes',
    version=version,
    packages=find_packages(),

    install_requires=[
        'django-userviews',
        'ergo',
        'Pillow',
    ],

    author='Eduardo Augusto Klosowski',
    author_email='eduardo_klosowski@yahoo.com',

    description='Animes para o Ergo',
    long_description=long_description,
    license='AGPLv3+',
    url='https://github.com/eduardoklosowski/ergo-animes',

    include_package_data=True,
    zip_safe=False,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
