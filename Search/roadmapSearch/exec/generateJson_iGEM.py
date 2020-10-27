import sbol
from typing import Dict, List, Tuple
import sys
import mysql.connector
from mysql.connector import errorcode
import json
import xml.etree.ElementTree as ET
import re
import os.path
import getopt

database_config = {
    'user': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'roadmapDB',
    'raise_on_warnings': True
}

activity_attr: List = [
    "persistentIdentity",
    "displayId",
    "version",
    "title",
    "description",
    "topLevel",
    "ownedBy",
    "creator",
    "endedAtTime"
]

componentDefinition_attr: List = [
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
    "role"
]

sequence_attr: List = [
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
]

component_attr: List = [
    "persistentIdentity",
    "displayId",
    "version",
    "title",
    "topLevel",
    "definition",
    "access",
    "father_id"
]

sequenceAnnotation_attr: List = [
    "persistentIdentity",
    "displayId",
    "version",
    "title",
    "topLevel",
    "component",
    "father_id"
]

location_attr: List = [
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


select_Activity = """
    select * 
    from Activity as a
    where exists(
        select * 
        from DesignGraph_Activity 
        where activity_id = a.persistentIdentity
        and designGraph_id = %s
    )
"""

select_DesignGraph = """
    select * 
    from DesignGraph
    where persistentIdentity = %s
"""

select_ComponentDefinition = """
    select *
    from ComponentDefinition as comdef
    where exists(
        select * 
        from DesignGraph_ComponentDefinition
        where graph_id = %s and componentDefinition_id = comdef.persistentIdentity
    )
"""

select_Sequence = """
    select * 
    from Sequence 
    where father_id like %s
"""

select_Component = """
    select * 
    from Component 
    where father_id = %s
"""

select_SequenceAnnotation = """
    select *
    from SequenceAnnotation
    where father_id = %s
"""

select_Location = """ 
    select *
    from Location 
    where father_id = %s
"""

select_statement: Dict = {
    "Activity": select_Activity,
    "Sequence": select_Sequence,
    "Component": select_Component,
    "SequenceAnnotation": select_SequenceAnnotation,
    "Location": select_Location
}

name_attr: Dict = {
    "Activity": activity_attr,
    "Sequence": sequence_attr,
    "Component": component_attr,
    "SequenceAnnotation": sequenceAnnotation_attr,
    "Location": location_attr
}


def decode(res: List) -> List:
    for i, row in enumerate(res):
        row_list: List = list(row)
        for j, col in enumerate(row_list):
            if isinstance(col, bytearray) and col is not None:
                decoded_col = col.decode()
                if decoded_col is None or len(decoded_col) == 0:
                    row_list[j] = None
                elif decoded_col[0] == '[':
                    row_list[j] = json.loads(decoded_col)
                else:
                    row_list[j] = decoded_col
        res[i] = tuple(row_list)
    return res


def generateSubObject(
    cursor: mysql.connector.cursor,
    arg_id: str,
    name: str
) -> List:
    '''
    for component, sequence, sequenceAnnotation 
    '''
    obj_list: List = []
    cursor.execute(select_statement[name], (arg_id,))
    obj_res = decode(cursor.fetchall())
    for obj_data in obj_res:
        obj_dict: Dict = {}
        for i, attr in enumerate(name_attr[name]):
            obj_dict[attr] = obj_data[i]
        if name == "SequenceAnnotation":
            seq_id = obj_dict["persistentIdentity"]
            location_list = generateSubObject(cursor, seq_id, "Location")
            obj_dict["Location"] = location_list
        obj_list.append(obj_dict)

    return obj_list

    # comdef_dict["Component"] = com_list


def generateJson(
    cursor: mysql.connector.cursor,
    graph_id: str
) -> None:
    output: Dict = {}

    cursor.execute(select_DesignGraph, (graph_id,))
    graph_res = decode(cursor.fetchall())

    if len(graph_res) == 0:
        return "{}"

    output["persistentIdentity"] = graph_res[0][0]
    output["article"] = graph_res[0][1]
    output["description"] = graph_res[0][2]

    act_id = graph_res[0][3]
    act_list = generateSubObject(cursor, graph_id, "Activity")
    output["Activity"] = act_list

    comdef_list: List = []
    cursor.execute(select_ComponentDefinition, (graph_id,))
    comdef_res = decode(cursor.fetchall())

    for comdef_data in comdef_res:
        comdef_dict: Dict = {}
        for i, attr in enumerate(componentDefinition_attr):
            if attr == "role":
                comdef_dict[attr] = comdef_data[-1]
            else:
                comdef_dict[attr] = comdef_data[i]

        comdef_id: str = comdef_dict["persistentIdentity"]

        comdef_dict["Sequence"] = generateSubObject(
            cursor, comdef_id, "Sequence")
        comdef_dict["Component"] = generateSubObject(
            cursor, comdef_id, "Component")
        comdef_dict["SequenceAnnotation"] = generateSubObject(
            cursor, comdef_id, "SequenceAnnotation")

        comdef_list.append(comdef_dict)

    output["ComponentDefinition"] = comdef_list

    return json.dumps(output)


def main(argv: List) -> None:

    graph_id: str = ""
    try:
        opts, args = getopt.getopt(
            argv, "i:", ["graph_id="])
    except getopt.GetoptError:
        print("generateJson_iGEM.py -i <input-graph-id>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("generateJson_iGEM.py -i <input-graph-id>")
            sys.exit()
        elif opt in ("-i", "--graph_id"):
            graph_id = arg

    try:
        cnx = mysql.connector.connect(**database_config)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor(prepared=True)

        output = generateJson(cursor, graph_id)
        print(output)

        cnx.commit()
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
