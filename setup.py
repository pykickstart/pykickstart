#!/usr/bin/python2

from distutils.core import setup

setup(name='pykickstart', version='0.42',
      description='Python module for manipulating kickstart files',
      author='Chris Lumens', author_email='clumens@redhat.com',
      url='http://fedoraproject.org/wiki/pykickstart',
      scripts=['validator/ksvalidator'], packages=['pykickstart'])
