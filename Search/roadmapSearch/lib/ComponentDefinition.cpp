#include "DAO.hpp"
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

BaseComDef::BaseComDef() {}
BaseComDef::BaseComDef(const string& persistentIdentity, const string& displayId, const string& useRole, vector<string>& role) : persistentIdentity(persistentIdentity), displayId(displayId), useRole(useRole), role(role) {}

ostream& operator<<(ostream& out, const BaseComDef& b) {
    out << "persistentIdentity = " << b.persistentIdentity << endl;
    out << "displayId = " << b.displayId << endl;
    out << "useRole = " << b.useRole << endl;
    out << "\n"
        << endl;
    return out;
}

ComponentDefinition::ComponentDefinition() : BaseComDef() {}

ComponentDefinition::ComponentDefinition(const json& j) {
    getValueFromJson<string>(j, "persistentIdentity", persistentIdentity);
    getValueFromJson<string>(j, "displayId", displayId);
    getValueFromJson<string>(j, "version", version);
    getValueFromJson<string>(j, "wasDerivedFrom", wasDerivedFrom);
    getValueFromJson<string>(j, "wasGeneratedBy", wasGeneratedBy);
    getValueFromJson<string>(j, "title", title);
    getValueFromJson<string>(j, "description", description);
    getValueFromJson<string>(j, "created", created);
    getValueFromJson<string>(j, "modified", modified);
    getValueFromJson<string>(j, "mutableProvenance", mutableProvenance);
    getValueFromJson<string>(j, "topLevel", topLevel);
    getValueFromJson<string>(j, "mutableDescription", mutableDescription);
    getValueFromJson<string>(j, "mutableNotes", mutableNotes);
    getValueFromJson<string>(j, "creator", creator);
    getValueFromJson<string>(j, "type", type);
    getVectorFromJson<string>(j, "role", role);

    useRole = "";
    for (auto const& rname : role) {
        for (auto const& basic_role : basic_roles) {
            if (rname == basic_role) {
                useRole = basic_role;
                break;
            }
        }
    }
    if (useRole == "") useRole = "Composite";

    // fix gene name
    if (useRole == "CDS" && displayId.substr(0, 4) != "BBa_") {
        displayId = getCDSName(displayId, 1)[0];
    }

    components.clear();
    if (j.find("Component") != j.end() && j["Component"].is_null() == false) {
        for (auto const& node : j["Component"]) {
            components.push_back(make_shared<Component>(Component(node)));
        }
    }

    sequences.clear();
    if (j.find("Sequence") != j.end() && j["Sequence"].is_null() == false) {
        for (auto const& node : j["Sequence"]) {
            sequences.push_back(make_shared<Sequence>(Sequence(node)));
        }
    }

    sequenceAnnotations.clear();
    if (j.find("SequenceAnnotation") != j.end() && j["SequenceAnnotation"].is_null() == false) {
        for (auto const& node : j["SequenceAnnotation"]) {
            sequenceAnnotations.push_back(make_shared<SequenceAnnotation>(SequenceAnnotation(node)));
        }
    }
}

vector<string> ComponentDefinition::getComponentPids() {
    auto coms = vector<string>();
    for (auto const& p_com : components) {
        coms.push_back(p_com->definition);
    }
    return coms;
}

json ComponentDefinition::generateJson() {
    json j;
    j["persistentIdentity"] = persistentIdentity;
    j["displayId"] = displayId;
    j["role"] = useRole;
    j["component"] = vector<json>();
    for (auto const& p_com : components) {
        j["component"].push_back(p_com->generateJson());
    }
    return j;
}

}  // namespace RoadmapSearch