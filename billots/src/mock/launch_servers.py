# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from subprocess import call
from multiprocessing.dummy import Pool as ThreadPool 
pool = ThreadPool(50)

def start_server(port):
    print("starting %s" % port)
    call("bserver %s test --prefix=%s" % (port, port), shell=True)

def main():
    ports = range(7333, 7350)
    pool.map(start_server, ports)

