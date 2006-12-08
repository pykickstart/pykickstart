#!/usr/bin/python

from pykickstart.version import *
from pykickstart.parser import *

# This is a temporary location for this logic.  It needs to be moved somewhere
# more useful soon.
def makeHandler(version):
    if version == FC5:
        from pykickstart.commands.fc5 import FC5Handler
        return FC5Handler()
    elif version == FC6:
        from pykickstart.commands.fc6 import FC6Handler
        return FC6Handler()

handler = makeHandler(FC6)
parser = KickstartParser(handler)
parser.readKickstart("ks.cfg")

print handler.__str__()
