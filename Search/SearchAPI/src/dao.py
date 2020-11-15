import json
import mysql.connector
from mysql.connector import errorcode
from typing import Dict, Tuple, List
from fuzzywuzzy import fuzz, process
from flask import jsonify
from common import database_config
from decorator import db_helper
import utility
import os
import sh
import glob
import random
from SBOLXMLconverter import *

componentDefinition_role_name: Dict = {}

componentDefinition_name: List = []

componentDefinition_attr: List = \
    ["persistentIdentity",
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
     "role"]

componentDefinition_role: List = \
    ["Promoter",
     "DNA",
     "RBS",
     "CDS",
     "Terminator",
     "Other",
     "Coding",
     "Reporter",
     "Translational_Unit",
     "engineered_region",
     "Generator",
     "Signalling",
     "Primer",
     "Regulatory",
     "Plasmid",
     "Tag",
     "Device",
     "Cell",
     "Conjugation",
     "Inverter",
     "Protein_Domain"
     ]

standard_role_list = [
    "interval",
    "unknown",
    "terminator",
    "rbs",
    "dna",
    "rna",
    "composite",
    "cds",
    "reporter",
    "generator",
    "primer",
    "promoter",
    "plasmid",
    "device",
    "cell",
    "scar"
]


def decode(res: List, is_name_list: bool) -> List:
    for i, row in enumerate(res):
        row_list: List = list(row)
        for j, col in enumerate(row_list):
            if isinstance(col, bytearray) and col is not None:
                row_list[j] = col.decode()
        if is_name_list == True:
            res[i] = row_list[0]
        else:
            res[i] = tuple(row_list)
    return res


@db_helper(lambda data: data)
def getTotalSize(cnx) -> str:
    output: str = None

    cursor = cnx.cursor(prepared=True)
    sql_get = "select count(*) from ComponentDefinition"
    cursor.execute(sql_get)
    res = cursor.fetchall()[0][0]
    output = str(res)
    cursor.close()
    cnx.close()

    return output


def elementListMapping(data_list: List) -> Dict:
    if len(data_list) == 0:
        return None
    output: Dict = {}
    for data in data_list:
        data_dict: Dict = {}
        for i, attr in enumerate(["displayId", "role", "mutableDescription", "creator"]):
            data_dict[attr] = data[i]
        output[data_dict["displayId"]] = data_dict
    return output


@db_helper(lambda data: data)
def getElementList(cnx, offset: str, num: str) -> Dict:
    output: str = None
    cursor = cnx.cursor(prepared=True)
    sql_get = "select displayId, outputRole, mutableDescription, creator from ComponentDefinition LIMIT %s,%s"
    cursor.execute(sql_get, (offset, num,))
    res = decode(cursor.fetchall(), is_name_list=False)
    output = elementListMapping(res)
    cursor.close()
    cnx.close()

    return output


def getElementNameList() -> List:
    try:
        cnx = mysql.connector.connect(**database_config)
    except mysql.connector.Error as err:
        response = err
    else:
        cursor = cnx.cursor(prepared=True)
        sql_get = "select distinct displayID from ComponentDefinition"
        cursor.execute(sql_get)
        res = cursor.fetchall()
        global componentDefinition_name
        componentDefinition_name = decode(res, is_name_list=True)

        global componentDefinition_role_name

        for role in standard_role_list:
            sql_get = "select distinct displayId from ComponentDefinition where outputRole like \"%" + role + "%\""
            cursor.execute(sql_get)
            res = cursor.fetchall()
            componentDefinition_role_name[role] = decode(
                res, is_name_list=True)

        cursor.close()
        cnx.close()


def elementMapping(data_list: List[List]) -> Dict:
    '''
    [[(attr1, attr2)], [...], [...]]
    '''
    if len(data_list) == 0:
        return None
    output: Dict = {}
    for data in data_list:
        data_dict: Dict = {}
        for i, attr in enumerate(componentDefinition_attr):
            if attr == "role":
                data_dict[attr] = data[0][-1]  # outputRole
                # data_dict[attr] = json.loads(data[0][i])
            else:
                data_dict[attr] = data[0][i]
        output[data_dict["displayId"]] = data_dict
    return output


@db_helper(lambda data: data)
def getElementByNameWithRoleFilter_fuzzy(cnx, name: str, limit_num: str, filter_list: str) -> Dict:
    limit_num = int(limit_num)
    output: Dict = {}

    cursor = cnx.cursor(prepared=True)

    possible_element_name: List = []

    if len(filter_list) == 0:
        possible_element_name = process.extract(
            name, componentDefinition_name, limit=limit_num)
    else:
        filter_role: List = filter_list.split('-')
        for role in filter_role:
            pname = process.extract(
                name, componentDefinition_role_name[role], limit=10 * limit_num)
            possible_element_name.extend(pname)

    possible_element_name.sort(key=lambda tp: tp[1], reverse=True)
    possible_element_name = possible_element_name[:min(
        limit_num, len(possible_element_name))]
    print(possible_element_name)

    sql_get = "SELECT * from ComponentDefinition WHERE displayId = %s or title = %s"
    allres: List[List] = []
    for element_name, value in possible_element_name:
        cursor.execute(sql_get, (element_name, element_name,))
        res = decode(cursor.fetchall(), is_name_list=False)
        allres.append(res)
        if value == 100:
            break

    output = elementMapping(allres)
    cursor.close()

    return output


@db_helper(lambda data: data)
def getElementByNameWithRoleFilter_like(cnx, name: str, limit_num: str, filter_list: str) -> Dict:
    limit_num = int(limit_num)
    output: Dict = {}
    allres: List = []

    cursor = cnx.cursor(prepared=True)

    role_like = ""
    filter_role: List = filter_list.split('-')
    for role in filter_role:
        if role_like != "":
            role_like += " or "
        role_like += "outputRole like \"%" + role + "%\""

    sql_get = "SELECT * from ComponentDefinition WHERE (" + role_like + ") and (displayId like \"%" + \
        name + "%\" or title like \"%" + name + \
        "%\") limit 0, " + str(limit_num)

    # print(sql_get)

    cursor.execute(sql_get)
    res = decode(cursor.fetchall(), is_name_list=False)

    for tp in res:
        allres.append([tp])

    print("before elementMapping")
    output = elementMapping(allres)
    cursor.close()

    return output


@db_helper(lambda data: data)
def getElementByName_fuzzy(cnx, name: str, limit_num: str) -> Dict:
    limit_num = int(limit_num)
    output: Dict = {}
    # try:
    cursor = cnx.cursor(prepared=True)

    possible_element_name: List = []

    possible_element_name = process.extract(
        name, componentDefinition_name, limit=limit_num)

    sql_get = "SELECT * from ComponentDefinition WHERE displayId = %s or title = %s"
    allres: List[List] = []
    for element_name, value in possible_element_name:
        cursor.execute(sql_get, (element_name, element_name, ))
        res = decode(cursor.fetchall(), is_name_list=False)
        allres.append(res)
        if value == 100:
            break
    output = elementMapping(allres)

    cursor.close()
    return output


@db_helper(lambda data: data)
def getElementByName_like(cnx, name: str, limit_num: str) -> Dict:
    limit_num = int(limit_num)
    output: Dict = {}
    allres: List = []
    # try:
    cursor = cnx.cursor(prepared=True)

    sql_get = "SELECT * from ComponentDefinition WHERE displayId like \"%" + \
        name + "%\" or title like \"%" + name + \
        "%\" limit 0, " + str(limit_num)
    cursor.execute(sql_get)
    res = decode(cursor.fetchall(), is_name_list=False)

    for tp in res:
        allres.append([tp])

    output = elementMapping(allres)
    cursor.close()
    return output


@db_helper(lambda data: data)
def deleteElement(cnx, displayId):
    cursor = cnx.cursor()
    tables = ["Location", "SequenceAnnotation",
              "Component", "Sequence", "ComponentDefinition"]
    print(tables)
    for table in tables:
        sql_delete = "delete from " + table + " where persistentIdentity like '%" + \
            "user-defined/" + table + "/" + displayId + "%'"
        cursor.execute(sql_delete)
    cnx.commit()


@db_helper(lambda data: data)
def addElement(cnx, data) -> None:
    flag, message = utility.addElementHandler(cnx, data)

    if flag == False:
        raise Exception(message)
    else:
        componentDefinition_name.append(message[0])
        componentDefinition_role_name[message[1]].append(message[0])


@db_helper(lambda data: data)
def addDesignGraph(cnx, data):
    jsondata = SBOLxml_to_json(data)
    print(jsondata)
    flag, message = utility.addDesignGraphHandler(cnx, json.loads(jsondata))
    if flag == False:
        raise Exception(message)


@db_helper(lambda data: data)
def getTFGene(cnx, tf_name) -> List:
    cursor = cnx.cursor(prepared=True)
    cursor.execute(
        "select gene_name from TF_ComponentDefinition where tf_name = %s", (tf_name,))
    res = decode(cursor.fetchall(), True)
    return res


def extractFileName(file_name):
    tp0: str = ""
    words = file_name.split('-')
    cnt = 0
    if words[0] == "recursive":
        tp0 = words[0] + "-" + words[1]
        cnt = 1
    else:
        tp0 = words[0]
        cnt = 0
    tp1: str = ""
    cnt += 1
    tp1 = words[cnt]
    cnt += 1
    tp2 = words[cnt]
    cnt += 1
    tp3 = words[cnt][:-6]
    return tp0, tp1, tp2, tp3


@db_helper(lambda data: data)
def roadmapSearch(cnx, data, mode, limit) -> None:
    request_id = random.randint(0, 1e9)
    now = os.path.split(os.path.realpath(__file__))[0]
    exec_file = os.path.join(os.path.join(os.path.join(os.path.join(
        os.path.join(now, ".."), ".."), "roadmapSearch"), "build"), "search")
    input_dir = os.path.join(os.path.join(os.path.join(os.path.join(
        os.path.join(now, ".."), "buffer"), "roadmapSearch"), "input"), str(request_id))
    input_file = os.path.join(input_dir, "input.json")
    exec_dir = os.path.join(os.path.join(os.path.join(
        os.path.join(now, ".."), ".."), "roadmapSearch"), "exec")
    output_dir = os.path.join(os.path.join(os.path.join(os.path.join(
        os.path.join(now, ".."), "buffer"), "roadmapSearch"), "output"), str(request_id))

    if os.path.exists(output_dir):
        files = glob.glob(os.path.join(output_dir, "*"))
        sh.rm(files)

    (destination) = os.makedirs(input_dir, exist_ok=True)
    (destination) = os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "w") as f:
        f.write(json.dumps(data))

    modes = mode.split('-')
    s = ""
    e = ""
    for mode in modes:
        if mode == "structure":
            s = "--structure"
        if mode == "rstructure":
            s = "--recursive-structure"
        if mode == "element":
            e = "--element"
        if mode == "relement":
            e = "--recursive-element"

    search = """
    {} -i {} {} {} --exec-dir {} --output-dir {} --limit {}
    """

    os.system(search.format(exec_file, input_file, s,
                            e, exec_dir, output_dir, str(limit)))

    g = os.walk(output_dir)
    output = {}
    files = []
    for path, dir_list, file_list in g:
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            files.append((file_name, file_path,))
    files.sort(key=lambda x: x[0])

    for data in files:
        file_name = data[0]
        file_path = data[1]
        tp0, tp1, tp2, tp3 = extractFileName(file_name)
        tp2 = "order-" + tp2
        if tp0 not in output.keys():
            output[tp0] = {}
        if tp1 not in output[tp0].keys():
            output[tp0][tp1] = {}
        if tp2 not in output[tp0][tp1].keys():
            output[tp0][tp1][tp2] = {}
        with open(file_path, "r") as f:
            content = f.read()
            if len(content) == 0:
                continue
            data = json.loads(content)
            output[tp0][tp1][tp2] = data

    rmdir = """
    rm -r {}
    """

    os.system(rmdir.format(input_dir))
    os.system(rmdir.format(output_dir))

    return output


def init() -> None:
    getElementNameList()
