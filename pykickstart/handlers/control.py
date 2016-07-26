#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007-2014 Red Hat, Inc.
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
__all__ = ["commandMap", "dataMap"]

import os
import sys
import importlib

commandMap = {}
dataMap = {}

if not commandMap:
    _path = os.path.dirname(__file__)
    if not _path in sys.path:
        sys.path.append(_path)

    for name in os.listdir(os.path.dirname(__file__)):
        if not (name.startswith("fc") or name.startswith("f") or name.startswith("rhel")):
            continue

        if not name.endswith(".py"):
            continue

        obj = importlib.import_module(name.replace(".py", ""))
        if not obj.__all__ or not obj.__all__[0].endswith("Handler"):
            continue

        # Now we've got a WhateverHandler module in obj.  This module should
        # export one class named WhateverHandler, which we can get at indirectly
        # through __all__, like so:
        handler = obj.__dict__[obj.__all__[0]]
        commandMap[handler.version] = handler.commandMap
        dataMap[handler.version] = handler.dataMap
