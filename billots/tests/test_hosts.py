# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from billots.src.model.hosts import Hosts
from billots.src.utils.socket_utils import SocketUtils
from .test_base import Tester

class Test_Hosts(Tester):
    def test_get_hosts(self):
        assert(Hosts(live = False).get_hosts() == [])

    def test_add_host(self):
        h = Hosts(live = False)
        h.add_host("1.2.3.4", 90)
        h.add_host("1.2.3.4", 90)
        assert(h.get_hosts() == [{"address": "1.2.3.4", "port": 90}])

    def test_remove_host(self):
        h = Hosts(live = False)
        h.add_host("1.2.3.4", 90)
        h.add_host("1.2.3.4", 100)
        h.add_host("1.2.3.5", 90)
        h.add_host("1.2.3.5", 90)

        assert(len(h.get_hosts()) == 3)
        
        h.remove_host("1.2.3.4", 90)

        assert(len(h.get_hosts()) == 2)
        assert({"address": "1.2.3.4", "port": 90} not in h.get_hosts())
        assert({"address": "1.2.3.4", "port": 100} in h.get_hosts())
        assert({"address": "1.2.3.5", "port": 90} in h.get_hosts())

        assert(h.host_exists("1.2.3.4", 90) == False)
        assert(h.host_exists("1.2.3.4", 100))
        assert(h.host_exists("1.2.3.5", 90))

    def test_host_exists(self):
        h = Hosts(live = False)
        h.add_host("1.2.3.4", 90)
        h.add_host("1.2.3.4", 100)
        h.add_host("1.2.3.5", 90)
        h.add_host("1.2.3.5", 90)

        assert(h.host_exists("1.2.3.4", 90))
        assert(h.host_exists("1.2.3.6", 90) == False)
        assert(h.host_exists("1.2.3.4", 100))
        assert(h.host_exists("1.2.3.5", 90))

    def test_hosts_by_name(self):
        name = "mint1.billots.org"

        h = Hosts(live = False)
        h.add_host(name, 90)
        assert(h.host_exists(name, 90))
        assert(len(h.get_hosts()) == 1)

        ip = SocketUtils.ip_for_host(name)
        h.add_host(ip, 90)
        assert(h.host_exists(name, 90))
        assert(h.host_exists(ip, 90))
        assert(len(h.get_hosts()) == 1)

    def test_hosts_by_ip(self):
        name = "mint1.billots.org"
        ip = SocketUtils.ip_for_host(name)

        h = Hosts(live = False)
        h.add_host(ip, 90)
        assert(h.host_exists(ip, 90))
        assert(h.host_exists(name, 90))
        assert(len(h.get_hosts()) == 1)

        h.add_host(name, 90)
        assert(h.host_exists(name, 90))
        assert(h.host_exists(ip, 90))
        assert(len(h.get_hosts()) == 1)
