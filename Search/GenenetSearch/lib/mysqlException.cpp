
#include "mysqlException.hpp"

#include <cppconn/exception.h>

#include <exception>
#include <string>

using std::string;

mysqlException::mysqlException(const sql::SQLException& e, string file_name, string function_name, string line_name) : sql::SQLException(e), file_name(file_name), function_name(function_name), line_name(line_name) {}
