# type stubs for pykickstart.base
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

from typing import Optional, Union, Any, List, Dict

from pykickstart.ko import KickstartObject
from pykickstart.parser import Script, Packages
from argparse import Namespace

class KickstartCommand(KickstartObject):
    # class attributes
    removedKeywords = ...       # type: List[str]
    removedAttrs = ...          # type: List[str]

    # instance attributes
    currentCmd = ...            # type: str
    currentLine = ...           # type: str
    handler = ...               # type: Optional[BaseHandler]
    lineno = ...                # type: int
    seen = ...                  # type: bool

    def __init__(self, writePriority: int, *args: Any, **kwargs: Any) -> None: ...

    def parse(self, args: List[str]) -> Optional[Union[BaseData, KickstartCommand]]: ...
    def dataList(self) -> List[BaseData]: ...

    @property
    def dataClass(self) -> Optional[BaseData]: ...

    def deleteRemovedAttrs(self) -> None: ...
    def set_to_self(self, namespace: Namespace) -> None: ...
    def set_to_obj(self, namespace: Namespace, obj: Any) -> None: ...

class BaseHandler(KickstartObject):
    # class attributes
    version = ...               # type: Optional[int]

    # instance attributes
    scripts = ...               # type: List[Script]
    packages = ...              # type: Packages
    platform = ...              # type: str
    commands = ...              # type: Dict[str, KickstartCommand]
    currentLine = ...           # type: str

    def __init__(self,
                 mapping: Dict[str, KickstartCommand] = None,
                 dataMapping: Dict[str, BaseData] = None,
                 commandUpdates: Dict[str, KickstartCommand] = None,
                 dataUpdates: Dict[str, BaseData] = None,
                 *args: Any,
                 **kargs: Any) -> None: ...

    def resetCommand(self, cmdName: str) -> None: ...
    def dispatcher(self, args: List[str], lineno: int) -> Optional[KickstartCommand]: ...
    def maskAllExcept(self, lst: List[str]) -> None: ...

class DeprecatedCommand(KickstartCommand):
    pass

class BaseData(KickstartObject):
    # class attributes
    removedKeywords = ...       # type: List[str]
    removedAttrs = ...          # type: List[str]

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def deleteRemovedAttrs(self) -> None: ...
