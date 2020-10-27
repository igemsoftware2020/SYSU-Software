#pragma once

#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {
using json = nlohmann::json;
using std::vector;

void inputGraphInitial(DesignGraph desigh_graph);

void searchInStructure(DesignGraph design_graph, const int &limit, const bool &recursive_flag, const string &exec_dir, const string &output_dir);

void searchInElement(DesignGraph design_graph, const int &limit, const bool &recursive_flag, const string &exec_dir, const string &output_dir);
}  // namespace RoadmapSearch