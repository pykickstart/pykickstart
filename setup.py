#!/usr/bin/python2

from distutils.core import setup

setup(name='pykickstart', version='1.31',
      description='Python module for manipulating kickstart files',
      author='Chris Lumens', author_email='clumens@redhat.com',
      url='http://fedoraproject.org/wiki/pykickstart',
      scripts=['tools/ksvalidator', 'tools/ksflatten'],
      packages=['pykickstart', 'pykickstart.commands', 'pykickstart.handlers'])
