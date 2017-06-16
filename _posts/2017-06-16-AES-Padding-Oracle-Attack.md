---
layout: post
title:  "Padding Oracle Attack"
date:   2017-06-16 00:00
categories: crypto
---

# 第６回CTF分科会資料

今日は先週に引き続きAES暗号関連の分野について見ていくことにする。先週は、AES暗号を実装したが、実はあれだけでは、少し足りない部分がある。というのも、やってみてわかると思うが、先週、暗号化できるのは16バイトまでのデータだけで、それより小さくても、大きくても暗号化ができない状態になっていて、これでは、いつも使うようなAES暗号とは程遠い。

ここで当然おもいつくのは、$16 \times k$バイトになるようにパッディングしたのちに、16バイトごとにAES暗号をかけて、それを送信するという方針である。しかし、これは果たして安全なのだろうか？今日は、いくつかのブロック暗号のモードについて見て行ったのち、これらに関連するCTFの問題について見ていくことにする。

## ブロック暗号

ブロック暗号とは、ある固定された長さの平文を同じ長さの平文に暗号化する暗号のことである。より厳密に言えば、平文の要素となりうる全ての集合をアルファベットとよび、これを $\Sigma$とかくとき、$E:\Sigma^n \longrightarrow \Sigma^n$となる全単射な暗号化関数と復号化関数(E, D)の組みが存在するようなものを言う。

この時、ブロック暗号では、固定長の長さの文字列しか暗号化することができない。これでは不便であるため、これを拡張するために、長い文字列をブロック長に分けて暗号化する方針がいくつかある。これについて説明する。

## ECBモード

もっとも愚直な方針。固定長lのブロック暗号に対して、平文を適当なPadding方法で長さlの倍数になるようにpadを追加したのち、lごとにブロックにわけ、それらに対して、順番に暗号化を実行する。

<div class="kwout" style="text-align: center;"><img src="http://kwout.com/cutout/u/ij/d6/t94_bor.jpg" alt="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation" title="Block cipher mode of operation - Wikipedia" width="599" height="378" style="border: none;" usemap="#map_uijd6t94" /><map id="map_uijd6t94" name="map_uijd6t94"><area coords="44,273,494,284" href="https://en.wikipedia.org/wiki/File:ECB_decryption.svg" alt="" shape="rect" /><area coords="44,86,494,97" href="https://en.wikipedia.org/wiki/File:ECB_encryption.svg" alt="" shape="rect" /></map><p style="margin-top: 10px; text-align: center;"><a href="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation">Block cipher mode of operation - Wikipedia</a> via <a href="http://kwout.com/quote/uijd6t94">kwout</a></p></div>

この方針は、多くの問題を有している。例えば、他の任意のブロックに依存しないため暗号文の順序を任意に変更することができてしまう。同じ鍵で暗号化した異なる文章を用いて、特定のブロックを書き換えることもでき、何もしなければこの改変に、通信者は気づくことができない。

## CBC モード

CBCモードとは上記したECBモードの欠点を補い、またある暗号のブロックがそれ以前のブロックに依存するようにすることで、同じ文章のブロックがあっても同じようには変換されず、また同じ文章を二度暗号化されても、ivが異なれば全く異なる暗号文が出力されるように、修正したものである。

このモードはあとで説明するPadding Oracle Attackという攻撃手法に弱く、しかししばしば用いられてきた手法（今でもかなり使われている？）なので、CTFでよく出る。

2014年のPOODLEというSSL v3の脆弱性は、このPadding Oracle Attackに基づいている。

参考：
[ももいろテクノロジー](http://inaz2.hatenablog.com/entry/2015/12/23/000923)
[POODLEに関する記事](http://developers.mobage.jp/blog/poodle)

具体的には、

<div class="kwout" style="text-align: center;"><img src="http://kwout.com/cutout/b/7n/nk/nif_bor.jpg" alt="https://ja.wikipedia.org/wiki/%E6%9A%97%E5%8F%B7%E5%88%A9%E7%94%A8%E3%83%A2%E3%83%BC%E3%83%89#Cipher_Block_Chaining_.28CBC.29" title="暗号利用モード - Wikipedia" width="503" height="391" style="border: none;" usemap="#map_b7nnknif" /><map id="map_b7nnknif" name="map_b7nnknif"><area coords="3,105,453,116" href="https://ja.wikipedia.org/wiki/%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB:CBC_encryption.svg" alt="" shape="rect" /><area coords="3,292,453,304" href="https://ja.wikipedia.org/wiki/%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB:CBC_decryption.svg" alt="" shape="rect" /></map><p style="margin-top: 10px; text-align: center;"><a href="https://ja.wikipedia.org/wiki/%E6%9A%97%E5%8F%B7%E5%88%A9%E7%94%A8%E3%83%A2%E3%83%BC%E3%83%89#Cipher_Block_Chaining_.28CBC.29">暗号利用モード - Wikipedia</a> via <a href="http://kwout.com/quote/b7nnknif">kwout</a></p></div>

Wikipediaに詳しいが、要するに、暗号化する時に、一つ前の暗号化済みブロックとのxorをとってから暗号化をしようというのがこの方針である。

これについて簡単な置換暗号で、実装をしたものが[docs/06/block.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/06/block.py)である。


## その他のモード

詳細は省略するが、[Block_cipher_mode_of_operation - Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)を見ると、上の他にいくつか、有名なブロック暗号のモードがあるとわかる。これらはどれも、どのデータをどのタイミングでxorして混ぜるか、の違いで並列性や誤りが連鎖的に発生しないなどの違いが生じるが、こまごまやっていてもつまらないので、とりあえずスルーする。

ofbモードとcfbモードについては実装をしてみたので、[docs/06/block.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/06/block.py)をみて欲しい。



## AESへの適用

　前回実装したAES暗号をCBCモードで実行できるように実装したものが、[docs/06/aes_cbc.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/06/aes_cbc.py)である。

　やったこととしては、データをパディングして、16バイトの倍数にしたところで、それぞれのブロックをCBCモードに基づいて暗号化したものを出力するようにしただけである。

　ここで、パディングの方法をどのようにとるのかが重要となる。ここではよく使われるPKCS7Paddingというものについて説明する。

参考
[What Is PKCS5Padding](http://www.herongyang.com/Cryptography/DES-JDK-What-Is-PKCS5Padding.html)

簡単に言えば、長さlのバイト列sについて(128bitなら)16で割ったあまりをmとすると、mが0ならm=16、それ以外ならそのままととって、m個分sの末尾にmというデータを追加する。つまり、どのような長さであっても末尾にPaddingが来るようになっている。

具体的には、例えば、[1,2,3,4,5,6,7,8,9,10,11,12,13,14]という列は長さが16で割って2余るので、末尾に[2,2]をくっつけて、[1,2,3,4,5,6,7,8,9,10,11,12,13,14,2,2]というデータを作る。また、

$$
[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
$$

のようなデータに対しては、$[16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16]$というデータを末尾に追加し

$$
[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16]
$$

というデータをつくってこれを暗号化に用いる。

## Padding Oracle Attack

非常に有名なPadding Oracle Attackという攻撃手法について説明する。

参考：
[ももいろテクノロジー](http://inaz2.hatenablog.com/entry/2015/12/23/000923)
[人素（とーしろー）の物思い](http://d.hatena.ne.jp/tooshiroo/20121103/p1)

あたりが日本語で参考になる。以下の文章は上の下位互換かもしれないけど僕の理解の整理のためなのでまぁ許して。

攻撃の状況としては、

* パディングがPKCS7に従っている
* ブロック暗号のモードがCBCである
* 送った暗号文のPaddingが正しいかどうか？　
* 何回でも暗号文の送信が可能か？

の二条件が必要となる。これが満たされている場合、Padding Oracle Attackが可能となる。

まず、攻撃の概要について説明する。我々は、Encryptedデータ、$encrypted$を保持している。このとき、例えば鍵の長さが128bitのAESの場合、16文字ごとにブロックが構成される。このブロックを前から$C\_1, C\_2, \cdots C\_n$とおく。同様に、平文については、$P\_1, P\_2, \cdots P\_n$とする。また暗号化関数をE、復号化関数をDとおく。すると次のような式が成り立つ（ただし+は全てxor)

$$
C\_1 = E(P\_1 + IV)\\\
C\_2 = E(P\_2 + C\_1)\\\
\vdots\\\
C\_k = E(P\_k + C\_{k-1})\\\
\vdots\\\
C\_n = E(P\_n + C\_{n-1})
$$

当然復号化は
$$
P\_1 = D(C\_1) + IV\\\
P\_2 = D(C\_2) + C\_1\\\
\vdots\\\
P\_k = D(C\_k) + C\_{k-1}\\\
\vdots\\\
P\_n = D(C\_n) + C\_{n-1}
$$

当然だが、鍵が（IVはわかったりわからなかったりすると思うが）、わからない状態でこの復号化を実行することはできない。しかし、上記した、パディングが適正か？を判定することができる場合、次のように考えることができる。

まず、$P\_k(k>1)$ の末尾1バイトについて考えると、末尾1バイトのみがpadとなっているようなとき、padの値は0x1である。ところで、上の式からもわかるように、CBCモードでは、ある暗号文ブロック$C\_k$は$C\_{k-1}$からしか影響を受けない。つまり、$C\_{k-1}$を恣意的に設定することで、$P'\_k = D(C\_k) + C'\_{k-1}$の末尾を適正なpadとなるような値に設定することができる。

つまり、これが成立するような $C^{1}\_{k-1}$ がとれるとき、次が成り立つ

$$
\begin{eqnarray}
P^{1}\_{k} &=& D(C\_k^{1}) + C^{1}\_{k-1}\\\
           &=& D(E(P\_k + C\_{k-1})) + C^{1}\_{k-1}\\\
           &=& P\_k + C\_{k-1} + C^{1}\_{k-1}
\end{eqnarray}
$$
ここで $P\_{k}^{1}$ は末尾が0x1である。つまり、末尾の1バイトについてここから逆算すると、

$$
P\_k = C\_{k-1} + C^{1}\_{k-1} + P^{1}\_{k}
$$
が成立する。これを末尾2,3,4..16バイトに順番に計算することで元の平文を復元することができる（鍵なしで！）

## 実践

これを実際に実践するために、github上に[serverプログラム](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/06/server.py)を作成した。今僕のパソコンでこのプログラムが動いている（やや恣意的だが）。このプログラムを攻撃して、鍵を使わずに復号してほしい。

