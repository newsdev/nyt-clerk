import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='nyt-clerk',
    version='0.0.1',
    author='Jeremy Bowers',
    author_email='jeremy.bowers@nytimes.com',
    url='',
    description='Python client for parsing SCOTUS data from multiple sources.',
    long_description=read('README.md'),
    packages=['clerk'],
    license="MIT",
    keywords='SCOTUS data parsing scraping legal law court',
    install_requires=['beautifulsoup4==4.4.0','requests==2.7.0','wheel==0.24.0]']
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache 2.0 Software License',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)