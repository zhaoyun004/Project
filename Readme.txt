ToBeDone：


一、Zh程序设计系统

XP上使用python3.4.2，其余使用3.6.8

(tobedone pdf tk gtk)

增加shell处理功能 --- 能直接运行外部命令。


二、C++ Easy GUI（移植到ZH平台上）

GUI版面设计应该类似于html、JavaScript、css组合，重点是，版面设计要和程序设计分离。

作者设计的这套GUI编写规则，是和程序设计语言无关的，理论上适用于任何程序设计语言。

移植到Python，使用tk，canvas库，可能会使用cario库。Cario是一个跨平台的图形库，在Windows上是一个类似gdi的做图库。


三、C、C++预处理器（宏替换，泛型特化）

支持宏的程序设计系统 -- C/C++ Lisp/Scheme ErLang Perl Filter :: CPP  Template :: Toolkit

M4(Macro Language 宏语言)

做宏处理器，方便之处在于，宏（预）处理器不需要理解太多的程序设计系统的语法规则，只是单纯的做宏替换。

你可以把这一套规则用在任何你熟悉的程序设计系统甚至是简单的配置文件之上。比如你也可以用这套宏系统来编写First.gui（窗口设计代码）。


用宏替代泛型


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