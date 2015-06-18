#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2012 Red Hat, Inc.
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
from pykickstart.version import FC3, F17, F21, F28
from pykickstart.base import KickstartCommand
from pykickstart.constants import CLEARPART_TYPE_ALL, CLEARPART_TYPE_LINUX, CLEARPART_TYPE_LIST, CLEARPART_TYPE_NONE
from pykickstart.options import KSOptionParser, commaSplit

class FC3_ClearPart(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=120, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.drives = kwargs.get("drives", [])
        self.initAll = kwargs.get("initAll", False)
        self.type = kwargs.get("type", None)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.type is None:
            return retval

        if self.type == CLEARPART_TYPE_NONE:
            clearstr = " --none"
        elif self.type == CLEARPART_TYPE_LINUX:
            clearstr = " --linux"
        elif self.type == CLEARPART_TYPE_ALL:
            clearstr = " --all"
        else:
            clearstr = ""

        if self.initAll:
            initstr = " --initlabel"
        else:
            initstr = ""

        if self.drives:
            drivestr = " --drives=" + ",".join(self.drives)
        else:
            drivestr = ""

        retval += "# Partition clearing information\nclearpart%s%s%s\n" % (clearstr, initstr, drivestr)
        return retval

    def _getParser(self):
        op = KSOptionParser(prog="clearpart", description="""
                            Removes partitions from the system, prior to creation
                            of new partitions. By default, no partitions are
                            removed.

                            If the clearpart command is used, then the ``--onpart``
                            command cannot be used on a logical partition.""",
                            version=FC3)
        op.add_argument("--all", dest="type", action="store_const",
                        const=CLEARPART_TYPE_ALL, version=FC3,
                        help="Erases all partitions from the system.")
        op.add_argument("--drives", type=commaSplit, help="""
                        Specifies which drives to clear partitions from. For
                        example, the following clears the partitions on the
                        first two drives on the primary IDE controller::

                        ``clearpart --all --drives=sda,sdb``""",
                        version=FC3)
        op.add_argument("--initlabel", dest="initAll", action="store_true",
                        default=False, version=FC3, help="""
                        Initializes the disk label to the default for your
                        architecture (for example msdos for x86 and gpt for
                        Itanium). This is only meaningful in combination with
                        the '--all' option.""")
        op.add_argument("--linux", dest="type", action="store_const",
                        const=CLEARPART_TYPE_LINUX, version=FC3,
                        help="Erases all Linux partitions.")
        op.add_argument("--none", dest="type", action="store_const",
                        const=CLEARPART_TYPE_NONE, version=FC3, help="""
                        Do not remove any partitions. This is the default""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

class F17_ClearPart(FC3_ClearPart):
    def __init__(self, *args, **kwargs):
        super(F17_ClearPart, self).__init__(*args, **kwargs)
        self.devices = kwargs.get("devices", [])

    def __str__(self):
        s = super(F17_ClearPart, self).__str__()
        if s and self.devices:
            s = s.rstrip()
            s += " --list=" + ",".join(self.devices)
            s += "\n"
        return s

    def _getParser(self):
        op = FC3_ClearPart._getParser(self)
        op.add_argument("--list", dest="devices", type=commaSplit,
                        version=F17, help="""
                        Specifies which partitions to clear. If given, this
                        supersedes any of the ``--all`` and ``--linux``
                        options. This can be across different drives::

                        ``clearpart --list=sda2,sda3,sdb1``""")
        return op

    def parse(self, args):
        obj = FC3_ClearPart.parse(self, args)
        if getattr(obj, "devices", []):
            obj.type = CLEARPART_TYPE_LIST

        return obj

class F21_ClearPart(F17_ClearPart):
    def __init__(self, *args, **kwargs):
        super(F21_ClearPart, self).__init__(*args, **kwargs)
        self.disklabel = kwargs.get("disklabel", "")

    def __str__(self):
        s = super(F21_ClearPart, self).__str__()
        if s and self.disklabel:
            s = s.rstrip()
            s += " --disklabel=%s\n" % self.disklabel
        return s

    def _getParser(self):
        op = F17_ClearPart._getParser(self)
        op.add_argument("--disklabel", default="", version=F21, help="""
                        Set the default disklabel to use. Only disklabels
                        supported for the platform will be accepted. eg. msdos
                        and gpt for x86_64 but not dasd.""")
        return op

class F28_ClearPart(F21_ClearPart):
    def __init__(self, *args, **kwargs):
        super(F28_ClearPart, self).__init__(*args, **kwargs)
        self.cdl = kwargs.get("cdl", False)

    def __str__(self):
        s = super(F28_ClearPart, self).__str__()
        if s and self.cdl:
            s = s.rstrip()
            s += " --cdl\n"
        return s

    def _getParser(self):
        op = super(F28_ClearPart, self)._getParser()
        op.add_argument("--cdl", dest="cdl", default=False, version=F28,
                        action="store_true", help="""
                        Reformat any LDL DASDs to CDL format.""")
        return op

class RHEL7_ClearPart(F28_ClearPart):
    pass
