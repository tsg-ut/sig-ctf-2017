---
layout: post
title:  "AES Implementation"
date:   2017-06-09 00:00
categories: crypto
---

# 第５回CTF分科会資料


AES暗号実装会の資料のまとめ。当日は資料が間に合わなかったので、口とホワイトボードで説明したが、一応自分用のメモも兼ねて、まとめておく。
当日の様子は次の様である。

![当日](https://lh3.googleusercontent.com/-DglTCid4HdM/WT-RFZeUMEI/AAAAAAAANCo/z6YTLIzVbS4SlplfLUeHcfPz32OVS3ELwCLcB/s0/Image+uploaded+from+iOS.jpg=250x"Image uploaded from iOS.jpg")


## AES暗号とは？

Advanced Encryption Standardの略。考案者はRijmenとDaemenで、元々はRijndael暗号として作り、それがAESとして規格化された。

対称鍵暗号の一つであり、対称鍵暗号としては多分最もよく使われている。[Wikipedia](https://ja.wikipedia.org/wiki/Advanced_Encryption_Standard)を見てみると、アーカイブファイルの暗号化から、TLS、無線LAN暗号化、ディスク暗号化、果てはWiiにまでととにかく、あらゆる方面で使われている。

## AES暗号関連のすでにある資料

* 日本語版Wikipediaはクソすぎてびっくりするが（だったら自分で編集すればいいのだが）、[英語版Wikipedia](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)はアルゴリズムが載っている
* [katagaitai CTF勉強会第三回の資料](https://www.slideshare.net/trmr105/katagaitai-ctf-3-crypto)
* The Design of Rijndael 開発者の書いたRijndael(AES)暗号に関する本

僕は、ブーフマンの「暗号理論入門 原書第3版」を参考に実装した。

（ところで、今ならe-Bookで買えばSpringerで1000円くらいで"The Design of Rijndael"買えました）

## AES暗号の仕組み

　SPN(Substitution Permutation Network)構造を持つ暗号で、置換と転置を繰り返すことで暗号化を行う。これらの各ステップは、（暗号操作に当然求められることであるが）全単射な計算によって実現される。具体的には、AESのアルゴリズムは、

* sub\_types
* shift\_rows
* mix\_columns
* add\_round\_key

の４つの処理に分けられる。SPN構造としては、Sにあたるのが、sub\_types、Pにあたるのがshift\_rows、mix\_columnsであり、add\_round\_keyは、鍵との演算を行う部分である。

そして、これを繰り返すことにより十分な撹拌を行い、暗号文からの平文の推定を困難にする。具体的には、128bitのAES暗号の場合は10回繰り返す（正確には最後のステップはmix\_columnsを行わない、またadd\_round\_keyは、この10回の操作の前に一度行うので計11回行う）。

全体像は、katagaitai CTFのスライドの

<iframe src="//www.slideshare.net/slideshow/embed_code/key/64h5UJ2CEVnwjv?startSlide=19" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/trmr105/katagaitai-ctf-3-crypto" title="katagaitai CTF勉強会 #3 crypto" target="_blank">katagaitai CTF勉強会 #3 crypto</a> </strong> from <strong><a target="_blank" href="//www.slideshare.net/trmr105">trmr </a></strong> </div>

がわかりやすい。なお、図のSがsub\_bytes、Permutationがshift\_rows、mix\_columnsに、そして、何も書かれていない四角の列が、add\_round\_keyに対応する。

以降これらの各ステップの詳細について説明する。

### 定数の定義

以降これらの定数は断りなく使う

$N\_b$：平文ブロックの個数。各平文ブロックは32ビット

$N\_k$：鍵となる32ビットの語の個数

$N\_r$：巡回の回数。AESでは、10, 12, 14と決められている。


### sub\_bytes

置換にあたる操作を行う。AESでは、前から順番に1バイトずつこの操作を適用していく。以降、1バイト=8ビットを取って来た時に、生成多項式$f(x) = x^8 + x^4 + x^3 + x + 1$とした時の有限体GF(2^8)（以降言及する有限体における数は全てこの有限体の元である）上における多項式の各項の係数に対応させる。

ベクトルと、8ビットの値を同一視するというのは例えば、3という数は、0b00000011と表されるが、これを各ビットを係数とした多項式$x + 1$と同一視するということである。この時3の逆数は$(x + 1)^{-1}$は、この生成多項式との拡張ユークリッドの互除法で計算可能で、$x^7 + x^6 + x^5 + x^4 + x^2 + x$であり、この時これは、ビットで表すと、0b11110110であり、これは十進法で、246である。

また、この値をビットベクトルとしてみる、というのは、単にこの0b11110110を並べた縦ベクトル

$$
(1,1,1,1,0,1,1,1,0)^T
$$

を考える、という意味である。

話題をsub\_bytesに戻すと、この処理は、各バイトを取り出してきてそれをS-boxと呼ばれる仕組みによって置換をする。具体的には、そのバイトがbという値であったとすると、次のように変換する。

$$
b' = Ab^{-1} + c
$$
$A$ : 8 x 8 の正則な定行列
$c$ : 定ベクトル

$b^{-1}$というのは、におけるb逆数であり、また、A,cとの演算は、bをビットベクトルと見たときのGF(2)における演算である。したがって、足し算は、排他的論理和と同じになる。

### shift\_rows

　入力として得られるバイト列は32ビットでアライメントされている。これをバイトの配列だと見た時、4バイト x (元のデータの長さ / 4)バイトの行列を生成する。

具体的には、

$$
(a\_0, a\_1, a\_2, a\_3, a\_4, a\_5, a\_6, a\_7, a\_8, a\_9, a\_{10}, a\_{11}, a\_{12}, a\_{13}, a\_{14}, a\_{15})
$$

というようなバイト列に対して


$$
\begin{pmatrix}
a\_0 & a\_1 & a\_2 & a\_3\\\
a\_4 & a\_5 & a\_6 & a\_7\\\
a\_8 & a\_9 & a\_{10} & a\_{11}\\\
a\_{12} & a\_{13} & a\_{14} & a\_{15}
\end{pmatrix}
$$

という行列を作る。shift\_rowsはこの行列に対して横方向のシフトを行う。具体的には、0行目は0個左へシフト、1行目は1個シフト..i行目はi個シフトという形でシフトをする。

つまり、上の行列は、

$$
A = \left(
        \begin{array}{ccc}
            a\_0 & a\_1 & a\_2 & a\_3 \\\
            a\_5 & a\_6 & a\_7 & a\_4 \\\
            a\_{10} & a\_{11} & a\_8 & a\_9 \\\
            a\_{15} & a\_{12} & a\_{13} & a\_{14}
        \end{array}
  \right)
$$

### mix\_columns

今度は先の行列に対して縦方向の混合を行う。これは、

$$
A =
\begin{pmatrix}
a\_0 & a\_1 & a\_2 & a\_3 \\\
a\_4 & a\_5 & a\_6 & a\_7 \\\
a\_8 & a\_9 & a\_{10} & a\_{11} \\\
a\_{12} & a\_{13} & a\_{14} & a\_{15}
\end{pmatrix}
$$

の各項はバイトであるので、0~255の値を持つGF(2^8)の値であると考えることができる。この行列に対して、定行列Bをかける。

$$
A \gets BA
$$

この行列計算における各かけ算と足し算が通常の四則演算ではないことに注意する。

### add\_round\_key

最後に必要となるのが、鍵との排他的論理和である。このステップによって、得られる暗号化結果が鍵を知らないと復号不可能となる。

このステップは非常に簡単で、r回目のadd\_round\_keyについて、鍵の $[r\times N\_b, (r+1)\times N\_b)$ の部分を用いて、バイトごとに排他的論理和をすればよい。

### key\_expansion

以上に加えて、add\_round\_keyで使う分だけKeyの長さを拡張する必要がある。これを行う操作が、key\_expansionである。

まず、最初にユーザーから与えられる鍵をKEYとし、この処理によって得られる拡張された鍵をEXPANDED\_KEYとする。EXPANDED\_KEYの長さは、$N\_b \times (N\_r + 1)$である。これは、add\_round\_keyの過程は、通常のSPNのラウンドに加えて最初に一度、行うためである。

このアルゴリズムは次の様である（これはもうコードを見た方が早い）

暗号理論入門より

```
KeyExpansion(byte key[4*Nk], word w[Nb*(Nr+1)], Nk)
begin
  word temp
  i = 0
  while (i < Nk)
    w[i] = word(key[4*i],key[4*i+1],key[4*i+2],key[4*i+3])
    i = i+1
  end while
  i = Nk
  while (i < Nb * (Nr + 1))
    temp = w[i-1]
    if (i mod Nk = 0)
      temp = SubWord(RotWord(temp)) xor Rcon[i/Nk]
    else if (Nk > 6 and i mod Nk = 4)
      temp = SubWord(temp)
    end if
    w[i] - w[i - Nk] xor temp
    i = i + 1
  end while
end
```

なお、SubWordは、subtypesと同じ定行列$A$と定ベクトル$c$を用いて、

$$
(b\_0, b\_1, b\_2, b\_3) \gets (Ab\_0^{-1} + c, Ab\_1^{-1} + c, Ab\_2^{-1} + c,Ab\_3^{-1} + c)
$$

より得られる。またRotWordは、

$$
(b\_0, b\_1, b\_2, b\_3) \gets (b\_1, b\_2, b\_3, b\_0)
$$

より得られる。
また、コード中に出てくる定数ベクトルRconの定義は次である。

$$
Rcon[n] = (2^n, 0, 0, 0) \\\
Rcon \in GF(2^8)^4
$$

普通の演算系では計算できないことに注意が必要である。


## 実装

以上で説明したことを実際に実装するのがこの分科会である。とはいえさすがに頭から全て実装するのは時間がかかりすぎて分科会内では終わらないので、AESとしては本質的ではない部分（有限体関連の計算など）は、すでに実装し終えている。

やるべきことは、用意したcheck.pyを実行した時に満点が取れるように、必要な部分を実装することである。

関連ファイルは、[sig-ctf-2017/docs/05](https://github.com/tsg-ut/sig-ctf-2017/tree/master/docs/05)にあるので落として欲しい。

実装練習に穴あきになっているファイルが[aes_imp.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/05/aes_imp.py)である。これを埋めて行って欲しい。また、関数が正しく動いているかどうかは、[check.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/05/check.py)を実行すると確認ができる。上記で説明した定数群の定義や、有限体に関する関数は、[constants.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/05/constants.py)、[tools.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/05/tools.py)にそれぞれある。

[aes.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/05/aes.py)は僕の（汚い）実装である。


あと、僕自身のコードが仕様通りになっていない可能性がある。この場合checkも当然間違えていることになるので、その場合は、[@moratorium08](https://twitter.com/moratorium08)まで知らせて欲しいです・・・
