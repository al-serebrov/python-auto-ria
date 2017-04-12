"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""


import requests
import json
from pprint import pprint
from fnmatch import fnmatch

# Search parameters
VEHICLE_TYPE = 'Легковые'
VEHICLE_MARK = 'Ford'
VEHICLE_MODEL = 'Focus'
VEHICLE_BODY = None
VEHICLE_YEAR_START = '2000'
VEHICLE_YEAR_END = '2006'
VEHICLE_REGION = 'Харьков'
# not implemented yet
# VEHICLE_MIN_PRICE = '4000'
# VEHICLE_MAX_PRICE = '5000'
# end

# auto.ria.com API parameters, defaulted to None
PARAMS = {
    'main_category': None,
    'body_id': None,
    'marka_id': None,
    'model_id': None,
    'yers': None,
    'gear_id': None,
    'fuel_id': None,
    'drive_id': None,
    'engineVolume': None,
    'options': None,
    'raceInt': None,
    'door': None,
    'state_id': None,
    'city_id': None,
    'carrying': None,
    'seats': None,
    'color_id': None,
    'custom': None,
    'damage': None,
    'under_credit': None,
    'confiscated_car': None,
    'onRepairParts': None,
}


def jsonify_response(url):
    """Send get request and return data in JSON."""
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)


def get_types():
    """Get available vehicle types from auto.ria.com."""
    url = 'http://api.auto.ria.com/categories'
    return jsonify_response(url)


def get_bodystyles(category):
    """Get available bodystyles from auto.ria.com."""
    url = 'http://api.auto.ria.com/categories/{}/bodystyles' \
          .format(str(category))
    return jsonify_response(url)


def get_marks(category):
    """Get available car marks from auto.ria.com."""
    url = 'http://api.auto.ria.com/categories/{}/marks' \
          .format(str(category))
    return jsonify_response(url)


def get_models(category, mark):
    """Get available models for selected mark from auto.ria.com."""
    url = 'http://api.auto.ria.com/categories/{}/marks/{}/models' \
          .format(str(category), str(mark))
    return jsonify_response(url)


def get_states():
    """Get available states from auto.ria.com."""
    url = 'http://api.auto.ria.com/states'
    return jsonify_response(url)


def select_type(vehicle_type):
    """Select vehicle type from available types."""
    for ve_type in types_list:
        if str(ve_type['name']) == vehicle_type:
            return ve_type['value']


def select_bodystyle(bodystyle):
    """Select bodystyle from available bodystyles."""
    if bodystyle is not None:
        for ve_bstyle in bodystyles_list:
            if str(ve_bstyle['name']) == bodystyle:
                return ve_bstyle['value']


def select_mark(mark):
    """Select mark from available marks."""
    for ve_mark in marks_list:
        if str(ve_mark['name']) == mark:
            return ve_mark['value']


def select_model(model):
    """Select model from available models."""
    for ve_model in models_list:
        if str(ve_model['name']) == model:
            return ve_model['value']


def select_state(state):
    """Select states from available states."""
    for ve_state in states_list:
        if fnmatch(ve_state['name'], '*' + state + '*'):
            return ve_state['value']


def compose_parameters():
    """Compose parameters for GET request."""
    params_dict = {}
    years_list = []
    global PARAMS
    params_dict['main_category'] = category_auto
    params_dict['marka_id'] = mark
    params_dict['model_id'] = model
    if VEHICLE_YEAR_START is not None and VEHICLE_YEAR_END is not None:
        years_list.append(VEHICLE_YEAR_START)
        years_list.append(VEHICLE_YEAR_END)
    elif VEHICLE_YEAR_END is not None:
        years_list.append(VEHICLE_YEAR_END)
    else:
        years_list.append(VEHICLE_YEAR_START)
    params_dict['yers'] = years_list
    if VEHICLE_BODY is not None:
        params_dict['body_id'] = bodystyle
    if VEHICLE_REGION is not None:
        params_dict['state_id'] = state
    return params_dict

"""
    The following parameters are not in use right now.
    Are to be added.
    'gear_type': 'gear_id',
    'fuel': 'fuel_id',
    'drive': 'drive_id',
    'engine': 'engineVolume',
    'options': 'options',
    'mileage': 'raceInt',
    'doors': 'door',
    'state': 'state_id',
    'city': 'city_id',
    'carrying': 'carrying',
    'seats': 'seats',
    'color': 'color_id',
    'custom': 'custom',
    'damage': 'damage',
    'credit': 'under_credit',
    'confiscated': 'confiscated_car',
    'on_repairment': 'onRepairParts',
"""
# Getting types and selecting one relying on search parameters
types_list = get_types()
category_auto = select_type(VEHICLE_TYPE)
# Getting bodystyles and selecting one relying on search parameters
bodystyles_list = get_bodystyles(category_auto)
bodystyle = select_bodystyle(VEHICLE_BODY)
# Getting marks list and selecting one relying on search parameters
marks_list = get_marks(category_auto)
mark = select_mark(VEHICLE_MARK)
# Getting models list and selecting one relying on search parameters
models_list = get_models(category_auto, mark)
model = select_model(VEHICLE_MODEL)
# Getting states list and selecting one relying on search parameters
states_list = get_states()
state = select_state(VEHICLE_REGION)

url = 'http://api.auto.ria.com/average'
# Composing parameters
params = compose_parameters()
# Senging GET request
response = requests.get(url, params=params)
# Formatiing response into JSON for convenience
average = json.loads(response.text)
pprint(params)
print(response.url)
pprint(average)
