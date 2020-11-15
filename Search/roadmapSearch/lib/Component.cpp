#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {

using std::cin;
using std::cout;
using std::endl;
using json = nlohmann::json;
using stringtream = std::stringstream;

Component::Component() {}

Component::Component(const json &j) {
    getValueFromJson<string>(j, "persistentIdentity", persistentIdentity);
    getValueFromJson<string>(j, "displayId", displayId);
    getValueFromJson<string>(j, "version", version);
    getValueFromJson<string>(j, "title", title);
    getValueFromJson<string>(j, "topLevel", topLevel);
    getValueFromJson<string>(j, "definition", definition);
    getValueFromJson<string>(j, "access", access);
    getValueFromJson<string>(j, "father_id", father_id);
}

json Component::generateJson() {
    json j;
    j["persistentIdentity"] = persistentIdentity;
    j["displayId"] = displayId;
    j["title"] = title;
    j["definition"] = definition;
    j["father_id"] = father_id;
    return j;
}

}  // namespace RoadmapSearch