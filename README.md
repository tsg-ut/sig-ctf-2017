# Sig-CTF-2017

## 資料

* [１回-Introduction](https://github.com/tsg-ut/sig-ctf-2017/tree/master/docs/01)
* [２回-Classical Cipher](https://github.com/tsg-ut/sig-ctf-2017/tree/master/docs/02)
* [３回-RSA](https://github.com/tsg-ut/sig-ctf-2017/tree/master/docs/03)

### 資料の綺麗な表示の仕方メモ

MathJaxがGithub上だとつらい感じになるので、例えば第三回の場合

```
https://stackedit.io/viewer#!url=https://raw.githubusercontent.com/tsg-ut/sig-ctf-2017/master/docs/03/README.md
```

のように```https://stackedit.io/viewer#!url=```をつけて、markdownのリンクを後ろにつけて表示すると綺麗に見える

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
