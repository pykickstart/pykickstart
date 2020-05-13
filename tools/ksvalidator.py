#!/usr/bin/env python3
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
from pykickstart.errors import KickstartError, KickstartParseError, KickstartVersionError,\
    KickstartParseWarning, KickstartDeprecationWarning
from pykickstart.load import load_to_file
from pykickstart.parser import KickstartParser, preprocessKickstart
from pykickstart.version import DEVEL, makeVersion, versionMap

def cleanup(dest, fn=None, exitval=1):
    shutil.rmtree(dest)

    # Don't care if this file doesn't exist.
    if fn is not None:
        try:
            os.remove(fn)
        except FileNotFoundError:
            pass

    return exitval

def main(argv):
    op = argparse.ArgumentParser(usage="%(prog)s [options] ksfile", add_help=False)
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
    op.add_argument("-h", "--help", dest="help", action="store_true", default=False,
                    help=_("show this help message and exit"))

    opts = op.parse_args(argv)

    # parse --help manually b/c we don't want to sys.exit before the
    # tests have finished
    if opts.help:
        return (0, op.format_help().split("\n"))

    if opts.listversions:
        versions = []
        for key in sorted(versionMap.keys()):
            versions.append(key)
        return (0, versions)

    if not opts.ksfile:
        return (1, op.format_usage().split("\n"))

    destdir = tempfile.mkdtemp("", "ksvalidator-tmp-", "/tmp")
    try:
        f = load_to_file(opts.ksfile, "%s/ks.cfg" % destdir)
    except KickstartError as e:
        return (cleanup(destdir),
                [_("Error reading %(filename)s:\n%(version)s") % {"filename": opts.ksfile, "version": e}])

    try:
        handler = makeVersion(opts.version)
    except KickstartVersionError:
        return (cleanup(destdir),
                [_("The version %s is not supported by pykickstart") % opts.version])

    ksparser = KickstartParser(handler, followIncludes=opts.followincludes,
                               errorsAreFatal=opts.firsterror)

    # turn kickstart parse warnings into errors
    warnings.filterwarnings(action="error", category=KickstartParseWarning)

    processedFile = None

    try:
        processedFile = preprocessKickstart(f)
        ksparser.readKickstart(processedFile)
        return (cleanup(destdir, processedFile, exitval=ksparser.errorsCount), [])
    except KickstartDeprecationWarning as err:
        return (cleanup(destdir, processedFile),
                [_("File uses a deprecated option or command.\n%s") % err])
    except KickstartParseError as err:
        return (cleanup(destdir, processedFile), [str(err)])
    except KickstartError:
        return (cleanup(destdir, processedFile),
                [_("General kickstart error in input file")])
    except Exception as e:                                      # pylint: disable=broad-except
        return (cleanup(destdir, processedFile),
                [_("General error in input file:  %s") % e])

if __name__ == "__main__":
    retval, messages = main(sys.argv[1:])
    for msg in messages:
        print(msg)
    sys.exit(retval)
