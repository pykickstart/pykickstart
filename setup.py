from distutils.command.install_scripts import install_scripts as _install_scripts
from distutils.file_util import move_file
import os
from setuptools import setup


# This is required so that the scripts are detected by code coverage during testing, but are
# installed without their filename extensions
class install_scripts(_install_scripts):
    def run(self):
        _install_scripts.run(self)

        for old in self.get_outputs():
            new = os.path.splitext(old)[0]
            # move_file doesn't have a way to tell it to overwrite, so remove
            # the existing copy to accomplish the same thing.
            if os.path.isfile(new) and os.path.exists(new):
                os.unlink(new)
            move_file(old, new)


setup(cmdclass={"install_scripts": install_scripts},
      name='pykickstart', version='3.31',
      description='Python module for manipulating kickstart files',
      author='Chris Lumens', author_email='clumens@redhat.com',
      url='http://fedoraproject.org/wiki/pykickstart',
      install_requires=['six', 'requests'],
      extras_require={
          "docs": ['Sphinx'],
          "test": ['coveralls', 'coverage', 'pocketlint', 'pylint']},
      # These are installed by install_scripts() without their filename extensions
      scripts=['tools/ksvalidator.py', 'tools/ksflatten.py', 'tools/ksverdiff.py', 'tools/ksshell.py'],
      packages=['pykickstart', 'pykickstart.commands', 'pykickstart.handlers'],
      data_files=[('share/man/man1', ['docs/ksvalidator.1', 'docs/ksflatten.1', 'docs/ksverdiff.1',
                                      'docs/ksshell.1'])],
      classifiers=["Programming Language :: Python :: 3"])
