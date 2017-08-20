# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from .crypto import Crypto
from .db import live_db, test_db

import json

class Notifications:
    use_db = None
    notify_prefix = "notify"

    def __init__(self, live = True):
        self.use_db = live_db if live else test_db

    def add(self, data):
        if type(data) != dict:
            return

        self.use_db.put(self.data_key(data), True)

    def exists(self, data):
        if type(data) != dict:
            return False

        return self.use_db.get(self.data_key(data)) == True

    def data_key(self, data):
        return self.notify_prefix + "." + Crypto.hash(str(sorted(data.items())))
