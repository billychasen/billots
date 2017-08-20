# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from billots.src.model.billot import Billot
from .test_base import Tester

class Test_Billot(Tester):
    def test_load_billot(self):
        b = Billot(live = False)
        b.load("abc")
        assert(b.owner == None)
        assert(b.id == "abc")

    def test_save_billot(self):
        b = Billot(live = False)
        b.id = 10
        b.owner = "mine"
        b.save()
        
        c = Billot(live = False)
        c.load(10)
        assert(c.owner == "mine")

    def test_value(self):
        b = Billot(live = False)
        b.id = "a-1"
        assert(b.value() == 100)
        b.id = "b-2345"
        assert(b.value() == 50)
        b.id = "b--1"
        assert(b.value() == 0)
        b.id = "b-94239475823945"
        assert(b.value() == 0)
        b.id = "HELLO"
        assert(b.value() == 0)
        b.id = "[0-9]+"
        assert(b.value() == 0)
    
    def test_value_not_in_db(self):
        b = Billot(live = False)
        assert(b.load("a-1").value() == 100)

    def test_change_owner(self):
        b = Billot(live = False)
        b.id = "a"
        b.owner = "joe"
        b.save()
        assert(b.load("a").owner == "joe")
        b.change_owner("jane")
        assert(b.load("a").owner == "jane")
                
    def test_json_serializable(self):
        b = Billot(live = False)
        b.id = "a"
        b.owner = "joe"
        b.save()
