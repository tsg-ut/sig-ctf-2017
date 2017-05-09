#!/bin/bash

mkdir problems
cd problems

mkdir problem1
wget https://github.com/TokyoWesterns/twctf-2016-problems/raw/master/Twin%20Primes/attachments/twin-primes.7z-39a1a147cbf55d4d944f8eacdbdf4ee7a967dd70ef0eaaa0a1cee5c58c641483 -O twin-primes.7z

7z e twin-primes.7z -oproblem1
mv twin-primes.7z problem1

mkdir problem2

wget https://github.com/ctfs/write-ups-2016/raw/master/su-ctf-2016/crypto/high-speed-rsa-keygen-150/RSA-Keygen.tar.gz

tar xvzf RSA-Keygen.tar.gz -C problem2

mv RSA-Keygen.tar.gz problem2/

wget http://files.quals.seccon.jp/AlphaComplex1.zip
unzip AlphaComplex1.zip
mv AlphaComplex1 problem3
mv AlphaComplex1.zip problem3


mkdir problem4
cd problem4
wget https://s3.amazonaws.com/hackthevote/best_rsa.878a518bf7012add6d071f3b52562e8b102e72a0cc815aee7cb007cdc03c7714.txt
cd ../
