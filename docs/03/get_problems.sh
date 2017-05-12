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

mkdir problem3
cd problem3

wget https://github.com/ctfs/write-ups-2015/raw/master/hack-lu-ctf-2015/crypto/creative-cheating/dump_2bd6da8de87c6f1170dec710f7268a16.pcapng

wget https://raw.githubusercontent.com/ctfs/write-ups-2015/master/hack-lu-ctf-2015/crypto/creative-cheating/README.md

cd ../

