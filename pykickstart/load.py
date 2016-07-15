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
import requests
import shutil
import six

from pykickstart.errors import KickstartError
from pykickstart.i18n import _
from requests.exceptions import SSLError, RequestException

_is_url = lambda location: '://' in location  # RFC 3986

SSL_VERIFY = True

def load_to_str(location):
    '''Load a destination URL or file into a string.
    Type of input is inferred automatically.

    Arguments:
    location -- URL or file name to load

    Returns: string with contents
    Raises: KickstartError on error reading'''

    if _is_url(location):
        return _load_url(location)
    else:
        return _load_file(location)

def load_to_file(location, destination):
    '''Load a destination URL or file into a file name.
    Type of input is inferred automatically.

    Arguments:
    location -- URL or file name to load
    destination -- destination file name to write to

    Returns: file name with contents
    Raises: KickstartError on error reading or writing'''

    if _is_url(location):
        contents = _load_url(location)

        # Write to file
        try:
            with open(destination, 'w') as fh:
                fh.write(contents)
        except IOError as e:
            raise KickstartError(_('Error writing file "%s":') % location + ': {e}'.format(e=str(e)))

        return destination
    else:
        _copy_file(location, destination)
        return destination

def _load_url(location):
    '''Load a location (URL or filename) and return contents as string'''

    try:
        request = requests.get(location, verify=SSL_VERIFY)
    except SSLError as e:
        raise KickstartError(_('Error securely accessing URL "%s"') % location + ': {e}'.format(e=str(e)))
    except RequestException as e:
        raise KickstartError(_('Error accessing URL "%s"') % location + ': {e}'.format(e=str(e)))

    if request.status_code != requests.codes.ok:        # pylint: disable=no-member
        raise KickstartError(_('Error accessing URL "%s"') % location + ': {c}'.format(c=str(request.status_code)))

    return request.text

def _load_file(filename):
    '''Load a file's contents and return them as a string'''

    try:
        if six.PY3:
            with open(filename, 'rb') as fh:
                contents = fh.read().decode("utf-8")
        else:
            with open(filename, 'r') as fh:
                contents = fh.read()
    except IOError as e:
        raise KickstartError(_('Error opening file: %s') % str(e))

    return contents

def _copy_file(filename, destination):
    '''Copy file to destination'''

    try:
        shutil.copyfile(filename, destination)
    except (OSError, IOError) as e:
        raise KickstartError(_('Error copying file: %s') % str(e))
