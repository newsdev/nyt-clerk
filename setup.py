import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='nyt-clerk',
    version='0.1.12',
    author='Jeremy Bowers',
    author_email='jeremy.bowers@nytimes.com',
    url='https://github.com/newsdev/nyt-clerk',
    description='Python client for parsing SCOTUS data from multiple sources.',
    long_description=read('README.rst'),
    packages=['clerk'],
    entry_points={
        'console_scripts': (
            'clerk = clerk:main',
        ),
    },
    license="Apache License 2.0",
    keywords='SCOTUS data parsing scraping legal law court',
    install_requires=['beautifulsoup4','html5lib','lxml','requests','nameparser','csvkit', 'pymongo', 'clint', 'cement'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
