#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008 Red Hat, Inc.
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
from pykickstart.version import FC3, FC6, F10, versionToLongString
from pykickstart.base import DeprecatedCommand, KickstartCommand
from pykickstart.options import KSOptionParser

class FC3_Monitor(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.hsync = kwargs.get("hsync", "")
        self.monitor = kwargs.get("monitor", "")
        self.vsync = kwargs.get("vsync", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.hsync:
            retval += " --hsync=%s" % self.hsync
        if self.monitor:
            retval += " --monitor=\"%s\"" % self.monitor
        if self.vsync:
            retval += " --vsync=%s" % self.vsync

        if retval:
            retval = "monitor%s\n" % retval

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="monitor", description="""
                            If the monitor command is not given, anaconda will
                            use X to automatically detect your monitor settings.
                            Please try this before manually configuring your
                            monitor.""", version=FC3)
        op.add_argument("--hsync", version=FC3, help="""
                        Specifies the horizontal sync frequency of the monitor.
                        """)
        op.add_argument("--monitor", version=FC3, help="""
                        Use specified monitor; monitor name should be from the
                        list of monitors in ``/usr/share/hwdata/MonitorsDB`` from
                        the hwdata package. The list of monitors can also be
                        found on the X Configuration screen of the
                        Kickstart Configurator. This is ignored if ``--hsync`` or
                        ``--vsync`` is provided. If no monitor information is
                        provided, the installation program tries to probe for
                        it automatically.""")
        op.add_argument("--vsync", version=FC3, help="""
                        Specifies the vertical sync frequency of the monitor.
                        """)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

class FC6_Monitor(FC3_Monitor):
    removedKeywords = FC3_Monitor.removedKeywords
    removedAttrs = FC3_Monitor.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_Monitor.__init__(self, writePriority, *args, **kwargs)
        self.probe = kwargs.get("probe", True)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.hsync:
            retval += " --hsync=%s" % self.hsync
        if self.monitor:
            retval += " --monitor=\"%s\"" % self.monitor
        if not self.probe:
            retval += " --noprobe"
        if self.vsync:
            retval += " --vsync=%s" % self.vsync

        if retval:
            retval = "monitor%s\n" % retval

        return retval

    def _getParser(self):
        op = FC3_Monitor._getParser(self)
        op.add_argument("--noprobe", dest="probe", action="store_false",
                        default=True, version=FC6, help="""
                        Do not probe the monitor.""")
        return op

class F10_Monitor(DeprecatedCommand, FC6_Monitor):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = FC6_Monitor._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(F10)
        return op
