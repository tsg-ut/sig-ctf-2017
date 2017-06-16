# coding:utf-8
from __future__ import division, print_function

def ecb(plaintexts, encryptor):
    return map(encryptor, plaintexts)

def cbc(plaintexts, encryptor, dec=False, iv=3):
    ret = [iv]
    if dec:
        tmp = [iv] + plaintexts
        for i, c in enumerate(tmp):
            if i == 0:
                continue
            ret.append(encryptor(c) ^ tmp[i-1])
    else:
        for p in plaintexts:
            ret.append(encryptor(p ^ ret[-1]))
    return ret[1:]

def sub_enc(d, encryptor, n, r):
    assert n % r == 0
    ret = 0
    for i in range(n // r):
        x = d % (1 << r)
        d = x // (1 << r)
        ret = (ret << r) + encryptor(x)
    return ret

def cfb(plaintexts, encryptor, dec=False):
    iv = 11 # 0b1011
    n = 4
    r = 2
    tmp_vec = iv
    shift = n - r
    ret = []
    for p in plaintexts:
        o = sub_enc(tmp_vec, encryptor, n, r)
        t = o >> shift
        if dec:
            m = p ^ t
            ret.append(m)
            tmp_vec = ((tmp_vec << r) ^ p) % (1 << n)
        else:
            c = p ^ t
            ret.append(c)
            tmp_vec = ((tmp_vec << r) ^ c) % (1 << n)
    return ret

def ofb(plaintexts, encryptor):
    iv = 11 # 0b1011
    n = 4
    r = 2
    tmp_vec = iv
    shift = n - r
    ret = []
    for p in plaintexts:
        o = sub_enc(tmp_vec, encryptor, n, r)
        t = o >> shift
        c = p ^ t
        ret.append(c)
        tmp_vec = o
    return ret

def str2vec(s):
    ret = []
    for c in s:
        x = ord(c)
        for i in range(4):
            tmp = x % 4
            x = x // 4
            ret.append(tmp)
    return ret

def vec2str(vec):
    assert len(vec) % 4 == 0
    s = ""
    for i in range(len(vec) // 4):
        d = vec[4*i:4*(i+1)]
        tmp = 0
        for j in range(3, -1, -1):
            tmp = tmp * 4 + d[j]
        s += chr(tmp)
    return s

def test_aes(x, iv, inv=False):
    cbc([1, 2, 3], f), invf, dec=True) == [1, 2, 3]

if __name__ == '__main__':

    s = "Hello I am moratorium08"

    vec = str2vec(s)
    print(vec2str(vec))

    replacement = [1, 2, 3, 0]
    def f(x):
        assert x >= 0 and x <= 3
        return replacement[x]

    def invf(x):
        assert x >= 0 and x <= 3
        return replacement.index(x)

    assert cbc(cbc([1, 2, 3], f), invf, dec=True) == [1, 2, 3]
    assert cfb(cfb([1, 2, 3], f), f, dec=True) == [1, 2, 3]
    assert ofb(ofb([1, 2, 3], f), f) == [1, 2, 3]

    #c = cbc(vec, f)
    #c = cfb(vec, f)
    c = ofb(vec, f)
    print(vec2str(c))
    #m2 = cbc(c, invf, dec=True)
    #m2 = cfb(c, f, dec=True)
    m2 = ofb(c, f)
    print(vec2str(m2))
