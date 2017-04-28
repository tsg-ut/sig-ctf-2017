# coding:utf-8

import hashlib

length = 28
f = open("table").read().rstrip("\n").split("\n")
table = [[x for x in y] for y in f]

def getval(key, cipher):
    for i,x in enumerate(table[0]):
        if x == key:
            col  = i

    for i in range(length):
        if table[i][col] == cipher:
            wei = i

    return table[0][wei]

def main():

    s = "VIGENERE"
    c ="LMIG}RPEDOEE"
    c2 = "WKJIQIWKJWMN"
    c3 = "DTSR}TFVUFWY"
    c4 ="OCBAJBQ"
    hash_ = "f528a6ab914c1ecf856a1d93103948fe"

    al = table[0]

    for i in range(28):
        for j in range(28):
            for k in range(28):
                for l in range(28):
                    val = ''.join([al[i],al[j],al[k],al[l]])
                    key = s + val
                    ret1 = ''.join([getval(key[i], c[i]) for i in range(len(c))])
                    ret2 = ''.join([getval(key[i], c2[i]) for i in range(len(c2))])
                    ret3 = ''.join([getval(key[i], c3[i]) for i in range(len(c3))])
                    ret4 = ''.join([getval(key[i], c4[i]) for i in range(len(c4))])

                    ret = ''.join([ret1, ret2, ret3, ret4])

                    if hashlib.md5(ret.encode('utf-8')).hexdigest() == hash_:
                        print(ret)
                        return

if __name__ == '__main__':
    main()
