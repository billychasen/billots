# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from billots.src.model.notifications import Notifications
from .test_base import Tester

class Test_Notifications(Tester):
    def test_add_notification(self):
        n = Notifications(live = False)
        n.add({"a": 5, "b": "hello", "c": 3})

    def test_exists_notification(self):
        data = {"a": 5, "b": "hello", "c": 3}

        n = Notifications(live = False)
        n.add(data)

        assert(n.exists(data) == True)
        assert(n.exists({"b": "hello", "c": 3, "a": 5}) == True)
        assert(n.exists({"b": "hello", "c": 2, "a": 5}) == False)
        assert(n.exists({}) == False)
        assert(n.exists([]) == False)
        assert(n.exists(None) == False)
        assert(n.exists(1) == False)
