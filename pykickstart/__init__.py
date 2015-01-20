
import gettext
import six

def _(x):
    if not x: # Workaround for gettext behaviour on empty strings
        return ''

    result = gettext.ldgettext('pykickstart', x)

    if six.PY3: # In Python 3, gettext returns bytes sometimes
        import sys
        if isinstance(result, bytes):
            result = result.decode(sys.getdefaultencoding())

    return result
