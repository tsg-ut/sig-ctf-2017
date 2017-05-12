# coding:utf-8
from __future__ import print_function
from base64 import b64decode as dec
from Crypto.Util.number import *
import re


class Data:
    def __init__(self, seq, data, sig):
        self.seq = int(seq)
        self.data = int(data, 16)
        self.sig = int(sig, 16)

    def __repr__(self):
        return ' '.join(map(hex, [self.seq, self.data, self.sig]))


with open("text", "r") as f:
    l = f.read().rstrip("\n").split("\n")

l = map(dec, l)

data_l = []

for x in l:
    l2 = x.rstrip(";").split(";")
    seq = re.match(".*SEQ = ([0-9]+)", l2[0]).group(1)
    data = re.match(".*DATA = 0x([0-9a-f]+)", l2[1]).group(1)
    sig = re.match(".*SIG = 0x([0-9a-f]+)", l2[2]).group(1)
    data_l.append(Data(seq, data, sig))


data_l.sort(key=lambda x: x.seq)

# 簡単に因数分解できる
p = 49662237675630289
q = 62515288803124247
n = p * q
e = 0x10001
phi = (p - 1) * (q - 1)
d = inverse(e, phi)


# デジタル署名用
pubkey =  0x53a121a11e36d7a84dde3f5d73cf

ret = []
for x in data_l:
    m = pow(x.data, d, n)
    sig = pow(x.sig, e, pubkey)
    if m == sig:
        ret.append(m)

print(''.join(map(chr, ret)))
