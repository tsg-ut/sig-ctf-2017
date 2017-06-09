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
    flag = sub_bytes([1, 2, 3, 4]) == [55, 147, 79, 211]
    flag &= sub_bytes(range(64))[0] == 198
    test("sub_bytes", flag)

    flag = shift_rows(range(1, 9)) == [1, 2, 3, 4, 8, 5, 6, 7]
    test("shift_rows", flag)

    flag = mix_columns(range(16)) == [8, 9, 10, 11, 28, 29, 30, 31, 0, 1, 2, 3, 20, 21, 22, 23]
    test("mix_columns", flag)


    flag = add_round_key(range(16), [range(4), range(4), range(4), range(4)]) == [0, 0, 0, 0, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12]
    test("add_round_key", flag)

    flag = inv_mix_columns(mix_columns([1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1])) == [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1]
    test("inv_mix_columns", flag)


    flag = inv_sub_bytes(sub_bytes([1, 2, 3, 4])) == [1, 2, 3, 4]
    test("inv_sub_bytes", flag)

    flag = inv_shift_rows(shift_rows(range(1, 9))) == [1, 2, 3, 4, 5, 6, 7, 8]
    test("inv_shift_rows", flag)

    state = map(ord, "ABCDEFGHIJKLMNOP")
    key = map(ord, "moratoriummormor")
    flag = encrypt(state, key) == [102, 38, 66, 6, 127, 187, 71, 229, 18, 191, 211, 61, 159, 96, 147, 138]
    test("encrypt", flag)

    flag = decrypt(encrypt(state, key), key) == state
    test("decrypt", flag)

if __name__ == '__main__':
    checkpoint()
    print("** Result **")
    print("  ",  correct_answer, " / ", cnt - 1)
