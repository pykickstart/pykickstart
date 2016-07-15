# type stubs for pykickstart.parser
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

from typing import Union, Optional, Any, List, Dict

from pykickstart.ko import KickstartObject
from pykickstart.base import BaseHandler, KickstartCommand, BaseData
from pykickstart.sections import Section

def preprocessFromStringToString(s: str) -> str: ...
def preprocessKickstartToString(f: str) -> str: ...
def preprocessFromString(s: str) -> str: ...
def preprocessKickstart(f: str) -> Optional[str]: ...

class Script(KickstartObject):
    # instance attributes
    script = ...        # type: str
    interp = ...        # type: str
    lineno = ...        # type: Optional[str]
    logfile = ...       # type: Optional[str]
    errorOnFail = ...   # type: bool
    typee = ...         # type: int

    def __init__(self, script: str, *args: Any, **kwargs: Any) -> None: ...

class Group(KickstartObject):
    # instance attributes
    name = ...          # type: str
    include = ...       # type: int

    def __init__(self, name: str = ..., include: int = ...) -> None: ...

class Packages(KickstartObject):
    # instance attributes
    addBase = ...           # type: bool
    nocore = ...            # type: bool
    default = ...           # type: bool
    environment = ...       # type: Optional[str]
    excludedList = ...      # type: List[str]
    exlucdedGroupList = ... # type: List[Group]
    excludeDocs = ...       # type: bool
    groupList = ...         # type: List[Group]
    handleMissing = ...     # type: int
    packageList = ...       # type: List[str]
    instLangs = ...         # type: Optional[List[str]]
    multiLib = ...          # type: bool
    excludeWeakdeps = ...   # type: bool
    seen = ...              # type: bool

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def add(self, pkgList: List[str]) -> None: ...

class KickstartParser(object):
    # instance attributes
    errorsAreFatal = ...        # type: bool
    followIncludes = ...        # type: bool
    handler = ...               # type: BaseHandler
    currentdir = ...            # type: Dict[int, str]
    missingIncludeIsFatal = ... # type: bool
    unknownSectionIsFatal = ... # type: bool
    version = ...               # type: int

    def __init__(self, handler: BaseHandler,
                 followIncludes: bool = ..., errorsAreFatal: bool = ...,
                 missingIncludeIsFatal: bool = ...,
                 unknownSectionIsFatal: bool = ...) -> None: ...

    def getSection(self, s: str) -> Section: ...
    def handleCommand(self, lineno: int, args: List[str]) -> Union[BaseData, KickstartCommand]: ...
    def registerSection(self, obj: Section) -> None: ...
    def readKickstartFromString(self, s: str, reset: bool = ...) -> None: ...
    def readKickstart(self, f: str, reset: bool = ...) -> None: ...
    def setupSections(self) -> None: ...
