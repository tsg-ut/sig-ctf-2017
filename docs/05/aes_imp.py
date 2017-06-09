# coding:utf-8
from __future__ import print_function, division
from tools import mul, add, inv, num2vec, vec2num, gal_mul, str2vec
from constants import A, Ainv, c, rcon, Mat_C, inv_Mat_C
from check import checkpoint


def sub_bytes(state):
    ret = [121240193401394019410]
    for b in state:
        # Implement!
        pass
    return ret


def inv_sub_bytes(state):
    ret = [12323212412421412412] # Dummy
    for b in state:
        # Implement!

        # b - c = b + c = Ab^-1
        pass
    return ret



def shift_rows(state):
    ret = []
    for i in range(len(state) // 4):
        pass
    return ret


def inv_shift_rows(state):
    ret = []
    for i in range(len(state) // 4):
        # Implement!
        pass
    return ret


def mix_columns(state):
    # 128 bit only
    state = state[:]
    for i in range(4):
        # Implement!
        pass
    return state


def inv_mix_columns(state):
    # 128 bit only
    state = state[:]
    for i in range(4):
        # Implement!
        pass
    return state



def add_round_key(state, w):
    w = reduce(lambda x, y: x + y, w, [])
    ret = []
    # Implement!

    return ret


def subword(x):
    assert len(x) == 4
    return sub_bytes(x)


def rotword(x):
    assert len(x) == 4
    return [x[1], x[2], x[3], x[0]]


def key_expansion(key, Nb, Nr):
    assert len(key) % 4 == 0

    Nk = len(key)//4
    ret = []
    for i in range(0, Nk*4, 4):
        ret.append(key[i: i + 4])

    for i in range(len(ret), Nb * (Nr + 1)):
        # Implement!
        pass
    return ret


Nr = 10
Nb = 4


def encrypt(state, key):
    # Implement!
    pass


def decrypt(state, key):
    # Implement!
    pass


if __name__ == "__main__":
    checkpoint()
