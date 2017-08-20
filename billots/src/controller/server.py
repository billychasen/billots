# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

import json
import logging
import os
from random import random
from twisted.internet import protocol, reactor

from billots.src.model.billot import Billot
from billots.src.model.billots import Billots
from billots.src.model.crypto import Crypto
from billots.src.model.hosts import Hosts
from billots.src.model.notifications import Notifications
from billots.src.utils.socket_utils import SocketUtils, SocketException
from billots.src.utils.utils import Utils

class Server(protocol.Protocol):
    msg_buffer = b""

    def __init__(self, live = True):
        self.live = live
        self.hosts = Hosts(live = live)

    def first_host(self, my_port):
        # add trusted hosts and ask for broadcasts
        trusted = self.trusted_hosts()["hosts"]
        for host in trusted:
            try:
                address = host["address"]
                port = host["port"]
                self.send(address, port, {"command": "broadcast_me", "port": my_port})
                self.hosts.add_host(address, port) # after if host is dead
        
                # get their hosts and add some of them
                hosts = self.send(address, port, {"command": "get_hosts"}, recv=True)
                hosts = self.decode_msg(hosts).get("hosts", [])
                hosts = [h for h in hosts if random() < 0.5]
                for h in hosts:
                    self.send(h["address"], h["port"], {"command": "broadcast_me", "port": my_port})
                    self.hosts.add_host(h["address"], h["port"])
            except SocketException:
                continue

    # Helpers

    def broadcast(self, msg, sample=1):
        for host in self.hosts.get_hosts():
            try:
                notification_msg = msg.copy()
                notification_msg["address"] = host["address"]
                notification_msg["port"] = host["port"]
                if not Notifications().exists(notification_msg) and random() < sample:
                    if self.live:
                        self.send(host["address"], host["port"], msg)
                    Notifications().add(notification_msg)
            except SocketException:
                self.hosts.remove_host(host["address"], host["port"])

    def send(self, address, port, msg, recv=False):
        return SocketUtils.send_json(address, port, msg, recv=recv)
        
    def decode_msg(self, data):
        try:
            msg = json.loads(data)
        except:
            return {}
        return msg

    def trusted_hosts(self):
        if self.live:
            filename = "trusted_hosts.json"
        else:
            filename = "trusted_test_hosts.json"

        dirname = os.path.dirname(os.path.abspath(__file__))
        with open(dirname + "/../resources/" + filename, "r") as f:
            return self.decode_msg(f.read())

    def bad_data(self, msg):
        for v in msg.values():
            dtype = type(v)
            if dtype in [float, int]:
                continue
            elif dtype == str or dtype == bytes:
                if len(v) > 1000:
                    print("bad1 %s %s" % (dtype, v))
                    return True
            else:
                print("bad2 %s %s" % (dtype, v))
                return True
        return False

    # Twisted

    def connectionMade(self):
        #print("Connection from", self.transport.getPeer())
        pass
        
    def dataReceived(self, data):
        try:
            self.msg_buffer += data
            if not SocketUtils.end_delim in data:
                return

            request = json.loads(Utils.safe_dec(self.msg_buffer))
            if self.bad_data(request):
                return

            self.msg_buffer = b""
            command = request.get("command")
            response = {}

            remote_host = None
            remote_port = None
            if self.live:
                remote_host, remote_port = (self.transport.getPeer().host, self.transport.getPeer().port)

            if not Notifications().exists(request):
                logging.info("%s:%s(%s) %s" % (remote_host, remote_port, Utils.time(), request))
                Notifications().add(request)

                if command == "get_hosts":
                    response = self.get_hosts()
                elif command == "who_owns":
                    response = self.who_owns(request["id"])
                elif command == "transfer":
                    response = self.transfer(request["id"], request["to"], 
                                             Utils.safe_enc(request["public_key"]),
                                             Utils.safe_enc(request["signature"]),
                                             request["transfer_id"])
                elif command == "broadcast_me":
                    response = self.broadcast_me(self.transport.getPeer().host, request.get("port", 7333))
                elif command == "list":
                    response = self.list_billots(request["owner"])
            else:
                response = {"error": "dupe msg"}
        except json.decoder.JSONDecodeError:
            response = {"error": "json error."}
        except UnicodeDecodeError:
            response = {"error": "unicode decode error."}
        except KeyError:
            response = {"error": "check that you've included all required call variables."}
        except:
            raise
            response = {"error": "unknown error"}

        encoded_response = Utils.safe_enc(json.dumps(Utils.safe_dec(response))) + SocketUtils.end_delim

        if self.live:
            self.transport.write(encoded_response)
        else:
            return encoded_response
        
    # API calls

    def list_billots(self, owner):
        billots = Billots(owner, live = self.live)
        return {"billots": [b.id for b in billots.get_billots()]}

    def broadcast_me(self, host, port=7333):
        self.hosts.add_host(host, port)
        return {"success": True}

    def get_hosts(self):
        return {"hosts": self.hosts.get_hosts()}

    def who_owns(self, id):
        b = Billot(live=self.live).load(id)
        return {"owner": b.owner}
    
    def transfer(self, id, to, public_key, signature, transfer_id):
        b = Billot(live=self.live).load(id)
        if b.owner == None:
            return {"error": "no owner"}

        if Crypto.hash(public_key) != b.owner:
            return {"error": "wrong owner"}

        data = "TRANSFER:%s->%s" % (id, to)
        if Crypto.verify_signed(public_key, signature, data):
            # Everything is valid
            old_owner = b.owner
            b.change_owner(to)
            msg = {"command": "transfer", "id": id, "to": to,
                   "public_key": public_key, "signature": signature,
                   "transfer_id": transfer_id}
            self.broadcast(msg)
            Billots(old_owner, live=self.live).remove_billot(b)
            Billots(to, live=self.live).add_billot(b)
            return {"success": True}

        return {"error": "bad signature"}
