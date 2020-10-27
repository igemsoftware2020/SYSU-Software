#include "common.hpp"

namespace RoadmapSearch {

using std::string;
using std::unordered_map;
using std::vector;
using json = nlohmann::json;
using std::unordered_map;

sql::Connection* con;

vector<string> roles = {
    "CDS",
    "Cell",
    "Chromosome",
    "Coding",
    "Composite",
    "Conjugation",
    "DNA",
    "Device",
    "Generator",
    "Intermediate",
    "Inverter",
    "Measurement",
    "Other",
    "Plasmid",
    "Plasmid_Backbone",
    "Primer",
    "Project",
    "Promoter",
    "Protein_Domain",
    "RBS",
    "RNA",
    "Regulatory",
    "Reporter",
    "Scar",
    "Signalling",
    "T7_RNA_Polymerase_Promoter",
    "T7_RNA_Polymerase_Promoter",
    "plasmid_vector",
    "Tag",
    "Temporary",
    "Terminator",
    "Translational_Unit",
    "engineered_region",
    "mature_transcript_region",
    "oriT",
    "plasmid_vector",
    "polypeptide_domain",
    "restriction_enzyme_assembly_scar",
    "ribosome_entry_site",
    "sequence_feature"};

vector<string> basic_roles = {"CDS", "RBS", "Promoter", "Terminator"};
unordered_map<string, char> roles_char;
unordered_map<char, string> char_roles;

void initRoleCharMap() {
    for (int i = 0; i < roles.size(); i++) {
        roles_char[roles[i]] = i + 'A';
        char_roles[i + 'A'] = roles[i];
    }
}

unordered_map<string, string> comdef_roleSeq;
unordered_map<string, string> comdef_comRoleSeq;
unordered_map<string, string> comdef_comRoleSeqRecursive;

string deleteTail(const string& s) {
    int len = s.size();
    if (s[len - 1] == '1' && s[len - 2] == '/') {
        return s.substr(0, len - 2);
    }
    return s;
}

void initSearch() {
    initRoleCharMap();

    auto stmt = con->prepareStatement("select persistentIdentity, RoleSeq, ComRoleSeq, ComRoleSeqRecursive from ComponentDefinition");
    auto res = stmt->executeQuery();

    comdef_roleSeq.clear();
    comdef_comRoleSeq.clear();
    comdef_comRoleSeqRecursive.clear();
    string pid, comRoleSeq, comRoleSeqRecursive;
    while (res->next()) {
        pid = res->getString("persistentIdentity");
        comdef_roleSeq[pid] = res->getString("RoleSeq");
        comRoleSeq = res->getString("ComRoleSeq");
        comRoleSeqRecursive = res->getString("ComRoleSeqRecursive");

        comdef_comRoleSeq[pid] = comRoleSeq;
        comdef_comRoleSeqRecursive[pid] = comRoleSeqRecursive;
    }
    delete res;
    delete stmt;
}

}  // namespace RoadmapSearch