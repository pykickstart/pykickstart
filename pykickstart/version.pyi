# type stubs for pykickstart.version
#
# David Shea <dshea@redhat.com>
#
# Copyright 2016 Red Hat, Inc.
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

from typing import Dict, Callable, Union

from pykickstart.base import BaseHandler

# Symbolic names for internal version numbers.
RHEL3 = ...     # type: int
FC3 = ...       # type: int
RHEL4 = ...     # type: int
FC4 = ...       # type: int
FC5 = ...       # type: int
FC6 = ...       # type: int
RHEL5 = ...     # type: int
F7  = ...       # type: int
F8 = ...        # type: int
F9 = ...        # type: int
F10 = ...       # type: int
F11 = ...       # type: int
F12 = ...       # type: int
F13 = ...       # type: int
RHEL6 = ...     # type: int
F14 = ...       # type: int
F15 = ...       # type: int
F16 = ...       # type: int
F17 = ...       # type: int
F18 = ...       # type: int
F19 = ...       # type: int
F20 = ...       # type: int
F21 = ...       # type: int
RHEL7 = ...     # type: int
F22 = ...       # type: int
F23 = ...       # type: int
F24 = ...       # type: int
F25 = ...       # type: int
F26 = ...       # type: int

DEVEL = F26     # type: int

versionMap = ...    # type: Dict[str, int]

def stringToVersion(s: str) -> int: ...
def versionToString(version: int, skipDevel: bool) -> str: ...
def versionToLongString(version: int) -> str: ...
def versionFromFile(f: str) -> int: ...

# The return type is the class type of a BaseHandler
def returnClassForVersion(version: Union[int, str]) -> Callable[[], BaseHandler]: ...

def makeVersion(version: int) -> BaseHandler: ...
