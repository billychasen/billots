# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

import os
from subprocess import call
from multiprocessing.dummy import Pool as ThreadPool 
pool = ThreadPool(50)

def test_disputed(port):
    print("sending %s" % port)
    dirname = os.path.dirname(os.path.abspath(__file__))
    call("bwallet --transfer a-1 7c21504b496eedb899c6ebfb508708277233ee8fc773d05223e0d31dffdab5d3f248e3e3d2c47d51652a0c8d19c1a9c8ef6d4939f9441fe247cf394821392976%s --server localhost:%s --keyfile %s/user1 --prefix=d%s" % (port, port, dirname, port), shell=True)

def main():
    ports = range(7335, 7346)
    pool.map(test_disputed, ports)

