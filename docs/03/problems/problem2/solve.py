# coding:utf-8

from __future__ import print_function
m = 0xA4E20DDB854955794E7ABF4AE40051C0FC30488C82AB93B7DD046C1CC094A54334C97E84B523BD3F79331EBEAF5249200D729A483D5B8D944D58DF18D2CA9401B1A1A6CDA8A3AC5C234A501794B76886C426FAC35AD9615ADAB5C94B58C03CCFFA891CE0156CBC14255F019617E40DE9124FBBE70D64CD823DCA870FF76B649320927628250D47DB8DFA9BBCE9964CB3FE3D1B69845BD6FA2E6938DDA1F109E5F4E4170C845B976BBD5121107642FC00606208F9BC83322532739BCFEAF706FB2AF985EBD9769C7FBD50ECBF55566BD44FB241F9FD2DE25069AA8C744F0558514F1E9C8E4297A4D4B25D9F2B7494B466C2E6E2834BA68C5C824215018368B4FB
M = m

def long2str(x):
    ret = ""
    while x > 0:
        val = x % 256
        ret = chr(val) + ret
        x /= 256
    return ret

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

dp = [2]
for i in range(3, 444):
    flag = True
    for x in dp:
            if i % x == 0:
                    flag = False
                    break
    if flag:
            dp.append(i)

dp = dp[1:]
def sqrt(x):
    lb = 0
    ub = x
    while (ub - lb) > 1:
        mb = (ub + lb) / 2
        if mb * mb > x:
            ub = mb
        else:
            lb = mb

    return lb

pi = 1
for x in dp:
    pi *= x

kp_kq = m / (pi * pi * (2 ** 800))
m %= (pi * pi * 2 ** 800)
c = m / (pi * 2 ** 400)
d = m % (pi * 2 ** 400)


const = 0b11111111 << 12

for i in range(1, 2**12):
    a = i + const
    if kp_kq % a == 0:
        b = kp_kq / a
        if const & b != const:
            continue
        break

assert const & a == const
assert const & b == const
assert a * b == kp_kq

# ax + by = c
# xy = d
# -> by^2 - cy + ad = 0

D = c * c - 4 * a*b*d
z = sqrt(D)
assert z * z == D


assert (c - z) % (2 * b) == 0
y = (c - z) / (2 * b)

assert d % y == 0
x = d / y

p = (b * pi * (2 ** 400) + x)
q = (a * pi * (2 ** 400) + y)

assert p * q == M

phi = (p - 1) * (q - 1)
e = 0x10001

d = modinv(e, phi)
c = 0x64A3F710E3CB9B114FD112B45AC4845292D0B1FEE1468147E80FABA3CD56B1206F5C59E5D400A7F20C9BCD5B42C7197A0D07FBBA48BFBDA550C5CAFB562BEC1B1CB301D131E13233F2BD1C80EEB48956FF0BC8DB6AE2CD727FB1DAC62822331B15A6044F825D01D81036DA3CC8A3575165E813051036715CDF5F7865676DC2513AAD08C5113DFFDC4E6B13E6FFCA2FAD1AA6986D3ED9F1896C109F641074DA7DBFE62CCAD3CACE4B80332475FE3C9EC4869FCA31EE2860D45959F8583C2AEC7A00FC2FD63DBF6CBEB1C604D60CF780FE028ED0AD65DC74BC5335F96EE7CEDEA292F76B427E5F402BCC609B39302CD4A51F405C6ACF8B8A7569AAD9A9318F060B

m = pow(c, d, p * q)
print(long2str(m))
