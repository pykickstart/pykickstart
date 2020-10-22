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
from pykickstart.version import FC3, F34, versionToLongString
from pykickstart.base import KickstartCommand, DeprecatedCommand
from pykickstart.options import KSOptionParser

class FC3_AutoStep(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.autostep = kwargs.get("autostep", False)
        self.autoscreenshot = kwargs.get("autoscreenshot", False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.autostep:
            if self.autoscreenshot:
                retval += "autostep --autoscreenshot\n"
            else:
                retval += "autostep\n"

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="autostep", description="""
                            Kickstart installs normally skip unnecessary screens.
                            This makes the installer step through every screen,
                            displaying each briefly.

                            This is mostly used for debugging.""",
                            version=FC3)
        op.add_argument("--autoscreenshot", action="store_true", default=False,
                        version=FC3, help="""
                        Take a screenshot at every step during installation and
                        copy the images over to ``/root/anaconda-screenshots`` after
                        installation is complete. This is most useful for
                        documentation.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        self.autostep = True
        return self

class F34_AutoStep(DeprecatedCommand, FC3_AutoStep):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = FC3_AutoStep._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(F34)
        return op
