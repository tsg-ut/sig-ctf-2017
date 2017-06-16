# coding:utf-8
from __future__ import division, print_function
from Crypto.Cipher import AES
import base64 as b64
import socket
#from server import decrypt_ok

host = "127.0.0.1"
port = 3000
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect((host, port))

def read_line(s):
    ret = ''
    while True:
        c = s.recv(1)
        if c == '\n' or c == '':
            break
        else:
            ret += c
    return ret


def decrypt_ok(s):
    r.send(b64.b64encode(s) + "\n")
    ret = read_line(r)
    print(ret)
    return ret[:4] == "True"

s = "gINabWwYFPehHNZv56TWeGeg/Pa6dxDdKjN1Bq0+TYfnAFxd08c0AmVWGalPzFTFf7b27jJx2kxpSKdQuBbGd4r2GuLalTVM/S3RSGr0aOo="

encrypted = b64.b64decode(s)

def seq2str(seq):
    return ''.join(map(chr, seq))

def set_iv_seq(seq, p, e, cnt):
    for i in range(cnt - 1):
        idx = 15 - i
        seq[idx] = cnt ^ ord(p[idx]) ^ ord(e[idx])


blocks = []
ret = ""
for i in range(len(encrypted) // 16):
    blocks.append(encrypted[16 * i : 16*(i+1)])

for k in range(1, len(blocks)):
    iv_seq = [0 for i in range(16)]
    plains = ["\x00" for i in range(16)]
    for i in range(16):
        for j in range(256):
            set_iv_seq(iv_seq, plains, blocks[k-1], i + 1)
            iv = seq2str(iv_seq)
            data = iv + blocks[k]
            if decrypt_ok(data):
                plains[15 - i] = chr(iv_seq[15 - i] ^ ord(blocks[k-1][15-i]) ^ (i + 1))
                break
            else:
                iv_seq[15 - i] += 1

    ret += ''.join(plains)
print(ret)

