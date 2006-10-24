#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
import warnings
from copy import copy
from optparse import *

from constants import *
from data import *
from errors import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

# Specialized OptionParser, mainly to handle the MappableOption and to turn
# off help.
class KSOptionParser(OptionParser):
    def exit(self, status=0, msg=None):
        pass

    def error(self, msg):
        if self.lineno != None:
            raise KickstartParseError, formatErrorMsg(self.lineno, msg=msg)
        else:
            raise KickstartParseError, msg

    def keys(self):
        retval = []

        for opt in self.option_list:
            if opt not in retval:
                retval.append(opt.dest)

        return retval

    def _init_parsing_state (self):
        OptionParser._init_parsing_state(self)
        self.option_seen = {}

    def check_values (self, values, args):
        for option in self.option_list:
            if (isinstance(option, Option) and option.required and \
               not self.option_seen.has_key(option)):
                raise KickstartValueError, formatErrorMsg(self.lineno, _("Option %s is required") % option)
            elif isinstance(option, Option) and option.deprecated and \
                 self.option_seen.has_key(option):
                warnings.warn(_("Ignoring deprecated option on line %s:  The %s option has been deprecated and no longer has any effect.  It may be removed from future releases, which will result in a fatal error from kickstart.  Please modify your kickstart file to remove this option.") % (self.lineno, option), DeprecationWarning)

        return (values, args)

    def __init__(self, map={}, lineno=None):
        self.map = map
        self.lineno = lineno
        OptionParser.__init__(self, option_class=KSOption,
                              add_help_option=False)

# Creates a new Option class that supports two new attributes:
# - required:  any option with this attribute must be supplied or an exception
#              is thrown
# - deprecated:  any option with this attribute will cause a DeprecationWarning
#                to be thrown if the option is used
# Also creates a new type:
# - ksboolean:  support various kinds of boolean values on an option
# And two new actions:
# - map :  allows you to define an opt -> val mapping such that dest gets val
#          when opt is seen
# - map_extend:  allows you to define an opt -> [val1, ... valn] mapping such
#                that dest gets a list of vals built up when opt is seen
class KSOption (Option):
    ATTRS = Option.ATTRS + ['deprecated', 'required']
    ACTIONS = Option.ACTIONS + ("map", "map_extend",)
    STORE_ACTIONS = Option.STORE_ACTIONS + ("map", "map_extend",)
    
    TYPES = Option.TYPES + ("ksboolean",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)

    def _check_required(self):
        if self.required and not self.takes_value():
            raise OptionError(_("Required flag set for option that doesn't take a value"), self)

    def _check_ksboolean(option, opt, value):
        if value.lower() in ("on", "yes", "true", "1"):
            return True
        elif value.lower() in ("off", "no", "false", "0"):
            return False
        else:
            raise OptionValueError(_("Option %s: invalid boolean value: %r") % (opt, value))

    # Make sure _check_required() is called from the constructor!
    CHECK_METHODS = Option.CHECK_METHODS + [_check_required]
    TYPE_CHECKER["ksboolean"] = _check_ksboolean

    def process (self, opt, value, values, parser):
        Option.process(self, opt, value, values, parser)
        parser.option_seen[self] = 1

    # Override default take_action method to handle our custom actions.
    def take_action(self, action, dest, opt, value, values, parser):
        if action == "map":
            values.ensure_value(dest, parser.map[opt.lstrip('-')])
        elif action == "map_extend":
            values.ensure_value(dest, []).extend(parser.map[opt.lstrip('-')])
        else:
            Option.take_action(self, action, dest, opt, value, values, parser)
