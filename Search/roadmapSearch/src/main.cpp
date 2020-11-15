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
#include <fstream>
#include <iostream>
#include <iterator>
#include <nlohmann/json.hpp>
#include <queue>
#include <set>
#include <sstream>
#include <stdexcept>
#include <typeinfo>
#include <unordered_map>
#include <vector>

#include "DAO.hpp"
#include "common.hpp"
#include "entity.hpp"
#include "mysqlException.hpp"
#include "search.hpp"

namespace RoadmapSearch {

using std::cin;
using std::cout;
using std::endl;
using std::exception;
using std::ifstream;
using std::string;
using std::stringstream;
using json = nlohmann::json;

void mainHandler(const string& host_name, const string& port_name, const string& user_name, const string& password, const string& database_name, const int& limit, const bool& structure_flag, const bool& element_flag, const bool& recursive_structure_flag, const bool& recursive_element_flag, const string& input_file_path, const string& exec_dir, const string& output_dir) throw() {
    try {
        // sql::Connection* con;
        sql::Statement* stmt;
        sql::ResultSet* res;
        sql::mysql::MySQL_Driver* driver;

        /* connect database*/
        driver = sql::mysql::get_mysql_driver_instance();
        con = driver->connect(host_name + ":" + port_name, user_name, password);
        con->setSchema(database_name);

        initSearch();

        // updatePaperComdefName();
        // updateRoleSeq(30000, 10000);
        // updateComRoleSeq(30000, 10000);

        ifstream fs(input_file_path);
        json j;
        fs >> j;

        DesignGraph design_graph = DesignGraph(j);

        if (element_flag || recursive_element_flag) {
            searchInElement(design_graph, limit, recursive_element_flag, exec_dir, output_dir);
        }
        if (structure_flag || recursive_structure_flag) {
            searchInStructure(design_graph, limit, recursive_structure_flag, exec_dir, output_dir);
        }

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

}  // namespace RoadmapSearch

using namespace std;
namespace po = boost::program_options;

int main(int argc, const char** argv) {
    try {
        string host_name, port_name, database_name, user_name, password, input_file_path;
        string exec_dir, output_dir;

        int limit;
        bool structure_flag = false, element_flag = false, recursive_structure_flag = false, recursive_element_flag = false;

        po::options_description desc("Allowed options");
        // clang-format off
        desc.add_options()
            ("help", "produce help message")
            ("host,h", po::value<string>(&host_name)->default_value("127.0.0.1"), "mysql database host name")
            ("port,P", po::value<string>(&port_name)->default_value("3306"), "mysql database port name")
            ("database,D", po::value<string>(&database_name)->default_value("roadmapDB"), "mysql database to use")
            ("user,u", po::value<string>(&user_name)->default_value("root"), "mysql database user name")
            ("password,p",po::value<string>(&password)->default_value(""), "mysql database password" )
            ("limit", po::value<int>(&limit)->default_value(20), "an integer <= 20, representing the maximum number of roadmap will be found (maybe less)")
            ("structure", po::bool_switch(&structure_flag)->default_value(false), "enable output of the structurally most similar roadmaps(not recursive)")
            ("element", po::bool_switch(&element_flag)->default_value(false), "enable output of the roadmaps with most similar elements(not recursive)")
            ("recursive-structure,rs", po::bool_switch(&recursive_structure_flag)->default_value(false), "enable searching the structurally most similar roadmaps(recursive searching constituent elements of a element, even when this element is not composite)")
            ("recursive-element,re", po::bool_switch(&recursive_element_flag)->default_value(false), "enable searching the roadmaps with most similar elements(recursive searching constituent elements of a element, even when this element is not composite)")
            ("input-file-path,i", po::value<string>(&input_file_path), "the path of input file")
            ("exec-dir",po::value<string>(&exec_dir), "the directory where the python json file generators are")
            ("output-dir", po::value<string>(&output_dir), "the directory where the output files are")
        ;
        // clang-format on
        po::positional_options_description p;
        p.add("input-file", 1);

        po::variables_map vm;
        po::store(po::command_line_parser(argc, argv).options(desc).positional(p).run(), vm);
        po::notify(vm);

        if (vm.count("help")) {
            cout << "Usage: options_description [options]\n";
            cout << desc;
            return 0;
        }

        if (vm.count("input-file-path") == 0) {
            cout << "Error: must include at least one input file\n\n";
            cout << "Usage: options_description [options]\n";
            cout << desc;
            return EXIT_SUCCESS;
        }

        RoadmapSearch::mainHandler(host_name, port_name, user_name, password, database_name, limit, structure_flag, element_flag, recursive_structure_flag, recursive_element_flag, input_file_path, exec_dir, output_dir);

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
