# coding:utf-8
from __future__ import print_function, division
from tools import mul, add, inv, num2vec, vec2num, gal_mul, str2vec
from constants import A, Ainv, c, rcon, Mat_C, inv_Mat_C
from check import checkpoint


def sub_bytes(state):
    ret = []
    for b in state:
        # Implement!
        ret.append(vec2num(add(mul(A, num2vec(inv(b))), c)))
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
        vec = state[4 * i:4 * (i+1)]
        for i in range(4):
            ret.append(vec[4*i: 4*(i+1)])
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


def get_word(x):
    assert len(x) == 4
    """tmp = 0
    for i in range(4):
        tmp = tmp * 256 + x[i]
    return tmp"""
    return x


def key_expansion(key, Nb, Nr):
    assert len(key) % 4 == 0

    Nk = len(key)//4
    ret = []
    for i in range(0, Nk*4, 4):
        ret.append(get_word(key[i: i + 4]))

    for i in range(len(ret), Nb * (Nr + 1)):
        # Implement!
        pass
    return ret


Nr = 10
Nb = 4


def encrypt(state, key):
    key = key_expansion(key, Nb, Nr)
    state = add_round_key(state, key[:Nb])
    for r in range(1, Nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key[r * Nb: (r + 1) * Nb])
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key[Nr * Nb:])
    return state


def decrypt(state, key):
    key = key_expansion(key, Nb, Nr)
    state = add_round_key(state, key[Nr*Nb:])
    for r in range(Nr - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, key[r * Nb: (r + 1) * Nb])
        state = inv_mix_columns(state)

    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, key[:Nb])
    return state




if __name__ == "__main__":
    checkpoint()
