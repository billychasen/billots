# Copyright (c) 2017-present, Billy Chasen.
# See LICENSE for details.
# Created by Billy Chasen on 8/17/17.

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512
from Crypto.Signature import PKCS1_v1_5
from billots.src.utils.utils import Utils

class Crypto:
    def __init__(self, key_size = 4096):
        self.key_size = key_size

    def generate_keys(self):
        """
          Generate a new private/public keypair
        """
        keys = RSA.generate(self.key_size)
        return {"public": keys.publickey().exportKey(),
                "private": keys.exportKey()}

    @staticmethod
    def hash(val):
        """
          Hash the value with SHA512
        """
        h = SHA512.new()
        h.update(Utils.safe_enc(val))
        return h.hexdigest()

    @staticmethod
    def sign(private_key, data):
        """
          Sign something with a private key
        """
        key = RSA.importKey(private_key)
        hashed = SHA512.new(Utils.safe_enc(data))
        signer = PKCS1_v1_5.new(key)
        return signer.sign(hashed)

    @staticmethod
    def verify_signed(public_key, signature, data):
        """
         Verify a signature
        """
        key = RSA.importKey(public_key)
        hashed = SHA512.new(Utils.safe_enc(data))
        verifier = PKCS1_v1_5.new(key)
        if verifier.verify(hashed, signature):
            return True
        return False
