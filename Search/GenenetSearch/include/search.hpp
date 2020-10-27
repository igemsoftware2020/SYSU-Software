#pragma once

#include "common.hpp"
#include "entity.hpp"

namespace std {
template <>
class hash<pair<string, string>> {
public:
    size_t operator()(const pair<string, string> &par) const {
        return hash<string>()(par.first) ^ hash<string>()(par.second);
    }
};
};  // namespace std

extern priority_queue<Proposal> proposals;
extern unordered_map<pair<string, string>, string> pname_tfname_effect;

void initSearch();

void getAllTFs();

void getAllEffect();

void getPossiblePros(const int &id);

vector<TP> getPossibleTFs(const string &pro_name, const string &effect);

void searchProposal();
