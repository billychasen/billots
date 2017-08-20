
from billots.src.controller.server import Server
from billots.src.controller.wallet import Wallet

from billots.src.model.billot import Billot
from billots.src.model.billots import Billots
from billots.src.model.crypto import Crypto
from billots.src.model.hosts import Hosts
from billots.src.model.notifications import Notifications

def checkVersion():
    import sys
    version = getattr(sys, "version_info", (0,))
    if version < (3, 0):
        raise ImportError("Billots requires Python 3. You can override this and try 2.x, but it's unsupported.")

checkVersion()
