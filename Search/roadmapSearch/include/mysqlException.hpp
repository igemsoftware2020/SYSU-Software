#pragma once

#include <cppconn/exception.h>

#include <exception>
#include <string>

using std::string;

struct mysqlException : public sql::SQLException {
    string file_name, function_name, line_name;
    mysqlException(const sql::SQLException& e, string file_name, string function_name, string line_name);
};