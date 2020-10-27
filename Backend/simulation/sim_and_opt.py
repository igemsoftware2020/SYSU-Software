# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import os
import re
import traceback
import sys

import numpy as np
from sbol import *

from optimize import optimization
from solve import solve_ode


def sim_and_opt(request):
    """
    {
        data: 
            {"parts":
                {"19529":"0","19530":"0","19531":"0"},
            "ks":
                {"19529":"0","19530":"0","19531":"0"},
            "ns":
                {"19529":"0","19530":"0","19531":"0"},
            "ds":
                {"19529":"0","19530":"0","19531":"0"},
            "lines":
                [{"start":19529,"end":19530,"type":"stimulation"},{"start":19529,"end":19532,"type":"stimulation"}],
            "time":"0",
            "target":"None",
            "targetAmount":"0",
            "type":"simulation"}
    }
    """

    data = json.loads(request)

    material_amount = data['parts']
    num_of_material = len(material_amount)
    lines = data['lines']
    material_id = []
    init_amount = []
    ks = data['ks']
    ds = data['ds']
    ns = data['ns']
    k_value = []
    d_value = []
    n_value = []
    targetAmount = float(data['targetAmount'])
    flag = data['type']

    for (k, v) in material_amount.items():
        material_id.append(int(k))
        init_amount.append(float(v))
    if data['target'] != "None":
        target = material_id.index(int(data['target']))

    for i in material_id:
        k_value.append(float(ks[str(i)]))
        d_value.append(float(ds[str(i)]))
        n_value.append(float(ns[str(i)]))

    matrix = [[0 for i in range(len(material_amount))]
              for j in range(len(material_amount))]

    for line in lines:
        start = line['start']
        end = line['end']
        if line['type'] == 'stimulation':
            matrix[material_id.index(end)][material_id.index(start)] = 1
        elif line['type'] == 'inhibition':
            matrix[material_id.index(end)][material_id.index(start)] = -1
        else:
            return {'success': -1}

    evol_t = float(data['time'])  # reaction duration

    data = {
        'matrix': matrix,
        'initial_value': init_amount,
        'd': d_value,
        'n': n_value,
    }
    # print(material_id)
    # print(data)
    k_op = None
    try:
        if flag == 'simulation':
            # y will be num_material * 1000 matrix
            t, y = solve_ode(data, k_value, evol_t)
        else:
            # print(data, evol_t, targetAmount, k_value, target)
            k_op = optimization(data, targetAmount, k_value, evol_t, target)
            t, y = solve_ode(data, k_op, evol_t)
    except:
        logging.info("Error while computing ode...")
        return {'success': -1}
    # print("New ks:", k_op)
    t = []
    y_np = np.array(y)
    for i in range(num_of_material):
        t.append(y_np[:, i])
        t[-1] = t[-1][::10]  # only return 100 values

    # All Data:
    # result = {
    #     "new_ks": k_op,
    #     "data":[],
    #     "parts": material_id,
    #     "xAxis": list(np.linspace(0, evol_t, 100)),
    # }
    # for i in range(num_of_material):
    #     result['data'].append({
    #         'name': material_id[i],
    #         'type': 'line', # requirement of echarts
    #         'data': list(t[i]),
    #         'showSymbol': False,
    #         'smooth': True,
    #     })

    # Target data
    # print(target)
    result = {
        "series": [{
            'name': material_id[target],
            'type': 'line',
            'data': list(t[target]),
            'showSymbol': False,
            'smooth': True,
        }],
        "parts": [material_id[target]],
        "xAxis": {'data': [round(i, 3) for i in list(np.linspace(0, evol_t, 100))]},
        "yAxis": {},
        "success": 0,
    }
    if flag == 'optimization':
        result["new_ks"] = [k_op[target]]

    return result


input_file = open(sys.argv[1], mode='r')
json_str = input_file.read()
input_file.close()
ret = sim_and_opt(json_str)
print(json.dumps(ret))
