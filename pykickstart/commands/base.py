#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

import warnings

# The base command class.  This holds all methods and data that are common to
# to every subclass - shouldn't be much stuff.
class KickstartCommand:
    def __init__(self):
        self.listeningFor = []

        # These will be set on the command object by the dispatcher.
        self.currentCmd = ""
        self.lineno = 0

    def __str__(self):
        return ""

    def _setToSelf(self, optParser, opts):
        for key in filter (lambda k: getattr(opts, k) != None, optParser.keys()):
            setattr(self, key, getattr(opts, key))

    def _setToObj(self, optParser, opts, obj):
        for key in filter (lambda k: getattr(opts, k) != None, optParser.keys()):
            setattr(obj, key, getattr(opts, key))

# Any command that is deprecated and no longer has any function should
# subclass from this.  Using any subclass will then cause a warning to be
# generated.
class DeprecatedCommand(KickstartCommand):
    def __init__(self):
        KickstartCommand.__init__(self)

    def parse(self, args):
        mapping = {"lineno": self.lineno, "cmd": self.currentCmd}
        warnings.warn(_("Ignoring deprecated command on line %(lineno)s:  The %(cmd)s command has been deprecated and no longer has any effect.  It may be removed from future releases, which will result in a fatal error from kickstart.  Please modify your kickstart file to remove this command.") % mapping, DeprecationWarning)

# The base Handler object, from which all version-specific handlers are
# derived.  A subclass of this object is what users will interact with for
# parsing, extracting data, and writing out kickstart files.
class BaseHandler:
    def __init__(self):
        self.handlers = {}

    # Writing out the command section of the kickstart file is easy.
    def __str__(self):
        retval = ""

        # Have to use this slightly roundabout method because we can't iterate
        # over the handler keys.  That's because multiple handler keys can map
        # to the same command object due to aliased commands.
        for (key, val) in self.__dict__.items():
            if key.startswith("_cmd_"):
                retval += val.__str__()

        return retval

    def _registerHandler(self, cmdObj, cmdList):
        # Convert the object's class name into a string that we can use as an
        # attribute to add.
        if cmdObj.__class__.__name__.startswith("Command"):
            cmdName = "_cmd_" + cmdObj.__class__.__name__[7:].lower()
        else:
            cmdName = "_cmd_" + cmdObj.__class__.__name__.lower()

        # Set up a mapping from each command string to an object that
        # handles it.  Multiple strings can map to the same instance
        # of an object.
        for str in cmdList:
            self.handlers[str] = cmdObj

        # Add an attribute on this handler object as well to control
        # access to this object.
        setattr(self, cmdName, cmdObj)

    # Called by the parser to handle an individual command.  This mainly exists
    # to internalize understanding of how the handler object is laid out and to
    # set currentCmd and lineno in a single place.
    def dispatcher(self, cmd, cmdArgs, lineno):
        if not self.handlers.has_key(cmd):
            raise KickstartParseError, formatErrorMsg(lineno, msg=_("Unknown command: %s" % cmd))
        else:
            if self.handlers[cmd] != None:
                self.handlers[cmd].currentCmd = cmd
                self.handlers[cmd].lineno = lineno
                self.handlers[cmd].parse(cmdArgs)
