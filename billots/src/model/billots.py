# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from .billot import Billot
from .db import live_db, test_db
import json

class Billots:
    use_db = None
    prefix = "billotlist."
    owner = None
    billots_key = None

    def __init__(self, owner, live = True):
        self.live = live
        self.owner = owner
        self.billots_key = "%s%s" % (self.prefix, owner)
        self.use_db = live_db if live else test_db

    def add_billot(self, billot):
        if billot.id == None:
            return

        if self.billot_exists(billot):
            return

        billots = self.get_billots()
        billots.append(billot)
        ids = [b.id for b in billots]
        self.use_db.put(self.billots_key, json.dumps(ids))

    def remove_billot(self, billot):
        if billot.id == None:
            return

        billots = self.get_billots()
        new_billots = [b.id for b in billots if b.id != billot.id]
        self.use_db.put(self.billots_key, json.dumps(new_billots))

    def billot_exists(self, billot):
        for b in self.get_billots():
            if b.id == billot.id:
                return True
        return False

    def get_billots(self):
        data = self.use_db.get(self.billots_key)
        if data == None:
            return []

        ids = json.loads(data)
        billots = []
        for id in ids:
            billots.append(Billot(live=self.live).load(id))
        return billots
