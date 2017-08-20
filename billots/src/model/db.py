# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

import leveldb
import sys

class DB:
    db = None
    name = None

    def __init__(self, name):
        self.name = name
        self.db = leveldb.LevelDB(name)

    def put(self, key, value):
        self.db.Put(str(key).encode(), str(value).encode())

    def get(self, key):
        try:
            val = self.db.Get(str(key).encode())
            try:
                val = int(val)
                return val
            except ValueError:
                pass
            
            retval = val.decode()
            if retval == "True":
                return True
            elif retval == "False":
                return False
            
            return retval
        except KeyError:
            return None

    def delete(self, key):
        self.db.Delete(str(key).encode())

    def reset(self, remake=True):
        if not self.name.endswith("test.db"):
            return

        try:
            import shutil
            shutil.rmtree(self.name)
        except:
            pass

        if self.db:
            del self.db

        if remake:
            self.db = leveldb.LevelDB(self.name)

prefix = ""
for arg in sys.argv:
    if arg.startswith("--prefix"):
        prefix = arg.split("=")[-1]

live_db = DB("%slive.db" % prefix)
test_db = DB("%stest.db" % prefix)
