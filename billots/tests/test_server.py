# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from billots.src.controller.server import Server
from billots.src.model.billot import Billot
from billots.src.model.billots import Billots
from billots.src.model.crypto import Crypto
from billots.src.utils.socket_utils import SocketUtils
from billots.src.utils.utils import Utils
from .test_base import Tester

import json
from time import time

c1 = Crypto(1024)
keys1 = c1.generate_keys()
keys2 = c1.generate_keys()

class Test_Server(Tester):
    def server_call(self, server, msg):
        response = server.dataReceived(Utils.safe_enc(json.dumps(msg)) + SocketUtils.end_delim)
        return json.loads(Utils.safe_dec(response))

    def test_transfer(self):
        tokenid = "a-1"
        b = Billot(live = False)
        b.id = tokenid
        b.owner = Crypto.hash(keys1["public"])
        b.public_key = keys1["public"]
        b.save()
        Billots(b.owner, live = False).add_billot(b)
        server = Server(live = False)

        # bad transfer
        sig = Crypto.sign(keys2["private"], "TRANSFER:%s->%s" % (tokenid, Crypto.hash(keys2["public"])))
        assert("error" in server.transfer(tokenid, Crypto.hash(keys2["public"]), keys2["public"], sig, 123))
        b2 = Billot(live = False).load(tokenid)
        assert(b2.owner == b.owner)

        # bad transfer #2
        sig = Crypto.sign(keys1["private"], "TRANSFER:%s->%s" % (tokenid, Crypto.hash(keys2["public"])))
        assert("error" in server.transfer(tokenid, Crypto.hash(keys2["public"]), keys1["public"], sig + b"a", 123))
        b2 = Billot(live = False).load(tokenid)
        assert(b2.owner == b.owner)

        # good transfer
        sig = Crypto.sign(keys1["private"], "TRANSFER:%s->%s" % (tokenid, Crypto.hash(keys2["public"])))
        assert(server.transfer(tokenid, Crypto.hash(keys2["public"]), keys1["public"], sig, 123))
        b3 = Billot(live = False).load(tokenid)
        assert(b3.owner == Crypto.hash(keys2["public"]))

        assert(len(Billots(Crypto.hash(keys1["public"]), live = False).get_billots()) == 0)
        assert(Billots(Crypto.hash(keys2["public"]), live = False).get_billots()[0].id == tokenid)
        
    def test_owner(self):
        tokenid = "a-1"
        b = Billot(live = False)
        b.id = tokenid
        b.owner = "max"
        b.save()

        server = Server(live = False)
        response = server.who_owns(tokenid)
        assert(response["owner"] == "max")
        response = server.who_owns(tokenid + "1")
        assert(response["owner"] == None)

    def test_hosts(self):
        server = Server(live = False)
        assert(len(server.get_hosts()["hosts"]) == 0)

    def test_broadcast_me(self):
        server = Server(live = False)
        server.broadcast_me("1.1.1.1")
        assert(len(server.get_hosts()["hosts"]) == 1)
        assert({"address": "1.1.1.1", "port": 7333} in server.get_hosts()["hosts"])

    def test_command_transfer(self):
        tokenid = "a-2"
        b = Billot(live = False)
        b.id = tokenid
        b.owner = Crypto.hash(keys1["public"])
        b.save()

        sig = Crypto.sign(keys1["private"], "TRANSFER:%s->%s" % (tokenid, Crypto.hash(keys2["public"])))

        server = Server(live = False)
        response = self.server_call(server, {"command": "transfer",
                                             "id": tokenid,
                                             "to": Crypto.hash(keys2["public"]),
                                             "public_key": Utils.safe_dec(keys1["public"]),
                                             "signature": Utils.safe_dec(sig),
                                             "transfer_id": time(),
                                             })
        assert(response["success"])

        response = self.server_call(server, {"command": "who_owns",
                                             "id": tokenid, "rid": time(),
                                             })
        check_owner = response["owner"]
        assert(Crypto.hash(keys2["public"]) == check_owner)

    def test_command_who_owns(self):
        server = Server(live = False)
        response = self.server_call(server, {"command": "who_owns",
                                             "id": "asdf", "rid": time(),
                                             })
        owner = response["owner"]
        assert(owner == None)

    def test_command_get_hosts(self):
        server = Server(live = False)
        server.first_host(7333)
        response = self.server_call(server, {"command": "get_hosts", "rid": time()})
        assert("hosts" in response)
