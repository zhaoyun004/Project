ToBeDone：


一、Zh程序设计系统 

XP上使用python3.4.2，其余使用3.6.8

(tobedone pdf tk gtk)


二、C、C++预处理器（宏替换，泛型特化）

支持宏的程序设计系统 -- C/C++ Lisp/Scheme ErLang 

Perl Filter :: CPP  Template :: Toolkit

M4(Macro Language 宏语言)

做宏处理器，方便之处在于，宏（预）处理器不需要理解太多的程序设计系统的语法规则，只是单纯的做宏替换。你可以把这一套规则用在任何你熟悉的程序设计系统甚至是简单的配置文件之上。比如你也可以用这套宏系统来编写First.gui（窗口设计代码）。

1. 定义常量

@define  A  3

2. 定义函数

@define  (Swap a b) ()

4. 文件包含

3. 泛型编程

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



三、C++ Easy GUI（移植到Python、ZH平台上）

GUI版面设计应该类似于html、JavaScript、css组合，重点是，版面设计要和程序设计分离。

作者设计的这套GUI编写规则，是和程序设计语言无关的，理论上适用于任何程序设计语言。




程序设计系统的几个重要元素：


一、基本数据类型
	
	静态类型还是动态类型？C/C++, Delphi(Object Pascal)是静态类型，变量需要指定类型；Python, Scheme, Php是动态类型，变量不需要指定类型。
	
二、数组、数据结构
	结构体、数组，链表，哈希数组，平衡树结构等等。C/C++复杂数据结构是通过标准模板库（STL）来实现；并不是语言核心，而Python Php等复杂数据结构则是语言核心。
		
三、条件和循环
	
	If for while 各个语言大同小异。 
		
四、函数

	函数是程序设计语言的重要元素。能否递归，能否把函数赋给变量使用，能否用无名函数？
	
五、自动内存回收
	
	C/C++申请内存，使用完成后，需要自己释放。malloc/free new/delete。其他大多语言不需要手动回收。
	
六、泛型编程（是否能用到宏系统中？）

	C++这类静态类型语言，应当有泛型编程元素，在C++里表现为模板template，有模板函数和类模板。
	
七、面向对象

	主要起封装作用。把数据和相关的函数封装在一起，便于修改和维护。父类和子类。 继承、多态。