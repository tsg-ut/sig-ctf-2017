# CTF分科会第一回

## CTFとは

　CTFはCapture The Flagの略で、平たく言えばコンピュータを題材にした謎解きのようなものである。フラグと呼ばれる文字列が問題のどこかに隠されているので、問題となっている題材の脆弱性やなんらかのトリックを見つけて、フラグを見つけだすのがCTFの大筋である。
　具体的には、不適切な暗号を破ったり、プログラムに含まれる脆弱性を突いて、フラグとなる文字列を見つけ出す。
　このとき、「どんな脆弱性があるか？」を見つけ、そしてその脆弱性を「どのように使うとフラグを手に入れることができるか？」を考え、競うことになる。
　IT関連の競技でいうと、競技プログラミングや、Kaggleのようなデータ解析の競技などがあるが、CTFもその一つであり、CTFは基本的にチーム戦で行われる。
　CTFとは、に関してはすでに十分に色々な資料がある（ので僕が書く必要はなかったが書いてしまった）。

[kimiyukiさんのブログ](https://kimiyuki.net/blog/2016/12/02/getting-started-with-ctf/)
[kikuchan98さんのslide](https://www.slideshare.net/kikuchan98/ctf-45624362/96)
など

## どのような分野があるのか？

これも上記した記事を見ればわかる話ではあるが、簡単にまとめる。

### Reversing

　ELFやPEのような実行可能ファイルが渡され、その解析に問題の主眼がおかれるような問題がこれにあたる。
　
### Pwnable(Exploit)

　実行可能ファイルの脆弱性を突いてフラグを手に入れる問題。脆弱性をつくパズル。

### Cryptography

　暗号に関する問題。非常に色々な問題があり、数学的に高度なものもあり、奥が深い。

### Web
　
　実際あまりよくわからないというのが正直なところ。多分分科会ではWebのプロがいない限りあまりやることはない。よくwebはエスパーと言われるのでそう思い込んでいるが、面白い問題は面白いと思うので、教えてほしい。

### Network

　あんまよくわからんその２。パケットを解析して、そこからデータを取り出すという認識でいるが、正しいかも怪しいので他の記事を当たった方が良い。

### Forensics/Steganography

　隠されたデータを掘り返す系問題。画像に巧妙にデータを隠したりする。steganographyに関しては、hakatashiさんが強い。


### PPC

　プログラムを書くことが主眼の問題。競技プログラミングのように計算量の良いアルゴリズムを考えて実装するというよりも、特定の操作を自動化するようなイメージが強い（簡単な暗号を大量に解きまくるプログラムを書く、というような）。
　
### Recon

　ネトスト


### 

## 良資料

### セキュリティコンテストチャレンジブック

　CTFにターゲットを絞って書かれた本。簡単なテクニックなどが記載されている。村人Bはこれを読めば倒せると言われている。


### katagaitai勉強会資料

　初学者がいきなり読むのはやや難しいかもしれないが、pwnable/cryptoを中心に比較的難しい問題についての解説がある。

### ももいろテクノロジー
　
　略してももテク。CTF中よくお世話になる。色々なテクが記載されている。ググるとよく引っかかるので、CTFで「〜がしたいなあ」と思った時に、辞書のようにも使える（？）。

## CTFの問題をとく

### 常駐CTF

　CTFというのは、基本的には１〜３日くらいの長さで時間を区切って行われるものであるが、世の中には常駐型CTFというものが存在する。

### [ksnctf](http://ksnctf.sweetduet.info/), [akictf](http://ctf.katsudon.org/)

　くさのさんのCTFなので「くさのしーてぃーえふ」と読む。エスパーっぽい問題（僕の認識違いかもしれない）もあるが、村人A/B(Villager A/B)はCTF beginnerの登竜門とされている。
　基本的にこの二つは、その系統のプログラミング経験のある人であれば、CTFそのものに詳しくなくてもある程度ググれば問題が解けるようになっているものがある程度あるので、点数が高くない問題をとりあえず解いてみて楽しむのも良さそう。
　

## [pwnabler.kr](http://pwnable.kr/), [maguro ctf](https://score.maguro.run/)

　pwnに関する問題がたくさんある（僕もやっていきたい）。

その他常駐CTFに関しては、[常設CTFまとめ](http://nanuyokakinu.hatenablog.jp/entry/2015/08/24/213158)に詳しい。

### 過去問に関して

　過去の大会で出題された問題は、多くはネットを調べれば手に入れることができるが（環境を再現できるかは別として）、非常に量が多いので、良問を集めたリストというものがある

* [pwn challenges list(@bata24)](https://pastebin.com/uyifxgPu)
* [Crypto Challenges List(2016)(@elliptic_shiho)](https://pastebin.com/28SrvQ9b)
（など？）


## この分科会に関して

　別に僕自身凄い強いというわけではなく、分科会を通して、勉強していきたいという気持ちが強いので、形式としては、各週問題を解説することを通して勉強会にするような形を取りたい。
　CTFには様々な分野があるが、個人的な興味があるという点で、Rev/Pwn, Cryptoの二つに主眼を置いていきたい（webとかなんにもわからへん・・・、プロがいたらその人が話してほしい）

## 今日に関して

　とりあえず、環境設定に関しては今日やって、という気持ちが強かったのだが、どうも非常に時間がかかることが分かったので、やり方だけ伝えて、あとは常駐CTFを眺める会にしたい。

　そもそも、来ている人々がどれくらい技量があるのかがわからないが、CTFは基本的に、CTFを学ぶ、というよりも、普段プログラミングやらインフラ整備をしていて得た知識が前提となる部分が強いので、何もプログラミングをやったことがない人が始めるようなことは少し難しい。
　多分分科会で扱う、Rev/Pwn、Cryptoはそれぞれ、前者はC言語による簡単なプログラミング、後者は数学（高校数学+α）が必要になる。

　

## Tool群

　ELFを解析する上で必要になるのは、主にELFをディスアセンブルツールと、動的に解析するツールである。前者としては、Objdump/IDA/Hopper Disassemblerなどがあり、後者としてはgdbがある。IDAもHopperも有料版を制限付きで無料でつかうことができ、objdump/gdbは無料である。

基本的には、この分科会では、[Objdump | Hopper] + gdbでやっていく。


## 環境構築（リモート）

　ELFが動く環境をリモートと呼び、自分が解析をしたりexploitを走らせるする側の環境をホストと呼ぶようにする。
　多くの人がホストとして使っているOSはwindows/macだと思うので
　ホスト側の環境構築は面倒臭さを回避するために、すでに用意したものがある。今日は基本的にこれを入れる分科会。
　まず、VagrantとVirtual Boxを入れます。これはググるとわかる。

次に、次のコマンドを打つ。

```
$ git clone https://github.com/tsg-ut/sig-ctf-2017
$ cd CTF_Vagrant
$ mkdir shared_folder
$ vagrant up
```

しかし、実はこれは結構時間がかかるので、家で寝る前とかに実行する感じの方が良さそうだった。なのでそうして欲しい。

## 環境構築（ホスト）

　正直、環境構築とは言っても、必要になったら随時入れるというイメージではあると思う。しかしそうは言った上で、CTFやる上では多分必須となるものが次である（これも気が向いたら入れる感じで良さそう）。
　
### IDA/Hopper

　グラフィカルなディスアセンブラ。どちらも有償だが、無料の制限ありバージョンが使えるので多分最初はそれを使うと良さそう。IDAは基本的にWindowsの人向けで、HopperはMacの人向け。能力的には、IDAが一枚上手だが、Hopperは有償版が安いし、x64のELFが無料で読めるのでそういった良さがある。

### x64dbg/Ollydbg/Immunity Debugger

　Windows用の動的解析に使うデバッガー。Windowsで動くPEバイナリがどのように動作するかを解析する際に使う。ksnctfを埋める際には必須だと思われる。どれかは入れておくと良さそう（多分x64dbg/x86dbgがx64に対応してて良い）。

### バイナリエディタ(BZ/Strings/0xED/Binary Ninja) 


　バイナリデータを表示し編集できるソフトウェア。CTFではしばしば、ファイルをバイナリエディタで眺めたり、書き換えたりする必要があるときがある。どれかは入れておくと良さそう（BZ/StringsはWindows、0xEDはMac、Binary Ninjaはクロスプラットフォームなので色々なところで使えるはず）。

### Python(2系)
　
　CTFerの多くがPythonを使ってスクリプトを組みがち。PwnやCryptoのwriteupは7割〜ほどがPythonで組まれている。あとPython3よりも2が好まれている印象がある。
　Rubyで頑張りたい人は[去年の部報のcookies146さんの記事](http://www.tsg.ne.jp/buho/312/buho312.pdf)を参照。


### z3

　SAT(充足可能性問題)を解いてくれるすごいやつ。連立方程式的なものを投げると解いてくれる。雰囲気は、[秋葉さんのブログ](https://topcoder.g.hatena.ne.jp/iwiwi/20121219/1355925708)参照。Crypto系問題などで使う時がある。
　多分CTF以外にもお世話になることはあり、入れておくと良さそう。

### angr

　シンボリック実行によりバイナリを解析するツール。最近のCTFではしばしばangrで自動化すれば解けてしまう問題があった（さすがに無くなってきたか？）。入れておくと幸せ。

### Wireshark

　パケット解析をするためのツール。CTFではパケットデータが渡される問題も多い（ネットワーク問に限らず）ので、これは入れておくべき。

### pari gp/sage mathなど高機能電卓

　Cryptoなどで、代数的な計算が必要になるときに使う。

他にもあるかもしれないが、まぁ上のものは、少なくとも存在は認識しておいた方が良さそう（必要になったらインストールをする）。

## 常駐CTFに関して

### CTFはじめての人

[cpaw ctf](https://ctf.cpaw.site/)は、割と誰でも（少し時間をかければ）全完できると思う（そうなるように作られている）。

### CTFはじめての人もそうじゃない人も

[ksnctf](http://ksnctf.sweetduet.info/)、[akictf](http://ctf.katsudon.org/)あたりをのぞいてみると良いと思う。特に、ksnctfのVillager BはCTF入門の登竜門なので、挑戦してみると良いと思う。




