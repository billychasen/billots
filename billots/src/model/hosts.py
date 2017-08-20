# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from .db import live_db, test_db
from billots.src.utils.socket_utils import SocketUtils

import json

class Hosts:
    use_db = None
    host_key = "hosts"

    def __init__(self, live = True):
        self.use_db = live_db if live else test_db
        if self.use_db.get(self.host_key) == None:
            self.use_db.put(self.host_key, "[]")

    def add_host(self, address, port):
        if address == None or port == None:
            return

        if self.host_exists(address, port):
            return 

        hosts = self.get_hosts()
        hosts.append({"address": address, "port": port})
        self.use_db.put(self.host_key, json.dumps(hosts))

    def remove_host(self, address, port):
        if address == None or port == None:
            return

        hosts = self.get_hosts()
        new_hosts = [h for h in hosts if h["address"] != address or h["port"] != port]
        self.use_db.put(self.host_key, json.dumps(new_hosts))

    def host_exists(self, address, port):
        addy_ip = SocketUtils.ip_for_host(address)
        for h in self.get_hosts():
            ip = SocketUtils.ip_for_host(h["address"])
            if h["address"] == address and h["port"] == port or \
               ((ip == address and h["port"] == port) and ip != None) or \
               ((ip == addy_ip and h["port"] == port) and (ip != None and addy_ip != None)):
                return True
        return False

    def get_hosts(self):
        return json.loads(self.use_db.get(self.host_key))
