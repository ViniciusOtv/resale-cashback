
from setuptools import find_packages, setup

__version__ = '0.1.0'
__description__ = 'Api Python Para cadastrar um novo revendedor(a) e retornar um cashback de acordo a bonificação'
__long_description__ = 'Api Python Para cadastrar um novo revendedor(a) e retornar um cashback de acordo a bonificação'

__author__ = 'Vinicius Otavio'
__author_email__ = 'vinicius.otv@hotmail.com'
testing_extras = [
    'pytest',
    'pytest-cov',
]

setup(
    name='resale api',
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    description=__description__,
    long_description=__long_description__,
    url='',
    keywords='API, MongoDB',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras},
)