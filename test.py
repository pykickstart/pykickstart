#!/usr/bin/python

from pykickstart.version import *
from pykickstart.parser import *

handler = makeHandler(FC6)
parser = KickstartParser(handler)
parser.readKickstart("ks.cfg")

print handler.__str__()
