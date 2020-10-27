#pragma once

#include "common.hpp"

using std::pair;
using std::shared_ptr;
using std::string;
using std::unordered_map;
using std::vector;

struct TP {  // TF or Promoter
    string name;
    int cite, sequence_len;

    TP();
    TP(const string &name, const int &cite, const int &sequence_len);
    TP(const TP &tp);

    bool operator<(const TP &tp) const;
    bool operator==(const TP &tp) const;
};

namespace std {
template <>
class hash<TP> {
public:
    size_t operator()(const TP &tp) const {
        return hash<string>()(tp.name) ^ hash<int>()(tp.cite) ^ hash<int>()(tp.sequence_len);
    }
};
};  // namespace std

struct Proposal {
    int cite, sequence_len, num_TFs;
    // unordered_map<TP, int> TFs;
    vector<bool> pfilled;
    vector<TP> pros;
    vector<vector<bool>> filled;
    vector<vector<TP>> solution;

    Proposal();
    Proposal(const Proposal &p);
    int getEffect(const int &x, const int &y, const TP &tf);
    bool checkTF(const int &x, const int &y, const TP &tf);
    bool addTF(const int &x, const int &y, const TP &tf);
    void deleteTF(const int &x, const int &y);
    void addPro(const int &pid, const TP &pro);
    void deletePro(const int &pid);

    bool operator<(const Proposal &p) const;  //the less, the better
};

int calSequenceClass(int sequence_len);

// pair<bool, Proposal> tryAddTF(const Proposal &p, const TP &tf);
