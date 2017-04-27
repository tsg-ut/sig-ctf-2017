# coding:utf-8
from cipher import decrypt, shift
import copy

key = "3feVJy69imM"
filename = "encrypted.txt"

encrypted = open(filename, "r").read()[:-3]

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
bases = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
ub = 126
lb = 32

available_keys = []

for keylength in range(5, 15):
    flag = True
    key_l = [list(chars[:]) for i in range(keylength)]
    for i in range(0, len(encrypted) - 2, 4):
        x = encrypted[i]
        tmp = key_l[i % keylength]
        for char in tmp[:]:
            a = shift(x, char, rev=True)
            idx = bases.index(a)
            if idx & 0b100000 != 0:
                tmp.remove(char)
                if len(tmp) == 0:
                    flag = False
                    break
            elif idx <= 7:
                tmp.remove(char)
                if len(tmp) == 0:
                    flag = False
                    break

        x = encrypted[i+1]
        tmp2 = key_l[(i+1) % keylength]
        for char in tmp2[:]:
            a = shift(x, char, rev=True)
            idx = bases.index(a)
            if idx & 0b001000 != 0:
                tmp2.remove(char)
                if len(tmp2) == 0:
                    flag = False
                    break

        x = encrypted[i+2]
        tmp3 = key_l[(i+2) % keylength]
        for char in tmp3[:]:
            a = shift(x, char, rev=True)
            idx = bases.index(a)
            if idx & 0b000010 != 0:
                tmp3.remove(char)
                if len(tmp3) == 0:
                    flag = False
                    break
    if flag:
        available_keys.append((keylength, copy.deepcopy(key_l)))

print("Availabe key length: ", [x[0] for x in available_keys])

## この時点でkeylength = 12と確定する。

## したがって、以降のコードはkeylength = 12
## 依存である（本来なら分けてコードを書くべきだが省スペースのため
## 一つのファイルに書く(一つのスクリプトだけで答えが出るほうがかっこいいし)

keylength = 12

key_l = available_keys[0][1]

for i in range(0, len(encrypted) - 2, 4):
    c = encrypted[i+2]
    key = key_l[(i+2) % keylength][0]
    shf = shift(c, key, rev=True)

    upper_bits = bases.index(shf) & 0x11
    tmp = key_l[(i+3) % keylength]
    if upper_bits == 0:
        print(c, key, shf)
        for char in tmp[:]:
            a = shift(encrypted[i+3], char, rev=True)
            idx = bases.index(a)
            if idx < lb:
                tmp.remove(char)
    if upper_bits == 1:
        for char in tmp[:]:
            a = shift(encrypted[i+3], char, rev=True)
            idx = bases.index(a)
            if idx == 63:
                tmp.remove(char)

## 以下手動で調節
## 冒頭の""SKU iA a'JaFangse""に着目し、
## 適切なBase64を返すように調節した
tmp = key_l[7]
for char in tmp[:]:
    a = shift(encrypted[7], char, rev=True)
    if a != "z":
        tmp.remove(char)

tmp = key_l[11]
for char in tmp[:]:
    a = shift(encrypted[11], char, rev=True)
    if a != "g":
        tmp.remove(char)

tmp = key_l[3]
for char in tmp[:]:
    a = shift(encrypted[15], char, rev=True)
    if a != "w":
        tmp.remove(char)


print(key_l)
print("Key(repr):", ''.join([x[0] for x in key_l]))

