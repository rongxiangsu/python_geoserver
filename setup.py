import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "airwing"

PACKAGES = ["airwing"]

DESCRIPTION = "this is a package for auto publish web map service in geosever and get geoinfo from the WMS."

LONG_DESCRIPTION = read("README.rst")

KEYWORDS = "geoserver python"

AUTHOR = "wushi"

AUTHOR_EMAIL = "hfutsrx@sina.com"

VERSION = "1.0.1"

URL = "https://github.com/surongxiang/python_geoserver"

LICENSE = "MIT"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)