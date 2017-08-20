# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

import time

class Utils:
    @staticmethod
    def safe_enc(val):
        return Utils.safe_array(val, True)

    @staticmethod
    def safe_dec(val):
        return Utils.safe_array(val, False)
            
    @staticmethod
    def safe_array(val, encode):
        if type(val) == list or type(val) == tuple:
            res = [Utils.safe_val(v, encode) for v in val]
            if type(val) == tuple:
                return tuple(res)
            return res
        elif type(val) == dict:
            return {k:Utils.safe_val(v, encode) for k,v in val.items()}
        return Utils.safe_val(val, encode)

    @staticmethod
    def safe_val(val, encode):
        if val == None:
            return None
        
        if encode:
            if type(val) == bytes:
                return val
            return val.encode("ISO-8859-1")
        else:
            if type(val) == bytes:
                return val.decode("ISO-8859-1")
            return val

    @staticmethod
    def time():
        return time.strftime("%Y-%m-%d %H:%M:%S")
