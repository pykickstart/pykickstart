#
# Radek Vykydal <rvykydal@redhat.com>
#
# Copyright 2018 Red Hat, Inc.
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

import warnings
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartValueError, formatErrorMsg
from pykickstart.options import KSOptionParser
from pykickstart.constants import NVDIMM_MODE_SECTOR, NVDIMM_ACTION_RECONFIGURE

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)


class RHEL7_NvdimmData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.action = kwargs.get("action", None)
        self.namespace = kwargs.get("namespace", "")
        self.mode = kwargs.get("mode", None)
        self.sectorsize = kwargs.get("sectorsize", None)

    def __eq__(self, y):
        if not y:
            return False
        return (self.action == y.action and
                self.namespace == y.namespace)

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = "%s" % self.action
        if self.action == NVDIMM_ACTION_RECONFIGURE:
            if self.namespace:
                retval += " --namespace=%s" % self.namespace
            if self.mode == NVDIMM_MODE_SECTOR:
                retval += " --mode=%s" % NVDIMM_MODE_SECTOR
                if self.sectorsize:
                    retval += " --sectorsize=%d" % self.sectorsize

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "nvdimm %s" % self._getArgsAsStr()
        return retval.strip() + "\n"


class RHEL7_Nvdimm(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=80, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)

        self.actionList = kwargs.get("actionList", [])
        self.validActions = [NVDIMM_ACTION_RECONFIGURE]
        self.validModes = [NVDIMM_MODE_SECTOR]

        self.op = self._getParser()

    def __str__(self):
        retval = ""

        for action in self.actionList:
            retval += action.__str__()

        if retval != "":
            retval = "# NVDIMM devices setup\n" + retval + "\n"

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--namespace", dest="namespace", required=True)
        op.add_option("--mode", choices=self.validModes, default=NVDIMM_MODE_SECTOR, dest="mode")
        op.add_option("--sectorsize", type=int)
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) > 1:
            message = _("Unexpected arguments to nvdimm command: %(arguments)s") % {"arguments": extra}
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=message))

        if not extra:
            message = _("Action argument is required for nvdimm command")
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=message))

        action = extra[0]

        if action not in self.validActions:
            message = _("Invalid action argument (choose from '%(valid_arguments)s')") \
                % {"valid_arguments": ",".join(self.validActions)}
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=message))

        nvdimm_data = self.handler.NvdimmData()
        self._setToObj(self.op, opts, nvdimm_data)
        nvdimm_data.lineno = self.lineno
        nvdimm_data.action = action

        # Check for duplicates in the data list.
        if nvdimm_data in self.dataList():
            warnings.warn(_("An action %(action)s on namespace %(namespace)s has already been defined.")
                          % {"action": action, "namespace": nvdimm_data.namespace})

        if action == NVDIMM_ACTION_RECONFIGURE and nvdimm_data.mode == NVDIMM_MODE_SECTOR \
                and not nvdimm_data.sectorsize:
            message = _("Action %(action)s with mode %(mode)s requires --sectorsize argument to be set") \
                      % {"action": action, "mode": nvdimm_data.mode}
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=message))

        return nvdimm_data

    def dataList(self):
        return self.actionList
