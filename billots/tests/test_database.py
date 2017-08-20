# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from billots.src.model.db import test_db
from .test_base import Tester

class Test_Database(Tester):
    def test_get_and_put(self):
        assert(test_db.get("key1") == None)
        assert(test_db.get("key2") == None)
        test_db.put("key1", "val1")
        test_db.put("key2", "val2")
        assert(test_db.get("key1") == "val1")
        assert(test_db.get("key2") == "val2")
        
    def test_delete(self):
        assert(test_db.get("key1") == None)
        test_db.put("key1", "val1")
        assert(test_db.get("key1") == "val1")
        test_db.delete("key1")
        assert(test_db.get("key1") == None)
        
    def test_integers(self):
        test_db.put("key1", 10)
        assert(test_db.get("key1") == 10)
        assert(test_db.get(10) == None)
        test_db.put(15, "hello")
        assert(test_db.get(15) == "hello")
        test_db.delete(15)
        assert(test_db.get(15) == None)

    def test_bool(self):
        test_db.put("key1", True)
        assert(test_db.get("key1") == True)
        test_db.put("key2", False)
        assert(test_db.get("key2") == False)
