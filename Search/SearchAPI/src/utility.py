from typing import Tuple, Dict, List
import json
import mysql.connector
from mysql.connector import errorcode
import datetime
import random
from common import *
from jsonExtractHandler import *


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

    try:
        cursor.execute(insert_statements[table], tuple(data_tuple))
    except Exception as err:
        print(err)
        return False, err


def insertHandler(cursor, input_value, table, is_list: bool):
    if is_list == True:
        value_list = input_value
        for values in value_list:
            insertData(cursor, values, table)
    else:
        values = input_value
        insertData(cursor, values, table)


def getGraphValues(cursor, data) -> (bool, str, Dict[str, str]):
    flag, message, graph_values = graphHandler(cursor, data)
    if flag == False:
        return False, message, None
    return True, None, graph_values


def getActValueList(cursor, data, graph_values) -> (bool, str, Dict[str, str], Dict[str, str]):
    act_value_list = []
    graph_act_value_list = []
    table = "Activity"
    if table in data:
        for actdata in data[table]:
            flag, message, act_values = actHandler(cursor, actdata)
            if flag == False:
                return False, message, None, None
            act_value_list.append(act_values)
            graph_act_value_list.append(
                {
                    "designGraph_id": graph_values["persistentIdentity"],
                    "activity_id": act_values["persistentIdentity"]
                }
            )
    return True, None, act_value_list, graph_act_value_list


def getComdefValues(cursor, data) -> (bool, str, Dict):

    global is_add_element
    if is_add_element == False:
        if "displayId" not in data:
            return False, "displayId of ComponentDefinition should be provided"
        cursor.execute(
            "select persistentIdentity from ComponentDefinition where displayId = '" + data["displayId"] + "'")
        r = cursor.fetchall()
        if r is not None and r != [] and r[0][0] is not None:
            return True, r[0][0], None

    comdef_values = {}
    seq_value_list = []
    com_value_list = []
    seqant_value_list = []
    location_value_list = []

    flag, message, comdef_values = comdefHandler(cursor, data)
    if flag == False:
        return False, message, None

    table = "Sequence"
    if table in data:
        for seqdata in data[table]:
            flag, message, seq_values = seqHandler(
                cursor, seqdata, comdef_values)
            if flag == False:
                return False, message, None
            seq_value_list.append(seq_values)

    table = "Component"
    if table in data:
        for comdata in data[table]:
            flag, message, com_values = comHandler(
                cursor, comdata, comdef_values)
            if flag == False:
                return False, message, None
            com_value_list.append(com_values)

    table = "SequenceAnnotation"
    if table in data:
        for seqantdata in data[table]:
            flag, message, seqant_values = seqantHandler(
                cursor, seqantdata, comdef_values)
            if flag == False:
                return False, message, None
            seqant_value_list.append(seqant_values)

            if "Location" not in seqantdata:
                return False, "At lease one location is needed for each SequenceAnnotation", None

            for location_data in seqantdata["Location"]:
                flag, message, location_values = locationHandler(
                    cursor, location_data, seqant_values, comdef_values)
                if flag == False:
                    return False, message, None
                location_value_list.append(location_values)

    res = {
        "ComponentDefinition": comdef_values,
        "Sequence": seq_value_list,
        "Component": com_value_list,
        "SequenceAnnotation": seqant_value_list,
        "Location": location_value_list
    }
    return True, None, res


def getComdefValueList(cursor, data, graph_values) -> (bool, str, Dict):
    res = {
        "ComponentDefinition": [],  # comdef_value_list
        "DesignGraph_ComponentDefinition": [],  # graph_comdef_value_list
        "Sequence": [],  # seq_value_list,
        "Component": [],  # com_value_list,
        "SequenceAnnotation": [],  # seqant_value_list,
        "Location": [],  # location_value_list
    }

    tables = ["ComponentDefinition", "DesignGraph_ComponentDefinition",
              "Sequence", "Component", "SequenceAnnotation", "Location"]

    table = "ComponentDefinition"
    if table in data:
        for comdefdata in data[table]:
            flag, message, comdef_res = getComdefValues(cursor, comdefdata)
            if flag == False:
                return False, message, None
            if comdef_res is None:
                res[tables[1]].append(
                    {
                        "graph_id": graph_values["persistentIdentity"],
                        "componentDefinition_id": message
                    }
                )
                continue
            res[tables[0]].append(comdef_res[tables[0]])
            res[tables[1]].append(
                {
                    "graph_id": graph_values["persistentIdentity"],
                    "componentDefinition_id": comdef_res[tables[0]]["persistentIdentity"]
                }
            )
            for i in range(2, 6):
                res[tables[i]].extend(comdef_res[tables[i]])
    return True, None, res


def addElementHandler(cnx, data) -> (bool, tuple):
    global is_add_element
    is_add_element = True

    cursor = cnx.cursor()

    flag, message, res = getComdefValues(cursor, data)
    if flag == False:
        return False, message

    tables = ["ComponentDefinition", "Sequence",
              "Component", "SequenceAnnotation", "Location"]
    insertHandler(cursor, res[tables[0]], tables[0], is_list=False)
    for i in range(1, len(tables)):
        insertHandler(cursor, res[tables[i]], tables[i], is_list=True)

    # cnx.commit()
    cursor.close()

    return True, None


def addDesignGraphHandler(cnx, data) -> (bool, tuple):

    global is_add_element
    is_add_element = False

    cursor = cnx.cursor()
    flag, message, graph_values = getGraphValues(cursor, data)
    if flag == False:
        return False, message

    flag, message, act_value_list, graph_act_value_list = \
        getActValueList(cursor, data, graph_values)
    if flag == False:
        return False, message

    flag, message, res = getComdefValueList(cursor, data, graph_values)
    if flag == False:
        return False, message

    insertHandler(cursor, graph_values, "DesignGraph", is_list=False)
    insertHandler(cursor, act_value_list, "Activity", is_list=True)
    insertHandler(cursor, graph_act_value_list,
                  "DesignGraph_Activity", is_list=True)
    tables = ["ComponentDefinition", "DesignGraph_ComponentDefinition", "Sequence",
              "Component", "SequenceAnnotation", "Location"]

    for i in range(len(tables)):
        insertHandler(cursor, res[tables[i]], tables[i], is_list=True)

    cnx.commit()
    cursor.close()

    return True, None


# --------------- test -----------------
# try:
#     cnx = mysql.connector.connect(**database_config)
#     cursor = cnx.cursor()
#     data = None
#     # with open('./testdata/addElement.json', 'r') as file:
#     #     data = file.read()
#     #     flag, message = addElementHandler(cnx, json.loads(data))
#     #     print(flag, message)
#     with open('./testdata/tmp.json', 'r') as file:
#         data = file.read()
#         print(data)
#         flag, message = addDesignGraphHandler(cnx, json.loads(data))
#         print(flag, message)
#     print("end")
# except mysql.connector.Error as err:
#     response = err
