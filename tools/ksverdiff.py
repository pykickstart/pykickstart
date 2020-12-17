#!/usr/bin/env python3
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2009-2014 Red Hat, Inc.
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

# Disable found-_-in-module-class
# pylint: disable=W9902

import argparse
import sys
from pykickstart.i18n import _
from pykickstart.base import DeprecatedCommand, RemovedCommand
from pykickstart.errors import KickstartVersionError
from pykickstart.version import makeVersion, versionMap

def getCommandSet(handler):
    return set(handler.commands.keys())

def getOptSet(lst):
    return set(map(lambda o: o.option_strings[0] if o.option_strings else '', lst))

def printList(lst):
    print(' '.join(lst))
    if lst:
        print()

def main(argv=None):
    op = argparse.ArgumentParser()
    op.add_argument("-f", "--from", dest="f")
    op.add_argument("-t", "--to", dest="t")
    op.add_argument("-l", "--listversions", dest="listversions", action="store_true",
                    default=False,
                    help=_("list the available versions of kickstart syntax"))

    opts = op.parse_args(argv)

    if opts.listversions:
        for key in sorted(versionMap.keys()):
            print(key)
        return 0

    if not opts.f or not opts.t:
        print(_("You must specify two syntax versions."))
        return 1

    try:
        fromHandler = makeVersion(opts.f)
        toHandler = makeVersion(opts.t)
    except KickstartVersionError as exn:
        print(_("The version %s is not supported by pykickstart") % exn)
        return 1

    fromCmdSet = getCommandSet(fromHandler)
    toCmdSet = getCommandSet(toHandler)
    bothSet = fromCmdSet & toCmdSet

    print(_("The following commands were removed in %s:") % opts.t)
    removed = [cmd for cmd in bothSet if
               isinstance(toHandler.commands[cmd], RemovedCommand) and
               not isinstance(fromHandler.commands[cmd], RemovedCommand)]
    printList(sorted(removed + list(fromCmdSet - toCmdSet)))

    print(_("The following commands were deprecated in %s:") % opts.t)
    printList(sorted([cmd for cmd in bothSet if
                      isinstance(toHandler.commands[cmd], DeprecatedCommand) and
                      not isinstance(toHandler.commands[cmd], RemovedCommand)]))

    print(_("The following commands were added in %s:") % opts.t)
    printList(sorted(toCmdSet - fromCmdSet))

    for cmd in sorted(bothSet):
        newOptList = []
        deprecatedOptList = []
        removedOptList = []

        fromCmd = fromHandler.commands[cmd]
        toCmd = toHandler.commands[cmd]

        if not hasattr(fromCmd, "op") or not hasattr(toCmd, "op"):
            continue

        fromOpt = fromCmd.op._actions
        toOpt = toCmd.op._actions

        newOptList = getOptSet(toOpt) - getOptSet(fromOpt)
        removedOptList = getOptSet(fromOpt) - getOptSet(toOpt)
        deprecatedOptList = getOptSet([cmd for cmd in toOpt if cmd.deprecated])

        if len(newOptList) > 0:
            print(_("The following options were added to the %(command_name)s command in %(version)s:") % {"command_name": cmd, "version": opts.t})
            printList(sorted(newOptList))

        if len(deprecatedOptList) > 0:
            print(_("The following options were deprecated from the %(command_name)s command in %(version)s:") % {"command_name": cmd, "version": opts.t})
            printList(sorted(deprecatedOptList))

        if len(removedOptList) > 0:
            print(_("The following options were removed from the %(command_name)s command in %(version)s:") % {"command_name": cmd, "version": opts.t})
            printList(sorted(removedOptList))

    return 0

if __name__ == "__main__":
    sys.exit(main())
