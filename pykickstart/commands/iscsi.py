#
# Chris Lumens <clumens@redhat.com>
# Peter Jones <pjones@redhat.com>
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
from pykickstart.version import FC6, F10, RHEL6, F17, versionToLongString
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.options import KSOptionParser

class FC6_IscsiData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.ipaddr = kwargs.get("ipaddr", "")
        self.port = kwargs.get("port", 3260)
        self.target = kwargs.get("target", "")
        self.user = kwargs.get("user", None)
        self.password = kwargs.get("password", None)

    def _getArgsAsStr(self):
        retval = ""

        if self.target:
            retval += " --target=%s" % self.target
        if self.ipaddr:
            retval += " --ipaddr=%s" % self.ipaddr
        if self.port != 3260:
            retval += " --port=%s" % self.port
        if self.user:
            retval += " --user=%s" % self.user
        if self.password:
            retval += " --password=%s" % self.password

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "iscsi%s\n" % self._getArgsAsStr()
        return retval

class F10_IscsiData(FC6_IscsiData):
    removedKeywords = FC6_IscsiData.removedKeywords
    removedAttrs = FC6_IscsiData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC6_IscsiData.__init__(self, *args, **kwargs)
        self.user_in = kwargs.get("user_in", None)
        self.password_in = kwargs.get("password_in", None)

    def _getArgsAsStr(self):
        retval = FC6_IscsiData._getArgsAsStr(self)

        if self.user_in:
            retval += " --reverse-user=%s" % self.user_in
        if self.password_in:
            retval += " --reverse-password=%s" % self.password_in

        return retval

class RHEL6_IscsiData(F10_IscsiData):
    removedKeywords = F10_IscsiData.removedKeywords
    removedAttrs = F10_IscsiData.removedAttrs

    def __init__(self, *args, **kwargs):
        F10_IscsiData.__init__(self, *args, **kwargs)
        self.iface = kwargs.get("iface", None)

    def _getArgsAsStr(self):
        retval = F10_IscsiData._getArgsAsStr(self)

        if self.iface:
            retval += " --iface=%s" % self.iface

        return retval

class F17_IscsiData(RHEL6_IscsiData):
    pass

class FC6_Iscsi(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=71, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.iscsi = kwargs.get("iscsi", [])

    def __str__(self):
        retval = ""
        for iscsi in self.iscsi:
            retval += iscsi.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="iscsi", description="""
                            Specifies additional iSCSI storage to be attached
                            during installation. If you use the iscsi parameter,
                            you must also assign a name to the iSCSI node, using
                            the iscsiname parameter. The iscsiname parameter
                            must appear before the iscsi parameter in the
                            kickstart file.

                            We recommend that wherever possible you configure
                            iSCSI storage in the system BIOS or firmware (iBFT
                            for Intel systems) rather than use the iscsi
                            parameter. Anaconda automatically detects and uses
                            disks configured in BIOS or firmware and no special
                            configuration is necessary in the kickstart file.

                            If you must use the iscsi parameter, ensure that
                            networking is activated at the beginning of the
                            installation, and that the iscsi parameter appears
                            in the kickstart file before you refer to iSCSI
                            disks with parameters such as clearpart or
                            ignoredisk.""",
                            version=FC6)
        op.add_argument("--target", help="The target iqn.", version=FC6)
        op.add_argument("--ipaddr", required=True, version=FC6, help="""
                        The IP address of the target to connect to.""")
        op.add_argument("--port", version=FC6, type=int, help="""
                        The port number to connect to (default, --port=3260).
                        """)
        op.add_argument("--user", version=FC6, help="""
                        The username required to authenticate with the target.
                        """)
        op.add_argument("--password", version=FC6, help="""
                        The password that corresponds with the username specified
                        for the target.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        dd = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, dd)
        dd.lineno = self.lineno
        return dd

    def dataList(self):
        return self.iscsi

    @property
    def dataClass(self):
        return self.handler.IscsiData

class F10_Iscsi(FC6_Iscsi):
    removedKeywords = FC6_Iscsi.removedKeywords
    removedAttrs = FC6_Iscsi.removedAttrs

    def _getParser(self):
        op = FC6_Iscsi._getParser(self)
        op.add_argument("--reverse-user", dest="user_in", version=F10, help="""
                        The username required to authenticate with the initiator
                        from a target that uses reverse CHAP authentication.""")
        op.add_argument("--reverse-password", dest="password_in",
                        version=F10, help="""
                        The password that corresponds with the username
                        specified for the initiator.""")
        return op

class RHEL6_Iscsi(F10_Iscsi):
    removedKeywords = F10_Iscsi.removedKeywords
    removedAttrs = F10_Iscsi.removedAttrs

    def _getParser(self):
        op = F10_Iscsi._getParser(self)
        op.add_argument("--iface", version=RHEL6, help="""
                        Bind connection to specific network interface instead
                        of using the default one determined by network layer.
                        Once used, it must be specified for all iscsi commands.
                        """)
        return op

class F17_Iscsi(RHEL6_Iscsi):
    def _getParser(self):
        op = super(F17_Iscsi, self)._getParser()
        for action in op._actions:
            # mark the fact that --iface is available since F17
            # while RHEL6 is based on F12
            if '--iface' in action.option_strings:
                action.help = action.help.replace(
                                versionToLongString(RHEL6),
                                versionToLongString(F17)
                            )

        return op
