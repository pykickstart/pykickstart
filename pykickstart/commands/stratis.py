from pykickstart.version import F45
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser


class F45_StratisFs(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.stratis = kwargs.get("stratisfs", False)

    def __str__(self):
        raise NotImplementedError()

    def _getParser(self):
        op = KSOptionParser(prog="stratisfs", description="""
                            Configure a Stratis filesystem.
                            """, version=F45)
        op.add_argument("mountpoint", version=F45,
                        help="""
                        Filesystem mountpoint. "none" is a valid value, which
                        means do not mount.
                        """)
        op.add_argument("name", version=F45,
                        help="""
                        Name of filesystem.
                        """)
        op.add_argument("--pool-name", version=F45,
                        help="""
                        Name of this filesystem's pool.
                        """)
        op.add_argument("--size", version=F45,
                        help="""
                        Initial filesystem size.
                        """)
        op.add_argument("--size-limit", version=F45,
                        help="""
                        Filesystem size limit. Must not be less than
                        filesystem size.
                        """)
        op.add_argument("--crypt", version=F45,
                        help="""
                        Whether this filesystem may be placed on an encrypted
                        pool.
                        """)
        return op

    def parse(self, args):
        self.op.parse_args(args=args, lineno=self.lineno)
        self.stratis = True
        return self

class F45_StratisPool(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.stratis = kwargs.get("stratispool", False)

    def __str__(self):
        raise NotImplementedError()

    def _getParser(self):
        op = KSOptionParser(prog="stratispool", description="""
                            Configure a Stratis pool.
                            """, version=F45)
        op.add_argument("name", version=F45,
                        help="""
                        Name of pool.
                        """)
        op.add_argument("device", version=F45, nargs="+",
                        help="""
                        Abstract ID of device to create pool from. May be
                        specified multiple times.
                        """)
        op.add_argument("--fs-limit", version=F45,
                        help="""
                        Restrict the pool to this number of filesystems.
                        """)
        op.add_argument("---overprovisioning", version=F45,
                        default=True,
                        help="""
                        Allow overprovisioning on this pool.
                        """)
        op.add_argument("--encrypt", version=F45,
                        default=False, action="store_true",
                        help="""
                        On reboot, request the user during setup to encrypt
                        this pool.
                        """)
        return op

    def parse(self, args):
        self.op.parse_args(args=args, lineno=self.lineno)
        self.stratis = True
        return self
