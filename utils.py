# -*- coding: utf-8 -*-

import base64

from Crypto.Hash import SHA, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def md5_encode(string):
    """
    md5加密
    """

    if isinstance(string, str):
        string = string.encode()

    return MD5.new(string).hexdigest()


def get_sign_data(*args):
    non_empty = [_f for _f in args if _f]

    if non_empty is None or len(non_empty) == 0:
        return ''
    else:
        return '\n'.join([str(i) for i in non_empty])


def get_rsa_sign(sign_data, key):

    if isinstance(sign_data, str):
        sign_data = sign_data.encode()

    sha1 = SHA.new(sign_data)
    key_der = base64.b64decode(key)
    rsa_key = RSA.importKey(key_der)
    rsa = PKCS1_v1_5.new(rsa_key)
    return base64.b64encode(rsa.sign(sha1))
