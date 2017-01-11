# Ignore PendingDeprecationWarnings in the pykickstart module itself.  There's
# nothing users of pykickstart can do about those.  Instead just print out ones
# for users of the code.
import warnings
warnings.filterwarnings("once", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning, module=".")
