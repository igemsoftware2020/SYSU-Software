#include "common.hpp"
#include "entity.hpp"

namespace RoadmapSearch {

using std::cout;
using std::endl;
using std::ostream;
using json = nlohmann::json;

Activity::Activity() {}

Activity::Activity(const json &j) {
    getValueFromJson(j, "persistentIdentity", persistentIdentity);
    getValueFromJson(j, "displayId", displayId);
    getValueFromJson(j, "version", version);
    getValueFromJson(j, "title", title);

    getVectorFromJson(j, "ownedBy", ownedBy);
    getVectorFromJson(j, "creator", creator);

    getValueFromJson(j, "endedAtTime", endedAtTime);
}

}  // namespace RoadmapSearch