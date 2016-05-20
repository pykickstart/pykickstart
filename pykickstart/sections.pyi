# Type stubs of pykickstart.sections
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

from typing import Any, Dict, List, Union

from pykickstart.base import BaseHandler

class Section(object):
    # class attributes
    allLines = ...      # type: bool
    sectionOpen = ...   # type: str

    # instance attributes
    handler = ...       # type: BaseHandler
    version = ...       # type: int

    # class type
    dataObj = ...       # type: type

    def __init__(self, handler: BaseHandler, **kwargs: Any) -> None: ...
    def handleLine(self, line: str) -> None: ...
    def handleHeader(self, lineno: int, args: List[str]) -> None: ...

    @property
    def seen(self) -> bool: ...

# These don't change anything from their parent types
class NullSection(Section): ...
class ScriptSection(Section): ...
class PreScriptSection(ScriptSection): ...
class PreInstallScriptSection(ScriptSection): ...
class PostScriptSection(ScriptSection): ...
class OnErrorScriptSection(ScriptSection): ...
class TracebackScriptSection(OnErrorScriptSection): ...
class PackageSection(Section): ...
