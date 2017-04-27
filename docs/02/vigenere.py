# coding:utf-8
import sys


if __name__ == '__main__':
    pass


init_key = "CRYPTO".upper()

def gen_key(key, length):
    len_key = len(key)
    pad = length % len_key
    return (key * (length // len_key)) + key[:pad]


def vin_crypt(ipt, decode=False):
    key = gen_key(init_key, len(ipt))

    x_vec = [x - 0x41 for x in map(ord, ipt)
            if x > 0x40 and x < 0x5b]
    key_vec = [ord(x) - 0x41 for x in key]

    if decode:
        c_vec = [(x - y) % 26 for x, y in zip(x_vec, key_vec)]
    else:
        c_vec = [(x + y) % 26 for x, y in zip(x_vec, key_vec)]
    c = ''.join([chr(x + 0x41) for x in c_vec])
    return c


def main():
    argv = sys.argv
    if len(argv) == 1:
        return
    if argv[1] == "e":
        print("Input: ", end="")
        ipt = input().upper()
        print("Output:", vin_crypt(ipt))
    elif argv[1] == "d":
        print("Input: ", end="")
        ipt = input().upper()
        print("Output:", vin_crypt(ipt, True))
    else:
        return


if __name__ == '__main__':
    main()
