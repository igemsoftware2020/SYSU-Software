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
using std::make_tuple;
using std::ostream;
using std::pair;
using std::shared_ptr;
using std::string;
using std::tuple;
using json = nlohmann::json;
using stringtream = std::stringstream;
using std::priority_queue;
using std::queue;
using std::to_string;
using std::unordered_map;

vector<string> getComponent(const bool& is_iGEM, const string persistentIdentity) {
    auto v = vector<string>();
    if (is_iGEM == false) return v;

    auto stmt = con->prepareStatement("select definition from Component where father_id = ?");
    stmt->setString(1, persistentIdentity);
    auto res = stmt->executeQuery();
    while (res->next()) {
        v.push_back(deleteTail(res->getString("definition")));
    }
    delete res;
    delete stmt;

    return v;
}

pair<shared_ptr<BaseComDef>, vector<string>> getBaseComDefAndComponent(const bool& is_iGEM, const string persistentIdentity) {
    if (is_iGEM == false) {
        auto stmt = con->prepareStatement("select name, role from PaperComponentDefinition where persistentIdentity = ?");
        stmt->setString(1, persistentIdentity);
        auto res = stmt->executeQuery();
        string displayId, useRole;
        auto role = vector<string>();
        while (res->next()) {
            displayId = res->getString("name");
            useRole = res->getString("role");
        }
        auto p = make_shared<BaseComDef>(BaseComDef(persistentIdentity, displayId, useRole, role));

        auto v = getComponent(is_iGEM, persistentIdentity);

        delete stmt;
        delete res;

        return pair<shared_ptr<BaseComDef>, vector<string>>(p, v);
    }

    auto stmt = con->prepareStatement("select displayId, useRole, role from ComponentDefinition where persistentIdentity = ?");
    stmt->setString(1, persistentIdentity);
    auto res = stmt->executeQuery();

    string displayId, roles, rname, useRole;
    auto role = vector<string>();
    while (res->next()) {
        displayId = res->getString("displayId");
        useRole = res->getString("useRole");
        roles = res->getString("role");
        auto root = json::parse(roles);
        for (auto node : root) {
            node.get_to(rname);
            role.push_back(rname);
        }
    }
    auto p = make_shared<BaseComDef>(BaseComDef(persistentIdentity, displayId, useRole, role));

    auto v = getComponent(is_iGEM, persistentIdentity);

    delete res;
    delete stmt;

    return pair<shared_ptr<BaseComDef>, vector<string>>(p, v);
}

vector<string> getGraphWithElements_iGEM(const vector<shared_ptr<BaseComDef>>& baseComDefs, const int& limit) {
    auto comdef_grade = unordered_map<string, int>();
    sql::PreparedStatement* stmt = nullptr;
    sql::ResultSet* res = nullptr;
    string comdef_pid, comdef_displayId;
    for (auto const& b : baseComDefs) {
        stmt = con->prepareStatement("select persistentIdentity, displayId from ComponentDefinition where persistentIdentity = ? or displayId = ?");
        stmt->setString(1, b->persistentIdentity);
        stmt->setString(2, b->displayId);
        res = stmt->executeQuery();

        while (res->next()) {
            comdef_pid = res->getString("persistentIdentity");
            comdef_displayId = res->getString("displayId");
            if (comdef_pid == b->persistentIdentity) {
                comdef_grade[comdef_pid] += 20;
            } else if (comdef_displayId == b->displayId) {
                comdef_grade[comdef_pid] += 10;
            }
        }

        // for (auto const& value : b->role) {
        //     stmt = con->prepareStatement("select persistentIdentity from ComponentDefinition where role like ?");
        //     stmt->setString(1, "%" + value + "%");
        //     res = stmt->executeQuery();
        //     while (res->next()) {
        //         comdef_pid = res->getString("persistentIdentity");
        //         comdef_grade[comdef_pid] += 1;
        //     }
        // }
    }

    auto graph_grade = unordered_map<string, int>();
    auto graph_grade_pairs = vector<pair<string, int>>();
    string graph_id;
    for (auto const& par : comdef_grade) {
        stmt = con->prepareStatement("select graph_id from DesignGraph_ComponentDefinition where componentDefinition_id = ?");
        stmt->setString(1, par.first);
        res = stmt->executeQuery();
        while (res->next()) {
            graph_id = res->getString("graph_id");
            if (graph_grade.find(graph_id) == graph_grade.end()) {
                graph_grade[graph_id] = 0;
            }
            graph_grade[graph_id] += par.second;
        }
    }

    for (auto const& par : graph_grade) {
        graph_grade_pairs.push_back(par);
    }

    sort(graph_grade_pairs.begin(), graph_grade_pairs.end(), [=](pair<string, int>& a, std::pair<string, int>& b) {
        return a.second > b.second;
    });

    auto graphs = vector<string>();
    int count = 0;
    for (auto const& par : graph_grade_pairs) {
        graphs.push_back(par.first);
        count++;
        if (count == limit) break;
    }

    delete stmt;
    delete res;

    return graphs;
}

vector<string> getGraphWithElements_paper(const vector<shared_ptr<BaseComDef>>& baseComDefs, const int& limit) {
    auto comdef_grade = unordered_map<string, int>();
    auto stmt = con->createStatement();
    sql::PreparedStatement* prep_stmt;
    sql::ResultSet* res = nullptr;
    string comdef_pid, comdef_name;
    for (auto const& b : baseComDefs) {
        res = stmt->executeQuery("select persistentIdentity, name from PaperComponentDefinition");

        while (res->next()) {
            comdef_pid = res->getString("persistentIdentity");
            comdef_name = res->getString("name");
            auto rt = -Levenshtein(b->displayId, comdef_name, false);
            if (abs(rt) <= 1)
                rt += 1000;
            else if (abs(rt) <= 2)
                rt += 100;
            else if (abs(rt) >= 5)
                rt = 0;
            comdef_grade[comdef_pid] += rt;
        }
    }

    auto graph_grade = unordered_map<string, int>();
    auto graph_grade_pairs = vector<pair<string, int>>();
    string graph_id;
    for (auto const& par : comdef_grade) {
        prep_stmt = con->prepareStatement("select graph_id from PaperComponentDefinition_PaperGraph where componentDefinition_id = ?");
        prep_stmt->setInt(1, atoi(par.first.c_str()));
        res = prep_stmt->executeQuery();
        while (res->next()) {
            graph_id = to_string(res->getInt("graph_id"));
            if (graph_grade.find(graph_id) == graph_grade.end()) {
                graph_grade[graph_id] = 0;
            }
            graph_grade[graph_id] += par.second;
        }
    }

    for (auto const& par : graph_grade) {
        graph_grade_pairs.push_back(par);
    }

    sort(graph_grade_pairs.begin(), graph_grade_pairs.end(), [=](pair<string, int>& a, std::pair<string, int>& b) {
        return a.second > b.second;
    });

    auto graphs = vector<string>();
    int count = 0;
    for (auto const& par : graph_grade_pairs) {
        graphs.push_back(par.first);
        count++;
        if (count == limit) break;
    }

    delete prep_stmt;
    delete stmt;
    delete res;

    return graphs;
}

vector<string> getGraphWithElements(const bool& is_iGEM, const vector<shared_ptr<BaseComDef>>& baseComDefs, const int& limit) {
    if (is_iGEM) {
        return getGraphWithElements_iGEM(baseComDefs, limit);
    }
    return getGraphWithElements_paper(baseComDefs, limit);
}

template <typename T>
void pushVectorIntoQueue(const vector<T>& vec, queue<T>& q) {
    for (auto const& value : vec) {
        q.push(value);
    }
}

vector<shared_ptr<BaseComDef>> getElementLinkedList(const bool& is_iGEM, const shared_ptr<ComponentDefinition>& root, const bool& recursive_flag) {
    auto linkedlist = vector<shared_ptr<BaseComDef>>();
    auto q = queue<string>();
    for (auto const& p_com : root->components) {
        q.push(deleteTail(p_com->definition));
    }
    while (!q.empty()) {
        auto pid = q.front();
        q.pop();
        auto par = getBaseComDefAndComponent(is_iGEM, pid);
        if (recursive_flag == true) {
            if (par.second.size() == 0) {
                linkedlist.push_back(par.first);
            }
            pushVectorIntoQueue<string>(par.second, q);
        } else {
            linkedlist.push_back(par.first);
        }
    }
    return linkedlist;
}

string getRoleSeqOfLinkedList(const vector<shared_ptr<BaseComDef>>& linkedlist) {
    string roleSeq = "";
    for (auto const& p_b : linkedlist) {
        roleSeq += roles_char[p_b->useRole];
    }
    return roleSeq;
}

vector<string> getGraphWithStructures_iGEM(const vector<vector<shared_ptr<BaseComDef>>>& linkedlists, const bool& recursive_flag, const int& limit) {
    priority_queue<pair<string, int>, vector<pair<string, int>>, CompareComdefGradePair> comdef_grade_q;

    unordered_map<string, string>& comdef_map = (recursive_flag == false) ? comdef_comRoleSeq : comdef_comRoleSeqRecursive;
    while (!comdef_grade_q.empty()) comdef_grade_q.pop();
    string roleSeq = "";
    for (auto const& linkedlist : linkedlists) {
        roleSeq = getRoleSeqOfLinkedList(linkedlist);
        for (auto const& par : comdef_map) {
            int rt = -Levenshtein(roleSeq, par.second, true);
            if (comdef_grade_q.size() <= 10 * limit || rt > comdef_grade_q.top().second) {  // edited
                comdef_grade_q.push(pair<string, int>(par.first, rt));
                while (comdef_grade_q.size() > 10 * limit) {
                    comdef_grade_q.pop();
                }
            }
        }
    }

    auto graph_grade = unordered_map<string, int>();
    auto stmt = con->prepareStatement("select graph_id from DesignGraph_ComponentDefinition where componentDefinition_id = ?");
    sql::ResultSet* res = nullptr;
    string graph_id;

    while (!comdef_grade_q.empty()) {
        auto par = comdef_grade_q.top();
        comdef_grade_q.pop();
        stmt->setString(1, par.first);
        res = stmt->executeQuery();
        while (res->next()) {
            graph_id = res->getString("graph_id");

            if (graph_grade.find(graph_id) == graph_grade.end()) {
                graph_grade[graph_id] = 0;
            }
            graph_grade[graph_id] += par.second;
        }
    }

    auto graph_grade_pairs = vector<pair<string, int>>();
    for (auto const& par : graph_grade) {
        graph_grade_pairs.push_back(par);
    }

    sort(graph_grade_pairs.begin(), graph_grade_pairs.end(), [=](pair<string, int>& a, std::pair<string, int>& b) {
        return a.second > b.second;
    });

    auto graphs = vector<string>();
    int count = 0;
    for (auto const& par : graph_grade_pairs) {
        graphs.push_back(par.first);
        count++;
        if (count == limit) break;
    }

    delete stmt;
    delete res;

    return graphs;
}

vector<string> getGraphWithStructures_paper(const vector<vector<shared_ptr<BaseComDef>>>& linkedlists, const bool& recursive_flag, const int& limit) {
    auto graph_grade = unordered_map<string, int>();
    auto stmt = con->createStatement();
    auto res = stmt->executeQuery("select persistentIdentity, role_seq from PaperGraph");

    auto roleSeqs = vector<string>();
    for (auto const& linkedlist : linkedlists) {
        auto roleSeq = getRoleSeqOfLinkedList(linkedlist);
        roleSeqs.push_back(roleSeq);
    }

    string graph_id, graph_roleSeq;
    while (res->next()) {
        graph_id = to_string(res->getInt("persistentIdentity"));
        graph_roleSeq = res->getString("role_seq");
        graph_grade[graph_id] = 0;
        for (auto const& roleSeq : roleSeqs) {
            graph_grade[graph_id] += -Levenshtein(roleSeq, graph_roleSeq, true);
        }
    }

    auto graph_grade_pairs = vector<pair<string, int>>();
    for (auto const& par : graph_grade) {
        graph_grade_pairs.push_back(par);
    }

    sort(graph_grade_pairs.begin(), graph_grade_pairs.end(), [=](pair<string, int>& a, std::pair<string, int>& b) {
        return a.second > b.second;
    });

    auto graphs = vector<string>();
    int count = 0;
    for (auto const& par : graph_grade_pairs) {
        graphs.push_back(par.first);
        count++;
        if (count == limit) break;
    }

    delete stmt;
    delete res;

    return graphs;
}

vector<string> getGraphWithStructures(const bool& is_iGEM, const vector<vector<shared_ptr<BaseComDef>>>& linkedlists, const bool& recursive_flag, const int& limit) {
    if (is_iGEM) {
        return getGraphWithStructures_iGEM(linkedlists, recursive_flag, limit);
    }
    return getGraphWithStructures_paper(linkedlists, recursive_flag, limit);
}

vector<string> getCDSName(const string& name, const int& limit) {
    priority_queue<pair<string, int>, vector<pair<string, int>>, CompareComdefGradePair> CDS_grade_q;

    while (!CDS_grade_q.empty()) {
        CDS_grade_q.pop();
    }

    vector<string> namesources = {"name", "synonyms", "ordered_locus_name", "ORF_name"};

    sql::PreparedStatement* stmt = nullptr;
    sql::ResultSet* res = nullptr;

    for (auto const& namesource : namesources) {
        string statement = "select distinct " + namesource + " from UniprotCDS";
        stmt = con->prepareStatement(statement);
        res = stmt->executeQuery();

        string CDSname = "";
        int rt = 0;
        while (res->next()) {
            CDSname = res->getString(namesource);
            rt = -Levenshtein(CDSname, name, false);
            if (CDS_grade_q.size() < limit || rt > CDS_grade_q.top().second) {
                CDS_grade_q.push(pair<string, int>(CDSname, rt));
                while (CDS_grade_q.size() > limit) {
                    CDS_grade_q.pop();
                }
            }
        }
    }

    delete stmt;
    delete res;

    auto similars = vector<string>();
    while (!CDS_grade_q.empty()) {
        auto par = CDS_grade_q.top();
        similars.push_back(par.first);
        CDS_grade_q.pop();
    }

    string tmp = "";
    int similar_size = similars.size();
    if (similars.size() > 1) {
        for (int i = 0; i < similar_size / 2; i++) {
            tmp = similars[i];
            similars[i] = similars[similar_size - i - 1];
            similars[similar_size - i - 1] = tmp;
        }
    }

    return similars;
}

/******* database update *******/

void updatePaperComdefName() {
    auto stmt = con->createStatement();
    auto res = stmt->executeQuery("select distinct origin_name from PaperComponentDefinition where role = \'CDS\'");

    auto update = con->prepareStatement("update PaperComponentDefinition set name = ? where origin_name = ?");

    string origin_name = "", name = "";
    while (res->next()) {
        origin_name = res->getString("origin_name");
        auto similars = getCDSName(origin_name, 1);
        name = similars[0];

        update->setString(1, name);
        update->setString(2, origin_name);
        update->execute();
    }

    delete update;
    delete stmt;
    delete res;
}

vector<string> getComponentLinkedList(const bool& is_iGEM, const string& root_pid, const bool& recursive_flag) {
    auto coms = getComponent(is_iGEM, root_pid);

    if (recursive_flag == false) {
        return coms;
    }

    // recursive_flag = true
    string pid;
    auto linkedlist = vector<string>();
    auto q = queue<string>();
    pushVectorIntoQueue(coms, q);

    while (!q.empty()) {
        auto pid = q.front();
        q.pop();
        coms = getComponent(is_iGEM, pid);
        if (coms.size() == 0) {
            linkedlist.push_back(pid);
        }
        pushVectorIntoQueue<string>(coms, q);
    }
    return linkedlist;
}

extern unordered_map<string, char> roles_char;
extern unordered_map<char, string> char_roles;

void updateRoleSeq(const int& offset, const int& cnt) {
    auto stmt = con->prepareStatement("select persistentIdentity from ComponentDefinition limit ?, ?");
    stmt->setInt(1, offset);
    stmt->setInt(2, cnt);
    auto res = stmt->executeQuery();

    auto update_roleSeq = con->prepareStatement("update ComponentDefinition set roleSeq = ? where persistentIdentity = ?");
    auto update_useRole = con->prepareStatement("update ComponentDefinition set useRole = ? where persistentIdentity = ?");

    string pid, roleSeq = "", useRole = "";
    while (res->next()) {
        pid = res->getString("persistentIdentity");
        auto par = getBaseComDefAndComponent(true, pid);

        useRole = "";
        roleSeq = "";
        for (auto const& r : par.first->role) {
            for (auto const& basic_role : basic_roles) {
                if (r == basic_role) {
                    useRole = basic_role;
                    roleSeq = roles_char[basic_role];
                    break;
                }
            }
            if (useRole != "") break;
        }
        if (useRole == "") {
            useRole = "Composite";
            roleSeq = roles_char["Composite"];
        }

        update_roleSeq->setString(1, roleSeq);
        update_roleSeq->setString(2, pid);
        update_roleSeq->execute();

        update_useRole->setString(1, useRole);
        update_useRole->setString(2, pid);
        update_useRole->execute();
    }

    delete update_useRole;
    delete update_roleSeq;
    delete res;
    delete stmt;
}

void updateComRoleSeq(const int& offset, const int& cnt) {
    auto stmt = con->prepareStatement("select persistentIdentity from ComponentDefinition limit ?, ?");
    stmt->setInt(1, offset);
    stmt->setInt(2, cnt);

    auto res = stmt->executeQuery();
    auto update = con->prepareStatement("update ComponentDefinition set comRoleSeq = ?, comRoleSeqRecursive = ? where persistentIdentity = ?");
    auto get_roleSeq = con->prepareStatement("select RoleSeq from ComponentDefinition where persistentIdentity = ?");
    sql::ResultSet* res_roleSeq = nullptr;

    string pid, s, sr;
    while (res->next()) {
        pid = res->getString("persistentIdentity");

        auto linkedlist = getComponentLinkedList(true, pid, false);

        s = "";
        for (auto const& compid : linkedlist) {
            get_roleSeq->setString(1, compid);
            res_roleSeq = get_roleSeq->executeQuery();
            while (res_roleSeq->next()) {
                s += res_roleSeq->getString("roleSeq");
            }
        }

        linkedlist = getComponentLinkedList(true, pid, true);
        sr = "";
        for (auto const& compid : linkedlist) {
            get_roleSeq->setString(1, compid);
            res_roleSeq = get_roleSeq->executeQuery();
            while (res_roleSeq->next()) {
                sr += res_roleSeq->getString("roleSeq");
            }
        }

        update->setString(1, s);
        update->setString(2, sr);
        update->setString(3, pid);
        update->execute();
    }

    delete get_roleSeq;
    delete res_roleSeq;
    delete res;
    delete update;
    delete stmt;
}

// void updateOriginRole(const int& offset, const int& cnt) {
//     auto stmt = con->prepareStatement("select persistentIdentity from ComponentDefinition limit ?, ?");
//     stmt->setInt(1, offset);
//     stmt->setInt(2, cnt);
//     auto res = stmt->executeQuery();

//     auto _stmt = con->prepareStatement("select role from _ComponentDefinition where persistentIdentity = ?");
//     sql::Resultset* res = nullptr;

//     auto update = con->prepareStatement("update ComponentDefinition set ComRoleSeq = ?, ComRoleSeqRecursive = ? where persistentIdentity = ?");
//     auto get_roleSeq = con->prepareStatement("select RoleSeq from ComponentDefinition where persistentIdentity = ?");
//     sql::ResultSet* res_roleSeq = nullptr;

//     string pid, s, sr;
//     while (res->next()) {
//         pid = res->getString("persistentIdentity");

//         _stmt->setString(1, pid);
//         _stmt->executeQuery();
//         res
//     }

//     delete get_roleSeq;
//     delete res_roleSeq;
//     delete res;
//     delete update;
//     delete stmt;
// }

}  // namespace RoadmapSearch