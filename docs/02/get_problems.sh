#!/bin/bash

mkdir problems
cd problems

mkdir problem2
wget https://github.com/TokyoWesterns/twctf-2016-problems/raw/master/Vigenere%20Cipher/attachments/vigenere.7z-d2c5a8316dac2abcebb2b2bfe1fa2875ce69e983252e6479fcc1ededf9e7de83 -O vigenere.7z

7z e vigenere.7z -oproblem2
mv vigenere.7z problem2

cd ../

