from distutils.core import setup
import argparse
import os

setup(name='pykickstart', version='3.1',
      description='Python module for manipulating kickstart files',
      author='Chris Lumens', author_email='clumens@redhat.com',
      url='http://fedoraproject.org/wiki/pykickstart',
      scripts=['tools/ksvalidator.py', 'tools/ksflatten.py', 'tools/ksverdiff.py', 'tools/ksshell.py'],
      packages=['pykickstart', 'pykickstart.commands', 'pykickstart.handlers'],
      data_files=[('share/man/man1', ['docs/ksvalidator.1', 'docs/ksflatten.1', 'docs/ksverdiff.1',
                                      'docs/ksshell.1'])])

# pykickstart tools were renamed to have .py extension because of code coverage reporting
# -> we need to rename it afterwards so that the tools don't have the extension after installation
parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("--root")
args = parser.parse_args()
if args.action == "install":
    for script in ['ksvalidator.py', 'ksflatten.py', 'ksverdiff.py', 'ksshell.py']:
        script_path = os.path.join(args.root, "usr", "bin", script)
        os.rename(script_path, script_path.rstrip(".py"))
