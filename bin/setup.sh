#!/bin/bash
sudo apt-get update
sudo apt-get -fuy -o Dpkg::Options::='--force-confold' install git
git clone https://github.com/zardus/ctf-tools.git /home/vagrant/ctf-tools/

cd "/home/vagrant/ctf-tools/bin"
BASE_ADDR="/home/vagrant/ctf-tools/"
PREFIX="/install"

lines=(
#"angr"
#"bindead"
#"checksec"
#"df"
#"gdb-heap"
#"gdb"
#"hash-identifier"
#"hashpump-partialhash"
#"hashpump"
#"libheap"
#"peda"
#"pwndbg"
"pwntools"
#"python-paddingoracle"
#"python-pin"
#"rp++"
)

sudo apt-get install build-essential g++
sudo apt-get -y install python2.7 python-pip python-dev libssl-dev libffi-dev
sudo apt-get -y install python3-pip
sudo pip install virtualenv virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh

export PATH=/home/vagrant/ctf-tools/bin/:$PATH
echo "export PATH=\"/home/vagrant/ctf-tools/bin:\$PATH\"" >> ~/.bashrc
echo "source ctf-tools-venv-activate" >> ~.bashrc



# IFS=$'\n' lines=($(cat tool_list))
for line in ${lines[@]}; do
    ret=$BASE_ADDR$line$PREFIX
    $ret
done
