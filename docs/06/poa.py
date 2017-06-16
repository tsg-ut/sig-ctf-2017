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
    # print(ret)
    return ret[:4] == "True"

s = "gINabWwYFPehHNZv56TWeGeg/Pa6dxDdKjN1Bq0+TYfnAFxd08c0AmVWGalPzFTFf7b27jJx2kxpSKdQuBbGd4r2GuLalTVM/S3RSGr0aOo="

encrypted = b64.b64decode(s)

