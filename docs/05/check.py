# coding:utf-8
from __future__ import print_function, division
from aes_imp import *

cnt = 1
correct_answer = 0
def test(s, flag):
    global cnt, correct_answer
    print(cnt, s, end="...")
    if flag:
        print("Succeeded!")
        correct_answer += 1
    else:
        print("Failed.")
    cnt += 1


def checkpoint():
    try:
        flag = sub_bytes([1, 2, 3, 4]) == [55, 147, 79, 211]
        flag &= sub_bytes(range(64))[0] == 198
    except:
        flag = False
    test("sub_bytes", flag)

    try:
        flag = shift_rows(range(1, 9)) == [1, 2, 3, 4, 8, 5, 6, 7]
    except:
        flag = False
    test("shift_rows", flag)

    try:
        flag = mix_columns(range(16)) == [8, 9, 10, 11, 28, 29, 30, 31, 0, 1, 2, 3, 20, 21, 22, 23]
    except:
        flag = False
    test("mix_columns", flag)

    try:
        k = key_expansion(range(1, 17), 4, 10)
        flag = [66, 157, 71, 129] == k[4]
        flag &= [71, 155, 64, 137] == k[5]
    except:
        flag = False
    test("key_expansion", flag)

    try:
        flag = add_round_key(range(16), [range(4), range(4), range(4), range(4)]) == [0, 0, 0, 0, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12]
    except:
        flag = False
    test("add_round_key", flag)

    try:
        flag = inv_mix_columns(mix_columns([1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1])) == [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1]
    except:
        flag = False
    test("inv_mix_columns", flag)

    try:
        flag = inv_sub_bytes(sub_bytes([1, 2, 3, 4])) == [1, 2, 3, 4]
    except:
        flag = False
    test("inv_sub_bytes", flag)

    try:
        flag = inv_shift_rows(shift_rows(range(1, 9))) == [1, 2, 3, 4, 5, 6, 7, 8]
    except:
        flag = False
    test("inv_shift_rows", flag)

    try:
        state = map(ord, "ABCDEFGHIJKLMNOP")
        key = map(ord, "moratoriummormor")
        flag = encrypt(state, key) == [202, 244, 61, 176, 117, 75, 101, 85, 160, 208, 75, 109, 240, 198, 240, 229]
    except:
        flag = False
    test("encrypt", flag)

    try:
        flag = decrypt(encrypt(state, key), key) == state
    except:
        flag = False
    test("decrypt", flag)

if __name__ == '__main__':
    checkpoint()
    print("** Result **")
    print("  ",  correct_answer, " / ", cnt - 1)
