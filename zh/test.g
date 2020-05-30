Type T, U;
T add(T a, T b, U c) {
    return a + b;
}

int main() {
    add(12, 34)         //特化成为add_int
    add(12.3, 34.5)     //特化成为add_float
}
