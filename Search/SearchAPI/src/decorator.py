from flask import jsonify
from common import database_config
import json
import mysql.connector
from mysql.connector import errorcode
from typing import Dict, Tuple, List


def db_helper(jsonfy_rule):
    def wrapper(func):
        def inner(*args, **kwargs):
            response: str = None
            try:
                cnx = mysql.connector.connect(**database_config)
            except mysql.connector.Error as err:
                response = err
            else:
                try:
                    result = func(cnx, *args, **kwargs)
                    response = __common_struct(jsonfy_rule(result))
                except Exception as e:
                    response = __common_struct(None, False, str(e))
            return response
        return inner
    return wrapper


def __common_struct(data, success=True, error_msg='error'):
    if success:
        result = {'response': data, 'status': 1, 'message': 'success'}
    else:
        result = {'response': data, 'status': 0, 'message': error_msg}
    return jsonify(result)
