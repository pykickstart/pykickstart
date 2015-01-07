
import gettext
import six

if six.PY3:
    import sys
    def _(x):
        result = gettext.ldgettext('pykickstart', x)
        if isinstance(result, bytes):
            return result.decode(sys.getdefaultencoding())
        else:
            return result
else:
    _ = lambda x: gettext.ldgettext("pykickstart", x)
