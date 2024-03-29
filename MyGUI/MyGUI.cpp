#include <windows.h>
#include <objidl.h>
#include <gdiplus.h>

#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <map>

#include <atlimage.h>

#include "../TinyTL/TObject.hpp"

//用于函数SetConsoleOutputCP(65001);更改cmd编码为utf8

using namespace Gdiplus;
using namespace std;

#pragma comment(lib,"User32.lib")
#pragma comment(lib,"ComCtl32.lib")
#pragma comment(lib, "gdiplus.lib")
#pragma comment(lib, "gdi32.lib")
#pragma comment(lib, "wsock32.lib")

#define IDT_TIMER1 12

#define RED_COLOR RGB(255,0,0)
#define BLUE_COLOR RGB(0,0,255)

// 字符串常量
vector<string> Val;

//存储@var部分的变量名和值Val的下标。
map<string, string> var;

int cxScreen,cyScreen;

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

void save_bmp(const char *filename, HDC hdcWindow)
{
	int width;
	int height;
	int xpos = 0;		// 起始x坐标
	int ypos = 0;		// 起始y坐标

	// 获取窗口的设备上下文（Device Contexts）
	// HDC hdcWindow = GetDC(NULL); // 要截图的窗口句柄，为空则全屏
	// 获取设备相关信息的尺寸大小
	width = GetDeviceCaps(hdcWindow, HORZRES);     
	height = GetDeviceCaps(hdcWindow, VERTRES);
	
	cout << width << height << "\n" ;
	
	int nBitPerPixel = GetDeviceCaps(hdcWindow, BITSPIXEL);
	
	CImage image;
	// 创建图像，设置宽高，像素
	image.Create(width, height, nBitPerPixel);
	// 对指定的源设备环境区域中的像素进行位块（bit_block）转换
	BitBlt(
		image.GetDC(),	// 保存到的目标 图片对象 上下文
		xpos, ypos,		// 起始 x, y 坐标
		width, height,	// 截图宽高
		hdcWindow,		// 截取对象的 上下文句柄
		0, 0,			// 指定源矩形区域左上角的 X, y 逻辑坐标
		SRCCOPY);

	// 释放 DC句柄
	// ReleaseDC(NULL, hdcWindow);
	// 释放图片上下文
	image.ReleaseDC();
	
	// 将图片以 BMP 的格式保存到 F:\ScreenShot.bmp
	image.Save(filename, Gdiplus::ImageFormatBMP);

	printf("截图已保存\n");
}

//去掉line开头的空白字符。
string Skip_Blank(string line) {
	int i;
  for (i=0; i<line.length(); i++) {
    if (line[i]!=' ' && line[i]!='\t')
      break;
  }
	if (i<line.length()-i)
		return line.substr(i, line.length()-i);
	else
		return "";
}

//得到一行文本的头一个单词。
string Get_First(string line) {
  string s = "";
  for (int i=0; i<line.length(); i++) {
    if (line[i] != ' ' && line[i] != '\t' && i < line.length())
      s += line[i];
    else
      break;
  }
  return s;
}

//判断某字符串是否正整数
bool Is_Int(string s) {
  for (auto i:s) {
    if (isdigit(i) == false)
      return false;
  }
  return true;
}

//判断s是否是Element函数调用，该函数为内置函数，用于返回某个节点。
bool Is_Fun_Element(string s) {
  return true;
}

//最近一次连接的远程服务器
string lasthost = "";

string Get_Host(string s) {
  string tmp;
  for (int i=0; i<s.length(); i++) {
    if (s[i]=='@') {
      tmp=s.substr(i+1);
      if (tmp == "_VAL") {
       i = atoi(s.substr(i+4).c_str());
        lasthost = Val[i];
        return lasthost;
      } else {
        lasthost = var[tmp];
        return lasthost;
      }
    }
  }
  return lasthost;
}

//取得函数名
string Get_Fun_Call(string s) {
  for (int i = 0; i < s.length(); i++) {
    if (s[i] == '@') {
      return s.substr(0, i);
    }
  }
  return s;
}

//检测s是否包含ch
bool HasChar(string s, char ch) {
  for (int i=0; i<=s.length(); i++) {
    if (s[i] == ch)
      return true;
  }
  return false;
}


class Connection {
  public:
    string Host;
    SOCKET sock;
    Connection(string s);
    ~Connection();
    //调用服务器远程函数，得到返回值
    string RPC(string s);
};

vector<class Connection*> vc;

//构造函数
Connection::Connection(string h) {
  Host = h;
  
  //初始化DLL
  WSADATA wsaData;
  WSAStartup(MAKEWORD(2, 2), &wsaData);
  //创建套接字
  SOCKET sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
  //向服务器发起请求
  sockaddr_in sockAddr;
  memset(&sockAddr, 0, sizeof(sockAddr));  //每个字节都用0填充
  sockAddr.sin_family = PF_INET;
  sockAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
  sockAddr.sin_port = htons(9999);
  connect(sock, (SOCKADDR*)&sockAddr, sizeof(SOCKADDR));
}

Connection::~Connection() {
  //关闭套接字
  closesocket(sock);
  //终止使用 DLL
  WSACleanup();
}

string Connection::RPC(string s) {
  //接收服务器传回的数据
  char szBuffer[64] = {0};
  send(sock, s.c_str(), s.length(), 0);
  recv(sock, szBuffer, 64, NULL);
  //输出接收到的数据
  printf("Message form server: %s\n", szBuffer);
  return szBuffer;
}


// 计算S。注意，运算符优先级。
string Evaluate(string f) {	  
  //@GUI节点的增删指令
  if (f[0]=='#') {
  
  }
  
  for (int i=0; i<f.length(); i++) {
	  
    //赋值语句
    if (f[i]=='=') {
      string v = f.substr(0, i);
      
      //列表或者字典元素赋值
      if (HasChar(v, '|') == true) {
        break;
      }
      
      //以$开头，表示要查改@GUI节点
      if (v[0]=='$') {
        break;
      }
      
      for (auto j: var) {
        if (j.first == v) {
          //变量赋值
          var[v] = Evaluate(f.substr(i+1, f.length()));
          break;
        }
      }
      
      break;
    }
  }
  
  /*
  
  //得到远程服务器。
  string host = Get_Host(f);
  
  //得到函数名和参数
  string n = Get_Fun_Call(f);
  
  for (auto i:vc) {
    if (i->Host==host) {
      return i->RPC(n);
    } else {
      class Connection *con = new Connection(host);
      vc.push_back(con);
      return con->RPC(n);
    }
  }
  */
  
  return "";
}


class Proc {
public:
  string name;    //过程名，可能是"@init" "" ...
  vector<string> s; //把过程的内容以空格区分，存进vector<string> s
  void Call();
};

void Proc::Call(){
	cout << "calling .." << name << "\n";
	for (auto i: s) {
		Evaluate(i);
	}
}

//过程列表
vector<class Proc *> vp;


//返回索引，-1表示没找到。
int InVal(string s) {
	for (int i=0; i<Val.size(); i++) {
		if (Val[i] == s) {
			return i;
		}
	}
	return -1;
}

/*将字符串存储到vector<string> val中，并用对应的vector下标来替换字符串。
  这么做的目的是为了方便做词法分析：以空格为间隔。*/
string String_2_Int(string line){
  int i = 0;
  string str = "";
  short n=0;
   
  while (1) {
    string s = "";
    
    while (line[i] != '\"') {
      str+=line[i];
      if (i == (line.length()-1))
        return str;
      i++;
    }
    
    //此处，检测到第一个“
    i++;
    
    while (line[i] != '\"') {
      s+=line[i];
      if (i == (line.length()-1)) {
        cout << " “不成对。\n";
        exit(0);
      }
      i++;
    }
    
    //此处，第二个"被检测到
    int m = InVal(s);
    
    //存数字索引   
    char buf[10];
    
    if (m >= 0 ) {
      sprintf(buf,"%d",m);
      str=str+"_VAL"+buf;				
    } else {
      Val.push_back(s);
      n = Val.size();		
      sprintf(buf,"%d",n-1);
      str=str+"_VAL"+buf;		
    }
    
    if (i == (line.length()-1))
      break;
    i++;
  }
  return str;
}

/* 指令块结构。一个指令块形式如下：

#LOOP i=0 i+1 i<4
.....
END

#IF i>12
.....
END

#DEF S1
.....
END

一个指令块里可能包含N个指令块

#LOOP i=0 i+1 i<4

#IF i>12
.....
END
.....

END

*/

class Instruction_Block {
	char * instruction;		//这里存第一行，也就是指令行  “#LOOP i=0 i+1 i<4”
};

class GUI_Element {
public:  
  
  unsigned short Level;         //控件在第几Level？
  string Name;                  //控件名称 ，可能的Val为"<window>" "<text>" "<div>" ...
  map<string, string> Property; //控件属性  titile=1, 1为Val的index.
  
  //控件矩形坐标  单位是分辨率  left top right bottom
  int l;
  int t;
  int r;
  int b;
  
  class GUI_Element *parent;    //父节点
  class GUI_Element *child;     //第一个子节点
  class GUI_Element *brother;   //第一个兄弟节点

  GUI_Element(string line);  
  
};

//line是文件中的一行：1 window title="第一个 窗口"
GUI_Element::GUI_Element(string line) {  
  string s = Get_First(line);
                            
  for (int i=0; i<s.length(); i++){
    if (!isdigit(s[i])) {
      cout << "You should start with Level number.\n";
      return;
    }
  }
  
  Level = atoi(s.c_str());
  
  string tmp = Skip_Blank(line.substr(s.length()));
  Name = Get_First(tmp);
  
  tmp = Skip_Blank(tmp.substr(Name.length()));
  string f = Get_First(tmp);
  //不是最后一个单词
  while (f != tmp) {
    for (int i=0; i<f.length(); i++) {
      if (f[i]=='=') {
        //cout << f.substr(i+1, f.length()) << "\n";
        Property[f.substr(0, i)] = f.substr(i+1, f.length());
        break;
      }
    }
    tmp = Skip_Blank(tmp.substr(f.length()));
    f = Get_First(tmp);
  }
  for (int i=0; i<f.length(); i++) {
    if (f[i]=='=') {
      Property[f.substr(0, i)] = f.substr(i+1, f.length());
    }
  }
  cout << Level << ", "<< Name << "\n";
  for(auto iter = Property.begin(); iter != Property.end(); iter++) {
    cout << iter->first << " : " << iter->second << endl;
  }
}

struct Window_Element {
  HWND  hwnd;
  class GUI_Element *head;
  void Draw_Window();
};

//窗口列表
//vector<struct Window_Element *> v_window;

//绘制Window
void Window_Element::Draw_Window() {
  
  class GUI_Element *tmp = this->head;
  
  //绘制顶层窗口
  if (tmp->Name == "WINDOW") {
    MSG         msg;
    string      title = "Test Window";
    
    int x = atof(tmp->Property["left"].c_str()) * cxScreen;
    int y = atof(tmp->Property["top"].c_str()) * cyScreen;
    int w = (atof(tmp->Property["right"].c_str()) - atof(tmp->Property["left"].c_str())) * cxScreen;
    int h = (atof(tmp->Property["bottom"].c_str()) - atof(tmp->Property["top"].c_str())) * cyScreen;
    
	cout << x << y << w << h << "--------------------------------";
	
    this->hwnd = CreateWindow(
      TEXT("MyClass"),   			  // window class name
      TEXT(title.c_str()),  		        
      WS_OVERLAPPEDWINDOW,     	// window style
      x,           	// initial x position
      y,           	// initial y position
      w,           	// initial x size
      h,           	// initial y size
      NULL,						            // parent window handle
      NULL,                     	// window menu handle
      NULL,          			  	    // program instance handle
      NULL);                    	// creation parameters			
      
    /*
    SetTimer(w.hwnd,             // handle to main window 
      IDT_TIMER1,            // timer identifier 
      1000,                 // 10-second interval 
      (TIMERPROC) NULL);     // no timer callback 

    SetWindowText(w.hwnd, "aaa");    */
	
	//去掉边框和标题栏
	LONG_PTR Style = ::GetWindowLongPtr(hwnd,GWL_STYLE);
	Style = Style &~WS_CAPTION &~WS_SYSMENU &~WS_SIZEBOX;
	::SetWindowLongPtr(hwnd, GWL_STYLE, Style);

	// 实现透明必须设置WS_EX_LAYERED标志
    LONG nRet = ::GetWindowLong(hwnd, GWL_EXSTYLE);
    nRet = nRet | WS_EX_LAYERED;
    ::SetWindowLong(hwnd, GWL_EXSTYLE, nRet);
	
	::SetLayeredWindowAttributes(hwnd, 0, 123, LWA_ALPHA);    // 设置半透明

    ShowWindow(this->hwnd, 1);
    UpdateWindow(this->hwnd);
	
	//发送一个WM_PAINTER消息，绘制子控件。
    //InvalidateRect(this->hwnd, NULL, TRUE);

    //消息循环
    while(GetMessage(&msg, NULL, 0, 0)) {
      TranslateMessage(&msg);
      DispatchMessage(&msg);
    }
  }
}

void DrawBezier(HDC hdc, POINT apt[]) {
    PolyBezier(hdc, apt, 4);
/*
    MoveToEx(hdc, apt[0].x, apt[0].y, NULL);
    LineTo(hdc, apt[1].x, apt[1].y);

    MoveToEx(hdc, apt[2].x, apt[2].y, NULL);
    LineTo(hdc, apt[3].x, apt[3].y);
	*/
}

//绘制Window以外的子控件。同一层，后绘制的可能会覆盖先绘制的;  先父后子，先兄后弟。
void Draw_Element(class GUI_Element *tmp, HDC hdc, HWND hwnd) {
	
  Graphics graphics(hdc);
  Pen blackPen(Color(255,255, 0, 0), 3);
	
  if (tmp->Name == "RECTANGLE" || tmp->Name == "RECT" || tmp->Name == "ELIPSE" || tmp->Name == "LINE") {
	
	//像素值
	int pt = tmp->parent->t;
	int pl = tmp->parent->l;
	int pr = tmp->parent->r;
	int pb = tmp->parent->b;
	
	int l = atof(tmp->Property["left"].c_str()) * (pr - pl) + pl;
	int t = atof(tmp->Property["top"].c_str()) * (pb - pt) + pt;
	int r = atof(tmp->Property["right"].c_str()) * (pr - pl) + pl;
	int b = atof(tmp->Property["bottom"].c_str()) * (pb - pt) + pt;
	
	cout << tmp->parent->Name << " parent name .. \n";
	cout << pl << " "<< pt << " " << pr  << " " << pb <<"  parent ... RECTANGLE\n";
	cout << l << " "<< t  << " " << r  << " " << b <<" local ... RECTANGLE\n";
	
	tmp->l = l;
	tmp->t = t;
	tmp->r = r;
	tmp->b = b;
	
	Rect rect(l, t, r, b);
	
	//RECT和RECTANGEL的区别是前者只做定位使用，并不绘制；后者会绘制矩形。
	if (tmp->Name == "RECT") {
	}
	
	if (tmp->Name == "RECTANGLE") {
		graphics.DrawRectangle(&blackPen, rect);
		
		/*
		HBRUSH hbrush;
		HPEN hpen;

		hpen = CreatePen(PS_SOLID, 10, RED_COLOR);  // 创建红色实心10px粗的画笔
		hbrush = CreateSolidBrush(BLUE_COLOR); // 创建蓝色画刷
		
		SelectObject(hdc, hpen);    // 指定画笔
		SelectObject(hdc, hbrush);  // 指定画刷
		
		Rectangle(hdc,l,t,r,b);
		
		// 清理资源
		DeleteObject(hpen);
		DeleteObject(hbrush);
		*/
	}
	
	//绘制直线
	if (tmp->Name == "LINE") {
		MoveToEx(hdc, l, t, NULL);
		LineTo(hdc, r, b);
	}
	
	if (tmp->Name == "ELIPSE") {    
		Ellipse(hdc,l,t,r,b);
	}
  }
  
  if (tmp->Name == "BEZIER") {
	POINT apt[4];
	
	apt[0].x = 10;
    apt[0].y = 10;

    apt[1].x = 50;
    apt[1].y = 50;

    apt[2].x = 80;
    apt[2].y = 80;

    apt[3].x = 200;
    apt[3].y = 200;
	
	DrawBezier(hdc, apt);
  }
  
	//GDI 文本呈现通常提供比 GDI + 更好的性能和更准确的文本度量。
  if (tmp->Name == "TEXT") {
	
    string s;
    
    s = tmp->Property["caption"];

    for (auto it: var) {
      if (it.first == s) {
        s = it.second;
      }
    }
   
    tmp->t = tmp->parent->t;
    tmp->l = tmp->parent->l;
    tmp->r = tmp->parent->r;
    tmp->b = tmp->parent->b;
    
    RECT re;  
    re.left=tmp->l; re.top=tmp->t; re.right=tmp->r; re.bottom=tmp->b;
    
    int i;
    if (s.substr(0, 4) == "_VAL")
       i = atoi(s.substr(4).c_str());
  
	SetTextColor(hdc,RGB(0,255,0));
	SetBkColor(hdc, 0x0000FF);
	//设置背景颜色为红色
    //SetBkMode(hdc,TRANSPARENT);
	//设置背景透明
	
	HFONT hf;
	LOGFONT lf;
	lf.lfHeight=40;
	lf.lfWidth=40;
	lf.lfEscapement=0;
	hf=CreateFontIndirect(&lf);
	SelectObject(hdc,hf);

    //TextOut(hdc, l, t, s.c_str(), s.length());	  
	// 单行显示 DT_SINGLELINE
	//多行显示, 遇到\r\n能自动换行显示
	//换行显示，超出边界自动换行显示
    DrawText(hdc, Val[i].c_str(), Val[i].length(), &re, DT_LEFT|DT_END_ELLIPSIS | DT_EDITCONTROL | DT_WORDBREAK);
  }
  
  //链接
  if (tmp->Name == "A") {
    cout<< "A...\n";
  }
  
  if (tmp->Property["sleep"]!="")
	Sleep(atoi(tmp->Property["sleep"].c_str()));
	
  if (tmp->child)
    Draw_Element(tmp->child, hdc, hwnd);
  if (tmp->brother)
    Draw_Element(tmp->brother, hdc, hwnd);
}


class MyGUI {
	public:
		MyGUI(char *filename);
		void Draw_Window(struct Window_Element *p);
		int MyGUI::Find_Window(HWND hwnd);
		struct Window_Element *Get_Window(int i);
	private:
		void read_gui(char *gui);
		static LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);
		WNDCLASS            wndClass;
		vector<struct Window_Element *> v_window;
};

struct Window_Element * MyGUI::Get_Window(int i) {
	return v_window[i];
}

//找到hwnd对应的Window_Element的数组下标，如果返回-1表示没有找到。
int MyGUI::Find_Window(HWND hwnd) {
  for (int i=0; i< v_window.size(); i++){
    if (Get_Window(i)->hwnd == hwnd) {
      return i;
    }
  }
  return -1;
}


//读取GUI描述文件，生成树形结构。
void MyGUI::read_gui(char *gui){
  ifstream in(gui);
  string line;
      
  MyAssert(Get_First("hello world"), "hello");
  
  if (in) {
      
    class GUI_Element *last = NULL;
    // line中不包括每行的换行符
    while (getline (in, line)) {
    
      line = Skip_Blank(line);
      cout << line << endl;
          
      if (line == "")
        continue;
	
      // ；开头表示注释
      if (line[0] == ';')
        continue;                
        
      //变量定义
      if (line=="@VAR") {
        while (getline (in, line)) {
          line = Skip_Blank(line);
          cout << line << "\n";          
          
          if (line == "")
            continue;
          if (line[0] == ';')
            continue;
          if (line == "END")
            break;
          
          string l = String_2_Int(line);
          cout << l << " ..\n";
          
          string f = Get_First(l);
          //不是最后一个单词
          while (f != l) {
            Evaluate(f);
            l = Skip_Blank(l.substr(f.length()));
            f = Get_First(l);
          }
          Evaluate(f);
        }
      }

      //图形描述
      if (line=="@GUI") {
        while (getline (in, line)) {
          line = Skip_Blank(line);
          cout << line << "\n";
					
          if (line == "")
            continue;
          if (line[0] == ';')
            continue;   
          if (line=="END")
            break;          
          
          string l = String_2_Int(line);
          cout << l << "\n";

          class GUI_Element *con = new GUI_Element(l);
          
          //顶层控件
          if (con->Level == 1 && con->Name=="WINDOW") {
            con->parent=NULL;
            con->child=NULL;
            con->brother=NULL;
            last = con;
            struct Window_Element *e = (struct Window_Element *)malloc(sizeof(struct Window_Element));
            e->hwnd = 0;
            e->head = con;
            v_window.push_back(e);
            continue;
          } 
          
          //非顶层控件
          if (last != NULL) {
            //last的子控件
            if (con->Level - last->Level == 1) {
              con->parent=last;
              con->child=NULL;
              con->brother=NULL;
              last->child = con;
              last = con;
              continue;
            }

            //last的兄弟控件
            if (con->Level == last->Level) {
              last->brother=con;
              
              con->parent=last->parent;
              con->child=NULL;
              con->brother=NULL;
              last = con;
              continue;
            }
            //last上层控件
            if (con->Level < last->Level && con->Level > 1) {
              while (con->Level != last->Level)
                last = last->parent;
              last->brother = con;
              con->parent=last->parent;
              con->child=NULL;
              con->brother=NULL;
              last = con;
              continue;
            }
            //控件层次错误
            cout << con->Level  << "..\n";
            cout << last->Level  << "..\n";
            if (con->Level - last->Level > 1) {
              cout << "Level error.\n";
              return;
            }
          }
        }
      }


      if (line=="@ZHUSHI") {
		while (getline (in, line)) {
		  line = Skip_Blank(line);
            cout << line << " ............................... \n";
          if (line == "")
            continue;
          if (line[0] == ';')
            continue;
          if (line=="END")
            break;
		}
	  }

	
      //初始化函数
      if (line=="@INIT") {
        while (getline (in, line)) {
          line = Skip_Blank(line);
          cout << line << "\n";
          if (line == "")
            continue;
          if (line[0] == ';')
            continue;
          if (line=="END")
            break;
          string l = String_2_Int(line);
          continue;
        }
      }

      //以@开头，可能为@INIT--初始化函数或者键盘鼠标处理函数。
      if (line[0] == '@') {
        class Proc *p = new(class Proc);
        p->name = line.substr(1);
        
        while (getline (in, line)) {
          line = Skip_Blank(line);
          cout << line << "\n";
          if (line == "")
            continue;
          if (line[0] == ';')
            continue;
          if (line=="END")
            break;
          
          string l = String_2_Int(line);

          string f = Get_First(l);
          //不是最后一个单词
          while (f != l) {
            p->s.push_back(f);
            l = Skip_Blank(l.substr(f.length()));
            f = Get_First(l);
          }
        }
        vp.push_back(p);
      }
    }
  } else {
      cout <<"no such file" << endl;
  }
}

MyGUI::MyGUI(char *filename) {
  
  wndClass.style          = CS_HREDRAW | CS_VREDRAW;
  //同一窗口类公用一个窗口处理过程
  wndClass.lpfnWndProc    = WndProc;
  wndClass.cbClsExtra     = 0;
  wndClass.cbWndExtra     = 0;
  wndClass.hInstance      = NULL;
  wndClass.hIcon          = LoadIcon(NULL, IDI_APPLICATION);
  wndClass.hCursor        = LoadCursor(NULL, IDC_ARROW);
  wndClass.hbrBackground  = (HBRUSH)GetStockObject(WHITE_BRUSH);
  wndClass.lpszMenuName   = NULL;
  wndClass.lpszClassName  = TEXT("MyClass");
  
  RegisterClass(&wndClass);
  
  read_gui(filename);
}

void MyGUI::Draw_Window(struct Window_Element *p) {
	p->Draw_Window();
}

MyGUI *gui;


//返回p所处的控件
GUI_Element * Find_Element(POINT p, GUI_Element *e) {
  GUI_Element *last = NULL;

  cout << "e->name = " << e->Name << "\n";
  
  if ((p.x >= e->l) && (p.y >= e->t) && (p.x <= e->r) && (p.y <= e->b))
      last = e;
    
  if (e->child != NULL) {
    if (e->child->Name == "RECTANGLE") {
      GUI_Element *tmp = Find_Element(p, e->child);
      if (tmp!=NULL)
        last = tmp;
    }
  } 
  
  if (e->brother!= NULL) {
    if (e->brother->Name == "RECTANGLE") {
      GUI_Element *tmp = Find_Element(p, e->brother);
      if (tmp!=NULL)
        last = tmp;
    }
  } 
  
  return last;
}

// vp里查找名为name的过程
class Proc * Find_Proc(string name) {
		for (auto i:vp) {
			if (i->name == name)
				return i;
		}
		return NULL;
}

//同一个窗口类公用一个窗口处理过程
LRESULT CALLBACK MyGUI::WndProc(HWND hWnd, UINT message, 
   WPARAM wParam, LPARAM lParam)
{
  int i;
  string s;
  RECT r;  
  
  switch(message) {
    //移动标题栏等
    case WM_SYSCOMMAND:
      i = gui->Find_Window(hWnd);
      
      //取得窗口客户区坐标
      GetClientRect(hWnd, &r);
      
      //取得移动后，修改窗体的客户区坐标。
      gui->Get_Window(i)->head->l = r.left;
      gui->Get_Window(i)->head->t = r.top;
      gui->Get_Window(i)->head->t = r.right;
      gui->Get_Window(i)->head->b = r.bottom;
			
      //InvalidateRect(hWnd, NULL, TRUE);
      
      return DefWindowProc(hWnd, message, wParam, lParam);
      
    case WM_LBUTTONDOWN:
      
      POINT point;
      
      GetCursorPos(&point);            // 获取鼠标指针位置（屏幕坐标）
      ScreenToClient(hWnd, &point);    // 将鼠标指针位置转换为窗口坐标
      cout << point.x << " "<< point.y << "\n";
      
      i = gui->Find_Window(hWnd);
      //遍历Window_Element，得到鼠标点击点所在的控件，并调用其处理函数。
      //遍历方式：先父后子，先兄后弟。
      class GUI_Element * tmp;
      tmp = Find_Element(point, gui->Get_Window(i)->head);
      
      s = tmp->Property["click"];
			cout << s  << " s = \n";
      int j;
      if (s.substr(0, 4) == "_VAL") {
        j = atoi(s.substr(4).c_str());
        cout<< j << " j =\n";
      }
      cout << Val[j] << " is clicked\n";
	  	  
	  save_bmp("test.bmp", GetDC(hWnd));
	  
	  class Proc * p;
	  p = Find_Proc(Val[j]);	  
      if (p!=NULL)
		p->Call();	
	  return 0;
    case WM_LBUTTONDBLCLK:
      return 0;
    case WM_RBUTTONDOWN:
      return 0;
    case WM_RBUTTONDBLCLK:
      return 0;
    case WM_MBUTTONDOWN:
      return 0;
    case WM_MBUTTONDBLCLK:
      return 0;
    //设置Edit控件的文本
    case WM_SETTEXT:
      return 0;
    case WM_TIMER: 
      //InvalidateRect(hWnd, NULL, TRUE);
      return 0;
      
    // WINDOW以外图形元素的绘制
    case WM_PAINT:
      PAINTSTRUCT pt;
      HDC hdc;
	  HPEN hpen; // 画笔
      
      hdc=BeginPaint(hWnd,&pt);

	  // 创建画笔
      hpen = CreatePen(PS_SOLID, 1, RGB(0, 0, 255));
	  // 选中画笔
      SelectObject(hdc, hpen);
      
      i = gui->Find_Window(hWnd);
            
      //取得窗口客户区坐标
      GetClientRect(hWnd, &r);
            
      //存储当前窗口客户区的top left right bottom
      gui->Get_Window(i)->head->l = r.left;
      gui->Get_Window(i)->head->t = r.top;
      gui->Get_Window(i)->head->r = r.right;
      gui->Get_Window(i)->head->b = r.bottom;

	  //Sleep(atoi(v_window[i]->head->Property["sleep"].c_str()));
      Draw_Element(gui->Get_Window(i)->head->child, hdc, hWnd);
      
	  // 删除画笔
      DeleteObject(hpen);
	  
      EndPaint(hWnd,&pt);
	  return 0;
    case WM_DESTROY:
      PostQuitMessage(0);
      return 0;
    default:
      return DefWindowProc(hWnd, message, wParam, lParam);
  }
  return 0;
}


int main(int argc, char **argv) {
  
  GdiplusStartupInput gdiplusStartupInput;
  ULONG_PTR           gdiplusToken;
	
  SetConsoleOutputCP(65001);
  cxScreen=GetSystemMetrics(SM_CXSCREEN);
  cyScreen=GetSystemMetrics(SM_CYSCREEN);
  if (argc == 1) {
    cout << "Need file name as args.\n";
    exit(1);
  }
  
  GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

  gui = new MyGUI(argv[1]);

  //打印所有Proc，确认读取无误。
  
  gui->Draw_Window(gui->Get_Window(0));
  
  delete gui;
  
  //释放内存
  GdiplusShutdown(gdiplusToken);
  
  return 0;
}