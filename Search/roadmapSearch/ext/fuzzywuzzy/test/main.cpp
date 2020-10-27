#include <iostream>
#include <utility>
#include <vector>

#include "fuzzywuzzy.hpp"
#include "process.hpp"

using std::cout;
using std::endl;
using std::pair;
using std::vector;

int main() {
    const string a = "I'm in your mind", b = "I'm in your mind fuzz";
    const string c = "fuzzy wuzzy was a bear", d = "wuzzy fuzzy was a bear";

    std::cout << fuzz::ratio(a, b) << '\n';
    std::cout << fuzz::partial_ratio(a, b) << '\n';
    std::cout << fuzz::token_sort_ratio(c, d) << '\n';
}
