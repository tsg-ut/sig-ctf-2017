#!/bin/bash

mkdir problems
cd problems

mkdir problem1
wget https://github.com/TokyoWesterns/twctf-2016-problems/raw/master/Twin%20Primes/attachments/twin-primes.7z-39a1a147cbf55d4d944f8eacdbdf4ee7a967dd70ef0eaaa0a1cee5c58c641483 -O twin-primes.7z

7z e twin-primes.7z -oproblem1
mv twin-primes.7z problem1

cd ../


