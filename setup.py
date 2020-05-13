from setuptools import setup

setup(name='pykickstart', version='3.27',
      description='Python module for manipulating kickstart files',
      author='Chris Lumens', author_email='clumens@redhat.com',
      url='http://fedoraproject.org/wiki/pykickstart',
      install_requires=['six', 'requests'],
      extras_require={
          "docs": ['Sphinx'],
          "test": ['coveralls', 'coverage', 'pocketlint', 'pylint']},
      scripts=['tools/ksvalidator.py', 'tools/ksflatten.py', 'tools/ksverdiff.py', 'tools/ksshell.py'],
      packages=['pykickstart', 'pykickstart.commands', 'pykickstart.handlers'],
      data_files=[('share/man/man1', ['docs/ksvalidator.1', 'docs/ksflatten.1', 'docs/ksverdiff.1',
                                      'docs/ksshell.1'])],
      classifiers=["Programming Language :: Python :: 3"])
