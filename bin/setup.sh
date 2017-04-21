#!/bin/bash
sudo apt-get update
sudo apt-get -fuy -o Dpkg::Options::='--force-confold' install git
git clone https://github.com/zardus/ctf-tools.git /home/vagrant/ctf-tools/

cd "/home/vagrant/ctf-tools/bin"
BASE_ADDR="/home/vagrant/ctf-tools/"
PREFIX="/install"

<<<<<<< HEAD
=======
lines=(
"angr"
"bindead"
"checksec"
"df"
"gdb-heap"
"gdb"
"hash-identifier"
"hashpump-partialhash"
"hashpump"
"libheap"
"peda"
"pwndbg"
"pwntools"
"python-paddingoracle"
"python-pin"
"rp++"
)

>>>>>>> parent of 2b22ebc... Modify Typo
sudo apt-get install build-essential g++
sudo apt-get install gdb
sudo apt-get -y install python2.7 python-pip python-dev libssl-dev libffi-dev
sudo apt-get -y install python3-pip
sudo pip install virtualenv virtualenvwrapper
sudo pip install --upgrade pwntools
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh

export PATH=/home/vagrant/ctf-tools/bin/:$PATH
echo "export PATH=\"/home/vagrant/ctf-tools/bin:\$PATH\"" >> ~/.bashrc
echo "source ctf-tools-venv-activate" >> ~.bashrc

mkdir ~/programs
mkdir ~/bin

export PATH=/home/vagrant/bin/:$PATH
echo "export PATH=\"/home/vagrant/bin:\$PATH\"" >> ~/.bashrc

cd ~/programs

# peda
git clone https://github.com/longld/peda.git
echo "source ~/programs/peda/peda.py" >> ~/.gdbinit

# pwndbg
cd ~/programs
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh

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
git clone  https://github.com/slimm609/checksec.sh
mv checksec.sh ~/bin/checksec


cd ~/programs
sudo opt-get -y install libc6-dbg
wget http://pastebin.com/raw/8Mx8A1zG -O libheap.py
echo 'from .libheap import *' > __init__.py
sudo mkdir -p /usr/local/lib/python3.4/dist-packages/libheap/
sudo mv libheap.py __init__.py /usr/local/lib/python3.4/dist-packages/libheap/
echo -e 'define heap\n  python from libheap import *\nend' >> ~/.gdbinit

cd ~/programs
