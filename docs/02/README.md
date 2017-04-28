# 第二回CTF分科会資料

　CTF分科会の初回は軽めの（古典暗号系の）暗号問について見ていき、CTFというゲームについて見ていく。
　一応、僕自身そんなに問題を知っているわけではないので、@elliptic\_shihoさんの[Crypto Challgenges List(2016)](https://pastebin.com/28SrvQ9b)をネタにしていく。
　付記する難易度は、このリストでどの難易度になっているかを表す。

## Caesar暗号
　
　この暗号方式が理解できない人は世の中にいないので、いわゆる「暗号とは？」のような概要を示す際に頻繁に用いられている。知っている人も多いと思うがいわゆる「換字暗号」と呼ばれる暗号の一種である。換字暗号とは、一定文字数シフトすることによって元の文字数ずらすことによって、平文から読めない文章（暗号文）に変えることで暗号化を行う。

　例を示すと、例えば5文字ずらしの場合
```
HELLOTSGTHISISSIGCTF
```
という文章があったときに
```
MJQQTYXLYMNXNXXNLHYK
```
が出力される。これはAsciiコードにおいてHが72であるのにたいして、Mが77であり、したがってHに5を足した値であるMが返されるということである。
　
　実装するまでもないが、一応実装したので、[このプログラム](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/02/caesar.py)を実行して欲しい。ただ実行して欲しい、ではつまらないので、

```
HWDUYTLWFUMD
```
これをプログラムを実行して解読して欲しい。

```
$ python caesar.py d
```
で実行可能。

## Vigenere暗号
　
　さすがに舐めているのかと言われそうであるが、Caesar暗号は一応導入で、今日は（そうは言っても軽めだが）Vigenere暗号という暗号に関する問題を見ていくつもりである。
　　[Wikipedia](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A3%E3%82%B8%E3%83%A5%E3%83%8D%E3%83%AB%E6%9A%97%E5%8F%B7)によると、15世紀後半から16世紀前半にかけて考えられた暗号らしい。いわゆる古典暗号の部類に入る。Caesar暗号の発展形で、Caesar暗号よりもencode/decodeが難しくなった分、Caesar暗号で出来た攻撃手法がすぐに成立するかはわからなくなった。

### Encode/Decode

　少し難しくなったとはいえ、現代のコンピュータを持つ我々にはそれほど難しいものではない。人間がEncode/Decodeする際には次のような表を用いる。

```
 |ABCDEFGHIJKLMNOPQRSTUVWXYZ
-+----------------------------
A|ABCDEFGHIJKLMNOPQRSTUVWXYZ
B|BCDEFGHIJKLMNOPQRSTUVWXYZA
C|CDEFGHIJKLMNOPQRSTUVWXYZAB
D|DEFGHIJKLMNOPQRSTUVWXYZABC
E|EFGHIJKLMNOPQRSTUVWXYZABCD
F|FGHIJKLMNOPQRSTUVWXYZABCDE
G|GHIJKLMNOPQRSTUVWXYZABCDEF
H|HIJKLMNOPQRSTUVWXYZABCDEFG
I|IJKLMNOPQRSTUVWXYZABCDEFGH
J|JKLMNOPQRSTUVWXYZABCDEFGHI
K|KLMNOPQRSTUVWXYZABCDEFGHIJ
L|LMNOPQRSTUVWXYZABCDEFGHIJK
M|MNOPQRSTUVWXYZABCDEFGHIJKL
N|NOPQRSTUVWXYZABCDEFGHIJKLM
O|OPQRSTUVWXYZABCDEFGHIJKLMN
P|PQRSTUVWXYZABCDEFGHIJKLMNO
Q|QRSTUVWXYZABCDEFGHIJKLMNOP
R|RSTUVWXYZABCDEFGHIJKLMNOPQ
S|STUVWXYZABCDEFGHIJKLMNOPQR
T|TUVWXYZABCDEFGHIJKLMNOPQRS
U|UVWXYZABCDEFGHIJKLMNOPQRST
V|VWXYZABCDEFGHIJKLMNOPQRSTU
W|WXYZABCDEFGHIJKLMNOPQRSTUV
X|XYZABCDEFGHIJKLMNOPQRSTUVW
Y|YZABCDEFGHIJKLMNOPQRSTUVWX
Z|ZABCDEFGHIJKLMNOPQRSTUVWXY
```

また、暗号化用の鍵が必要で（要するにVigenere暗号は共通鍵暗号）、今回は、「CRYPTO」を使うことにする。Vigenere暗号のEncrypt/Decryptは、この鍵と表を使う。


### Encrypt

　例えば「PLAINTEXT」という文字を暗号化しようとすることにする。一文字目Pを暗号化するには、鍵となる「CRYPTO」の一文字目Cを使い、上の表でP行C列にあたる文字を参照する。これはRである。平文二文字目「L」は、鍵の二文字目であるRを用いてL行R列・・・と順番に行う。すると、鍵の長さが6文字であるのに対して、平文の長さは9文字であり、7文字目の平文を暗号化しようとすると、鍵が足りなくなってしまう。
　ここで、鍵は仮想的に「CRYPTOCRYPTOCRYPTO...」と無限に続くものだと仮定して、7文字目のCを再び用いて暗号化する。これにより、全て暗号化すると、「PLAINTEXT」は鍵「CRYPTO」により、「RCYXGHGOR」に暗号化される。

### Decrypt
　
　これはさっきの例に対して、逆の操作をすればよく、暗号文「RCYXGHGOR」を鍵「CRYPTO」で復号する際には、鍵一文字目Cについて、C列目を上から見ていき、暗号文Rと一致する行の文字を見ると、それは「P」、次に鍵の二文字目Rについて・・・と同様に行うと、「PLAINTEXT」が復号される。

### 実際に試して見る
　
　[Vigenere暗号を簡単に実装したもの](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/02/vigenere.py)を作ったので、これを使って様子を眺めてみる。

　例えば、
```
EIWEMCIIYEAM
```
この暗号文は何を意味しているのだろうか？
　またこの様子を見ると、Caesar暗号とは違いすぐに解析するのは難しそうだというさまが見えてくる。

### より一般に

　Caesar暗号とVigenere暗号で何が違うのだろうか。Caesar暗号は一般に鍵をずらし文字数kと見ることができる（これが26通りしかないのでクソだが）。

$$
\boldsymbol{c} = \boldsymbol{x} + \boldsymbol{k} \bmod 26 \\
\begin{eqnarray}
\boldsymbol{k}
 = \left(
     \begin{array}{c}
       k \\
       k \\
       \vdots \\
       k
     \end{array}
   \right)
\end{eqnarray}
kは定数
$$
一方で、Vigenere暗号では、Encrypt/Decryptの式は同じであるが、鍵が、ベクトル$\boldsymbol{k}$であると考えると、複雑さが明らかに異なることがよくわかる。

$$
\boldsymbol{c} = \boldsymbol{x} + \boldsymbol{k} \bmod 26 \\
\begin{eqnarray}
\boldsymbol{k}
 = \left(
     \begin{array}{c}
       k_1 \\
       k_2 \\
       \vdots \\
       k_n \\
       k_1 \\
       \vdots
     \end{array}
   \right)
\end{eqnarray}\\
k_1 \cdots k_nは定数, 鍵長n
$$

## （一般的な）攻撃手法に関して

　Caesar暗号は、頻度分析や、そもそもAlphabetのみの場合26通りしかない場合などは全て列挙することで解析可能である。
　
　ただ、これらは一定の長さの文章が必要である。まぁしかしこれは当然で、鍵に「CRYPTO」という長さの文字列を使っているのに、暗号化したい文章が「CRYPTOGRAPHY」程度の短い文字列であれば、そもそも暗号化する必要がない（その鍵を秘密に渡すやりかたで渡せば良い）。このような共通鍵暗号は一般的に、十分強度のある一定の長さの鍵に対して、ある程度長い文章（これは鍵よりもかなり長い）の秘密を保つのに使われる。したがって、本来の使い道がされていれば、十分長い文章であることを仮定してよい。したがって、この場合、Caesar暗号は非常に脆弱であると言える。

　一方で、Vigenere暗号はどうだろうか。鍵によって、ずれる数が異なるし、そもそも鍵がどれくらいの長さなのかわからない。これは解析可能なのか。

## カシスキーテスト

　[Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)によれば、「カシスキー」という名前がついているが、最初に見つけたのはBabbageだとされている。まぁ、どちらにせよ（どちらにせよで済まされてはたまらないが）この手法は19世紀中頃には見つかっていたようである。
　
　Vigenere暗号がもっとも解析を困難にしている点は、鍵の周期がわからない点である。これさえわかれば、ほとんどCaesar暗号と言ってもいいはずである（同じ周期の文字は同じ数だけずらされているだけであり、文字の分布は、通常のCaesar暗号のときのように、その言語で使われやすい文字ほど現れやすくなるはず）。


　例えば、英語で言えば三文字のTheはよく現れうる単語であり、したがって、鍵の同じ部分で2度以上暗号化されることがありうる。
　
　仮に、鍵の長さがわかってしまえば、さっき書いた通り、頻度分析を行えば、鍵の文字が何であるかが推察可能となる。

　これはとりあえず実装するのがややめんどうだったので、[Vigenere Solver](https://www.guballa.de/vigenere-solver)を使った。
　今回暗号化する文章は、英語版Wikipediaの[Vigenere Cipher]()の最初に二段落を切り出してきたものである。

```
THEFIRSTWELLDOCUMENTEDDESCRIPTIONOFAPOLYALPHABETICCIPHERWASFORMULATEDBYLEONBATTISTAALBERTIAROUNDANDUSEDAMETALCIPHERDISCTOSWITCHBETWEENCIPHERALPHABETSALBERTISSYSTEMONLYSWITCHEDALPHABETSAFTERSEVERALWORDSANDSWITCHESWEREINDICATEDBYWRITINGTHELETTEROFTHECORRESPONDINGALPHABETINTHECIPHERTEXTLATERINJOHANNESTRITHEMIUSINHISWORKPOLIGRAPHIAINVENTEDTHETABULARECTAACRITICALCOMPONENTOFTHEVIGENRECIPHERTHETRITHEMIUSCIPHERHOWEVERONLYPROVIDEDAPROGRESSIVERIGIDANDPREDICTABLESYSTEMFORSWITCHINGBETWEENCIPHERALPHABETSWHATISNOWKNOWNASTHEVIGENRECIPHERWASORIGINALLYDESCRIBEDBYGIOVANBATTISTABELLASOINHISBOOKLACIFRADELSIGGIOVANBATTISTABELLASOHEBUILTUPONTHETABULARECTAOFTRITHEMIUSBUTADDEDAREPEATINGCOUNTERSIGNAKEYTOSWITCHCIPHERALPHABETSEVERYLETTERWHEREASALBERTIANDTRITHEMIUSUSEDAFIXEDPATTERNOFSUBSTITUTIONSBELLASOSSCHEMEMEANTTHEPATTERNOFSUBSTITUTIONSCOULDBEEASILYCHANGEDSIMPLYBYSELECTINGANEWKEYKEYSWERETYPICALLYSINGLEWORDSORSHORTPHRASESKNOWNTOBOTHPARTIESINADVANCEORTRANSMITTEDOUTOFBANDALONGWITHTHEMESSAGEBELLASOSMETHODTHUSREQUIREDSTRONGSECURITYFORONLYTHEKEYASITISRELATIVELYEASYTOSECUREASHORTKEYPHRASESAYBYAPREVIOUSPRIVATECONVERSATIONBELLASOSSYSTEMWASCONSIDERABLYMORESECURE
```
不要な記号やスペースは取り除かれている。これを暗号化すると

```
SMCCDLZVRJKEXJHTZVYFWJFLBYOHURFJHVHVUNESVQOURMQLOEJRLEDWUXNZVTHZKTNZIALCPAFHCACEPSFYIWYYVDFQHOIIZAUFEWJCTNPXKHGMCYYFDXBMINBHGTSNWZYLNJZHUFBMUSRCFAXNNFKOVCFAYUFBPBLTLITMDKOHGXXVQOURMQLYCMCAORJTBMUSYJWCLUIIRJZEOZKUDNNBHSBFXUAGYGXPLDYHAXETWRGACAONKREZWVTMJRIIIIHAXLXHNCINPFMYFBXCWJZWSXROQZGVCUFPQOJJKDXRODNOGHNTLCIMHFNZDCVQSRCOZUFFVCUXZSSXXOMDGRMGDGTLLPXZHPFOCJCGHNFJJSDAKZRLNGCRCBMWCZDJOGMYGXNMNSUVXUMYEPYDBQMMTZPLTJSKRJMTUVUPPSVTVPNBRXGSZLPIDIZGXKWDQZNFSHNLBUPSJKCJLZYDYBACILARKHQWTEPYDBQFJMCUIGOXVAUONRAFHWFUYUJOQGJTFBYUTZHHIBZWVNJZDAMKUJHIXICPXLPDZIARADTUNEMMLZKZCWYDQJXNIPPCNRUIJPKNTTRJGFLUOFFLGLQUUDVYSBMOFARCWMKUJLKQFKYSMJHAJZYZUOGFQRTEMGLVYRPEDRGRNVBVVICXXVWDCVLFATIJXQKSJPPDAUCFJXMINBHGTSOAVJLAWIOMYYZNZGQJQRFZYSRIHTWXGHBWIAJPQDUUFOWHMBZRHHJFEWJCMRTBCUYQOYYPJKRNVNYHGLEUGTUINHIZXMPNWOGHJLXUIYSUVAMLZGYWKCRZZPOCAWONNGMXTTYUMQWGUPUUZGFLDZXZKHUKRVTXDYVNFATIHWATJJWHZSZYZWDMSKNBNCWKKOPNUATNWBPJLZJJWSIBMFRRJVZGCPAXXLSMNXMNPGNNMTXQFMPVZDLXCUBIFSYCAJOAQAGZGXVQNAXHULNVONIBRXYDZVLNGFRHMHJSUFOFZAUYNMRHWCANNYQILRXWPWHGPQAJUPSHPEDPCVVMPVDXQXFVYHIVWKWGUFCKPDHSOZUZJJWSDYTUGERDQKGAIHWMQJTFJOZRMNUTNZHNAMPDKGVPXJYDQJXNIZUTXSXGRFRPFYEAJGYJXIXRMOZMLEPWD
```

となる。これを、さっきのSolverに投げて見てほしい。なかなかにうまくいくとわかる。
　もちろんこの手法もそもそもある程度文章が長くないと効果を発揮しないが、基本的に、このような暗号はある程度長い文章を暗号化するために用いられるはずであり、したがって基本的にVigenere暗号は実用的ではないということがわかる。一方で、これは日本語だと比較的強いのではないかという疑念も残る。しかし、実用的な暗号としては、ただ解読できないだけではなく、同じ文章を送られたときに同じ文章であることがわからない必要性などがあり、結局このままだと実用的ではない。
　
　
## \[Easy\]Vigenere(SECCON Online CTF 2016)

　ここからは、実用云々ではなく、CTFの問題について考えていく。最初の問題は、昨年のSECCONのOnline予選の問題で、Vigenere暗号に関する問題。問題としては、非常に簡単な部類に入るが、さっきまでの一般手法ではない方針を考える必要がある。

### Statement

```
Vigenere

k: ????????????
p: SECCON{???????????????????????????????????}
c: LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ

k=key, p=plain, c=cipher, md5(p)=f528a6ab914c1ecf856a1d93103948fe

|ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
-+----------------------------
A|ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
B|BCDEFGHIJKLMNOPQRSTUVWXYZ{}A
C|CDEFGHIJKLMNOPQRSTUVWXYZ{}AB
D|DEFGHIJKLMNOPQRSTUVWXYZ{}ABC
E|EFGHIJKLMNOPQRSTUVWXYZ{}ABCD
F|FGHIJKLMNOPQRSTUVWXYZ{}ABCDE
G|GHIJKLMNOPQRSTUVWXYZ{}ABCDEF
H|HIJKLMNOPQRSTUVWXYZ{}ABCDEFG
I|IJKLMNOPQRSTUVWXYZ{}ABCDEFGH
J|JKLMNOPQRSTUVWXYZ{}ABCDEFGHI
K|KLMNOPQRSTUVWXYZ{}ABCDEFGHIJ
L|LMNOPQRSTUVWXYZ{}ABCDEFGHIJK
M|MNOPQRSTUVWXYZ{}ABCDEFGHIJKL
N|NOPQRSTUVWXYZ{}ABCDEFGHIJKLM
O|OPQRSTUVWXYZ{}ABCDEFGHIJKLMN
P|PQRSTUVWXYZ{}ABCDEFGHIJKLMNO
Q|QRSTUVWXYZ{}ABCDEFGHIJKLMNOP
R|RSTUVWXYZ{}ABCDEFGHIJKLMNOPQ
S|STUVWXYZ{}ABCDEFGHIJKLMNOPQR
T|TUVWXYZ{}ABCDEFGHIJKLMNOPQRS
U|UVWXYZ{}ABCDEFGHIJKLMNOPQRST
V|VWXYZ{}ABCDEFGHIJKLMNOPQRSTU
W|WXYZ{}ABCDEFGHIJKLMNOPQRSTUV
X|XYZ{}ABCDEFGHIJKLMNOPQRSTUVW
Y|YZ{}ABCDEFGHIJKLMNOPQRSTUVWX
Z|Z{}ABCDEFGHIJKLMNOPQRSTUVWXY
{|{}ABCDEFGHIJKLMNOPQRSTUVWXYZ
}|}ABCDEFGHIJKLMNOPQRSTUVWXYZ{

Vigenere cipher
https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher

```

　問題を見ると、鍵の長さがわかるし、簡単そうだなあと思えるが、しかし一つ問題がある。それは、文章となるフラグが短いので頻度分析を行うのは難しい。
　
　そこで見えるのが、なぜかmd5が与えられている点である。md5が与えられる理由は、しばしば"有名なmd5"が存在して、ググるとそのmd5の元が分かるというケースがあるが、今回はそうではない（しかし、実はこれがクソで、出題中に誰かがこの答えをネットの解析機にかけて、そのパターンになってしまっていたらしいが、それは無かったと考える）。
　
　また、鍵の長さは12だが、平文はどうやら"SECCON{"から始まるようなので、鍵のうちの7文字はもうすでにわかっているのである。するとのこり5文字である。

　$26^5 = 11881376$であるから、Pythonで全探索しても十分、人間的な時間で終わる。そして、ここでmd5の意味も分かる。自動化の際の一致判定に使えるのである。

　あとはスクリプトを書けばフラグが出るはずである。スクリプトは[docs/02/problems/problem1/solve.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/02/problems/problem1/solve.py)である。

### 速度に関して

　スクリプトを見るとわかるように、多重ループが含まれる処理は基本的にPythonは弱い（例えば行列計算などをPythonで全てまるまる書くと大変遅い）。しかし、こういう多重ループが含まれる処理はしばしば、pypyというJITコンパイル機能を持つ処理系を使用することで、ある程度（スクリプトは同じで）高速化可能である。

　簡易的な速度測定を行うと、明らかな違いがわかる

#### python（普通の処理系）
```
$ pyenv local 3.5.1
$ time python solve.py
SECCON{ABABABCDEDEFGHIJJKLMNOPQRSTTUVWXYYZ}
python solve.py  18.76s user 0.29s system 92% cpu 20.637 total
```

#### pypy

```
$ pyenv local pypy3-2.4.0
$ time python solve.py
SECCON{ABABABCDEDEFGHIJJKLMNOPQRSTTUVWXYYZ}
python solve.py  2.45s user 0.05s system 98% cpu 2.547 total
```
　
　今回の問題では、この程度の差異が大きな問題になることはないかもしれないが、angrなどを実行する場合は、しばしばpypyを使用すべきである場合が存在する。

　CTFに限らず軽量プログラミング言語（LL）は、基本的に速度が犠牲になっている場合が多く、愚直に多重ループが含まれる計算などを実装するとCより100倍遅くなることもあり、その場合はCやJavaなどを使うべきかもしれない（競技プログラミングなんかはまさにそう）。


## \[Medium\]Vigenere Cipher(Tokyo Westerns/MMA CTF 2016)

### 問題の取得(7zが必要)
```
$ ./get_problems.sh
```

### 概要

　同じVigenere Cipherを題材にした問題。加えて、Base64がどういう風にEncode/Decodeしているかを少し知っておく必要がある。まさにCTF問題、という感じのパズルなので、時間があれば下の方を見る前に考えて見ると良さそう。

### Base64とは？

　バイト列を識字可能文字64文字でエンコーディングするために開発された符号化方法である。内容に関しては、[Wikipedia](https://ja.wikipedia.org/wiki/Base64)に詳しいが、概要をざっくりと解説する。

　Base64はバイトデータをA-Za-z0-9+/の64文字でエンコーディングする。例えば、ABCというバイト列があるとする。これは

```
0x41 0x42 0x43
```
という列であり、これを二進数で表すと、

```
01000001 01000010 01000011
```

となる。ところで、 Base64は1文字が64通りなので、一つの文字で表せる情報量は$log_264 = 6$であり、6ビットとなる。よって、上記のビット列を6ビットごとに区切ると、

```
010000 010100 001001 000011
```

となる。これらをWikipediaの変換表に照らし合わせると、

```
QUJD
```
となる。実際Pythonでやってみると、

```
In [1]: import base64

In [2]: base64.b64encode("ABC")
Out[2]: 'QUJD'
```
となって、確かにそうなっているさまがわかる。


### まず分かること（思考できること）

* READMEを見ると、元はASCIIファイルらしい。
* base64で符号化したものに対して、vigenere暗号をかけている
* Vigenere.pyより、鍵の長さは5から14
* 鍵の長さがどれくらいかわからないし、全て識字可能文字になるような鍵を全探索しようとしても計算量が$64^x$であり、鍵長5ならまだしも6ですでにきつそう。


### 方針

* 5~14の周期ごとにBase64によるデコードが識字可能になるような文章を出力するために必要な条件で鍵の書く文字を絞っていき、最後は頑張って推測する。

### 初期スクリプト

　まず、前提として、元がAscii textであるという事実がある。これを満たすためには基本的には元のデータが128未満である必要がある。したがって、正しいデータかどうか？ということが意味するのはBase64 decodeした時に値が128未満になるか？ということを意味している。文章で書いても難しいので、以下に具体的な方針を書く。

具体的には、次の手順で絞る。

1. まず鍵の長さをkとする。
2. 鍵候補として、であるcharsを持つ配列をその鍵の長さだけ用意する
3. Base64の性質より、暗号文を四文字ずつ区切って見ていき、各文字について以下のスキームで可能な文字かどうかを判断する。

#### 一文字目

一文字目は、元のバイトで言うところの頭6ビットにあたる。ここで1バイト目が128以下になるかどうかを調べるには、先頭1ビットが立っているかどうかを調べれば良い。

#### 二文字目、三文字目

二文字目は、decode後1バイト目の末尾2ビットが頭の2ビットになっているので、頭から3ビット目が立っているかどうか？を見る、三文字目は5ビット目を見る。

#### 四文字目

　ここらへんは試行錯誤の過程なので、口で説明するのは難しいが、上記の４つを指定すると、keylengthが合わないものは、可能な鍵がなくなる場合が発生するようになる。
　逆に言えば、上記の処理をした段階で、可能な鍵が残るのは、keylength = 12の時のみである。ここまでで4文字目、8文字目、12文字目以外の鍵はすでにわかってしまう。今回は、さらにタブ、改行を無視すると、さらに下位ビットも削除できて、これでうまくいく。要するに、残った文字はある程度推測可能なので、元の文章が意味のあるものになるように鍵を絞っていく。
　
```
[['s'], ['h'], ['A'], ['W', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6'], ['I'], ['8'], ['H'], ['S', 'T', 'U', '1', '2', '4', '5', '8', '9', '+', '/'], ['X'], ['L'], ['F'], ['R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', '5', '6']]
```

ここまで絞ったところで、包括的なアプローチは難しそうになってきたので、base64で戻した文章のおかしな部分を探していく。すると冒頭

```
SKU iA a'JaFangse
```

この文章は、明らかに「〜〜 is  a Japanese ...」と続いていそうである。すなわち、6文字目のAがsになるように8番目のキーを設定する。また「 a 」、「Japanese」になるようにそれぞれ鍵を調節すると、最終的に鍵を得る。

解答スクリプトは、[docs/02/problems/problem2/solve.py](https://github.com/tsg-ut/sig-ctf-2017/blob/master/docs/02/problems/problem2/solve.py)にあるので、実行してみて実際にキーが出る様子を理解すると、文章で言ったことが理解しやすそうである。

### その他方針

　実は、地味にこの問題日本語文書が充実していた・・・・・（し、僕が新たに書いてもネットにゴミが増えるだけだった）
* [TW / MMACTF2016 Crypto200 「Vigenere Cipher」を解いてみた](http://73spica.tech/blog/tw_mma_ctf_2016_vigenere-cipher/)
* [Tokyo Westerns/MMA CTF 2nd 2016: Vigenere Cipher](https://kimiyuki.net/blog/2016/09/05/twctf-2016-vigenere-cipher/)


　ここら辺を見ているとみなカシスキーテストをしているが、僕はカシスキーテストをやっても良い結果が得られなかったので、何が悪いねんってなった。少なくともカシスキーなしで解答しているので、完全に同じ解答ではなさそう？

