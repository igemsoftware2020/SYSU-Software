import json
import mysql.connector
from mysql.connector import errorcode
from typing import Dict, Tuple, List
from fuzzywuzzy import fuzz, process
from flask import jsonify
from common import database_config
from decorator import db_helper

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
            if attr == "role":
                data_dict[attr] = json.loads(data[i])
            else:
                data_dict[attr] = data[i]
        output[data_dict["displayId"]] = data_dict
    return output


@db_helper(lambda data: data)
def getElementList(cnx, offset: str, num: str) -> Dict:
    output: str = None
    cursor = cnx.cursor(prepared=True)
    sql_get = "select displayId, role, mutableDescription, creator from ComponentDefinition LIMIT %s,%s"
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

        for role in componentDefinition_role:
            sql_get = "select distinct displayID from ComponentDefinition where role like \"%" + role + "%\""
            cursor.execute(sql_get)
            res = cursor.fetchall()
            componentDefinition_role_name[role] = decode(
                res, is_name_list=True)

        cursor.close()
        cnx.close()


def elementMapping(data_list: List[List]) -> Dict:
    if len(data_list) == 0:
        return None
    output: Dict = {}
    for data in data_list:
        data_dict: Dict = {}
        for i, attr in enumerate(componentDefinition_attr):
            if attr == "role":
                data_dict[attr] = json.loads(data[0][i])
            else:
                data_dict[attr] = data[0][i]
        output[data_dict["displayId"]] = data_dict
    return output


@db_helper(lambda data: data)
def getElementByName(cnx, name: str, limit_num: str, filter_list: str) -> Dict:
    limit_num = int(limit_num)
    output: Dict = {}
    try:
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

        sql_get = "SELECT * from ComponentDefinition WHERE displayID = %s"
        allres: List[List] = []
        for element_name, value in possible_element_name:
            cursor.execute(sql_get, (element_name,))
            res = decode(cursor.fetchall(), is_name_list=False)
            allres.append(res)
            if value == 100:
                break
        output = elementMapping(allres)
        cursor.close()
    except Exception as e:
        output["ERROR"] = "ERROR: " + str(e)
    return output


def init() -> None:
    getElementNameList()
