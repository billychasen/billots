# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from billots.src.model.db import test_db
import pytest

class Tester:
    @pytest.yield_fixture(autouse=True)
    def run_around_tests(self):
        test_db.reset()
        yield
        test_db.reset(remake=False)
