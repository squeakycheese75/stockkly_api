from setuptools import setup, find_packages

setup(
    name='stockkly_api',
    version='1.0.0',
    description='Code for a RESTful API based',
    url='https://github.com/squeakycheese75/stockklyApi',
    author='Jamie Wooltorton',

    keywords='rest',

    packages=find_packages(),

    install_requires=['flask-restplus==0.12.1'],
)
