ToBeDone：


一、Zh程序设计

XP上使用python3.4.2，其余使用3.6.8

(tobedone pdf tk gtk)

增加shell处理功能 --- 能直接运行外部命令。



二、MyGUI图形界面设计

MyGUI类似于html、JavaScript、css组合。

Python，使用tk，canvas，cario库。Cario是一个跨平台的图形库，在Windows上是一个类似gdi的绘图库。



专利收费方式：

一、按年缴费

图形设计需求量大的软件公司，按年收取专利费，60000/年，赠送Windows 10版本开源的C++图形解释器，大公司可以自行开发自己的C/C++ Java Python各种语言的图形解释库函数，自行移植到Linux不限制源文件的使用次数。


本公司只维护WIndows 10 C++版本的原型系统，其余操作系统，其余程序设计系统的库本公司不做开发，只收取专利年费。同时，本公司将维护并改进专利，对专利技术进行版本升级。



二、按月缴费
20000/月，赠送C++图形解释器


三、按文件数目缴费

按文件/Window数目灵活收费




三、C、C++预处理器（宏替换，泛型特化）

支持宏的程序设计系统 -- C/C++ ErLang Perl Filter :: CPP  Template :: Toolkit  Lisp/Scheme


M4(Macro Language 宏语言)

做宏处理器，方便之处在于，宏（预）处理器不需要理解太多的程序设计系统的语法规则，只是单纯的做宏替换。

你可以把这一套规则用在任何你熟悉的程序设计系统甚至是简单的配置文件之上。比如你也可以用这套宏系统来编写First.gui（窗口设计代码）。


用宏替代泛型？


1. 定义常量

@define  A  3

2. 定义函数

@define  (Swap a b) ()

3. 文件包含


4. 泛型编程

Type T, U;

struct  pair {
	T a;
	U b;
}

Type V {int float char}

T add(T a, T b) {
    return a + b + A;
}

float sub(T a, U b)

int main() {
    add(12, 34)         //特化成为add_int
    add(12.3, 34.5)     //特化成为add_float
    add(12.3, 34)		//特化报错！
}


设置环境变量：

INLUCDE	： D:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910\include;D:\Windows Kits\10\Include\10.0.19041.0\shared;D:\Windows Kits\10\Include\10.0.19041.0\ucrt;D:\Windows Kits\10\Include\10.0.19041.0\um;D:\Windows Kits\10\Include\10.0.19041.0\winrt;

Lib	： D:\Windows Kits\10\Lib\10.0.19041.0\ucrt\x64;D:\Windows Kits\10\Lib\10.0.19041.0\um\x64;D:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910\lib\x64;
