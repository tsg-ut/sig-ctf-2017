#!/bin/bash
sudo apt-get update

sudo apt-get -y install build-essential g++
sudo apt-get -y install python2.7 python-pip python-dev libssl-dev libffi-dev
sudo apt-get -y install g++-multilib
sudo apt-get -y install gdb socat git
sudo pip install --upgrade pip
sudo pip install virtualenv virtualenvwrapper
sudo pip install --upgrade pwntools

mkdir ~/programs
mkdir ~/bin

export PATH=/home/vagrant/bin/:$PATH
echo "export PATH=\"/home/vagrant/bin:\$PATH\"" >> ~/.bashrc

cd ~/programs

# peda
git clone https://github.com/longld/peda.git
echo "source ~/programs/peda/peda.py" >> ~/.gdbinit

cd ~/programs

# rp++
wget https://github.com/downloads/0vercl0k/rp/rp-lin-x64
chmod +x rp-lin-x64
mv rp-lin-x64 ~/bin/

wget https://github.com/downloads/0vercl0k/rp/rp-lin-x86
chmod +x rp-lin-x86
mv rp-lin-x86 ~/bin/

# checksec
cd ~/programs
wget https://github.com/slimm609/checksec.sh/archive/1.6.tar.gz
tar zxvf 1.6.tar.gz
mv checksec.sh-1.6/checksec ~/bin/checksec.sh


cd ~/programs
sudo opt-get -y install libc6-dbg
wget http://pastebin.com/raw/8Mx8A1zG -O libheap.py
echo 'from .libheap import *' > __init__.py
sudo mkdir -p /usr/local/lib/python3.4/dist-packages/libheap/
sudo mv libheap.py __init__.py /usr/local/lib/python3.4/dist-packages/libheap/
echo -e 'define heap\n  python from libheap import *\nend' >> ~/.gdbinit

cd ~/programs

