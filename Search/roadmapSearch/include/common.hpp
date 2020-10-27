#pragma once

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/prepared_statement.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <json/json.h>
#include <mysql_connection.h>
#include <mysql_driver.h>

#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <nlohmann/json.hpp>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <typeinfo>
#include <unordered_map>
#include <utility>
#include <vector>

namespace RoadmapSearch {

using std::cout;
using std::endl;
using std::range_error;
using std::shared_ptr;
using std::string;
using std::vector;
using json = nlohmann::json;
using std::unordered_map;

extern sql::Connection* con;
extern vector<string> basic_roles;
extern unordered_map<string, char> roles_char;
extern unordered_map<char, string> char_roles;
extern unordered_map<string, string> comdef_roleSeq;
extern unordered_map<string, string> comdef_comRoleSeq;
extern unordered_map<string, string> comdef_comRoleSeqRecursive;

template <typename T>
void getValueFromJson(const json& j, const string& name, T& value) throw() {
    if (j.find(name) != j.end() && j[name].is_null() == false) {
        j[name].get_to(value);
        return;
    }
    if (typeid(value) == typeid(string) || typeid(value) == typeid(int)) {
        value = T();  // "" or 0
    } else {
        throw range_error("No " + name + " in current json object");
    }
}

template <typename T>
void getVectorFromJson(const json& j, const string& name, vector<T>& vec) throw() {
    vec.clear();
    T value;
    if (j.find(name) != j.end()) {
        for (auto const& node : j[name]) {
            node.get_to(value);
            vec.push_back(value);
        }
    }
}

string deleteTail(const string& s);

void initSearch();

}  // namespace RoadmapSearch
