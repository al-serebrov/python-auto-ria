"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""


import requests
import json
from fnmatch import fnmatch


def make_request(url: str) -> json:
    """Send get request and return data in JSON.

    Args:
        url - string with url returning needed
        data (categories, bodystyles etc.)

    Returns:
        JSON-formatted response text.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print('Ups! Something went wrong in processing of {}'.format(url))


def get_categories() -> json:
    """Get available vehicle types from auto.ria.com.

    No args needed because the list has fixed url.

    Returns:
        JSON-formatted list of pairs ''name: value'' like:
        [
            {
            "name": "Легковые",
            "value": 1
            },
            ...
        ]
    """
    url = 'http://api.auto.ria.com/categories'
    return make_request(url)


def get_bodystyles(category: int) -> json:
    """Get available bodystyles from auto.ria.com.

    Args:
        category - integer with needed category id.
    Returns:
        JSON-formatted list of pairs ''name: value'' like:
        [
            {
            "name": "Седан",
            "value": 3
            },
            ...
        ]
    """
    url = 'http://api.auto.ria.com/categories/{}/bodystyles' \
          .format(str(category))
    return make_request(url)


def get_marks(category: int) -> json:
    """Get available car marks from auto.ria.com.

    Args:
        category - integer with needed category id.

    Returns:
        JSON-formatted list of pairs ''name: value'' like:
        [
            {
            "name": "Acura",
            "value": 98
            },
            ...
        ]
    """
    url = 'http://api.auto.ria.com/categories/{}/marks' \
          .format(str(category))
    return make_request(url)


def get_models(category: int, mark: int) -> json:
    """Get available models for selected mark from auto.ria.com.

    Args:
        category - integer with needed category id.
        mark - integer with needed mark id
            (since we're getting models of the mark)

    Returns:
        JSON-formatted list of pairs ''name: value'' like:
        [
            {
            "name": "CL",
            "value": 953
            },
            ...
        ]
    """
    url = 'http://api.auto.ria.com/categories/{}/marks/{}/models' \
          .format(str(category), str(mark))
    return make_request(url)


def get_states() -> json:
    """Get available states from auto.ria.com.

    Args aren't needed because the url is fixed.

    Returns:
        JSON-formatted list of pair ''name: value'' like:
        [
            {
            "name": "Винницкая",
            "value": 1
            },
            ...
        ]
    """
    url = 'http://api.auto.ria.com/states'
    return make_request(url)


def select_item(item_to_select: str, items_list: json) -> int:
    """Select vehicle type, bodystyle, mark, model from the given list.

    This function is intended to convert human-readable search parameter,
    for instance, ''Винница'' into API-understandable state identifier,
    for the given example it would be 1.

    Args:
        item_to_select - string, could be not 100% accurate as it is in the
            auto.ria.ua lists, e.g. value ''Харьков'' is acceptable,
            because the parameter is wildcarted in comprasion like
            ''*Харьков*'', the function will find suitable name
            ''Харьковская'' and will return its id.
        items_list - JSON-formatted list of pairs ''name: value'',
                obtained from one of the ''get_'' functions.

    Returns:
        integer with needed item (category, bodystyle, mark etc.) identifyer.
    """
    if item_to_select is not None and items_list is not None:
        for item in items_list:
            if fnmatch(item['name'], '*' + item_to_select + '*'):
                return item['value']
    else:
        return None


def get_average(category: str, mark: str, model: str, bodystyle: str = None,
                years_start_end: list = None, state: str = None) -> json:
    """Compose parameters for GET request and send it.

    Get average price using search parameters.

    Args:
        category - (required) string with vehicle type,
                   e.g. ''Легковые''
        mark - (required) string with mark, like ''Renault''
        model - (requred) sting with model, like ''Scenic''
        bodystyle - (optional) string with bodystyle, e.g. ''Седан''
        year_start_end - (optional) list with start and end mfr year,
                        e.g. ''[2005, 2006]'', also one of years could be
                        ''None'', e.g. ''[2005, None]''
            <== note: make this parameter behave like on auto.ria: if there's
            only start year end=current_year, vice versa - start=1950==>
        state - (optional) string with state (city), e.g. ''Харьков''
        ******************************************************************
        The following search parameters are not in use right now.
        Are to be added.
        gear_type - (optional) list with gearshift types,
                    e.g. ''[Механическая, Автоматическая]''
        fuel - (optional) list with gasoline types,
                e.g. ''[Бензин, Газ/Бензин]''
        drive - (optional) list with drive types,
                e.g. ''[Передний, Полный]''
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
        ******************************************************************

        Returns:
            JSON-formatted output with data as described here:
            https://goo.gl/WVCVi8
    """
    params_dict = {}

    # Getting list of categories and selecting needed id
    categories_list = get_categories()
    selected_category = select_item(category, categories_list)
    params_dict['main_category'] = selected_category

    # Getting list of bodysyles and selecting needed id
    bodystyles_list = get_bodystyles(selected_category)
    selected_bodystyle = select_item(bodystyle, bodystyles_list)
    params_dict['body_id'] = selected_bodystyle

    # Getting list of marks and selecting needed id
    marks_list = get_marks(selected_category)
    selected_mark = select_item(mark, marks_list)
    params_dict['marka_id'] = selected_mark

    # Getting list of models and selecting needed id
    models_list = get_models(selected_category, selected_mark)
    selected_model = select_item(model, models_list)
    params_dict['model_id'] = selected_model

    # Getting list of states and selecting needed id
    states_list = get_states()
    selected_state = select_item(state, states_list)
    params_dict['state_id'] = selected_state

    # Creting a list from start and end years
    params_dict['yers'] = years_start_end

    # Getting average price
    url = 'http://api.auto.ria.com/average'
    # Senging GET request
    response = requests.get(url, params=params_dict)
    # Formatiing response into JSON for convenience
    average = json.loads(response.text)
    return [params_dict, response.url, average]
