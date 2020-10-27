#pragma once

#include <functional>

#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {

using std::cin;
using std::cout;
using std::endl;
using std::make_shared;
using std::ostream;
using std::pair;
using std::shared_ptr;
using std::string;
using std::tuple;
using json = nlohmann::json;
using stringtream = std::stringstream;
using std::function;
using std::priority_queue;
using std::queue;
using std::unordered_map;

struct CompareComdefGradePair {
    bool operator()(const pair<string, int>& lhs, const pair<string, int>& rhs) {
        return lhs.second > rhs.second;
    }
};

pair<shared_ptr<BaseComDef>, vector<string>> getBaseComDefAndComponent(const bool& is_iGEM, const string persistentIdentity);

vector<string> getComponent(const bool& is_iGEM, const string persistentIdentity);

vector<string> getGraphWithElements(const bool& is_iGEM, const vector<shared_ptr<BaseComDef>>& baseComDefs, const int& limit);

vector<shared_ptr<BaseComDef>> getElementLinkedList(const bool& is_iGEM, const shared_ptr<ComponentDefinition>& root, const bool& recursive_flag);

vector<string> getGraphWithStructures(const bool&, const vector<vector<shared_ptr<BaseComDef>>>& linkedlists, const bool& recursive_flag, const int& limit);

vector<string> getCDSName(const string& name, const int& limit);

/*** update database ***/

void updatePaperComdefName();

void updateRoleSeq(const int& offset, const int& cnt);

void updateComRoleSeq(const int& offset, const int& cnt);

}  // namespace RoadmapSearch