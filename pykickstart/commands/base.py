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
from pykickstart.errors import *
from pykickstart.parser import Packages

class KickstartCommand:
    """The base class for all kickstart commands.  This is an abstract class."""
    def __init__(self):
        """Create a new KickstartCommand instance.  Instance attributes:

           currentCmd -- The name of the command in the input file that caused
                         this handler to be run.
           lineno     -- The current line number in the input file.
        """

        # We don't want people using this class by itself.
        if self.__class__ is KickstartCommand:
            raise TypeError, "KickstartCommand is an abstract class."

        # These will be set by the dispatcher.
        self.currentCmd = ""
        self.lineno = 0

    def __call__(self, *args, **kwargs):
        """Set multiple attributes on a subclass of KickstartCommand at once
           via keyword arguments.  Valid attributes are anything specified in
           a subclass, but unknown attributes will be ignored.
        """
        for (key, val) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        return ""

    # Set the contents of the opts object (an instance of optparse.Values
    # returned by parse_args) as attributes on the KickstartCommand object.
    # It's useful to call this from KickstartCommand subclasses after parsing
    # the arguments.
    def _setToSelf(self, optParser, opts):
        for key in filter (lambda k: getattr(opts, k) != None, optParser.keys()):
            setattr(self, key, getattr(opts, key))

    # Sets the contents of the opts object (an instance of optparse.Values
    # returned by parse_args) as attributes on the provided object obj.  It's
    # useful to call this from KickstartCommand subclasses that handle lists
    # of objects (like partitions, network devices, etc.) and need to populate
    # a Data object.
    def _setToObj(self, optParser, opts, obj):
        for key in filter (lambda k: getattr(opts, k) != None, optParser.keys()):
            setattr(obj, key, getattr(opts, key))

class DeprecatedCommand(KickstartCommand):
    """Specify that a command is deprecated and no longer has any function.
       Any command that is deprecated should be subclassed from this class,
       only specifying an __init__ method that calls the superclass's __init__.
    """
    def __init__(self):
        """Create a new DeprecatedCommand instance."""
        KickstartCommand.__init__(self)

    def parse(self, args):
        """Print a warning message if the command is seen in the input file."""
        mapping = {"lineno": self.lineno, "cmd": self.currentCmd}
        warnings.warn(_("Ignoring deprecated command on line %(lineno)s:  The %(cmd)s command has been deprecated and no longer has any effect.  It may be removed from future releases, which will result in a fatal error from kickstart.  Please modify your kickstart file to remove this command.") % mapping, DeprecationWarning)

class BaseHandler:
    """Each version of kickstart syntax is provided by a subclass of this
       class.  These subclasses are what users will interact with for parsing,
       extracting data, and writing out kickstart files.  This is an abstract
       class.
    """
    def __init__(self):
        """Create a new BaseHandler instance.  Instance attributes:

           handlers -- A mapping from a string command to a KickstartCommand
                       subclass object that handles it.  Multiple strings can
                       map to the same object, but only one instance of the
                       handler object should ever exist.  Most users should
                       never have to deal with this directly, as it is
                       manipulated through registerHandler and dispatcher.
           scripts --  A list of pykickstart.parser.Script instances, which is
                       populated by KickstartParser.addScript and describes the
                       %pre/%post/%traceback script section of the input file.
           packages -- An instance of pykickstart.parser.Packages which
                       describes the packages section of the input file.
           platform -- A string describing the hardware platform, which is
                       needed only by system-config-kickstart.
        """

        # We don't want people using this class by itself.
        if self.__class__ is BaseHandler:
            raise TypeError, "BaseHandler is an abstract class."

        self.handlers = {}

        # This isn't really a good place for these, but it's better than
        # everything else I can think of.
        self.scripts = []
        self.packages = Packages()
        self.platform = ""

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        retval = ""

        if self.platform != "":
            retval += "#platform=%s" % self.platform

        # Have to use this slightly roundabout method because we can't iterate
        # over the handler keys.  That's because multiple handler keys can map
        # to the same command object due to aliased commands.
        for (name, obj) in self.__dict__.items():
            if name.startswith("Command"):
                retval += obj.__str__()

        for script in self.scripts:
            retval += script.__str__()

        retval += self.packages.__str__()

        return retval

    def registerHandler(self, cmdObj, cmdList):
        """Set up a mapping from each string command in cmdList to the instance
           of the KickstartCommand subclass object cmdObj.  Using a list of
           commands allows for aliasing commands to each other.  Also create a
           new attribute on this BaseHandler subclass named
           cmdObj.__class__.__name__ with a value of cmdObj.
           cmdObj.__class__.__name__ must begin with "Command".
        """

        for str in cmdList:
            self.handlers[str] = cmdObj

        # Add an attribute on this command object as well.  We need this for
        # the __str__ method to work correctly, as well as to provide a way
        # for subclasses to set values on command handlers via their __call__
        # methods.
        setattr(self, cmdObj.__class__.__name__, cmdObj)

    def dispatcher(self, cmd, cmdArgs, lineno):
        """Given the command string cmd and the list of arguments cmdArgs, call
           the appropriate KickstartCommand handler that has been previously
           registered.  lineno is needed for error reporting.  If cmd does not
           exist in the handlers dict, KickstartParseError will be raised.  A
           handler of None for the given command is not an error.
        """
        if not self.handlers.has_key(cmd):
            raise KickstartParseError, formatErrorMsg(lineno, msg=_("Unknown command: %s" % cmd))
        else:
            if self.handlers[cmd] != None:
                self.handlers[cmd].currentCmd = cmd
                self.handlers[cmd].lineno = lineno
                self.handlers[cmd].parse(cmdArgs)
