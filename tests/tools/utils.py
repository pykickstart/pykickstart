import os
import tempfile

def mktempfile(content="", prefix="ks-", text=True):
    """
    Create a temporary file with defined content and return it's path.
    """
    handle, path = tempfile.mkstemp(prefix=prefix, text=text)
    os.write(handle, str.encode(content))
    os.close(handle)
    return path
