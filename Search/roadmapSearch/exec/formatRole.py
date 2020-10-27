from typing import List, Tuple, Dict
import sys
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import errorcode

database_config = {
    'user': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'roadmapDB',
    'raise_on_warnings': True
}

role_list = [
    "CDS",
    "Cell",
    "Chromosome",
    "Coding",
    "Composite",
    "Conjugation",
    "DNA",
    "Device",
    "Generator",
    "Intermediate",
    "Inverter",
    "Measurement",
    "Other",
    "Plasmid",
    "Plasmid_Backbone",
    "Primer",
    "Project",
    "Promoter",
    "Protein_Domain",
    "RBS",
    "RNA",
    "Regulatory",
    "Reporter",
    "Scar",
    "Signalling",
    "T7_RNA_Polymerase_Promoter",
    "T7_RNA_Polymerase_Promoter",
    "plasmid_vector",
    "Tag",
    "Temporary",
    "Terminator",
    "Translational_Unit",
    "engineered_region",
    "mature_transcript_region",
    "oriT",
    "plasmid_vector",
    "polypeptide_domain",
    "restriction_enzyme_assembly_scar",
    "ribosome_entry_site",
    "sequence_feature"
]


def formatRole() -> None:
    filepath = "role.csv"
    f = open(filepath, "r")
    for line in f:
        linesplit = line.split("\"")
        words: List = []
        for word in linesplit:
            if len(word) == 0:
                continue
            if (word[0] >= 'a' and word[0] <= 'z') or (word[0] >= 'A' and word[0] <= 'Z'):
                words.append(word)
        words.sort()
        s = "update ComponentDefinition set role = REPLACE(role, \'" + \
            line[:-1] + "\', \'["
        for i, word in enumerate(words):
            if i != 0:
                s += ", "
            s += "\"" + word + "\""
        s += "]\');"
        print(s)


def getRole(line: str) -> List:
    linesplit = line.split("\"")
    words: List = []
    for word in linesplit:
        if len(word) == 0:
            continue
        if (word[0] >= 'a' and word[0] <= 'z') or (word[0] >= 'A' and word[0] <= 'Z'):
            words.append(word)
    return words


def updateRoleSeq(cursor) -> None:
    role_char: Dict = {}
    for i, role in enumerate(role_list):
        role_char = i + 'A'

    cursor.execute("select persistentIdentity, role from ComponentDefinition")
    res = cursor.fetchall()
    



def main() -> None:

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

        cnx.commit()
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    sys.exit(main())
