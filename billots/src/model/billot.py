# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from .db import live_db, test_db
import json
import os
import re
from billots.src.utils.utils import Utils

class Billot:
    owner = None
    id = None
    use_db = None
    prefix = "billot."

    def __init__(self, owner = None, id = None, live = True):
        self.owner = owner
        self.id = id
        self.use_db = live_db if live else test_db

    def load(self, id):
        self.id = id
        str = self.use_db.get("%s%s" % (self.prefix, id))
        if str:
            vals = json.loads(str)
            self.id = vals.get("id")
            self.owner = vals.get("owner")
        return self

    def save(self):
        if self.owner == None or self.id == None:
            return

        self.use_db.put("%s%s" % (self.prefix, self.id), json.dumps({
                    "id": self.id,
                    "owner": self.owner,
                    }))

    def value(self):
        """
         Figure out the intrinsic value of this billot based on id
        """
        if self.id == None:
            return 0

        dirname = os.path.dirname(os.path.abspath(__file__))
        with open(dirname + "/../resources/values.json", "r") as f:
            values = json.loads(f.read())["values"]
        for value in values:
            regex = re.compile("^%s([0-9]+)$" % re.escape(value["prefix"]))
            match = re.match(regex, self.id)
            if match:
                num = int(match.group(1))
                if num <= value["circulation"] and num >= 0:
                    return value["value"]
        return 0

    def change_owner(self, new_owner):
        """
         Allow the owner to change to a new owner
         NOTE: This is not doing any owner verification
        """
        if self.id == None:
            return

        self.owner = new_owner
        self.save()

    def __str__(self):
        return "%s:%s" % (self.owner, self.id)
