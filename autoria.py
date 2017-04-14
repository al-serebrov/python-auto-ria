"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""


import requests
import json
from fnmatch import fnmatch


def jsonify_response(url):
    """Send get request and return data in JSON."""
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)


def get_categories():
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


def select_item(item_to_select, items_list):
    """Select vehicle type, bodystyle, mark, model from the given list."""
    if item_to_select is not None and items_list is not None:
        for item in items_list:
            if fnmatch(item['name'], '*' + item_to_select + '*'):
                return item['value']
    else:
        return None


def compose_parameters(search_parameters):
    """Compose parameters for GET request."""
    params_dict = {}
    years_list = []

    categories_list = get_categories()
    category = select_item(search_parameters['VEHICLE_TYPE'], categories_list)
    params_dict['main_category'] = category

    bodystyles_list = get_bodystyles(category)
    bodystyle = select_item(search_parameters['VEHICLE_BODY'], bodystyles_list)
    params_dict['body_id'] = bodystyle

    marks_list = get_marks(category)
    mark = select_item(search_parameters['VEHICLE_MARK'], marks_list)
    params_dict['marka_id'] = mark

    models_list = get_models(category, mark)
    model = select_item(search_parameters['VEHICLE_MODEL'], models_list)
    params_dict['model_id'] = model

    states_list = get_states()
    state = select_item(search_parameters['VEHICLE_REGION'], states_list)
    params_dict['state_id'] = state

    vehicle_year_start = search_parameters['VEHICLE_YEAR_START']
    vehicle_year_end = search_parameters['VEHICLE_YEAR_END']
    years_list.append(vehicle_year_start)
    years_list.append(vehicle_year_end)
    params_dict['yers'] = years_list

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


def get_average(search_parameters):
    """Get average price using search parameters.

    Returns processed search parameters, generated url,
    and JSON response from the server
    """
    url = 'http://api.auto.ria.com/average'
    # Composing parameters
    params = compose_parameters(search_parameters)
    # Senging GET request
    response = requests.get(url, params=params)
    # Formatiing response into JSON for convenience
    average = json.loads(response.text)
    return [params, response.url, average]
