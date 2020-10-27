#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {

using std::cin;
using std::cout;
using std::endl;
using json = nlohmann::json;
using stringtream = std::stringstream;

Sequence::Sequence() {}

Sequence::Sequence(const json &j) {
    getValueFromJson<string>(j, "persistentIdentity", persistentIdentity);
    getValueFromJson<string>(j, "displayId", displayId);
    getValueFromJson<string>(j, "version", version);
    getValueFromJson<string>(j, "wasDerivedFrom", wasDerivedFrom);
    getValueFromJson<string>(j, "wasGeneratedBy", wasGeneratedBy);
    getValueFromJson<string>(j, "topLevel", topLevel);
    getVectorFromJson<string>(j, "ownedBy", ownedBy);
    getValueFromJson<string>(j, "elements", elements);
    getValueFromJson<string>(j, "encoding", encoding);
    getValueFromJson<string>(j, "father_id", father_id);
}

}  // namespace RoadmapSearch