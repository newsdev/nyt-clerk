import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='nyt-clerk',
    version='0.0.16',
    author='Jeremy Bowers',
    author_email='jeremy.bowers@nytimes.com',
    url='https://github.com/newsdev/nyt-clerk',
    description='Python client for parsing SCOTUS data from multiple sources.',
    long_description=read('README.rst'),
    packages=['clerk'],
    license="Apache License 2.0",
    keywords='SCOTUS data parsing scraping legal law court',
    install_requires=['beautifulsoup4==4.4.0','html5lib==0.999999','lxml==3.4.4','requests==2.7.0','six==1.9.0','wheel==0.24.0','nameparser==0.3.10'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
