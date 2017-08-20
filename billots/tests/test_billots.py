# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from billots.src.model.billot import Billot
from billots.src.model.billots import Billots
from .test_base import Tester

class Test_Billots(Tester):
    def test_get_billots(self):
        assert(Billots("abc", live = False).get_billots() == [])

    def create_billots(self):
        b1 = Billot(owner = "me", id = "a-1", live = False)
        b1.save()

        b1t = Billot(live = False).load("a-1")
        assert(b1t.id == "a-1")

        b2 = Billot(owner = "me", id = "a-2", live = False)
        b2.save()

        b3 = Billot(owner = "me", id = "b-1", live = False)
        b3.save()

        b4 = Billot(owner = "me", id = "b-2", live = False)
        b4.save()
        
        return [b1, b2, b3, b4]

    def test_add_billot(self):
        billots = self.create_billots()

        b = Billots("abc", live = False)
        b.add_billot(billots[0])
        b.add_billot(billots[1])
        assert(b.get_billots()[0].id == billots[0].id)
        assert(b.get_billots()[1].id == billots[1].id)

        b = Billots("123", live = False)
        assert(len(b.get_billots()) == 0)

    def test_remove_billot(self):
        billots = self.create_billots()

        b = Billots("abc", live = False)
        b.add_billot(billots[0])
        b.add_billot(billots[1])
        b.add_billot(billots[1]) # dupe
        b.add_billot(billots[2])

        b2 = Billots("123", live = False)
        b2.add_billot(billots[3])

        assert(len(b.get_billots()) == 3)
        
        b.remove_billot(billots[0])

        assert(len(b.get_billots()) == 2)
        for bb in b.get_billots():
            assert(bb.id != "a-1")

        assert(len(b2.get_billots()) == 1)
        assert(b2.get_billots()[0].id == billots[3].id)
