# coding:utf-8
from constants import inv_mat



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
def inv(b):
    return inv_mat[b]

def num2vec(b):
    l = map(int, bin(b)[2:])
    return (8 - len(l)) * [0] + l

def vec2num(v):
    return int(''.join(map(str, v)), 2)
