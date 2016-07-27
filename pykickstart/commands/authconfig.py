#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
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
from pykickstart.version import FC3
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class FC3_Authconfig(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.authconfig = kwargs.get("authconfig", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.authconfig:
            retval += "# System authorization information\nauth %s\n" % self.authconfig

        return retval

    def parse(self, args):
        self.authconfig = self.currentLine[len(self.currentCmd):].strip()
        return self

    def _getParser(self):
        op = KSOptionParser(prog="authconfig",  description="""
                            This required command sets up the authentication
                            options for the system. This is just a wrapper
                            around the authconfig program, so all options
                            recognized by that program are valid for this
                            command. See the manual page for authconfig for a
                            complete list.

                            By default, passwords are normally encrypted and
                            are not shadowed.""", version=FC3)
        op.add_argument("options", metavar="[options]", nargs=1, help="""
                        See ``man authconfig``.""", version=FC3)
        return op

