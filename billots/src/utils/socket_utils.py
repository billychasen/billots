# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from .utils import Utils

import json
import socket

class SocketException(Exception):
    pass

class SocketUtils:
    end_delim = b"\r\n\r\n"

    @staticmethod
    def send_json(address, port, msg, recv=False):
        encoded_msg = Utils.safe_enc(json.dumps(Utils.safe_dec(msg)))
        return SocketUtils.send(address, port, encoded_msg, recv)

    @staticmethod
    def send(address, port, msg, recv=False):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((address, port))
            s.sendall(msg + SocketUtils.end_delim)
            if recv:
                data = b""
                while True:
                    data += s.recv(1024)
                    if not data or data.endswith(SocketUtils.end_delim):
                        break
                s.close()
                return data
            else:
                s.close()
        except: # TODO: distinguish between exceptions
            raise SocketException

    @staticmethod
    def ip_for_host(host):
        try:
            return socket.gethostbyaddr(host)[2][0]
        except:
            return None
