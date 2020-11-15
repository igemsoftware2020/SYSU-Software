#include "DAO.hpp"
#include "common.hpp"
#include "entity.hpp"
#include "utility.hpp"

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
using std::queue;
using std::unordered_map;

DesignGraph::DesignGraph() {
}

DesignGraph::DesignGraph(const json& j) {
    getValueFromJson<string>(j, "persistentIdentity", persistentIdentity);
    getValueFromJson<string>(j, "article", article);
    getValueFromJson<string>(j, "description", description);

    activities.clear();
    if (j.find("Activity") != j.end() && j["Activity"].is_null() == false) {
        for (auto const& node : j["Activity"]) {
            activities.push_back(make_shared<Activity>(Activity(node)));
        }
    }

    componentDefinitions.clear();
    if (j.find("ComponentDefinition") != j.end() && j["ComponentDefinition"].is_null() == false) {
        for (auto const& node : j["ComponentDefinition"]) {
            componentDefinitions.push_back(make_shared<ComponentDefinition>(ComponentDefinition(node)));
        }
    }

    int sum_iGEM = 0, sum_all = 0;
    for (auto const& p_comdef : componentDefinitions) {
        if (p_comdef->displayId.substr(0, 4) == "BBa_") {
            sum_iGEM++;
        }
        sum_all++;
    }
    if (sum_iGEM > sum_all / 2) {
        is_iGEM = true;
    } else {
        is_iGEM = false;
    }
}

vector<shared_ptr<BaseComDef>> DesignGraph::getBaseComDef(const bool& recursive_flag) {
    auto v = vector<shared_ptr<BaseComDef>>();
    for (auto p : componentDefinitions) {
        v.push_back(make_shared<BaseComDef>(*p));
    }
    if (recursive_flag == false) return v;

    v.clear();
    auto in = unordered_map<string, bool>();
    auto p_comdef_direct = unordered_map<string, shared_ptr<ComponentDefinition>>();
    auto q = queue<string>();
    while (!q.empty()) q.pop();
    string pid;
    for (auto p_comdef : componentDefinitions) {
        pid = p_comdef->persistentIdentity;
        q.push(pid);
        in[pid] = true;
        p_comdef_direct[pid] = p_comdef;
        for (auto p_com : p_comdef->components) {
            pid = deleteTail(p_com->definition);
            if (!in[pid]) {
                in[pid] = true;
                q.push(pid);
            }
        }
    }

    string cur;
    while (!q.empty()) {
        cur = q.front();
        q.pop();
        shared_ptr<BaseComDef> p = nullptr;
        vector<string> com_pids;
        if (p_comdef_direct[cur]) {
            auto p_comdef = p_comdef_direct[cur];
            p = make_shared<BaseComDef>(*p_comdef);
            com_pids = p_comdef->getComponentPids();
        } else {
            auto par = getBaseComDefAndComponent(is_iGEM, cur);
            p = par.first;
            com_pids = par.second;
        }
        v.push_back(p);
        for (auto pid : com_pids) {
            if (!in[pid]) {
                in[pid] = true;
                q.push(pid);
            }
        }
    }

    return v;
}

vector<string> DesignGraph::getComDefRoots() {
    auto uf = UnionFind<string>();
    for (auto const& p_comdef : componentDefinitions) {
        for (auto const& p_com : p_comdef->components) {
            uf.faRelation(deleteTail(p_com->definition), p_comdef->persistentIdentity);
        }
    }
    return uf.getRoot();
}

vector<vector<shared_ptr<BaseComDef>>> DesignGraph::getStructure(const bool& recursive_flag) {
    auto linkedlists = vector<vector<shared_ptr<BaseComDef>>>();
    if (is_iGEM == false) {
        auto linkedlist = vector<shared_ptr<BaseComDef>>();
        for (auto const& p_comdef : componentDefinitions) {
            auto p = make_shared<BaseComDef>(BaseComDef(p_comdef->persistentIdentity, p_comdef->displayId, p_comdef->useRole, p_comdef->role));
            linkedlist.push_back(p);
        }
        linkedlists.push_back(linkedlist);
    } else {
        auto roots = getComDefRoots();
        auto is_root = unordered_map<string, bool>();
        for (auto const& value : roots) {
            is_root[value] = true;
        }

        for (auto const& p_comdef : componentDefinitions) {
            if (is_root[p_comdef->persistentIdentity]) {
                auto linkedlist = getElementLinkedList(is_iGEM, p_comdef, recursive_flag);
                linkedlists.push_back(linkedlist);
            }
        }
    }
    return linkedlists;
}

void DesignGraph::output() {
    for (auto const& p_comdef : componentDefinitions) {
        cout << "comdef name = " << p_comdef->displayId << endl;
    }
}

json DesignGraph::generateJson() {
    json j;
    j["persistentIdentity"] = persistentIdentity;
    j["article"] = article;
    j["description"] = description;
    j["ComponentDefinition"] = vector<json>();
    for (auto const& p_comdef : componentDefinitions) {
        j["ComponentDefinition"].push_back(p_comdef->generateJson());
    }
    return j;
}

}  // namespace RoadmapSearch