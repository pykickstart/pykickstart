#
# Tomas Radej <tradej@redhat.com>
#
# Copyright 2015 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.
#
import gettext
import os
import six

def _find_locale_files():
    module_path = os.path.abspath(__file__)
    locale_path = os.path.join(os.path.dirname(module_path), 'locale')

    gettext.bindtextdomain("pykickstart", locale_path)
    gettext.textdomain("pykickstart")

if six.PY3:
    import sys

    _find_locale_files()

    def _(x):
        if x == '':  # Workaround for gettext's behaviour on empty strings
            return ''

        result = gettext.lgettext(x)
        if isinstance(result, bytes):
            return result.decode(sys.getdefaultencoding())
        else:
            return result
else:
    _find_locale_files()

    _ = lambda x: gettext.lgettext(x) if x else ''
