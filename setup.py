
from setuptools import setup

setup(
    name='seo-protocol',
    version='0.1.0',
    packages=['src.seo_protocol'],
    install_requires=[
        'pygithub',
        'nltk',
        'google-api-python-client',
        'oauth2client',
        'sqlite3',
        'matplotlib',
        'jinja2',
        'retrying'
    ],
    entry_points={
        'console_scripts': [
            'seo-protocol=seo_protocol_cli:main',
        ],
    },
)
    