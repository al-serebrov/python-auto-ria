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


def get_average(category, mark, model, bodystyle=None,
                year_start=None, year_end=None, state=None):
    """Compose parameters for GET request."""
    """Get average price using search parameters.

    Returns processed search parameters, generated url,
    and JSON response from the server
    """
    params_dict = {}
    years_list = []

    categories_list = get_categories()
    selected_category = select_item(category, categories_list)
    params_dict['main_category'] = selected_category

    bodystyles_list = get_bodystyles(selected_category)
    selected_bodystyle = select_item(bodystyle, bodystyles_list)
    params_dict['body_id'] = selected_bodystyle

    marks_list = get_marks(selected_category)
    selected_mark = select_item(mark, marks_list)
    params_dict['marka_id'] = selected_mark

    models_list = get_models(selected_category, selected_mark)
    selected_model = select_item(model, models_list)
    params_dict['model_id'] = selected_model

    states_list = get_states()
    selected_state = select_item(state, states_list)
    params_dict['state_id'] = selected_state

    years_list.append(year_start)
    years_list.append(year_end)
    params_dict['yers'] = years_list

    url = 'http://api.auto.ria.com/average'
    # Senging GET request
    response = requests.get(url, params=params_dict)
    # Formatiing response into JSON for convenience
    average = json.loads(response.text)
    return [params_dict, response.url, average]

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
