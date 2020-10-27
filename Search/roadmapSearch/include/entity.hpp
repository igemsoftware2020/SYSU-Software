#pragma once

#include "common.hpp"

namespace RoadmapSearch {

using std::ostream;
using std::shared_ptr;
using std::string;
using std::vector;
using json = nlohmann::json;

struct BaseComDef;
struct DesignGraph;
struct Activity;
struct ComponentDefinition;
struct Sequence;
struct Component;
struct SequenceAnnotation;
struct Location;

struct DesignGraph {
    string persistentIdentity;
    string article;
    string description;
    vector<shared_ptr<Activity>> activities;
    vector<shared_ptr<ComponentDefinition>> componentDefinitions;

    bool is_iGEM;

    DesignGraph();
    DesignGraph(const json &);
    vector<shared_ptr<BaseComDef>> getBaseComDef(const bool &recursive_flag);
    vector<string> getComDefRoots();
    vector<vector<shared_ptr<BaseComDef>>> getStructure(const bool &recursive_flag);
    friend ostream &operator<<(ostream &, const DesignGraph &);
};

struct Activity {
    string persistentIdentity;
    string displayId;
    string version;
    string title;
    string description;
    vector<string> ownedBy;
    vector<string> creator;
    string endedAtTime;

    Activity();
    Activity(const json &);
    friend ostream &operator<<(ostream &, const Activity &);
};

struct BaseComDef {
    string persistentIdentity;
    string displayId;
    string useRole;
    vector<string> role;

    BaseComDef();
    BaseComDef(const string &, const string &, const string &, vector<string> &);
    friend ostream &operator<<(ostream &, const BaseComDef &);
};

struct ComponentDefinition : public BaseComDef {
    // string persistentIdentity;
    // string displayId;
    string version;
    string wasDerivedFrom;
    string wasGeneratedBy;
    string title;
    string description;
    string created;
    string modified;
    string mutableProvenance;
    string topLevel;
    string mutableDescription;
    string mutableNotes;
    string creator;
    string type;
    // vector<string> role;
    vector<shared_ptr<Component>> components;
    vector<shared_ptr<ComponentDefinition>> children;
    vector<shared_ptr<Sequence>> sequences;
    vector<shared_ptr<SequenceAnnotation>> sequenceAnnotations;

    ComponentDefinition();
    ComponentDefinition(const json &);
    vector<string> getComponentPids();
    friend ostream &operator<<(ostream &, const ComponentDefinition &);
};

struct Sequence {
    string persistentIdentity;
    string displayId;
    string version;
    string wasDerivedFrom;
    string wasGeneratedBy;
    string topLevel;
    vector<string> ownedBy;
    string elements;
    string encoding;
    string father_id;

    Sequence();
    Sequence(const json &);
    friend ostream &operator<<(ostream &, const Sequence &);
};

struct Component {
    string persistentIdentity;
    string displayId;
    string version;
    string title;
    string topLevel;
    string definition;
    string access;
    string father_id;

    Component();
    Component(const json &);
    friend ostream &operator<<(ostream &, const Component &);
};

struct SequenceAnnotation {
    string persistentIdentity;
    string displayId;
    string version;
    string title;
    string topLevel;
    string component;
    string father_id;
    vector<shared_ptr<Location>> locations;

    SequenceAnnotation();
    SequenceAnnotation(const json &);
    friend ostream &operator<<(ostream &, const SequenceAnnotation &);
};

struct Location {
    string persistentIdentity;
    string displayId;
    string version;
    string topLevel;
    string direction;
    int start, end;
    string orientation;
    string father_id;

    Location();
    Location(const json &);
    friend ostream &operator<<(ostream &, const Location &);
};

}  // namespace RoadmapSearch