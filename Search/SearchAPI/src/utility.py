from typing import Tuple, Dict, List
import json
from common import database_config
import mysql.connector
from mysql.connector import errorcode
import datetime
import random

role_char = {
    "CDS": "A",
    "RBS": "T",
    "Promoter": "R",
    "Terminator": "_",
    "Composite": "E"
}


def getValue(data, name: str, table: str, must: bool, unique: bool, in_database: bool, cursor) -> (bool, str):
    if name not in data:
        if must == True:
            return False, name + " of " + table + " should be provided"
        else:
            return True, None

    value = data[name]

    if unique == True:
        statement = "select count(*) from " + table + \
            " where " + name + " = %s"
        cursor.execute(statement, (value,))
        res = cursor.fetchall()
        if (in_database == True and res[0][0] != 1) or (in_database == False and res[0][0] != 0):
            return False, name + " of " + table + " should be unique"
    return True, value


def comdefHandler(cursor, data) -> (bool, str, Dict[str, str]):
    names = [
        "displayId",
        "wasGeneratedBy",
        "title",
        "description",
        "mutableProvenance",
        "mutableDescription",
        "mutableNotes",
        "creator",
        "ownedBy",
        "role",
        "useRole"
    ]

    musts = [
        True,   # "displayId",
        False,  # "wasGeneratedBy",
        True,   # "title",
        False,  # "description",
        False,  # "mutableProvenance",
        False,  # "mutableDescription",
        False,  # "mutableNotes",
        True,   # "creator",
        True,   # "ownedBy",
        True,   # "role",
        False   # "useRole"
    ]

    uniques = [
        True,   # "displayId",
        False,  # "wasGeneratedBy",
        False,  # "title",
        False,  # "description",
        False,  # "mutableProvenance",
        False,  # "mutableDescription",
        False,  # "mutableNotes",
        False,  # "creator",
        False,  # "ownedBy",
        False,  # "role",
        False   # "useRole"
    ]

    in_databases = [False] * len(names)

    now = datetime.datetime.now()

    value_dict = {}
    table = "ComponentDefinition"
    for i, name in enumerate(names):
        flag, value = getValue(data=data, name=name, table=table,
                               must=musts[i], unique=uniques[i], in_database=in_databases[i], cursor=cursor)
        value_dict[name] = value
        if flag == False:
            return False, value, None
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/ComponentDefinition/" + \
        value_dict["displayId"]
    value_dict["version"] = "1"
    value_dict["wasDerivedFrom"] = None
    value_dict["created"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    value_dict["modified"] = value_dict["created"]
    value_dict["topLevel"] = None
    value_dict["type"] = "http://www.biopax.org/release/biopax-level3.owl#DnaRegion"

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
    names = ["elements", "encoding"]
    musts = [True, False]
    uniques = [False, False]
    in_databases = [False, False]

    value_dict = {}
    for i, name in enumerate(names):
        flag, value = getValue(data=data, name=name, table="",
                               must=musts[i], unique=uniques[i], in_database=in_databases[i], cursor=cursor)
        value_dict[name] = value
        if flag == False:
            return False, value, None
    value_dict["displayId"] = "sequence_" + str(random.randint(0, 100000000))
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/Sequence/" + \
        comdef_values["displayId"] + "/" + value_dict["displayId"]
    value_dict["version"] = "1"
    value_dict["wasDerivedFrom"] = None
    value_dict["wasGeneratedBy"] = comdef_values["wasGeneratedBy"]
    value_dict["topLevel"] = None
    value_dict["ownedBy"] = comdef_values["ownedBy"]
    value_dict["father_id"] = comdef_values["persistentIdentity"]

    return True, None, value_dict


def comHandler(cursor, data, comdef_values) -> (bool, str, Dict[str, str]):
    names = ["title"]
    musts = [True]
    uniques = [True]
    in_databases = [True]

    value_dict = {}
    for i, name in enumerate(names):
        flag, value = getValue(data=data, name=name, table="ComponentDefinition",
                               must=musts[i], unique=uniques[i], in_database=in_databases[i], cursor=cursor)
        value_dict[name] = value
        if flag == False:
            return False, value, None

    value_dict["displayId"] = "component" + str(random.randint(0, 100000000))
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/Component/" + \
        comdef_values["displayId"] + "/" + value_dict["displayId"]
    value_dict["version"] = "1"
    value_dict["topLevel"] = None

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
    names = ["direction", "start", "end", "orientation"]
    musts = [True, True, True, False]
    uniques = [False, False, False, False]
    in_databases = [False, False, False, False]

    value_dict = {}
    for i, name in enumerate(names):
        flag, value = getValue(data=data, name=name, table="",
                               must=musts[i], unique=uniques[i], in_database=in_databases[i], cursor=cursor)
        value_dict[name] = value
        if flag == False:
            return False, value, None

    value_dict["displayId"] = "range" + str(random.randint(0, 100000000))
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/Location/" + \
        comdef_values["displayId"] + "/" + value_dict["displayId"]
    value_dict["version"] = "1"
    value_dict["topLevel"] = None
    value_dict["father_id"] = seqant_values["persistentIdentity"]

    return True, None, value_dict


def seqantHandler(cursor, data, comdef_values) -> (bool, str, Dict[str, str]):
    names = ["title"]
    musts = [True]
    uniques = [False]
    in_databases = [False]

    value_dict = {}
    for i, name in enumerate(names):
        flag, value = getValue(data=data, name=name, table="",
                               must=musts[i], unique=uniques[i], in_database=in_databases[i], cursor=cursor)
        value_dict[name] = value
        if flag == False:
            return False, value, None

    value_dict["displayId"] = "annotation" + str(random.randint(0, 100000000))
    value_dict["persistentIdentity"] = "sysu-igem-2020-user-defined/SequenceAnnotation/" + \
        comdef_values["displayId"] + "/" + value_dict["displayId"]
    value_dict["version"] = "1"
    value_dict["topLevel"] = None

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


insert_statements = {
    "ComponentDefinition": """
    insert into ComponentDefinition(
        persistentIdentity,
        displayId,
        version,
        wasDerivedFrom,
        wasGeneratedBy,
        title,
        description,
        created,
        modified,
        mutableProvenance,
        topLevel,
        mutableDescription,
        mutableNotes,
        creator,
        type,
        role,
        comRoleSeq,
        comRoleSeqRecursive,
        roleSeq,
        originRole,
        useRole,
        outputRole
        ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    "Sequence": "insert into Sequence values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "Component": "insert into Component values(%s, %s, %s, %s, %s, %s, %s, %s)",
    "SequenceAnnotation": "insert into SequenceAnnotation values(%s, %s, %s,%s, %s, %s, %s)",
    "Location": "insert into Location values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
}

table_attrs = {
    "ComponentDefinition": [
        "persistentIdentity",
        "displayId",
        "version",
        "wasDerivedFrom",
        "wasGeneratedBy",
        "title",
        "description",
        "created",
        "modified",
        "mutableProvenance",
        "topLevel",
        "mutableDescription",
        "mutableNotes",
        "creator",
        "type",
        "role",
        "comRoleSeq",
        "comRoleSeqRecursive",
        "roleSeq",
        "originRole",
        "useRole",
        "outputRole"
    ],
    "Sequence": [
        "persistentIdentity",
        "displayId",
        "version",
        "wasDerivedFrom",
        "wasGeneratedBy",
        "topLevel",
        "ownedBy",
        "elements",
        "encoding",
        "father_id"
    ],
    "Component": [
        "persistentIdentity",
        "displayId",
        "version",
        "title",
        "topLevel",
        "definition",
        "access",
        "father_id"
    ],
    "SequenceAnnotation": [
        "persistentIdentity",
        "displayId",
        "version",
        "title",
        "topLevel",
        "component",
        "father_id"
    ],
    "Location": [
        "persistentIdentity",
        "displayId",
        "version",
        "topLevel",
        "direction",
        "start",
        "end",
        "orientation",
        "father_id"
    ]
}


def insertData(cursor, value_list, table) -> (bool, str):
    global insert_statements
    global table_attrs
    attrs = table_attrs[table]

    data_tuple = []
    for attr in attrs:
        value = value_list[attr]
        if type(value) == type([]):
            value = json.dumps(value)
        data_tuple.append(value)

    cursor.execute(insert_statements[table], tuple(data_tuple))


def addElementHandler(cnx, data) -> (bool, str):
    cursor = cnx.cursor()

    comdef_values = None
    seq_value_list = []
    com_value_list = []
    seqant_value_list = []
    location_value_list = []

    flag, message, comdef_values = comdefHandler(cursor, data)
    if flag == False:
        return False, message

    table = "Sequence"
    if table in data:
        for seqdata in data[table]:
            flag, message, seq_values = seqHandler(
                cursor, seqdata, comdef_values)
            if flag == False:
                return False, message
            seq_values["ownedBy"] = comdef_values["ownedBy"]
            seq_value_list.append(seq_values)

    table = "Component"
    if table in data:
        for comdata in data[table]:
            flag, message, com_values = comHandler(
                cursor, comdata, comdef_values)
            if flag == False:
                return False, message
            com_value_list.append(com_values)

    table = "SequenceAnnotation"
    if table in data:
        for seqantdata in data[table]:
            flag, message, seqant_values = seqantHandler(
                cursor, seqantdata, comdef_values)
            if flag == False:
                return False, message
            seqant_value_list.append(seqant_values)

            if "Location" not in seqantdata:
                return False, "At lease one location is needed for each SequenceAnnotation"

            for location_data in seqantdata["Location"]:
                flag, message, location_values = locationHandler(
                    cursor, location_data, seqant_values, comdef_values)
                if flag == False:
                    return False, message
                location_value_list.append(location_values)

    insertData(cursor, comdef_values, "ComponentDefinition")

    for seq_values in seq_value_list:
        insertData(cursor, seq_values, "Sequence")
    for com_values in com_value_list:
        insertData(cursor, com_values, "Component")
    for seqant_values in seqant_value_list:
        insertData(cursor, seqant_values, "SequenceAnnotation")
    for location_values in location_value_list:
        insertData(cursor, location_values, "Location")

    cnx.commit()
    cursor.close()

    return True, (comdef_values["displayId"], comdef_values["role"],)

# --------------- test -----------------
# try:
#     cnx = mysql.connector.connect(**database_config)
#     cursor = cnx.cursor()
#     data = None
#     with open('./doc/addElement.json', 'r') as file:
#         data = file.read()
#         flag, message = addElementHandler(cursor, data)
#         print(flag, message)

# except mysql.connector.Error as err:
#     response = err
