from setuptools import setup

__author__ = 'Atsushi Odagiri <aodagx@gmail.com>'
__version__ = '0.0'

requires = [
    "pyramid",
    "pyramid_tm",
    "whoosh",
    "transaction",
]

setup(
    name="pyramid_whoosh",
    packages=["pyramid_whoosh"],
    install_requires=requires,
)
