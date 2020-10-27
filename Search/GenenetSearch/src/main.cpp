#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/prepared_statement.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <json/json.h>
#include <mysql_connection.h>
#include <mysql_driver.h>

#include <algorithm>
#include <boost/program_options.hpp>
#include <cmath>
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <iterator>
#include <nlohmann/json.hpp>
#include <queue>
#include <stdexcept>
#include <unordered_map>
#include <vector>

#include "common.hpp"
#include "convert.hpp"
#include "entity.hpp"
#include "mysqlException.hpp"
#include "search.hpp"

namespace po = boost::program_options;
using std::cin;
using std::cout;
using std::endl;
using std::exception;
using std::ifstream;
using std::string;
using std::stringstream;
using std::to_string;
using json = nlohmann::json;

int num_pro;
vector<vector<int>> adj;
int max_accept_len;
int max_ideal_len;
int user_add_len;
int per_tf_len;
int limit;
double threshold;
sql::Connection* con;

int getSignal(double value, double threshold) {
    if (value > threshold) return 1;
    if (value < -threshold) return -1;
    return 0;
}

void output(const Proposal& p) {
    for (int i = 0; i < num_pro; i++) {
        cout << "Promoter " << i << " name = " << p.pros[i].name << " cite = " << p.pros[i].cite << " sequence_len = " << p.pros[i].sequence_len << endl;
    }
    for (int i = 0; i < num_pro; i++) {
        for (int j = 0; j < num_pro; j++) {
            auto const& tf = p.solution[i][j];
            if (adj[i][j] != 0) {
                cout << tf.name << " ";
            } else {
                cout << "0"
                     << " ";
            }
        }
        cout << endl;
    }
}

void mainHandler(const string& host_name, const string& port_name, const string& user_name, const string& password, const string& database_name) throw() {
    try {
        sql::Statement* stmt;
        sql::ResultSet* res;
        sql::mysql::MySQL_Driver* driver;

        /* connect database*/
        driver = sql::mysql::get_mysql_driver_instance();
        con = driver->connect(host_name + ":" + port_name, user_name, password);
        con->setSchema(database_name);

        initSearch();
        searchProposal();
        if (proposals.size() == 0) {
            cout << "{}" << endl;
        }

        auto const& p = proposals.top();
        // output(p);
        json j;
        auto proposal = convert(p);
        j["Proposals"] = proposal;
        cout << j << endl;

        con->commit();
        delete con;
    } catch (mysqlException& e) {
        throw e;
    } catch (sql::SQLException& e) {
        throw mysqlException(e, string(__FILE__), string(__FUNCTION__), std::to_string(__LINE__));
    } catch (exception& e) {
        throw e;
    }
}

int main(int argc, const char** argv) {
    try {
        string host_name, port_name, database_name, user_name, password;

        // int limit;

        po::options_description desc("Allowed options");
        // clang-format off
        desc.add_options()
            ("help", "produce help message")
            ("host,h", po::value<string>(&host_name)->default_value("127.0.0.1"), "mysql database host name")
            ("port,P", po::value<string>(&port_name)->default_value("3306"), "mysql database port name")
            ("database,D", po::value<string>(&database_name)->default_value("genenetDB"), "mysql database to use")
            ("user,u", po::value<string>(&user_name)->default_value("root"), "mysql database user name")
            ("password,p",po::value<string>(&password)->default_value(""), "mysql database password" )
            ("limit", po::value<int>(&limit)->default_value(1), "an integer <= 20, representing the maximum number of roadmap will be found (maybe less)")
            ("max-accept-len", po::value<int>(&max_accept_len)->default_value(20000), "max accept sequence len of a plasmid")
            ("max-ideal-len", po::value<int>(&max_ideal_len)->default_value(10000), "max ideal sequence len of a plasmid")
            ("threshold", po::value<double>(&threshold)->default_value(0.5), "threshold")
            ("per-tf-len", po::value<int>(&per_tf_len)->default_value(1000), "sequence len that will be add for each tf")
        ;
        // clang-format on
        po::positional_options_description p;

        po::variables_map vm;
        po::store(po::command_line_parser(argc, argv).options(desc).positional(p).run(), vm);
        po::notify(vm);

        if (vm.count("help")) {
            cout << "Usage: options_description [options]\n";
            cout << desc;
            return 0;
        }

        /******** input *******/
        // cout << "n = " << endl;
        cin >> num_pro;
        // cout << "user_add_len = " << endl;
        cin >> user_add_len;
        adj.clear();
        // cout << "matrix = " << endl;
        double value;
        for (int i = 0; i < num_pro; i++) {
            adj.push_back(vector<int>());
            for (int j = 0; j < num_pro; j++) {
                cin >> value;
                adj[i].push_back(getSignal(value, threshold));
            }
        }

        mainHandler(host_name, port_name, user_name, password, database_name);

    } catch (mysqlException& e) {
        cout << "# ERR: SQLException in " << e.file_name << "(" << e.function_name << ") on line " << e.line_name << endl;
        cout << "# ERR: " << e.what() << " (MySQL error code: " << e.getErrorCode() << ", SQLState: " << e.getSQLState() << " )" << endl;
        return EXIT_FAILURE;
    } catch (sql::SQLException& e) {
        cout << "# ERR: SQLException in " << __FILE__ << "(" << __FUNCTION__ << ") on line " << __LINE__ << endl;
        cout << "# ERR: " << e.what() << " (MySQL error code: " << e.getErrorCode() << ", SQLState: " << e.getSQLState() << " )" << endl;
        return EXIT_FAILURE;
    } catch (std::exception& e) {
        cout << e.what() << "\n";
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
