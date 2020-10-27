from flask import Flask, jsonify, request
from typing import Dict, Tuple, List
import dao

app = Flask(__name__)


@app.route('/api/element/totalsize', methods=['GET'])
def totalsize() -> str:
    return dao.getTotalSize()


@app.route('/api/element/elementlist/offset=<offset>&num=<num>', methods=['GET'])
def getElementList(offset: str, num: str) -> str:
    return dao.getElementList(offset, num)


@app.route("/api/element/name=<name>&rolefilter=<filter_list>&limit=<limit_num>", methods=['GET'])
def getElementByName(name: str, limit_num: str, filter_list: str) -> None:
    method = request.method
    data = request.form
    return dao.getElementByName(name, limit_num, filter_list)


@app.route("/api/element/name=<element_name>", methods=['PUT', 'DELETE'])
def putOrDeleteElement(element_name: str, limit_num: int) -> None:
    method = request.method
    data = request.form
    if method == 'DELETE':
        pass
    if method == 'PUT':
        pass


if __name__ == '__main__':
    dao.init()
    app.run(debug=True)
