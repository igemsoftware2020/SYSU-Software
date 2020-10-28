from flask import Flask, jsonify, request
from typing import Dict, Tuple, List
import dao
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/element/totalsize', methods=['GET'])
def totalsize():
    return dao.getTotalSize()


@app.route('/api/element/elementlist/offset=<offset>&num=<num>', methods=['GET'])
def getElementList(offset: str, num: str):
    return dao.getElementList(offset, num)

# fuzzy 加上title


@app.route("/api/element/fuzzy/name=<name>&limit=<limit_num>", methods=['GET'])
def getElementByName_fuzzy(name: str, limit_num: str):
    return dao.getElementByName_fuzzy(name, limit_num)


@app.route("/api/element/like/name=<name>&limit=<limit_num>", methods=['GET'])
def getElementByName_like(name: str, limit_num: str):
    return dao.getElementByName_like(name, limit_num)


@app.route("/api/element/fuzzy/name=<name>&rolefilter=<filter_list>&limit=<limit_num>", methods=['GET'])
def getElementByNameWithRoleFilter_fuzzy(name: str, limit_num: str, filter_list: str):
    method = request.method
    data = request.form
    return dao.getElementByNameWithRoleFilter_fuzzy(name, limit_num, filter_list)


@app.route("/api/element/like/name=<name>&rolefilter=<filter_list>&limit=<limit_num>", methods=['GET'])
def getElementByNameWithRoleFilter_like(name: str, limit_num: str, filter_list: str):
    method = request.method
    data = request.form
    return dao.getElementByNameWithRoleFilter_like(name, limit_num, filter_list)


@app.route("/api/element/delete/displayId=<displayId>", methods=['DELETE'])
def DeleteElement(displayId: str):
    return dao.deleteElement(displayId)


@app.route("/api/element/modify/displayId=<displayId>", methods=['PUT'])
def ModifyElement(displayId: str):
    dao.deleteElement(displayId)
    data = request.get_json()
    return dao.addElement(data)


@app.route("/api/element/add", methods=['POST'])
def addElement():
    data = request.get_json()
    return dao.addElement(data)


@app.route("/api/element/tf=<tf_name>", methods=['GET'])
def searchTF(tf_name: str):
    return dao.getTFGene(tf_name)


# mode = <structure-rstructure-element-relement>, 4选n
@app.route("/api/gene-circuit/search/mode=<mode>&limit=<limit>", methods=['POST'])
def searchRoadmap(mode: str, limit: int):
    data = request.get_json()
    return dao.roadmapSearch(data, mode, limit)


@app.route("/api/design-graph/add", methods=['POST'])
def addDesighGraph():
    data = request.get_json()
    return dao.addDesighGraph(data)


if __name__ == '__main__':
    dao.init()
    app.run(debug=False,host='0.0.0.0',port=5001)
