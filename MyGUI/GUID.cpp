#include <unistd.h>
#include <stdlib.h>
#include <iostream>

using namespace std;

int main() {
	int pid;
	
	pid = fork();
	
	//父进程 -- 得到子进程号
	if (pid>0) {
	
	} 
	
	//子进程
	if (pid==0) {
	}
	
	if (pid<0) {
		cout << "Fork error\n";
	}
	
	return 0;
}