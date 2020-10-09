#include <stdio.h>

#define SUM(a, b) { a + b }

//type指定数据类型
#define SWAP(a, b, type) {type c; c = a; a = b; b = c;}

#define MAX(a,b) ((a) > (b) ? (a) : (b))

#define MAX3(a,b,c) ((a) > (b) ? MAX(a,c) : (MAX(b,c)))

int main()
{
	float c = SUM(4, 8.7);
	int a = SUM(4, 8);
	
   /* 我的第一个 C 程序 */
   printf("Hello, World! %f %d  \n", c, a);
   
   int b = 3;
   
   SWAP(a, b, int)
   printf("Hello, World! %d %f \n",  a, MAX3(a, b, c));   
   
   return 0;
}