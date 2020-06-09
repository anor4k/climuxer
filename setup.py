from setuptools import setup

setup(
    name = 'climuxer',
    version = '0.1.0',
    py_modules = ['climuxer'],
    install_requires = [
        'click',
        'pymediainfo',
    ],
    entry_points = {
        'console_scripts': [
            'climuxer = climuxer:main',
        ]
    },
)
