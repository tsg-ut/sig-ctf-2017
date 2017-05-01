# Sig-CTF-2017

また、削ぎ落としたツール群は、僕が知っていて、今回の分科会で使いうるもの、かつ、bin/pwn/cryptoで使うもの、に限定したので、こんな有用なツール消してるじゃん、みたいなことがあれば僕に使い方を教えてくれると助かります

## 資料

* [１回](https://github.com/tsg-ut/sig-ctf-2017/tree/master/docs/01)
* [２回](https://github.com/tsg-ut/sig-ctf-2017/tree/master/docs/02)


# Usage

## Vagrant

### Setup
次のものをとりあえず入れます
* Vagrant
* Virtualbox

その後

```
$ git clone https://github.com/tsg-ut/sig-ctf-2017
$ cd sig-ctf-2017
$ vagrant up
```

でツール群が入ります。vagrantで起動した仮想環境に接続するには、

### Usage

```
$ vagrant ssh
```

### Destroy

環境を消す

```
$ vagrant destroy
```
