# -*- mode: ruby -*-
# vi: set ft=ruby :

$bootstrap = <<SCRIPT
sudo apt-get update
sudo apt-get -fuy -o Dpkg::Options::='--force-confold' install git

git clone https://github.com/tsg-ut/sig-ctf-2017 /home/vagrant/sig-ctf-2017
/home/vagrant/sig-ctf-2017/bin/manage-tools -s setup
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "sig-ctf-2017"
  config.vm.provision "shell", privileged: false, inline: $bootstrap
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
  end
  config.vm.network :forwarded_port, host: 3000, guest: 3000
  config.vm.network :private_network, ip: "192.168.33.10"
end
