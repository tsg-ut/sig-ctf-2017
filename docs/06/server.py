#!/usr/bin/env python
# coding:utf-8
from __future__ import print_function
from Crypto.Cipher import AES
import sys
import base64 as b64



with open("key", "r") as f:
    key = f.readline()[:16]
    iv_true = f.readline()[:16]

with open("flag", "r") as f:
    raw = f.read()

def decrypt_ok(c):
    cipher = AES.new(key, AES.MODE_CBC, IV=iv_true)
    m = cipher.decrypt(c)
    pad = ord(m[-1])
    if pad > 16 or pad == 0:
        return False
    for i in range(pad):
        #print(ord(m[-i-1]), end=" ")
        if ord(m[-i-1]) != pad:
            return False
    return True


def create():
    print(key, iv_true, raw)

    pad = 16 - (len(raw) % 16)
    raw = raw + ''.join([chr(pad) for i in range(pad)])

    cipher = AES.new(key, AES.MODE_CBC, IV=iv_true)
    encrypted = cipher.encrypt(raw)
    print(b64.b64encode(encrypted))
    assert decrypt_ok(encrypted)

if __name__ == '__main__':
    # create()
    while True:
        s = raw_input()
        try:
            flag = decrypt_ok(b64.b64decode(s))
        except:
            print("False")
            sys.stdout.flush()
            continue
        print(flag)
        sys.stdout.flush()

