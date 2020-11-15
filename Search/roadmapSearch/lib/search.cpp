#include "search.hpp"

#include <boost/filesystem.hpp>

#include "DAO.hpp"
#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {
using json = nlohmann::json;
using std::string;
using std::to_string;
using std::vector;

auto const ps = boost::filesystem::path::preferred_separator;

vector<string> split(const string &str, const string &delim) {
    vector<string> tokens;
    size_t prev = 0, pos = 0;
    do {
        pos = str.find(delim, prev);
        if (pos == string::npos) pos = str.length();
        string token = str.substr(prev, pos - prev);
        if (!token.empty()) tokens.push_back(token);
        prev = pos + delim.length();
    } while (pos < str.length() && prev < str.length());
    return tokens;
}

string formatPid(const string &pid) {
    auto tokens = split(pid, "/");
    string s = "";
    for (auto const &token : tokens) {
        if (s != "") s += "-";
        s += token;
    }
    return s;
}

void searchInStructure(DesignGraph design_graph, const int &limit, const bool &recursive_flag, const string &exec_dir, const string &output_dir) {
    auto linkedlists = design_graph.getStructure(recursive_flag);
    auto graphs_iGEM = getGraphWithStructures(true, linkedlists, recursive_flag, limit);
    auto graphs_paper = getGraphWithStructures(false, linkedlists, recursive_flag, limit);

    string command = "";
    string type = "structure";
    if (recursive_flag) type = "recursive-structure";

    int cnt = 0;
    for (auto const &pid : graphs_iGEM) {
        cout << "structure: iGEM pid = " << pid << endl;
        command = "python " + exec_dir + ps + "generateJson_iGEM.py -i " + pid + " > " + output_dir + ps + type + "-iGEM-" + to_string(++cnt) + "-" + formatPid(pid) + ".json";
        system(command.c_str());
    }
    cnt = 0;
    for (auto const &pid : graphs_paper) {
        cout << "structure: paper pid = " << pid << endl;
        command = "python " + exec_dir + ps + "generateJson_paper.py -i " + pid + " > " + output_dir + ps + type + "-paper-" + to_string(++cnt) + "-" + pid + ".json";
        system(command.c_str());
    }
}

void searchInElement(DesignGraph design_graph, const int &limit, const bool &recursive_flag, const string &exec_dir, const string &output_dir) {
    auto baseComDefs = design_graph.getBaseComDef(recursive_flag);

    string command = "";
    string type = "element";
    if (recursive_flag) type = "recursive-element";
    auto graphs = getGraphWithElements(design_graph.is_iGEM, baseComDefs, limit);

    int cnt = 0;
    for (auto const &pid : graphs) {
        cout << "element: pid = " << pid << endl;
        if (design_graph.is_iGEM) {
            command = "python " + exec_dir + ps + "generateJson_iGEM.py -i " + pid + " > " + output_dir + ps + type + "-iGEM-" + to_string(++cnt) + "-" + pid + ".json";
            system(command.c_str());
        } else {
            cout << "element: paper pid = " << pid << endl;
            command = "python " + exec_dir + ps + "generateJson_paper.py -i " + pid + " > " + output_dir + ps + type + "-paper-" + to_string(++cnt) + "-" + pid + ".json";
            system(command.c_str());
        }
    }
}

}  // namespace RoadmapSearch