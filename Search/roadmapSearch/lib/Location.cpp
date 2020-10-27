#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {

using std::cin;
using std::cout;
using std::endl;
using json = nlohmann::json;
using stringtream = std::stringstream;

Location::Location() {}

Location::Location(const json& j) {
    getValueFromJson<string>(j, "persistentIdentity", persistentIdentity);
    getValueFromJson<string>(j, "displayId", displayId);
    getValueFromJson<string>(j, "version", version);
    getValueFromJson<string>(j, "topLevel", topLevel);
    getValueFromJson<string>(j, "direction", direction);
    getValueFromJson<int>(j, "start", start);
    getValueFromJson<int>(j, "end", end);
    getValueFromJson<string>(j, "orientation", orientation);
    getValueFromJson<string>(j, "father_id", father_id);
}

}  // namespace RoadmapSearch