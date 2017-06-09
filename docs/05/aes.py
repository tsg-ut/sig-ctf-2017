# coding:utf-8
from __future__ import print_function, division

def mul(A, v):
    ret = []
    for i in range(len(A)):
        tmp = 0
        for j in range(len(A)):
            tmp = tmp ^ (A[i][j] * v[j])
        ret.append(tmp)
    return ret

def add(v1, v2):
    ret = []
    for i in range(len(v1)):
        ret.append(v1[i] ^ v2[i])
    return ret

# 暗号理論入門p142
A = [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1]
    ]
Ainv = [
        [1,0,0,1,0,0,1,0],
        [0,1,1,1,0,1,1,1],
        [0,0,1,1,1,1,1,0],
        [0,0,0,1,0,0,1,1],
        [1,0,1,1,0,1,1,1],
        [0,1,0,1,1,1,1,0],
        [1,1,0,0,0,1,1,0],
        [0,0,1,1,1,1,0,1]
        ]
c = [1, 1, 0, 0, 0, 1, 1, 0]

binv = [1, 1, 1, 1, 0, 1, 1, 0]


#print(mul(A, binv))
#print(add(mul(A, binv), c))


inv_mat = [0, 1, 141,246,203,82,123,209,232,79,41,192,176,225,229,199,116,180,170,75,153,43,96,95,88,63,253,204,255,64,238,178,58,110,90,241,85,77,168,201,193,10,152,21,48,68,162,194,44,69,146,108,243,57,102,66,242,53,32,111,119,187,89,25,29,254,55,103,45,49,245,105,167,100,171,19,84,37,233,9,237,92,5,202,76,36,135,191,24,62,34,240,81,236,97,23,22,94,175,211,73,166,54,67,244,71,145,223,51,147,33,59,121,183,151,133,16,181,186,60,182,112,208,6,161,250,129,130,131,126,127,128,150,115,190,86,155,158,149,217,247,2,185,164,222,106,50,109,216,138,132,114,42,20,159,136,249,220,137,154,251,124,46,195,143,184,101,72,38,200,18,74,206,231,210,98,12,224,31,239,17,117,120,113,165,142,118,61,189,188,134,87,11,40,47,163,218,212,228,15,169,39,83,4,27,252,172,230,122,7,174,99,197,219,226,234,148,139,196,213,157,248,144,107,177,13,214,235,198,14,207,173,8,78,215,227,93,80,30,179,91,35,56,52,104,70,3,140,221,156,125,160,205,26,65,28]
def inv(b):
    return inv_mat[b]

def num2vec(b):
    l = map(int, bin(b)[2:])
    return (8 - len(l)) * [0] + l

def vec2num(v):
    return int(''.join(map(str, v)), 2)

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
        tmp = add(v, c) #b - c = b + c = Ab^-1
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

assert shift_rows([1,2,3,4,5,6,7,8]) == [1, 2, 3, 4, 8, 5, 6, 7]

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


# https://en.wikipedia.org/wiki/Finite_field_arithmetic#Rijndael.27s_finite_field
def gal_mul(a, b):
    p = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        b = b >> 1
        carry = a & 0b10000000
        a = a << 1
        if carry == 0b10000000:
            a ^= 0x1b
    return p % 256


# Rijndael Mix Columns
Mat_C = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
        ]
# https://en.wikipedia.org/wiki/Rijndael_mix_columns#InverseMixColumns
inv_Mat_C = [
        [14, 11, 13, 9],
        [9, 14, 11, 13],
        [13, 9, 14, 11],
        [11, 13, 9, 14]
        ]
def mix_columns(state):
    # 128 bit only
    assert len(state) == 16
    state = state[:]
    for i in range(4):
        vec = []
        for j in range(4):
            vec.append(state[4 * j + i])
        ret = []
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
        ret = []
        for k in range(4):
            tmp = 0
            for l in range(4):
                tmp = tmp ^ gal_mul(inv_Mat_C[k][l], vec[l])
            state[4 * k + i] = tmp
    return state

assert inv_mix_columns(mix_columns([1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2,
    1])) == [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1]

def add_round_key(state, w):
    w = reduce(lambda x, y: x + y, w, [])
    assert len(state) == len(w)
    return [x ^ y for (x, y) in zip(state, w)]

#assert (add_round_key([1,2,3,4], [5,6,7,8])) == [4, 4, 4, 12]

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

#assert hex(get_word([0xde, 0xad, 0xbe, 0xef])) == "0xdeadbeef"

# https://en.wikipedia.org/wiki/Rijndael_key_schedule
rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d
]

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

def encrypt(state, key):
    #state = map(ord, "ABCDEFGHIJKLMNOP")
    Nr = 10
    Nk = 4
    Nb = 4
    key = key_expansion(key, Nb, Nr)
    state = add_round_key(state, key[:Nb])
    for r in range(1, Nr):
        #print(state, len(state))
        state = sub_bytes(state)
        #print("sub_bytes", state, len(state))
        state = shift_rows(state)
        #print("shift_rows", state, len(state))
        state = mix_columns(state)
        #print("mix_col", state, len(state))
        state = add_round_key(state, key[r * Nb: (r + 1) *Nb])
        #print("addr", state, len(state))

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key[Nr * Nb:])
    #print(state)
    #print(''.join(map(hex, state)).replace("0x", ""))
    return state

def decrypt(state, key):
    Nr = 10
    Nk = 4
    Nb = 4
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
    #print(state)
    #print(''.join(map(hex, state)).replace("0x", ""))
    return state



def main():
    state = map(ord, "ABCDEFGHIJKLMNOP")
    key = map(ord, "moratoriummormor")
    print("Before:", state)
    c = encrypt(state, key)
    print("After:", decrypt(c, key))



main()

