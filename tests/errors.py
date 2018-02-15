import unittest
from tests.baseclass import ParserTest

from pykickstart.errors import formatErrorMsg, KickstartError, KickstartParseError, \
    KickstartVersionError, _format_error_message


class ErrorMessage_TestCase(ParserTest):
    def runTest(self):
        # For now, just verify that calling formatErrorMsg with no message
        # returns something.  Digging in and checking what the message is
        # when we could be running "make check" in another language is hard.

        # NOTE: formatErrorMsg is replaced with _format_error_message.
        self.assertNotEqual(_format_error_message(47), "")

        # Function formatErrorMsg is deprecated and returns its arguments now.
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(formatErrorMsg(47), (47, ""))

        with self.assertWarns(DeprecationWarning):
            self.assertEqual(formatErrorMsg(47, "OH NO!"), (47, "OH NO!"))


class Exception_TestCase(ParserTest):
    def runTest(self):
        self.assertEqual(str(KickstartError("OH NO!")), "OH NO!")
        self.assertEqual(str(KickstartParseError("OH NO!")), "OH NO!")
        self.assertEqual(str(KickstartVersionError("OH NO!")), "OH NO!")

        err = KickstartError()
        self.assertEqual(err.message, "")
        self.assertEqual(err.lineno, None)
        self.assertEqual(err.value, "")
        self.assertEqual(str(err), "")

        err = KickstartError("OH NO!")
        self.assertEqual(err.message, "OH NO!")
        self.assertEqual(err.lineno, None)
        self.assertEqual(err.value, "OH NO!")
        self.assertEqual(str(err), "OH NO!")

        err = KickstartError(lineno=0)
        self.assertEqual(err.message, "")
        self.assertEqual(err.lineno, 0)
        self.assertEqual(err.value, _format_error_message(msg="", lineno=0))
        self.assertEqual(str(err), _format_error_message(msg="", lineno=0))

        err = KickstartError(lineno=1)
        self.assertEqual(err.message, "")
        self.assertEqual(err.lineno, 1)
        self.assertEqual(err.value, _format_error_message(msg="", lineno=1))
        self.assertEqual(str(err), _format_error_message(msg="", lineno=1))

        err = KickstartError("OH NO!", lineno=0)
        self.assertEqual(err.message, "OH NO!")
        self.assertEqual(err.lineno, 0)
        self.assertEqual(err.value, _format_error_message(msg="OH NO!", lineno=0))
        self.assertEqual(str(err), _format_error_message(msg="OH NO!", lineno=0))

        err = KickstartError("OH NO!", lineno=1)
        self.assertEqual(err.message, "OH NO!")
        self.assertEqual(err.lineno, 1)
        self.assertEqual(err.value, _format_error_message(msg="OH NO!", lineno=1))
        self.assertEqual(str(err), _format_error_message(msg="OH NO!", lineno=1))

        err = KickstartError("OH NO!", lineno=1, formatting=True)
        self.assertEqual(err.message, "OH NO!")
        self.assertEqual(err.lineno, 1)
        self.assertEqual(err.value, _format_error_message(msg="OH NO!", lineno=1))
        self.assertEqual(str(err), _format_error_message(msg="OH NO!", lineno=1))

        err = KickstartError("OH NO!", lineno=1, formatting=False)
        self.assertEqual(err.message, "OH NO!")
        self.assertEqual(err.lineno, 1)
        self.assertEqual(err.value, "OH NO!")
        self.assertEqual(str(err), "OH NO!")

        with self.assertWarns(DeprecationWarning):
            err = KickstartError(formatErrorMsg(lineno=0))
            self.assertEqual(err.message, "")
            self.assertEqual(err.lineno, 0)
            self.assertEqual(err.value, _format_error_message(msg="", lineno=0))
            self.assertEqual(str(err), _format_error_message(msg="", lineno=0))

        with self.assertWarns(DeprecationWarning):
            err = KickstartError(formatErrorMsg(lineno=1))
            self.assertEqual(err.message, "")
            self.assertEqual(err.lineno, 1)
            self.assertEqual(err.value, _format_error_message(msg="", lineno=1))
            self.assertEqual(str(err), _format_error_message(msg="", lineno=1))

        with self.assertWarns(DeprecationWarning):
            err = KickstartError(formatErrorMsg(msg="OH NO!", lineno=0))
            self.assertEqual(err.message, "OH NO!")
            self.assertEqual(err.lineno, 0)
            self.assertEqual(err.value, _format_error_message(msg="OH NO!", lineno=0))
            self.assertEqual(str(err), _format_error_message(msg="OH NO!", lineno=0))

        with self.assertWarns(DeprecationWarning):
            err = KickstartError(formatErrorMsg(msg="OH NO!", lineno=1))
            self.assertEqual(err.message, "OH NO!")
            self.assertEqual(err.lineno, 1)
            self.assertEqual(err.value, _format_error_message(msg="OH NO!", lineno=1))
            self.assertEqual(str(err), _format_error_message(msg="OH NO!", lineno=1))


if __name__ == "__main__":
    unittest.main()
