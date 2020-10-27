#include "utility.hpp"

#include <cctype>

#include "DAO.hpp"
#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {

using std::cin;
using std::cout;
using std::endl;
using std::get;
using std::make_shared;
using std::ostream;
using std::shared_ptr;
using std::vector;
using json = nlohmann::json;
using stringtream = std::stringstream;
using std::max;
using std::min;
using std::queue;
using std::tolower;
using std::unordered_map;

int Levenshtein(const string& a, const string& b, const bool& case_sensitive) {
    auto dp = vector<int>();
    for (int i = 0; i <= max(a.size(), b.size()); i++) {
        dp.push_back(0);
    }
    for (int j = 1; j <= b.size(); j++) {
        dp[j] = j;
    }
    int t1, t2;
    for (int i = 1; i <= a.size(); i++) {
        t1 = dp[0]++;
        for (int j = 1; j <= b.size(); j++) {
            t2 = dp[j];
            if ((case_sensitive == true && a[i - 1] == b[j - 1]) || (case_sensitive == false && tolower(a[i - 1]) == tolower(b[j - 1]))) {
                dp[j] = t1;
            } else {
                dp[j] = min(t1, min(dp[j - 1], dp[j])) + 1;
            }
            t1 = t2;
        }
    }
    return dp[b.size()];
}

}  // namespace RoadmapSearch
