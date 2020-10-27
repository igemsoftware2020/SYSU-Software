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
#include <cmath>
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

#define PI 3.14159265358979323846

using std::cout;
using std::endl;
using std::range_error;
using std::shared_ptr;
using std::string;
using std::vector;
using json = nlohmann::json;
using std::pair;
using std::priority_queue;
using std::unordered_map;

extern int num_pro;
extern vector<vector<int>> adj;
extern int max_accept_len;
extern int max_ideal_len;
extern int user_add_len;
extern int per_tf_len;
extern int limit;
extern double threshold;
extern sql::Connection* con;