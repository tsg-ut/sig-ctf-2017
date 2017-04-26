# coding:utf-8
import sys

key = 5

def encrypt(ipt):
    x_vec = [chr((x - 0x41 + key) % 26 + 0x41)
            for x in map(ord, ipt)
            if x > 0x40 and x < 0x5b]
    return ''.join(x_vec)


def decrypt(ipt):
    x_vec = [chr((x - 0x41 - key) % 26 + 0x41)
            for x in map(ord, ipt)
            if x > 0x40 and x < 0x5b]
    return ''.join(x_vec)


def main():
    argv = sys.argv
    if len(argv) == 1:
        return
    if argv[1] == "e":
        print("Input: ", end="")
        ipt = input().upper()
        print("Output:", encrypt(ipt))
    elif argv[1] == "d":
        print("Input: ", end="")
        ipt = input().upper()
        print("Output:", decrypt(ipt))
    else:
        return

if __name__ == '__main__':
    main()
