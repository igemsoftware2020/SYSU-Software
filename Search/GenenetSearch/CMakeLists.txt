project(GenenetSearch)
cmake_minimum_required(VERSION 3.6)

set(SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src")
set(JSON_BuildTests OFF CACHE INTERNAL "")

find_package( Boost 1.65 COMPONENTS program_options filesystem REQUIRED )

include_directories("${Boost_INCLUDE_DIR}")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include/mysql")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/ext/nlohmann_json/include")

add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/lib")
add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/ext/nlohmann_json")

set(SOURCE_FILES "${SRC_DIR}/main.cpp")

add_executable(genenet_search ${SOURCE_FILES})

target_link_libraries(
    genenet_search 
    PRIVATE 
    # roadmapSearchLib 
    genenet_search_lib
    nlohmann_json::nlohmann_json 
    # ${CMAKE_CURRENT_SOURCE_DIR}/lib/libjsoncpp.a 
    mysqlcppconn 
    ${Boost_LIBRARIES} 
)

