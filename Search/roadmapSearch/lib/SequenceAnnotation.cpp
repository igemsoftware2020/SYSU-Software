#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {

using std::cin;
using std::cout;
using std::endl;
using std::make_shared;
using std::shared_ptr;
using json = nlohmann::json;
using stringtream = std::stringstream;

SequenceAnnotation::SequenceAnnotation() {}

SequenceAnnotation::SequenceAnnotation(const json& j) {
    getValueFromJson<string>(j, "persistentIdentity", persistentIdentity);
    getValueFromJson<string>(j, "displayId", displayId);
    getValueFromJson<string>(j, "version", version);
    getValueFromJson<string>(j, "title", title);
    getValueFromJson<string>(j, "topLevel", topLevel);
    getValueFromJson<string>(j, "father_id", father_id);

    locations.clear();
    if (j.find("Location") != j.end() && j["Location"].is_null() == false) {
        for (auto const& node : j["Location"]) {
            locations.push_back(make_shared<Location>(Location(node)));
        }
    }
}

}  // namespace RoadmapSearch