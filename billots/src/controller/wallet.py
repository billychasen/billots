# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

import argparse
from collections import defaultdict
import json
import os
from time import time

from billots.src.model.billot import Billot
from billots.src.model.billots import Billots
from billots.src.model.crypto import Crypto
from billots.src.utils.socket_utils import SocketUtils, SocketException
from billots.src.utils.utils import Utils

class Wallet():
    def __init__(self, keyfile, address, port, trusted):
        self.keyfile = keyfile
        self.server_address = address
        self.server_port = port
        self.trusted = self.trusted_hosts(trusted)

    def generate_keys(self, path, silent=False):
        keys = Crypto().generate_keys()
        with open(path, "w") as f:
            f.write(Utils.safe_dec(keys["private"]))
        with open("%s.pub" % path, "w") as f:
            f.write(Utils.safe_dec(keys["public"]))
        self.sprint(silent, "keys written to: %s" % path)

    def list_billots(self, silent=False):
        owner = self.owner_hash(silent=True)
        res = SocketUtils.send_json(self.trusted[0]["address"], self.trusted[0]["port"],
                                    {"command": "list", "owner": owner, "rid": time()}, recv=True)
        res = json.loads(res)
        if "error" in res:
            self.sprint(silent, "Error: %s" % res["error"])
            return []

        total = 0
        verified_ids = []
        for bid in res["billots"]:
            if self.check_owner(bid, silent=True) == owner:
                b = Billot().load(bid)
                self.sprint(silent, "Billot: %s Value: %s" % (b.id, b.value()))
                total += b.value()
                verified_ids.append(bid)

        self.sprint(silent, "Total: %s" % total)
        return verified_ids

    def transfer(self, id, to, silent=False):
        with open(self.keyfile, "r") as f:
            private_key = f.read().strip()

        with open("%s.pub" % self.keyfile, "r") as f:
            public_key = f.read().strip()

        sig = Crypto.sign(private_key, "TRANSFER:%s->%s" % (id, to))
        res = SocketUtils.send_json(self.server_address, self.server_port, {"command": "transfer",
                                                                            "id": id,
                                                                            "to": to,
                                                                            "public_key": public_key,
                                                                            "signature": sig,
                                                                            "transfer_id": time(),
                                                                            }, recv=True)
        res = json.loads(res)
        if "error" in res:
            self.sprint(silent, "Error: %s" % res["error"])
            return False
        else:
            self.sprint(silent, "Transfer broadcasted.")
            return True

    def who_owns(self, id, silent=False):
        res = SocketUtils.send_json(self.server_address, self.server_port, {"command": "who_owns", "id": id, "rid": time()}, recv=True)
        res = json.loads(res)
        if "error" in res:
            self.sprint(silent, "Error: %s" % res["error"])
            return False
        else:
            self.sprint(silent, "Owner: %s" % res["owner"])
            return res["owner"]

    def check_owner(self, id, silent=False):
        """
          This checks across multiple servers to see who the owner is. The algorithm
          for this could either be (1) only check trusted hosts (2) some majority vote
          or (3) roll your own.

          Current algorithm is a mix of (1) and (2)
        """
        owners = defaultdict(int)

        for host in self.trusted:
            try:
                res = SocketUtils.send_json(host["address"], host["port"], {"command": "who_owns", "id": id, "rid": time()}, recv=True)
                res = json.loads(res)
                if not "error" in res:
                    owners[res["owner"]] += 1
            except SocketException:
                continue

        if len(owners) == 0:
            self.sprint(silent, "No owner")
            return False

        for owner in owners.keys():
            if owners[owner] > (len(self.trusted) / 2.0):
                self.sprint(silent, "Owner: %s" % owner)
                return owner

        self.sprint(silent, "Disputed owner")
        return False

    def owner_hash(self, silent=False):
        with open(self.keyfile + ".pub", "r") as f:
            key = f.read().strip()
            self.sprint(silent, "Hash: %s" % Crypto.hash(key))
            return Crypto.hash(key)

    def sprint(self, silent, msg):
        if not silent:
            print(msg)

    def trusted_hosts(self, hosts):
        if hosts == None or len(hosts) == 0:
            dirname = os.path.dirname(os.path.abspath(__file__))
            with open(dirname + "/../resources/trusted_hosts.json", "r") as f:
                return json.loads(f.read())["hosts"]

        trusted = []
        for host in hosts:
            parts = host.strip(",").split(":")
            if "-" in parts[1]:
                prange = parts[1].split("-")
                for p in range(int(prange[0]), int(prange[1]) + 1):
                    trusted.append({"address": parts[0], "port": p})
            else:
                trusted.append({"address": parts[0], "port": int(parts[1])})
        return trusted

def main():
    parser = argparse.ArgumentParser(description="Do some billoty stuff.")    
    parser.add_argument("--genkeys", nargs="?", type=str, metavar=("FILENAME"), const="key",
                        help="Generate a new private/public key.", required=False)
    parser.add_argument("--list", nargs="?", const=True, help="List all owned billots.", required=False)
    parser.add_argument("--hash", nargs="?", const=True, help="Your public hash (for getting billots).", required=False)
    parser.add_argument("--transfer", nargs=2, metavar=("ID", "TO"), help="Transfer a billot to a specified new owner.", required=False)
    parser.add_argument("--check-owner", nargs=1, metavar=("ID"), help="Checks the owner of a billot based on consensus.", required=False)
    parser.add_argument("--who-owns", nargs=1, metavar=("ID"), help="Who owns a billot (on a specific server).", required=False)
    parser.add_argument("--server", nargs=1, default=["mint1.billots.org:7333"], metavar="HOST:PORT",
                        help="The server to broadcast transfers to.", required=False)
    parser.add_argument("--trusted", nargs="*", metavar="HOST:PORT", help="Supply a list of trusted hosts (instead of trusted_hosts file). Also accepts a port range: localhost:7333-7340 (inclusive).",
                        required=False)
    parser.add_argument("--keyfile", type=str, help="Use this keyfile.", required=False)

    args, unknown = parser.parse_known_args()
    keyfile = args.keyfile or "key"
    server_address, server_port = args.server[0].split(":")
    server_port = int(server_port)
    wallet = Wallet(keyfile, server_address, server_port, args.trusted)

    if args.genkeys:
        wallet.generate_keys(args.genkeys)
    elif args.list:
        wallet.list_billots()
    elif args.hash:
        wallet.owner_hash()
    elif args.transfer:
        wallet.transfer(args.transfer[0], args.transfer[1])
    elif args.who_owns:
        wallet.who_owns(args.who_owns[0])
    elif args.check_owner:
        wallet.check_owner(args.check_owner[0])
    else:
        parser.print_help()

if __name__ == '__main__':
    print("Run this as bwallet. If you want to run the script directly, you need to copy to the root directory.")
    #main()
