#include "entity.hpp"

#include "common.hpp"
#include "search.hpp"

using std::atan;
using std::exp;
using std::pow;

TP::TP() {}

TP::TP(const string& name, const int& cite, const int& sequence_len) : name(name), cite(cite), sequence_len(sequence_len) {
}

TP::TP(const TP& tp) : name(tp.name), cite(tp.cite), sequence_len(tp.sequence_len) {}

bool TP::operator<(const TP& tp) const {
    if (sequence_len == tp.sequence_len)
        return cite > tp.cite;
    return sequence_len < tp.sequence_len;
}

bool TP::operator==(const TP& tp) const {
    return name == tp.name && cite == tp.cite && sequence_len == tp.sequence_len;
}

Proposal::Proposal() : cite(0), sequence_len(user_add_len), num_TFs(0) {
    // TFs.clear();
    pfilled.clear();
    pros.clear();
    for (int i = 0; i < num_pro; i++) {
        pfilled.push_back(false);
        pros.push_back(TP());
    }
    filled.clear();
    solution.clear();
    for (int i = 0; i < num_pro; i++) {
        filled.push_back(vector<bool>());
        solution.push_back(vector<TP>());
        for (int j = 0; j < num_pro; j++) {
            filled[i].push_back(false);
            solution[i].push_back(TP());
        }
    }
}

Proposal::Proposal(const Proposal& p) : cite(p.cite), sequence_len(p.sequence_len), num_TFs(p.num_TFs) {
    pfilled.clear();
    pros.clear();
    for (int i = 0; i < num_pro; i++) {
        pfilled.push_back(p.pfilled[i]);
        pros.push_back(p.pros[i]);
    }
    filled.clear();
    solution.clear();
    for (int i = 0; i < num_pro; i++) {
        filled.push_back(vector<bool>());
        solution.push_back(vector<TP>());
        for (int j = 0; j < num_pro; j++) {
            filled[i].push_back(p.filled[i][j]);
            solution[i].push_back(p.solution[i][j]);
        }
    }
}

int calSequenceClass(int sequence_len) {
    if (sequence_len <= max_ideal_len) return 0;
    if (sequence_len <= max_accept_len) return 1;
    return 2;
}

bool sameEffect(string effect, const int adj_effect) {
    if (effect == "-" and adj_effect == -1) return true;
    if (effect == "+" and adj_effect == 1) return true;
    return false;
}

bool Proposal::checkTF(const int& x, const int& y, const TP& tf) {
    auto const& pro = pros[x];
    auto const& par = pair<string, string>(pro.name, tf.name);
    if (pname_tfname_effect.find(par) == pname_tfname_effect.end()) {
        return true;
    }
    auto const& effect = pname_tfname_effect[par];
    return sameEffect(effect, adj[x][y]);
}

int Proposal::getEffect(const int& x, const int& y, const TP& tf) {
    auto const& pro = pros[x];
    auto const& par = pair<string, string>(pro.name, tf.name);
    if (pname_tfname_effect.find(par) == pname_tfname_effect.end()) {
        return 0;
    }
    auto const& effect = pname_tfname_effect[par];
    if (effect == "+") return 1;
    if (effect == "-") return -1;
    return 0;
}

bool Proposal::addTF(const int& x, const int& y, const TP& tf) {
    // cout << "x = " << x << " y = " << y << " tf.name = " << tf.name << endl;
    /*********** version 1 ***********/
    // auto newp = *this;
    // auto int_eff = getEffect(x, y, tf);
    // if (int_eff != adj[x][y]) return false;
    // newp.cite += tf.cite;
    // newp.sequence_len += tf.sequence_len + per_tf_len;
    // newp.num_TFs += 1;
    // *this = newp;
    // return true;

    /*********** version 2 ***********/
    // auto newp = *this;
    // for (int i = x; i < num_pro; i++) {
    //     for (int j = (i > x) ? 0 : y; j < num_pro; j++) {
    //         auto int_eff = getEffect(i, j, tf);
    //         if (i == x && j == y && int_eff != adj[i][j]) return false;
    //         if (int_eff != 0 && int_eff != adj[i][j]) return false;
    //         if (newp.filled[i][j] == false && adj[i][j] != 0) {
    //             newp.filled[i][j] = true;
    //             newp.solution[i][j] = tf;
    //         }
    //     }
    // }

    // newp.cite += tf.cite;
    // newp.sequence_len += tf.sequence_len + per_tf_len;
    // newp.num_TFs += 1;
    // *this = newp;
    // return true;

    solution[x][y] = tf;
    cite += tf.cite;
    sequence_len += tf.sequence_len + per_tf_len;
    num_TFs += 1;

    return true;
}

void Proposal::deleteTF(const int& x, const int& y) {
    const TP& tf = solution[x][y];
    for (int i = x; i < num_pro; i++) {
        for (int j = (i > x) ? 0 : y; j < num_pro; j++) {
            if (filled[i][j] == true && solution[i][j] == tf) {
                filled[i][j] = false;
            }
        }
    }
    cite -= tf.cite;
    sequence_len -= tf.sequence_len + per_tf_len;
    num_TFs -= 1;
}

void Proposal::addPro(const int& pid, const TP& pro) {
    pfilled[pid] = true;
    pros[pid] = pro;
    cite += pro.cite;
    sequence_len += pro.sequence_len;
}

void Proposal::deletePro(const int& pid) {
    pfilled[pid] = false;
    auto const& pro = pros[pid];
    cite -= pro.cite;
    sequence_len -= pro.sequence_len;
}

double calSequenceLenGrade(const int& sequence_len) {
    double range = max_accept_len - max_ideal_len;
    double x = (sequence_len - max_ideal_len) / range;
    return 1 - pow(x, 3);
}

double calCiteGrade(const int& cite) {
    return atan(cite) * 2 / PI;
}

double calGrade(const int& sequence_len, const int& cite) {
    return calSequenceLenGrade(sequence_len) + calCiteGrade(cite);
}

bool Proposal::operator<(const Proposal& p) const {  // if this < p ?
    int sequence_class = calSequenceClass(sequence_len);
    int p_sequence_class = calSequenceClass(p.sequence_len);
    // 最高优先级: 是否超过max_accept_len
    if (sequence_class == 2 && p_sequence_class < 2) {
        return false;
    }
    if (sequence_class < 2 && p_sequence_class == 2) {
        return true;
    }
    // 次高优先级：使用的TF数量
    if (num_TFs != p.num_TFs) {
        return num_TFs < p.num_TFs;
    }
    // 低优先级：sequence_len都小于max_ideal_len，比较cite
    if (sequence_class == 0 && p_sequence_class == 0) {
        return cite > p.cite;
    }
    if (sequence_class == 2 && p_sequence_class == 2) {
        return sequence_len < p.sequence_len;
    }
    // 最后： 比较grade
    return calGrade(sequence_len, cite) > calGrade(p.sequence_len, p.cite);
}