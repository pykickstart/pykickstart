#!/usr/bin/python2

from distutils.core import setup

setup(name='pykickstart', version='1.50',
      description='Python module for manipulating kickstart files',
      author='Chris Lumens', author_email='clumens@redhat.com',
      url='http://fedoraproject.org/wiki/pykickstart',
      scripts=['tools/ksvalidator', 'tools/ksflatten', 'tools/ksverdiff'],
      packages=['pykickstart', 'pykickstart.commands', 'pykickstart.handlers'])
