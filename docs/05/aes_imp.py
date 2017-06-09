# coding:utf-8
from __future__ import print_function, division
from tools import mul, add, inv, num2vec, vec2num, gal_mul, str2vec
from constants import A, Ainv, c, rcon, Mat_C, inv_Mat_C
from check import checkpoint


def sub_bytes(state):
    ret = []
    for b in state:
        binv = inv(b)
        v = num2vec(binv)
        ret.append(vec2num(add(mul(A, v), c)))
    return ret


def inv_sub_bytes(state):
    ret = []
    for b in state:
        v = num2vec(b)
        tmp = add(v, c)  # b - c = b + c = Ab^-1
        tmp = mul(Ainv, tmp)
        ret.append(inv(vec2num(tmp)))
    return ret

assert inv_sub_bytes(sub_bytes([1, 2, 3, 4])) == [1, 2, 3, 4]


def shift_rows(state):
    assert len(state) % 4 == 0
    ret = []
    for i in range(len(state) // 4):
        vec = [state[4*i + ((0 - i) % 4)],
               state[4*i + ((1 - i) % 4)],
               state[4*i + ((2 - i) % 4)],
               state[4*i + ((3 - i) % 4)]]
        ret.extend(vec)
    return ret

assert shift_rows(range(1, 9)) == [1, 2, 3, 4, 8, 5, 6, 7]


def inv_shift_rows(state):
    assert len(state) % 4 == 0
    ret = []
    for i in range(len(state) // 4):
        vec = [state[4*i + ((0 + i) % 4)],
               state[4*i + ((1 + i) % 4)],
               state[4*i + ((2 + i) % 4)],
               state[4*i + ((3 + i) % 4)]]
        ret.extend(vec)
    return ret

assert inv_shift_rows(shift_rows(range(1, 9))) == [1, 2, 3, 4, 5, 6, 7, 8]

def mix_columns(state):
    # 128 bit only
    assert len(state) == 16
    state = state[:]
    for i in range(4):
        vec = []
        for j in range(4):
            vec.append(state[4 * j + i])
        for k in range(4):
            tmp = 0
            for l in range(4):
                tmp = tmp ^ gal_mul(Mat_C[k][l], vec[l])
            state[4 * k + i] = tmp
    return state


def inv_mix_columns(state):
    # 128 bit only
    assert len(state) == 16
    state = state[:]
    for i in range(4):
        vec = []
        for j in range(4):
            vec.append(state[4 * j + i])
        for k in range(4):
            tmp = 0
            for l in range(4):
                tmp = tmp ^ gal_mul(inv_Mat_C[k][l], vec[l])
            state[4 * k + i] = tmp
    return state


assert inv_mix_columns(mix_columns([1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1])) == [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1]

def add_round_key(state, w):
    w = reduce(lambda x, y: x + y, w, [])
    assert len(state) == len(w)
    return [x ^ y for (x, y) in zip(state, w)]


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

    #ret.append(vec2num(add(mul(A, v), c)))
    for i in range(len(ret), Nb * (Nr + 1)):
        tmp = ret[-1]
        if (i % Nk) == 0:
            tmp = subword(rotword(tmp))
            tmp[0] = tmp[0] ^ rcon[i // Nk]
        elif (Nk > 6 and (i % Nk) == 4):
            tmp = subword(tmp)
        tmp2 = []
        for j in range(4):
            tmp2.append(ret[i - Nk][0] ^ tmp[0])
        ret.append(tmp)
    return ret

k = key_expansion(range(1, 17), 4, 10)
assert len(k) == 44

Nr = 10
Nk = 4
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
