#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2006, 2007, 2008, 2012 Red Hat, Inc.
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
"""
Base classes for creating commands and syntax version object.

This module exports several important base classes:

    BaseData - The base abstract class for all data objects.  Data objects
               are contained within a BaseHandler object.

    BaseHandler - The base abstract class from which versioned kickstart
                  handler are derived.  Subclasses of BaseHandler hold
                  BaseData and KickstartCommand objects.

    DeprecatedCommand - An abstract subclass of KickstartCommand that should
                        be further subclassed by users of this module.  When
                        a subclass is used, a warning message will be
                        printed.

    KickstartCommand - The base abstract class for all kickstart commands.
                       Command objects are contained within a BaseHandler
                       object.
"""
from pykickstart.i18n import _

import six
import warnings
from pykickstart import __version__
from pykickstart.errors import KickstartParseError, KickstartParseWarning, KickstartDeprecationWarning
from pykickstart.ko import KickstartObject
from pykickstart.version import versionToString
from pykickstart.parser import Packages

###
### COMMANDS
###
class KickstartCommand(KickstartObject):
    """The base class for all kickstart commands.  This is an abstract class."""
    removedKeywords = []
    removedAttrs = []

    def __init__(self, writePriority=0, *args, **kwargs):
        """Create a new KickstartCommand instance.  This method must be
           provided by all subclasses, but subclasses must call
           KickstartCommand.__init__ first.  Instance attributes:

           currentCmd    -- The name of the command in the input file that
                            caused this handler to be run.
           currentLine   -- The current unprocessed line from the input file
                            that caused this handler to be run.
           handler       -- A reference to the BaseHandler subclass this
                            command is contained withing.  This is needed to
                            allow referencing of Data objects.
           lineno        -- The current line number in the input file.
           seen          -- If this command was ever used in the kickstart file,
                            this attribute will be set to True.  This allows
                            for differentiating commands that were omitted
                            from those that default to unset.
           writePriority -- An integer specifying when this command should be
                            printed when iterating over all commands' __str__
                            methods.  The higher the number, the later this
                            command will be written.  All commands with the
                            same priority will be written alphabetically.
        """

        # We don't want people using this class by itself.
        if self.__class__ is KickstartCommand:
            raise TypeError("KickstartCommand is an abstract class.")

        KickstartObject.__init__(self, *args, **kwargs)

        self.writePriority = writePriority

        # These will be set by the dispatcher.
        self.currentCmd = ""
        self.currentLine = ""
        self.handler = None
        self.lineno = 0
        self.seen = False

        # If a subclass provides a removedKeywords list, warn if the user
        # continues to use some of the removed keywords
        for arg in (kw for kw in self.removedKeywords if kw in kwargs):
            warnings.warn("The '%s' keyword has been removed." % arg, KickstartParseWarning, stacklevel=2)

    def __call__(self, *args, **kwargs):
        """Set multiple attributes on a subclass of KickstartCommand at once
           via keyword arguments.  Valid attributes are anything specified in
           a subclass, but unknown attributes will be ignored.
        """
        self.seen = True

        for (key, val) in list(kwargs.items()):
            # Ignore setting attributes that were removed in a subclass, as
            # if they were unknown attributes.
            if key in self.removedAttrs:
                continue

            if hasattr(self, key):
                setattr(self, key, val)

    def __str__(self):
        """Return a string formatted for output to a kickstart file.  This
           method must be provided by all subclasses.
        """
        return KickstartObject.__str__(self)

    # pylint: disable=unused-argument
    def parse(self, args):
        """Parse the list of args and set data on the KickstartCommand object.
           This method must be provided by all subclasses.
        """
        raise TypeError("parse() not implemented for KickstartCommand")
    # pylint: enable=unused-argument

    def dataList(self):
        """For commands that can occur multiple times in a single kickstart
           file (like network, part, etc.), return the list that we should
           append more data objects to.
        """
        return None

    @property
    def dataClass(self):
        """For commands that can occur multiple times in a single kickstart
           file, return the class that should be used to store the data from
           each invocation.  An instance of this class will be appended to
           dataList.  For all other commands, return None.
        """
        return None

    def deleteRemovedAttrs(self):
        """Remove all attributes from self that are given in the removedAttrs
           list.  This method should be called from __init__ in a subclass,
           but only after the superclass's __init__ method has been called.
        """
        for attr in [k for k in self.removedAttrs if hasattr(self, k)]:
            delattr(self, attr)

    def set_to_self(self, namespace):
        """Set the contents of the namespace object (an instance of argparse.Namespace
           returned by parse_arguments) as attributes on the KickstartCommand object.
           It's useful to call this from KickstartCommand subclasses after parsing
           the arguments.
        """
        self.set_to_obj(namespace, self)

    # Just calls set_to_self - exists for backwards compatibility.
    def _setToSelf(self, namespace):
        warnings.warn("_setToSelf has been renamed to set_to_self.  The old name will be removed in a future release.", PendingDeprecationWarning, stacklevel=2)
        self.set_to_self(namespace)

    def set_to_obj(self, namespace, obj):
        """Sets the contents of the namespace object (an instance of argparse.Namespace
           returned by parse_arguments) as attributes on the provided object obj.  It's
           useful to call this from KickstartCommand subclasses that handle lists
           of objects (like partitions, network devices, etc.) and need to populate
           a Data object.
        """
        for (key, val) in vars(namespace).items():
            if val is not None:
                setattr(obj, key, val)

    # Just calls set_to_obj - exists for backwards compatibility.
    def _setToObj(self, namespace, obj):
        warnings.warn("_setToObj has been renamed to set_to_obj.  The old name will be removed in a future release.", PendingDeprecationWarning, stacklevel=2)
        self.set_to_obj(namespace, obj)

class DeprecatedCommand(KickstartCommand):
    """Specify that a command is deprecated and no longer has any function.
       Any command that is deprecated should be subclassed from this class,
       only specifying an __init__ method that calls the superclass's __init__.
       This is an abstract class.
    """
    def __init__(self, writePriority=None, *args, **kwargs):
        # We don't want people using this class by itself.
        if self.__class__ is DeprecatedCommand:
            raise TypeError("DeprecatedCommand is an abstract class.")

        # Create a new DeprecatedCommand instance.
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)

    def dataList(self):
        """Override the method of the deprecated command."""
        return None

    @property
    def dataClass(self):
        """Override the attribute of the deprecated command."""
        return None

    def __str__(self):
        """Placeholder since DeprecatedCommands don't work anymore."""
        return ""

    def parse(self, args):
        """Print a warning message if the command is seen in the input file."""
        mapping = {"lineno": self.lineno, "cmd": self.currentCmd}
        warnings.warn(_("Ignoring deprecated command on line %(lineno)s:  The %(cmd)s command has been deprecated and no longer has any effect.  It may be removed from future releases, which will result in a fatal error from kickstart.  Please modify your kickstart file to remove this command.") % mapping, KickstartDeprecationWarning)

###
### HANDLERS
###
class KickstartHandler(KickstartObject):
    """An empty kickstart handler.

       This handler doesn't handle anything by default.

       version -- The version this syntax handler supports.  This is set by
                  a class attribute of a KickstartHandler subclass and is used to
                  set up the command dict.  It is for read-only use.
    """
    version = None

    def __init__(self, *args, **kwargs):
        """Create a new KickstartHandler instance.

           Instance attributes:

           commands -- A mapping from a string command to a KickstartCommand
                       subclass object that handles it.  Multiple strings can
                       map to the same object, but only one instance of the
                       command object should ever exist.  Most users should
                       never have to deal with this directly, as it is
                       manipulated internally and called through dispatcher.
           currentLine -- The current unprocessed line from the input file
                          that caused this handler to be run.
        """
        KickstartObject.__init__(self, *args, **kwargs)

        # These will be set by the dispatcher.
        self.commands = {}
        self.currentLine = ""

        # A dict keyed by an integer priority number, with each value being a
        # list of KickstartCommand subclasses.  This dict is maintained by
        # registerCommand and used in __str__.  No one else should be touching
        # it.
        self._writeOrder = {}

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        retval = ""

        lst = list(self._writeOrder.keys())
        lst.sort()

        for prio in lst:
            for obj in self._writeOrder[prio]:
                obj_str = obj.__str__()
                if isinstance(obj_str, six.text_type) and not six.PY3:
                    obj_str = obj_str.encode("utf-8")
                retval += obj_str

        return retval

    def _insertSorted(self, lst, obj):
        length = len(lst)
        i = 0

        while i < length:
            # If the two classes have the same name, it's because we are
            # overriding an existing class with one from a later kickstart
            # version, so remove the old one in favor of the new one.
            if obj.__class__.__name__ > lst[i].__class__.__name__:
                i += 1
            elif obj.__class__.__name__ == lst[i].__class__.__name__:
                lst[i] = obj
                return
            elif obj.__class__.__name__ < lst[i].__class__.__name__:
                break

        if i >= length:
            lst.append(obj)
        else:
            lst.insert(i, obj)

    def _setCommand(self, cmdObj):
        # Add an attribute on this version object.  We need this to provide a
        # way for clients to access the command objects.  We also need to strip
        # off the version part from the front of the name.
        if cmdObj.__class__.__name__.find("_") != -1:
            name = cmdObj.__class__.__name__.split("_", 1)[1]
            if not six.PY3:
                name = unicode(name)    # pylint: disable=undefined-variable
        else:
            name = cmdObj.__class__.__name__.lower()
            if not six.PY3:
                name = unicode(name)    # pylint: disable=undefined-variable

        setattr(self, name.lower(), cmdObj)

        # Also, add the object into the _writeOrder dict in the right place.
        if cmdObj.writePriority is not None:
            if cmdObj.writePriority in self._writeOrder:
                self._insertSorted(self._writeOrder[cmdObj.writePriority], cmdObj)
            else:
                self._writeOrder[cmdObj.writePriority] = [cmdObj]

    def registerCommand(self, cmdName, cmdClass):
        # First make sure we haven't instantiated this command handler
        # already.  If we have, we just need to make another mapping to
        # it in self.commands.
        # NOTE:  We can't use the resetCommand method here since that relies
        # upon cmdClass already being instantiated.  We'll just have to keep
        # these two code blocks in sync.
        cmdObj = None

        for (_key, val) in list(self.commands.items()):
            if val.__class__.__name__ == cmdClass.__name__:
                cmdObj = val
                break

        # If we didn't find an instance in self.commands, create one now.
        if cmdObj is None:
            cmdObj = cmdClass()
            self._setCommand(cmdObj)

        # Finally, add the mapping to the commands dict.
        self.commands[cmdName] = cmdObj
        self.commands[cmdName].handler = self

    def registerData(self, dataName, dataClass):
        # We also need to create attributes for the various data objects.
        setattr(self, dataName, dataClass)

    def resetCommand(self, cmdName):
        """Given the name of a command that's already been instantiated, create
           a new instance of it that will take the place of the existing
           instance.  This is equivalent to quickly blanking out all the
           attributes that were previously set.

           This method raises a KeyError if cmdName is invalid.
        """
        if cmdName not in self.commands:
            raise KeyError

        cmdObj = self.commands[cmdName].__class__()

        self._setCommand(cmdObj)
        self.commands[cmdName] = cmdObj
        self.commands[cmdName].handler = self

    def dispatcher(self, args, lineno):
        """Call the appropriate KickstartCommand handler for the current line
           in the kickstart file.  A handler for the current command should
           be registered, though a handler of None is not an error.  Returns
           the data object returned by KickstartCommand.parse.

           args    -- A list of arguments to the current command
           lineno  -- The line number in the file, for error reporting
        """
        cmd = args[0]

        if cmd not in self.commands:
            raise KickstartParseError(_("Unknown command: %s") % cmd, lineno=lineno)
        elif self.commands[cmd] is not None:
            self.commands[cmd].currentCmd = cmd
            self.commands[cmd].currentLine = self.currentLine
            self.commands[cmd].lineno = lineno
            self.commands[cmd].seen = True

            # The parser returns the data object that was modified.  This is either
            # the command handler object itself (a KickstartCommand object), or it's
            # a BaseData subclass instance that should be put into the command's
            # dataList.  The latter is done via side effects.
            #
            # Regardless, return the object that was given to us by the parser.
            obj = self.commands[cmd].parse(args[1:])

            # Here's the side effect part - don't worry about lst not being returned.
            lst = self.commands[cmd].dataList()
            if isinstance(obj, BaseData) and lst is not None:
                lst.append(obj)

            return obj


class BaseHandler(KickstartHandler):
    """A base kickstart handler.

       Each version of kickstart syntax is provided by a subclass of this
       class. These subclasses are what users will interact with for parsing,
       extracting data, and writing out kickstart files.  This is an abstract
       class.
    """

    def __init__(self, mapping=None, dataMapping=None, commandUpdates=None,
                 dataUpdates=None, *args, **kwargs):
        """Create a new BaseHandler instance.  This method must be provided by
           all subclasses, but subclasses must call BaseHandler.__init__ first.

           mapping          -- A custom map from command strings to classes,
                               useful when creating your own handler with
                               special command objects.  It is otherwise unused
                               and rarely needed.  If you give this argument,
                               the mapping takes the place of the default one
                               and so must include all commands you want
                               recognized.
           dataMapping      -- This is the same as mapping, but for data
                               objects.  All the same comments apply.
           commandUpdates   -- This is similar to mapping, but does not take
                               the place of the defaults entirely.  Instead,
                               this mapping is applied after the defaults and
                               updates it with just the commands you want to
                               modify.
           dataUpdates      -- This is the same as commandUpdates, but for
                               data objects.


           Instance attributes:

           packages -- An instance of pykickstart.parser.Packages which
                       describes the packages section of the input file.
           platform -- A string describing the hardware platform, which is
                       needed only by system-config-kickstart.
           scripts  -- A list of pykickstart.parser.Script instances, which is
                       populated by KickstartParser.addScript and describes the
                       %pre/%pre-install/%post/%traceback script section of the
                       input file.
        """

        # We don't want people using this class by itself.
        if self.__class__ is BaseHandler:
            raise TypeError("BaseHandler is an abstract class.")

        KickstartHandler.__init__(self, *args, **kwargs)

        # This isn't really a good place for these, but it's better than
        # everything else I can think of.
        self.scripts = []
        self.packages = Packages()
        self.platform = ""

        # Any sections that we do not understand but want to prevent causing errors
        # are represented by a NullSection.  We want to preserve those on output, so
        # keep a list of their string representations here.  This is likely to change
        # in the future.  Don't rely on this exact implementation.
        self._null_section_strings = []

        self._registerCommands(mapping, dataMapping, commandUpdates, dataUpdates)

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        retval = "# Generated by pykickstart v%s\n" % __version__

        if self.platform:
            retval += "#platform=%s\n" % self.platform

        retval += "#version=%s\n" % versionToString(self.version)

        retval += KickstartHandler.__str__(self)

        for script in self.scripts:
            script_str = script.__str__()
            if isinstance(script_str, six.text_type) and not six.PY3:
                script_str = script_str.encode("utf-8")
            retval += script_str

        if self._null_section_strings:
            retval += "\n"

            for s in self._null_section_strings:
                retval += s

        retval += self.packages.__str__()

        return retval

    def _registerCommands(self, mapping=None, dataMapping=None, commandUpdates=None,
                          dataUpdates=None):
        if mapping == {} or mapping is None:
            from pykickstart.handlers.control import commandMap
            cMap = commandMap[self.version]
        else:
            cMap = mapping

        if dataMapping == {} or dataMapping is None:
            from pykickstart.handlers.control import dataMap
            dMap = dataMap[self.version]
        else:
            dMap = dataMapping

        # Apply the command and data updates, but do
        # not modify the original command and data maps.
        if isinstance(commandUpdates, dict):
            cMap = dict(cMap)
            cMap.update(commandUpdates)

        if isinstance(dataUpdates, dict):
            dMap = dict(dMap)
            dMap.update(dataUpdates)

        for (cmdName, cmdClass) in list(cMap.items()):
            self.registerCommand(cmdName, cmdClass)

        # No checks here because dMap is a bijection.  At least, that's what
        # the comment says.  Hope no one screws that up.
        for (dataName, dataClass) in list(dMap.items()):
            self.registerData(dataName, dataClass)

    def maskAllExcept(self, lst):
        """Set all entries in the commands dict to None, except the ones in
           the lst.  All other commands will not be processed.
        """
        self._writeOrder = {}

        for (key, _val) in list(self.commands.items()):
            if key not in lst:
                self.commands[key] = None

    def hasCommand(self, cmd):
        """Return true if there is a handler for the string cmd."""
        return hasattr(self, cmd)

###
### DATA
###
class BaseData(KickstartObject):
    """The base class for all data objects.  This is an abstract class."""
    removedKeywords = []
    removedAttrs = []

    def __init__(self, *args, **kwargs):
        """Create a new BaseData instance.

           lineno -- Line number in the ks-file where this object was defined
        """

        # We don't want people using this class by itself.
        if self.__class__ is BaseData:
            raise TypeError("BaseData is an abstract class.")

        KickstartObject.__init__(self, *args, **kwargs)
        self.lineno = 0

        # If a subclass provides a removedKeywords list, warn if the user
        # continues to use some of the removed keywords
        for arg in (kw for kw in self.removedKeywords if kw in kwargs):
            warnings.warn("The '%s' keyword has been removed." % arg, KickstartParseWarning, stacklevel=2)

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        return ""

    def __call__(self, *args, **kwargs):
        """Set multiple attributes on a subclass of BaseData at once via
           keyword arguments.  Valid attributes are anything specified in a
           subclass, but unknown attributes will be ignored.
        """
        for (key, val) in list(kwargs.items()):
            # Ignore setting attributes that were removed in a subclass, as
            # if they were unknown attributes.
            if key in self.removedAttrs:
                continue

            if hasattr(self, key):
                setattr(self, key, val)

    def deleteRemovedAttrs(self):
        """Remove all attributes from self that are given in the removedAttrs
           list.  This method should be called from __init__ in a subclass,
           but only after the superclass's __init__ method has been called.
        """
        for attr in [k for k in self.removedAttrs if hasattr(self, k)]:
            delattr(self, attr)
