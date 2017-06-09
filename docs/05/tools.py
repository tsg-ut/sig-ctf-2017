# coding:utf-8
from constants import inv_mat


# Aとvはともに1ビットの値をもつ、行列とベクトルである。つまり、
# A = [[1, 0, ], [1, 1]]
# v = [1, 1]
# のようなことである。これらに対して演算Avを行い、その配列を返す。
def mul(A, v):
    ret = []
    for i in range(len(A)):
        tmp = 0
        for j in range(len(A)):
            tmp = tmp ^ (A[i][j] * v[j])
        ret.append(tmp)
    return ret


# 上記したような設定で、ベクトルの足し算（排他的論理和）を行う
def add(v1, v2):
    ret = []
    for i in range(len(v1)):
        ret.append(v1[i] ^ v2[i])
    return ret


# GF(2^8)上に置ける値bに対する逆数を返す
def inv(b):
    return inv_mat[b]


# 数をビットベクトルに変換する
def num2vec(b):
    l = map(int, bin(b)[2:])
    return (8 - len(l)) * [0] + l

# ビットベクトルを数に変換する
def vec2num(v):
    return int(''.join(map(str, v)), 2)

# 文字列を数を入れた配列に変換する
def str2vec(s):
    return map(ord, s)



# https://en.wikipedia.org/wiki/Finite_field_arithmetic#Rijndael.27s_finite_field
# 有限体上におけるa, bのかけ算を行う
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
