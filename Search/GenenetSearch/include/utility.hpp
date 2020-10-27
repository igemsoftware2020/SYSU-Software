#pragma once

#include <array>

#include "common.hpp"

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
using std::array;
using std::max;
using std::queue;
using std::unordered_map;

template <class T>
struct UnionFind {
    unordered_map<T, T> fa;

    UnionFind();

    void initial(const T& x);

    T findFa(const T& x);

    void faRelation(const T& son, const T& father);

    vector<T> getRoot();
};

template <typename T>
UnionFind<T>::UnionFind() {
    fa.clear();
}
template <typename T>
void UnionFind<T>::initial(const T& x) {
    if (fa.find(x) == fa.end()) {
        fa[x] = x;
    }
}

template <typename T>
T UnionFind<T>::findFa(const T& x) {
    initial(x);
    if (fa[x] != x) {
        fa[x] = findFa(fa[x]);
    }
    return fa[x];
}

template <typename T>
void UnionFind<T>::faRelation(const T& son, const T& father) {
    findFa(son);
    findFa(father);
    initial(fa[son]);
    if (fa[son] != son) return;
    fa[fa[son]] = father;
}

template <typename T>
vector<T> UnionFind<T>::getRoot() {
    T x;
    auto roots = vector<T>();
    for (auto const& par : fa) {
        x = par.first;
        fa[x] = findFa(x);
        if (fa[x] == x) {
            roots.push_back(x);
        }
    }
    return roots;
}

int Levenshtein(const string& a, const string& b, const bool& case_sensitive);

}  // namespace RoadmapSearch
