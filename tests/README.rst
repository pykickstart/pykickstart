Testing pykickstart
===================

Pykickstart's test suite requires the nosetests Python package. To execute it
from inside the source directory run the command::

    make test

It is also possible to generate test coverage reports using the Python coverage
tool. To do that execute::

    make coverage

To execute the Pylint code analysis tool run::

    make check

Running Pylint requires Python3 due to usage of pocket-lint.


Test Suite Architecture
------------------------

Pykickstart's test suite relies on several base classes listed below. All test
cases inherit from them.

- :class:`unittest.TestCase` - the standard unit test class in Python.
  Used only for base classes described below;


- :class:`~tests.baseclass.CommandTest` - intended as a base class for
  tests related to pykicsktart commands. The important functions are:

  - `self.assert_parse` - KickstartParseError is not raised. If a matching
    value is supplied make sure the resulting string matches it;
  - `self.assert_parse_error` - assert that parsing the supplied string raises
    the specified exception (KickstartParseError by default);
  - `self.assert_deprecated` - ensure that the provided option is listed as
    deprecated;
  - `self.assert_removed` - ensure that the provided option is not present in
    option_list;
  - `self.assert_required` - ensure that the provided option is labelled as
    required in option_list;
  - `self.assert_type` - ensure that the provided option is of the requested
    type;

- :class:`~tests.baseclass.ParserTest` - base class for tests related to parsing
  functionality. Always uses the DEVEL version of pykickstart. Important
  functions are:

  - `self.assert_parse` - parsing of this string is expected to finish without
    raising an exception; if it raises an exception, the test failed;
  - `self.assert_parse_error` - parsing of this command sequence is expected to
    raise an exception (KickstartParseError by default). Matching regular
    expression can also be provided.

- :class:`~tests.baseclass.CommandSequenceTest` - inherits from
  :class:`~tests.baseclass.ParserTest`, enables testing kickstart indepdent
  command sequences and checking if their parsing raises or doesn't raise a
  parsing exception.

In addition any other assert methods from :class:`unittest.TestCase` can be used
as well to provide better test coverage.

Test scenarios are defined inside the `runTest` method of each test class using
multiple assert statements.

In order to get a high level view of how test classes inherit from each other
you can generate an inheritance diagram::

    PYTHONPATH=. python3-pyreverse -p "Pykickstart_Tests" -o svg -SkAmy tests/
