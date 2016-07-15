import unittest

from pykickstart.version import makeVersion, versionMap

class Attribute_TestCase(unittest.TestCase):
    def _valid_attr(self, attr):
        # Throw out attributes that:
        # * Start with an underscore - they're probably internal use only things
        # * Are deprecated - we don't set those attributes on the object
        # * Are marked as notest - We are doing something weird with those
        # * Are positional arguments (e.g. no option_strings present)
        return not attr.dest.startswith("_") and not attr.deprecated and \
               not attr.notest and len(attr.option_strings) > 0

    def _test_one_command(self, handler, cmdClass):
        # Create an instance of the command class here so we have something
        # to inspect for attributes.  We'll throw this away after we're
        # done using it.
        cmdObj = cmdClass()
        cmdObj.handler = handler

        # Some commands are very simple and don't need a parser.  We don't
        # need to test those commands.
        if not hasattr(cmdObj, "op"):
            return

        attrs = list(set((x.dest, x.type) for x in cmdObj.op._actions if self._valid_attr(x)))
        call_kwargs = {}
        init_kwargs = {}

        # Set some known sentinel value, being careful to handle types.
        for a in attrs:
            if a[1] == int:
                call_kwargs[a[0]] = 47
                init_kwargs[a[0]] = 147
            elif a[1] == bool:
                call_kwargs[a[0]] = False
                init_kwargs[a[0]] = True
            elif getattr(a[1], "func_name", "") == "commaSplit":
                call_kwargs[a[0]] = ["call-placeholder"]
                init_kwargs[a[0]] = ["init-placeholder"]
            else:
                call_kwargs[a[0]] = "call-placeholder"
                init_kwargs[a[0]] = "init-placeholder"

        # If this is a command that can be listed more than once, instantiate its
        # data class and use that for the rest of the testing.  Otherwise, create
        # a new instance of the command class.
        if cmdObj.dataClass is not None:
            obj = cmdObj.dataClass(**init_kwargs)
        else:
            obj = cmdClass(**init_kwargs)

        del(cmdObj)

        obj.seen = True

        # Test that passing all the attributes into the __init__ method worked.
        for a in attrs:
            val = getattr(obj, a[0])
            if a[1] == int:
                self.assertEqual(val, 147, "init: %s got %s, expected 147" % (a[0], val))
            elif a[1] == bool:
                self.assertTrue(val, "init: %s got %s, expected True" % (a[0], val))
            else:
                self.assertEqual(val, "init-placeholder", "init: %s got %s, expected 'init-placeholder'" % (a[0], val))

        # And then test that passing in all the attributes via the __call__
        # method also worked.
        obj(**call_kwargs)

        for a in attrs:
            val = getattr(obj, a[0])
            if a[1] == int:
                self.assertEqual(val, 47, "init: %s got %s, expected 47" % (a[0], val))
            elif a[1] == bool:
                self.assertFalse(val, "init: %s got %s, expected False" % (a[0], val))
            else:
                self.assertEqual(val, "call-placeholder", "init: %s got %s, expected 'call-placeholder'" % (a[0], val))

    def runTest(self):
        for ver in versionMap.values():
            handler = makeVersion(ver)
            for cmdClass in (v for (k, v) in handler.commandMap.items() if k != "method"):
                self._test_one_command(handler, cmdClass)
