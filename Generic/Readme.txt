C新泛型系统   该系统实现C宏替换以及泛型特化


#define A 12

Type T, U;

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