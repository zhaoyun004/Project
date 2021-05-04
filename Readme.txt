C:\Windows\System32\drivers\etc\hosts文件，修改后能连上大部分国外网站：
https://raw.githubusercontent.com/racaljk/hosts/master/hosts

hosts文件末尾添加：
151.101.185.194 http://github.global.ssl.fastly.net 
192.30.253.112 http://github.com



git for windows镜像下载：
https://github.com/waylau/git-for-win

git clone https://github.com/zhangyun007/Sword.git
git config --global user.email "zhangxp147@qq.com"
git config --global user.name "zhangyun007"
  
进入项目根目录下：
git add *
git commit -a
git push

创建分支
git branch new
git checkout new



编程相关软件：

Visual Studio C++ Community 2019:
https://visualstudio.microsoft.com/zh-hans/vs/features/cplusplus/

下载安装C++相关的开发软件。

虽然，我们可能并不需要VS的各种高级功能，但是其中的命令行编译工具是必不可缺少的 -- 或者您可以选择开源项目Mingw或者模拟GNU Linux系统的mysys2。

进入Developer Command Prompt for VS 2019命令行下，运行cl test.cpp编译您的程序。 


notepad++编辑器：https://notepad-plus-plus.org/
默认的风格可能不是很喜欢，点击“设置/语言格式设置”，然后在”选择主题“选项里选择自己喜爱的主题；点击视图/自动换行。




ToBeDone：



一、Zh程序设计

XP上使用python3.4.2，其余使用3.6.8

(tobedone pdf tk gtk)

增加shell处理功能 --- 能直接运行外部命令。



二、MyGUI图形界面设计

MyGUI类似于html、JavaScript、css组合。

Python，使用tk，canvas，cario库。Cario是一个跨平台的图形库，在Windows上是一个类似gdi的绘图库。




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
