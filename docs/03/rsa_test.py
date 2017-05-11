# coding:utf-8
from __future__ import print_function
from Crypto.Util.number import *

def str2long(s):
    ret = 0
    for x in map(ord, s):
        ret = ret * 256 + x
    return ret

def long2str(x):
    ret = ""
    while x > 0:
        val = x % 256
        ret = chr(val) + ret
        x /= 256
    return ret

# sorry...
def gen_two_primes(N):
    return getPrime(N), getPrime(N)

def egcd(a, b):
    x_a, x_b = 1, 0
    y_a, y_b = 0, 1
    n = 1
    while True:
        q = a / b
        r = a % b
        if r == 0:
            break
        a, b = b, r
        x_b, x_a = x_a + q * x_b, x_b
        y_b, y_a = y_a + q * y_b, y_b
        n += 1

    return ((-1) ** n) * x_b, ((-1) ** (n + 1)) * y_b


def inv(x, mod):
    ret, _ = egcd(x, mod)
    return ret % mod

def pow_bin(m, e, N):
    ret = 1
    while e > 0:
        if e & 1:
            ret = (ret * m) % N
        m = (m * m) % N
        e = e >> 1
    return ret

if __name__ == '__main__':
    print("[Input]: ",)
    m = str2long(raw_input())

    p, q = gen_two_primes(1024)
    N = p * q
    e = 0x10001  # famous prime
    phi = (p - 1) * (q - 1)
    d = inv(e, phi)

    private_key = (p, q, d)
    public_key = (N, e)

    print("[Public key]")
    print(public_key)

    print("[Private key]")
    print(private_key)

    # This pow_bin can be achieved by standard pow
    # pow_bin implementation is for practice
    c = pow_bin(m, e, N)
    print(c)

    m2 = pow_bin(c, d, N)
    assert m == m2
    print(long2str(m2))
