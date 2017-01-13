Pykickstart
===========

Pykickstart is a Python 2 and Python 3 library consisting of a data
representation of kickstart files, a parser to read files into that
representation, and a writer to generate kickstart files.

Online documentation
--------------------

Online documentation for kickstart and the Pykickstart library is available on Read the Docs:
https://pykickstart.readthedocs.io

How to generate the kickstart documentation
-------------------------------------------

The pykickstart documentation is generated dynamically from the source code with Sphinx.

To generate the documentation first make sure you have the Python bindings for Sphinx
and the ordered set Python module installed.
At least on Fedora this means installing the ``python3-sphinx`` and ``python3-orderedset`` packages.

Then change directory to the ``docs`` folder:

``cd docs``

And generate the docs with:

``make html``
