# coding:utf-8
from __future__ import division, print_function
import sys
sys.path.append("../05")
import aes

def num2seq(num):
    ret = []
    while num != 0:
        ret.append(num % 256)
        num = num // 256
    return ret[::-1]

def seq2num(seq):
    ret = 0
    for x in seq:
        num = x
        ret = ret * 256 + x
    return ret

assert seq2num(num2seq(0x18191a)) == 0x18191a


def enc(plain, key, iv):
    plain = list(plain)
    key = map(ord, key)
    l = len(plain)
    pad = (16 - l % 16)
    pads = [chr(pad) for i in range(pad)]
    plain.extend(pads)

    ret = [seq2num(map(ord, iv))]
    for i in range(0, len(plain), 16):
        data = seq2num(map(ord, plain[i:i+16]))
        xored = data ^ ret[-1]
        c = aes.encrypt(num2seq(xored), key)
        ret.append(seq2num(c))
    ret2 = []
    for x in ret[1:]:
        ret2.extend(num2seq(x))
    return ''.join(map(chr, ret2))


def dec(crypt, key, iv):
    crypt = list(crypt)
    key = map(ord, key)
    l = len(crypt)

    ret = []
    tmp = [seq2num(map(ord, iv))]
    for i in range(0, len(crypt), 16):
        data = seq2num(map(ord, crypt[i:i+16]))
        tmp.append(data)
    for i, c in enumerate(tmp):
        if i == 0:
            continue
        xored = seq2num(aes.decrypt(num2seq(c), key))
        c = xored ^ tmp[i - 1]
        ret.extend(num2seq(c))

    return ''.join(map(chr, ret))


if __name__ == '__main__':
    s =  "helloworldaaslkd"
    pw = "moramoramoramora"
    iv  = "abcdefhjijklmnop"

    c = enc(s, pw, iv)
    print(c)
    print(dec(c, pw, iv))
