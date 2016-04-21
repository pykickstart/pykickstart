#!/usr/bin/python
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005-2014 Red Hat, Inc.
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

# pylint: disable=broad-except,found-_-in-module-class

import argparse
import os
import sys
import warnings
import tempfile
import shutil
from pykickstart.i18n import _
from pykickstart.errors import KickstartError, KickstartParseError, KickstartVersionError
from pykickstart.load import load_to_file
from pykickstart.parser import KickstartParser, preprocessKickstart
from pykickstart.version import DEVEL, makeVersion, versionMap

def cleanup(dest, fn=None, exitval=1):
    shutil.rmtree(dest)

    # Don't care if this file doesn't exist.
    if fn is not None:
        try:
            os.remove(fn)
        except Exception:
            pass

    sys.exit(exitval)

op = argparse.ArgumentParser(usage="%(prog)s [options] ksfile")
op.add_argument("ksfile", nargs="?",
                help=_("filename or URL to read from"))
op.add_argument("-e", "--firsterror", dest="firsterror", action="store_true",
                default=False, help=_("halt after the first error or warning"))
op.add_argument("-i", "--followincludes", dest="followincludes",
                action="store_true", default=False,
                help=_("parse include files when %%include is seen"))
op.add_argument("-l", "--listversions", dest="listversions", action="store_true",
                default=False,
                help=_("list the available versions of kickstart syntax"))
op.add_argument("-v", "--version", dest="version", default=DEVEL,
                help=_("version of kickstart syntax to validate against"))

opts = op.parse_args(sys.argv[1:])

if opts.listversions:
    for key in sorted(versionMap.keys()):
        print(key)

    sys.exit(1)

if not opts.ksfile:
    op.print_usage()
    sys.exit(1)

destdir = tempfile.mkdtemp("", "ksvalidator-tmp-", "/tmp")
try:
    f = load_to_file(opts.ksfile, "%s/ks.cfg" % destdir)
except KickstartError as e:
    print(_("Error reading %(filename)s:\n%(version)s") % {"filename": opts.ksfile, "version": e})
    cleanup(destdir)

try:
    handler = makeVersion(opts.version)
except KickstartVersionError:
    print(_("The version %s is not supported by pykickstart") % opts.version)
    cleanup(destdir)

ksparser = KickstartParser(handler, followIncludes=opts.followincludes,
                           errorsAreFatal=opts.firsterror)

# turn DeprecationWarnings into errors
warnings.filterwarnings("error")

processedFile = None

try:
    processedFile = preprocessKickstart(f)
    ksparser.readKickstart(processedFile)
    cleanup(destdir, processedFile, exitval=0)
except DeprecationWarning as msg:
    print(_("File uses a deprecated option or command.\n%s") % msg)
    cleanup(destdir, processedFile)
except KickstartParseError as msg:
    print(msg)
    cleanup(destdir, processedFile)
except KickstartError:
    print(_("General kickstart error in input file"))
    cleanup(destdir, processedFile)
except Exception as e:
    print(_("General error in input file:  %s") % e)
    cleanup(destdir, processedFile)
