from setuptools import setup

setup(
    name = 'remuxer',
    version = '0.1.0',
    py_modules = ['remuxer'],
    install_requires = [
        'click',
        'pymediainfo',
    ],
    entry_points = {
        'console_scripts': [
            'remuxer = remuxer:main',
        ]
    },
)