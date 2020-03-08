import os
from setuptools import setup, find_packages
import subprocess

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.adoc')
    )

version = None
try:
    version = subprocess.check_output('git describe --tags', shell=True, universal_newlines=True)
except:
    version = '0.0.1'
    pass

if not version:
    raise Exception('Could not determine version from git')

version = version.lstrip('v')
version = version.strip()


setup(
    name='ebay-oauth-python-client',
    version=version,
    description='EBay OAuth Python Client',
    long_description=long_description,
    url='https://github.com/store-manager/ebay-oauth-python-client',
    author='Chris Lapa',
    author_email='36723261+chris-lapa@users.noreply.github.com',
    license='Apache License 2.0',
    packages=find_packages(),
    keywords="ebay, oauth, python",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License 2.0",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
          'PyYAML==5.1',
          'selenium==3.141.0',
          'requests'
    ],
    zip_safe=True,
    test_suite="tests"
)