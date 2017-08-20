# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from billots.src.model.crypto import Crypto
from .test_base import Tester

class Test_Crypto(Tester):
    def test_hash(self):
        t = "ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff"
        assert(Crypto.hash("test") == t)
        assert(Crypto.hash("test2") != t)
    
    def test_new_keys(self):
        c = Crypto(1024)
        keys = c.generate_keys()
        assert("private" in keys)
        assert("public" in keys)

    def test_signing_data(self):
        c = Crypto(1024)
        msg = "There is nothing permanent except change."
        keys = c.generate_keys()
        bad_keys = c.generate_keys()
        sig = Crypto.sign(keys["private"], msg)
        assert(Crypto.verify_signed(keys["public"], sig, msg))
        assert(Crypto.verify_signed(keys["public"], sig, msg + "1") == False)
        assert(Crypto.verify_signed(bad_keys["public"], sig, msg) == False)

