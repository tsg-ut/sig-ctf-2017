# coding:utf-8
from __future__ import print_function
from Crypto.Util.number import inverse, long_to_bytes
import Crypto.PublicKey.RSA as RSA

def sqrt(x):
    lb = 0
    ub = x
    while (ub - lb) > 1:
        mb = (ub + lb) / 2
        if mb * mb > x:
            ub = mb
        else:
            lb = mb

    return lb

with open("key1", "r") as f:
    n1 = int(f.readline())
with open("key2", "r") as f:
    n2 = int(f.readline())

b = (n2 - n1 - 4)
assert b % 2 == 0
b = b / 2

c = n1

D_tmp = b * b - 4 * c
D = sqrt(D_tmp)
assert D_tmp == D * D

tmp = b + D
assert tmp % 2 == 0

p, q = (b + D) / 2, (b - D) / 2

assert p * q == n1 # 因数分解できちゃった


# あとはやるだけ
e = long(65537)
d1 = inverse(e, (p-1)*(q-1))
d2 = inverse(e, (p+1)*(q+1))
rsa1 = RSA.construct((n1, e, d1))
rsa2 = RSA.construct((n2, e, d2))

with open("encrypted", "rb") as f:
    enc = int(f.read().strip("\n"))

tmp = rsa2.decrypt(enc)
flag = rsa1.decrypt(tmp)
print(long_to_bytes(flag))
