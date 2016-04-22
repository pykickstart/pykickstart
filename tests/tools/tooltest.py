import unittest
import subprocess
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


class ToolTest(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super(ToolTest, self).__init__(methodName)
        self.tool = ""
        self.cmd_params = ""
        # individual coverage files are needed because the test cases are run in parallel
        self.coverage_file = ".coverage.tools." + type(self).__name__

    def tool_setup(self, tool, cmd_params=None):
        if cmd_params:
            self.cmd_params = cmd_params
        else:
            self.cmd_params = ["--branch", "--omit=*usr*"]
        self.tool = tool

    def run_tool(self, tool_params=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        args = ["coverage", "run", "--append"]
        args += self.cmd_params + ["tools/" + self.tool]

        if tool_params:
            args += tool_params
        process = subprocess.Popen(args=args,
                                   env=dict(os.environ,
                                            COVERAGE_FILE=self.coverage_file),
                                   stdout=stdout,
                                   stderr=stderr)
        out, err = process.communicate()
        out = list(map(bytes.decode, out.splitlines()))
        err = list(map(bytes.decode, err.splitlines()))
        retval = process.wait()
        return (retval, out, err)

        
class KsvalidatorTest(ToolTest):
    def __init__(self, methodname="runTest"):
        super(KsvalidatorTest, self).__init__(methodname)
        self.tool_setup(tool="ksvalidator.py")
