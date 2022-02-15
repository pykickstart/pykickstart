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

# Disable found-_-in-module-class
# pylint: disable=W9902

import argparse
import os
import sys
import warnings
import tempfile
import shutil
import glob
from pykickstart.i18n import _
from pykickstart.errors import KickstartError, KickstartParseError, KickstartVersionError,\
    KickstartParseWarning, KickstartDeprecationWarning
from pykickstart.load import is_url, load_to_file
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
    op = argparse.ArgumentParser(usage="%(prog)s [options] ksfile [ksfile...]", add_help=False)
    op.add_argument("ksfile", nargs="*",
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

    rc = 0
    retmsg = []

    # unpack any globs
    ksfiles = []
    for inksfile in opts.ksfile:
        if is_url(inksfile):
            ksfiles.append(inksfile)
        else:
            ksfiles.extend(glob.glob(inksfile))

    # check if there are any files to check
    if not ksfiles:
        return (1, ["No files match the patterns."])

    # iterate over files to check them
    with tempfile.TemporaryDirectory(prefix="ksvalidator-tmp-") as destdir:
        for ksfile in ksfiles:
            print(_("\nChecking kickstart file %(filename)s\n") % {"filename": ksfile})

            try:
                f = load_to_file(ksfile, os.path.join(destdir, "ks.cfg"))
            except KickstartError as e:
                rc += 1
                retmsg.append(_("Error reading %(filename)s:\n%(version)s") % {"filename": ksfile, "version": e})

            try:
                handler = makeVersion(opts.version)
            except KickstartVersionError:
                # return immediately because bad version is fatal for all files
                return (1, [_("The version %s is not supported by pykickstart") % opts.version])

            # turn kickstart parse warnings into errors
            warnings.filterwarnings(action="error", category=KickstartParseWarning)

            ksparser = KickstartParser(handler, followIncludes=opts.followincludes,
                                       errorsAreFatal=opts.firsterror)

            try:
                processedFile = preprocessKickstart(f)
                if processedFile is None:
                    raise RuntimeError("Empty file")
                ksparser.readKickstart(processedFile)
                rc += ksparser.errorsCount
            except KickstartDeprecationWarning as err:
                rc += 1
                retmsg.append(_("File uses a deprecated option or command.\n%s") % err)
            except KickstartParseError as err:
                rc += 1
                retmsg.append(str(err))
            except KickstartError:
                rc += 1
                retmsg.append(_("General kickstart error in input file"))
            except Exception as e:        # pylint: disable=broad-except
                rc += 1
                retmsg.append(_("General error in input file:  %s") % e)

    return rc, retmsg


if __name__ == "__main__":
    retval, messages = main(sys.argv[1:])
    for msg in messages:
        print(msg)
    sys.exit(retval)
