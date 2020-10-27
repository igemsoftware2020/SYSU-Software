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


def generateComDef(cursor, graph_id):
    comdef = []
    cursor.execute(
        "select componentDefinition_id from PaperComponentDefinition_PaperGraph where graph_id = %s", (graph_id,))
    res = decode(cursor.fetchall())
    for i, value in enumerate(res):
        comdef_id = value[0]
        cursor.execute(
            "select * from PaperComponentDefinition where persistentIdentity = " +
            str(comdef_id))
        r = decode(cursor.fetchall())

        comdef.append({})
        comdef[i]["perisistentIdentity"] = comdef_id
        comdef[i]["role"] = r[0][2]
        comdef[i]["displayId"] = r[0][3]

    return comdef


def generateJson(
    cursor: mysql.connector.cursor,
    graph_id: str
):
    cursor.execute(
        "select father_id from PaperGraph where persistentIdentity = %s", (graph_id,))
    paper_id = cursor.fetchall()[0][0]
    cursor.execute(
        "select * from Paper where persistentIdentity = %s", (str(paper_id), ))
    res = decode(cursor.fetchall())

    output: Dict = {}
    output["article"] = {}
    output["article"]["title"] = res[0][1]
    output["article"]["url"] = res[0][2]
    output["article"]["authors"] = res[0][3]
    output["article"]["abstract"] = res[0][4]
    output["article"]["vol"] = res[0][5]
    output["article"]["issue"] = res[0][6]
    output["article"]["type"] = res[0][7]
    output["article"]["date"] = res[0][8]
    output["article"]["jourName"] = res[0][9]

    output["ComponentDefinition"] = generateComDef(cursor, graph_id)

    return json.dumps(output)


def main(argv: List) -> None:

    graph_id: str = ""
    try:
        opts, args = getopt.getopt(
            argv, "i:", ["graph_id="])
    except getopt.GetoptError:
        print("generateJson_paper.py -i <input-graph-id>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("generateJson_paper.py -i <input-graph-id>")
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
