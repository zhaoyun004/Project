#include <iostream>

int main(int argc, char* argv[])
{
    int i = 1;
    _asm 
    {
        mov dword ptr [i],2
    }
    std::cout << i << std::endl;
    return 0;
}