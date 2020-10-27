#include "common.hpp"
#include "entity.hpp"
#include "search.hpp"

json convert(const Proposal &p) {
    json out;

    auto pros = vector<json>();
    for (int i = 0; i < num_pro; i++) {
        auto const &pro = p.pros[i];
        json comdef;
        comdef["displayId"] = pro.name;
        comdef["title"] = pro.name;
        comdef["role"] = "promoter";
        comdef["genenet_promoter_id"] = i;
        pros.push_back(comdef);
    }
    out["Promoters"] = pros;

    auto cdss = vector<json>();
    for (int i = 0; i < num_pro; i++) {
        for (int j = 0; j < num_pro; j++) {
            if (adj[i][j] == 0) continue;
            auto const &tf = p.solution[i][j];
            json comdef;
            comdef["displayId"] = tf.name;
            comdef["title"] = tf.name;
            comdef["role"] = "cds";
            comdef["genenet_cds_id"] = i * num_pro + j;
            cdss.push_back(comdef);
        }
    }
    out["CDSs"] = cdss;
    out["n"] = num_pro;

    return out;
}