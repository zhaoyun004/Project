注意区别几个命令胡不同：erl.exe是单行交互程序，erlc.exe是用于编译源文件到字节码；escript.exe则用于执行脚本文件。

一、编译成字节码运行：

用 erlc 编译
mkdir -p ./ebin
erlc -o ebin useless.erl

编译后的 beam 文件会在 ebin 目录下，然后你启动 erlang shell：
$ erl -pa ./ebin
Erlang/OTP 19 [erts-8.3] [source] [64-bit] [smp:4:4] [async-threads:10] [hipe] [kernel-poll:false]

Eshell V8.3  (abort with ^G)
1> useless:add(1, 2).
3
2> useless:add(1, 2, 1).
4

erl -pa 参数的意思是 Path Add, 添加目录到 erlang 的 beam 文件查找目录列表里。

ErLang里的所谓的“变量”只能绑定一次，实际就是“常量”。


二、erl shell里直接编译运行

