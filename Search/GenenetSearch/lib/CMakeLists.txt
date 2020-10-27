include_directories("${Boost_INCLUDE_DIR}")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include/mysql")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/ext/nlohmann_json/include")

add_library(
    genenet_search_lib
    common.cpp
    entity.cpp
    mysqlException.cpp
    search.cpp
    convert.cpp
)