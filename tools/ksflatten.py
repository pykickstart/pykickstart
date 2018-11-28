#!/usr/bin/env python3
#
# Simple script to take a kickstart config, read it in, parse any %includes,
# etc to write out a flattened config that is stand-alone
#
# Copyright 2007-2014, Red Hat, Inc.
# Jeremy Katz <katzj@redhat.com>
# Chris Lumens <clumens@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from __future__ import print_function

import sys
import argparse
import pykickstart
import pykickstart.parser
from pykickstart.i18n import _
from pykickstart.version import DEVEL, makeVersion
from pykickstart.errors import KickstartVersionError

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="kscfg", required=True,
                        help=_("Path to kickstart config file"))
    parser.add_argument("-v", "--version", dest="version", default=DEVEL,
                        help=_("Kickstart version to use for interpreting config"))
    parser.add_argument("-o", "--output", dest="output",
                        help=_("Write flattened config to OUTPUT"))

    return parser.parse_args(argv)

def main(argv=sys.argv[1:]):
    opts = parse_args(argv)
    if not opts.kscfg:
        return (1, _("Need to specify a config to flatten"))

    try:
        ksversion = makeVersion(opts.version)
    except KickstartVersionError:
        print(_("The version %s is not supported by pykickstart") % opts.version)
        sys.exit(1)

    ksparser = pykickstart.parser.KickstartParser(ksversion)
    try:
        ksparser.readKickstart(opts.kscfg)
    except IOError as msg:
        return (1, _("Failed to read kickstart file '%(filename)s' : %(error_msg)s") % {"filename": opts.kscfg, "error_msg": msg})
    except pykickstart.errors.KickstartError as e:
        return (1, _("Failed to parse kickstart file '%(filename)s' : %(error_msg)s") % {"filename": opts.kscfg, "error_msg": e})

    if opts.output:
        try:
            f = open(opts.output, 'w')
        except IOError as msg:
            return (1, _("Failed to open output file '%(filename)s' : %(error_msg)s") % {"filename": opts.output, "error_msg": msg})
    else:
        f = sys.stdout

    f.write("%s" % ksparser.handler)

    if opts.output:
        f.close()

    return (0, '')

if __name__ == "__main__":
    retval, msg = main()
    if msg:
        print(msg, file=sys.stderr)
    sys.exit(retval)
