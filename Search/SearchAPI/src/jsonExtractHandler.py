from typing import Tuple, Dict, List
import json
from common import *
import mysql.connector
from mysql.connector import errorcode
import datetime
import random

is_add_element: bool = True


def getValue(data, name: str, due_table: str, search_table: str, must: bool, unique: bool, in_database: bool, cursor) -> (bool, str):
    if name not in data:
        if must == True:
            return False, name + " of " + due_table + " should be provided"
        else:
            return True, None

    value = data[name]

    global is_add_element
    if is_add_element == True and due_table == "Component" and unique == True:
        in_database = True

    if unique == True:
        statement = "select count(*) from " + search_table + \
            " where " + name + " = %s"
        cursor.execute(statement, (value,))
        res = cursor.fetchall()

        if (in_database == True and res[0][0] != 1) or (in_database == False and res[0][0] != 0):
            return False, name + " of " + due_table + " should be unique"

    return True, value


def putValueIntoDict(cursor, data, handler_attr, value_dict, due_table, search_table):
    for i in range(len(handler_attr)):
        name = handler_attr[i]["name"]
        must = handler_attr[i]["must"]
        unique = handler_attr[i]["unique"]
        in_database = handler_attr[i]["in_database"]

        flag, value = getValue(data=data, name=name, due_table=due_table, search_table=search_table,
                               must=must, unique=unique, in_database=in_database, cursor=cursor)
        value_dict[name] = value
        if flag == False:
            return False, value
    return True, None


def updateValue(value_dict, name, value):
    if value_dict[name] is None:
        value_dict[name] = value


def graphHandler(cursor, data) -> (bool, str, Dict[str, str]):
    value_dict = {}
    flag, value = putValueIntoDict(cursor, data, graph_handler_attr,
                                   value_dict, "DesignGraph", "DesignGraph")
    if flag == False:
        return False, value, None

    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/DesignGraph/" + \
        str(random.randint(0, 100000000))

    return True, None, value_dict


def actHandler(cursor, data) -> (bool, str, Dict[str, str]):
    value_dict = {}
    flag, value = putValueIntoDict(cursor, data, act_handler_attr,
                                   value_dict, "Activity", "Activity")
    if flag == False:
        return False, value, None

    updateValue(value_dict, "displayId", value_dict["title"])

    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/Activity/" + \
        value_dict["displayId"]

    return True, None, value_dict


def comdefHandler(cursor, data) -> (bool, str, Dict[str, str]):
    value_dict = {}
    flag, value = putValueIntoDict(cursor, data, comdef_handler_attr,
                                   value_dict, "ComponentDefinition", "ComponentDefinition")
    if flag == False:
        return False, value, None

    now = datetime.datetime.now()
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/ComponentDefinition/" + \
        value_dict["displayId"]
    updateValue(value_dict, "version", 1)
    updateValue(value_dict, "created", now.strftime("%Y-%m-%dT%H:%M:%SZ"))
    updateValue(value_dict, "modified", value_dict["created"])
    updateValue(value_dict, "type",
                "http://www.biopax.org/release/biopax-level3.owl#DnaRegion")

    value_dict["comRoleSeq"] = ""
    value_dict["comRoleSeqRecursive"] = ""
    if "Component" in data.keys():
        for child in data["Component"]:
            cursor.execute(
                "select roleSeq, comRoleSeqRecursive from ComponentDefinition where title = '" + child["title"] + "'")
            res = cursor.fetchall()
            if res is None or res == [] or res[0] is None or res[0] == []:
                continue
            value_dict["comRoleSeq"] += res[0][0]
            value_dict["comRoleSeqRecursive"] += res[0][1]

    value_dict["originRole"] = value_dict["role"]

    basic_roles = ["Promoter", "CDS", "RBS", "Terminator"]
    value_dict["useRole"] = "Composite"
    for rname in value_dict["role"]:
        for basic_role in basic_roles:
            if rname == basic_role:
                value_dict["useRole"] = basic_role

    value_dict["roleSeq"] = role_char[value_dict["useRole"]]
    value_dict["outputRole"] = value_dict["role"]

    return True, None, value_dict


def seqHandler(cursor, data, comdef_values) -> (bool, str, Dict[str, str]):
    value_dict = {}
    flag, value = putValueIntoDict(cursor, data, seq_handler_attr,
                                   value_dict, "Sequence", "Sequence")
    if flag == False:
        return False, value, None

    updateValue(value_dict, "displayId", "sequence_" +
                str(random.randint(0, 100000000)))
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/Sequence/" + \
        comdef_values["displayId"] + "/" + value_dict["displayId"]
    updateValue(value_dict, "version", 1)
    value_dict["father_id"] = comdef_values["persistentIdentity"]

    return True, None, value_dict


def comHandler(cursor, data, comdef_values) -> (bool, str, Dict[str, str]):
    value_dict = {}
    flag, value = putValueIntoDict(cursor, data, com_handler_attr,
                                   value_dict, "Component", "ComponentDefinition")
    if flag == False:
        return False, value, None

    updateValue(value_dict, "displayId", "component" +
                str(random.randint(0, 100000000)))
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/Component/" + \
        comdef_values["displayId"] + "/" + value_dict["displayId"]

    updateValue(value_dict, "version", 1)

    statement = "select persistentIdentity from ComponentDefinition where displayId = %s"
    cursor.execute(statement, (value_dict["title"],))
    res = cursor.fetchall()
    definition = res[0][0]
    if definition == "https://synbiohub.org/public/igem/" + value_dict["title"]:
        definition += "/1"
    value_dict["definition"] = definition

    value_dict["access"] = "http://sbols.org/v2#public"
    value_dict["father_id"] = comdef_values["persistentIdentity"]

    return True, None, value_dict


def locationHandler(cursor, data, seqant_values, comdef_values) -> (bool, str, Dict[str, str]):

    value_dict = {}
    flag, value = putValueIntoDict(cursor, data, location_handler_attr,
                                   value_dict, "Location", "Location")
    if flag == False:
        return False, value, None

    updateValue(value_dict, "displayId", "range" +
                str(random.randint(0, 100000000)))
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/Location/" + \
        comdef_values["displayId"] + "/" + value_dict["displayId"]
    updateValue(value_dict, "version", 1)
    value_dict["father_id"] = seqant_values["persistentIdentity"]

    return True, None, value_dict


def seqantHandler(cursor, data, comdef_values) -> (bool, str, Dict[str, str]):
    value_dict = {}
    flag, value = putValueIntoDict(cursor, data, seqant_handler_attr,
                                   value_dict, "SequenceAnnotation", "SequenceAnnotation")
    if flag == False:
        return False, value, None

    updateValue(value_dict, "displayId", "annotation" +
                str(random.randint(0, 100000000)))
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/SequenceAnnotation/" + \
        comdef_values["displayId"] + "/" + value_dict["displayId"]

    updateValue(value_dict, "version", 1)

    statement = "select persistentIdentity from ComponentDefinition where displayId = %s"
    cursor.execute(statement, (value_dict["title"],))
    res = cursor.fetchall()
    definition: str = None
    if res is not None:
        definition = res[0][0]
    if definition == "https://synbiohub.org/public/igem/" + value_dict["title"]:
        definition += "/1"
    value_dict["component"] = definition

    value_dict["father_id"] = comdef_values["persistentIdentity"]

    return True, None, value_dict
