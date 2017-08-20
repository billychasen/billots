# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

import logging
import os
from twisted.internet import reactor, protocol
import sys

from billots.src.controller.server import Server
from billots.src.model.billot import Billot
from billots.src.model.crypto import Crypto

def test_data():
    # Populate with some test data
    user1 = {}
    user2 = {}
    user3 = {}

    dirname = os.path.dirname(os.path.abspath(__file__))

    with open(dirname + "/../mock/user1", "r") as f:
        user1["private"] = f.read().strip()
    with open(dirname + "/../mock/user1.pub", "r") as f:
        user1["public"] = f.read().strip()
    with open(dirname + "/../mock/user2", "r") as f:
        user2["private"] = f.read().strip()
    with open(dirname + "/../mock/user2.pub", "r") as f:
        user2["public"] = f.read().strip()
    with open(dirname + "/../mock/user3", "r") as f:
        user3["private"] = f.read().strip()
    with open(dirname + "/../mock/user3.pub", "r") as f:
        user3["public"] = f.read().strip()

    user1["hash"] = Crypto.hash(user1["public"])
    user2["hash"] = Crypto.hash(user2["public"])
    user3["hash"] = Crypto.hash(user3["public"])

    b = Billot(owner = user1["hash"], id = "a-1")
    b.save()
    b = Billot(owner = user1["hash"], id = "b-1")
    b.save()
    b = Billot(owner = user1["hash"], id = "c-1")
    b.save()

    b = Billot(owner = user2["hash"], id = "d-1")
    b.save()
    b = Billot(owner = user2["hash"], id = "e-1")
    b.save()
    b = Billot(owner = user2["hash"], id = "f-1")
    b.save()

    b = Billot(owner = user3["hash"], id = "g-1")
    b.save()
    b = Billot(owner = user3["hash"], id = "h-1")
    b.save()
    b = Billot(owner = user3["hash"], id = "i-1")
    b.save()

def main():
    if len(sys.argv) < 2:
        print("Required: specify a port")
        return

    live = True
    my_port = int(sys.argv[1])
    logging.basicConfig(filename="server%s.log" % my_port, level=logging.INFO)
    logging.info("Starting server on %s" % my_port)

    if len(sys.argv) > 2 and sys.argv[2] == "test":
        test_data()
        live = False

    Server(live=live).first_host(my_port)

    factory = protocol.ServerFactory()
    factory.protocol = Server
    reactor.listenTCP(my_port, factory)
    reactor.run()

if __name__ == '__main__':
    print("Run this as bserver. If you want to run the script directly, you need to copy to the root directory.")
    #main()

