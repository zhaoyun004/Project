// hash example
#include <iostream>
#include <functional>
#include <vector>
#include <algorithm>
#include <iterator>

int main() {
    std::hash<int> hash_int;// Function object to hash int
    std::vector<int> n{-5, -2, 2, 5, 10};
    std::transform(std::begin(n), std::end(n),std::ostream_iterator<size_t> (std:: cout," "), hash_int);
}
