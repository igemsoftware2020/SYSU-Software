#include "search.hpp"

#include "common.hpp"
#include "entity.hpp"

using std::pair;
using std::sort;
using std::unordered_map;
using std::vector;

priority_queue<Proposal> proposals;
// vector<priority_queue<TP>> pros;
vector<vector<TP>> pros;
unordered_map<TP, bool> pros_used;
vector<TP> tfs;
unordered_map<TP, bool> tfs_used;
unordered_map<string, vector<vector<TP>>> pname_tfs;
unordered_map<pair<string, string>, string> pname_tfname_effect;

void initSearch() {
    pros.clear();
    pname_tfs.clear();
    for (int i = 0; i < num_pro; i++) {
        pros.push_back(vector<TP>());
        getPossiblePros(i);
        for (auto const &pro : pros[i]) {
            if (pname_tfs.find(pro.name) == pname_tfs.end()) {
                pname_tfs[pro.name].push_back(vector<TP>());
                pname_tfs[pro.name].push_back(vector<TP>());
                pname_tfs[pro.name][0] = getPossibleTFs(pro.name, "-");
                pname_tfs[pro.name][1] = getPossibleTFs(pro.name, "+");
            }
            if (pros_used.find(pro) == pros_used.end()) {
                pros_used[pro] = false;
            }
        }
    }
    // getAllTFs();
    getAllEffect();
}

void getAllEffect() {
    auto stmt = con->prepareStatement("select pro_name, TF_name, effect from genenet_BindingSite");
    auto res = stmt->executeQuery();

    string pro_name, TF_name, effect;
    while (res->next()) {
        pro_name = res->getString("pro_name");
        TF_name = res->getString("TF_name");
        effect = res->getString("effect");
        pname_tfname_effect[pair<string, string>(pro_name, TF_name)] = effect;
    }

    delete stmt;
    delete res;
}

void getPossiblePros(const int &id) {
    int num_pos_TFs = 0, num_neg_TFs = 0;
    for (int j = 0; j < num_pro; j++) {
        if (adj[id][j] == 1) num_pos_TFs++;
        if (adj[id][j] == -1) num_neg_TFs++;
    }
    string statement = "select distinct pro_name, cite, sequence_len from genenet_Promoter where num_pos_TFs = ? and num_neg_TFs = ?";
    auto stmt = con->prepareStatement(statement);
    stmt->setInt(1, num_pos_TFs);
    stmt->setInt(2, num_neg_TFs);

    auto res = stmt->executeQuery();
    string name;
    int cite, sequence_len;
    while (res->next()) {
        name = res->getString("pro_name");
        cite = res->getInt("cite");
        sequence_len = res->getInt("sequence_len");
        pros[id].push_back(TP(name, cite, sequence_len));
    }
    sort(pros[id].begin(), pros[id].end());

    delete stmt;
    delete res;
}

void getAllTFs() {
    string statement = "select distinct TF_name, cite, sequence_len from genenet_TF";
    auto stmt = con->prepareStatement(statement);

    auto res = stmt->executeQuery();

    string name;
    int cite, sequence_len;
    while (res->next()) {
        name = res->getString("TF_name");
        cite = res->getInt("cite");
        sequence_len = res->getInt("sequence_len");
        tfs.push_back(TP(name, cite, sequence_len));
    }
    for (auto const &tf : tfs) {
        if (tfs_used.find(tf) == tfs_used.end()) {
            tfs_used[tf] = false;
        }
    }

    delete stmt;
    delete res;
}

vector<TP> getPossibleTFs(const string &pro_name, const string &effect) {
    string statement = "select distinct TF_name, TF_cite, TF_sequence_len from genenet_BindingSite where pro_name = ? and effect = ?";
    auto stmt = con->prepareStatement(statement);
    stmt->setString(1, pro_name);
    stmt->setString(2, effect);

    auto res = stmt->executeQuery();
    auto tfs = vector<TP>();
    string name;
    int cite, sequence_len;
    while (res->next()) {
        name = res->getString("TF_name");
        cite = res->getInt("TF_cite");
        sequence_len = res->getInt("TF_sequence_len");
        tfs.push_back(TP(name, cite, sequence_len));
    }

    delete stmt;
    delete res;
    return tfs;
}

pair<int, int> nextXY(const int &x, const int &y) {
    if (y < num_pro - 1) {
        return pair<int, int>(x, y + 1);
    }
    return pair<int, int>(x + 1, 0);
}

void output(Proposal &p) {
    cout << "Proposal: " << endl;
    for (int i = 0; i < num_pro; i++) {
        cout << "Promoter " << i << " name = " << p.pros[i].name << " cite = " << p.pros[i].cite << " sequence_len = " << p.pros[i].sequence_len << endl;
    }

    for (int i = 0; i < num_pro; i++) {
        for (int j = 0; j < num_pro; j++) {
            auto const &tf = p.solution[i][j];
            if (adj[i][j] != 0) {
                cout << tf.name << " ";
            } else {
                cout << "0"
                     << " ";
            }
        }
        cout << endl;
    }
    cout << "\n"
         << endl;
}

void search(const int &pid, const int &x, const int &y, Proposal &cur) {
    if (proposals.size() >= limit) return;
    if (pid == num_pro && x == num_pro && y == 0) {
        proposals.push(cur);
        return;
    }
    if (pid < num_pro) {
        for (auto const &pro : pros[pid]) {
            if (pros_used[pro] == true) continue;
            pros_used[pro] = true;
            cur.addPro(pid, pro);
            search(pid + 1, x, y, cur);
            pros_used[pro] = false;
            cur.deletePro(pid);
        }
    } else {
        auto par = nextXY(x, y);
        if (cur.filled[x][y] == true || adj[x][y] == 0) {
            search(pid, par.first, par.second, cur);
            return;
        }
        auto const &pro = cur.pros[x];
        auto tfs = pname_tfs[pro.name][(adj[x][y] == -1) ? 0 : 1];
        for (auto const &tf : tfs) {
            if (tfs_used[tf] == true) continue;
            if (cur.addTF(x, y, tf) == true) {
                tfs_used[tf] = true;
                search(pid, par.first, par.second, cur);
                tfs_used[tf] = false;
                cur.deleteTF(x, y);
            }
        }
    }
}

void searchProposal() {
    auto cur = Proposal();
    search(0, 0, 0, cur);
}
