注意区别几个命令胡不同：erl.exe是单行交互程序，erlc.exe是用于编译源文件到字节码；escript.exe则用于执行脚本文件。

一、erl shell里直接编译运行

c(tut6)


二、编译成字节码运行：

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



三、ErLang特性

1、ErLang中的变量只能绑定一次，这在其他一些程序设计系统中被称为“常量”。

2、ErLang中没有while和for循环，应使用递归来实现循环。

3、ErLang中有if和case语句，实现条件和分支语句，但是也可以用函数匹配来代替。

3、ErLang中的消息传递模型，和Unix Shell环境下的|管道操作很像。Posix C API中pipe()函数用于创建管道，其区别是，调用Pipe创建管道后，用户发送的数据是字节流，而ErLang传递的消息则是有数据类型的。


