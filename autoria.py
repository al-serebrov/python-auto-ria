"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""


import requests
import json
from fnmatch import fnmatch
from typing import Union


class RiaAPI:
    """Python auto.ria.com API.

    This class contains methods to work with auto.ria.com API:
    get categories, bodystyles, states etc. lists with identifiers,
    send a request to calculate average price
    """

    def __init__(self):
        """Constructor."""
        self._base_url = 'http://api.auto.ria.com'

    def _make_request(self, url: str, parameters: dict = None) \
            -> Union[dict, list]:
        """Send get request and return data in JSON.

        Args:
            url - url returning needed data
            parameters - request GET parameters (if any)

        Returns:
            Dictionary with response text.
        """
        req_url = self._base_url + url
        response = requests.get(url=req_url, params=parameters)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(
                'Error making a request to: {}, response: {}, {}'
                .format(url, response.status_code, response.text))

    def get_categories(self) -> Union[dict, list]:
        """Get available vehicle types from auto.ria.com.

        Returns:
            The list of dictionaries with categories like:
            [
                {
                "name": "Легковые",
                "value": 1
                },
                ...
            ]
        """
        return self._make_request('/categories')

    def get_bodystyles(self, category: int) -> Union[dict, list]:
        """Get available bodystyles from auto.ria.com.

        Args:
            category - needed category id.
        Returns:
            The list of dictionaries with bodystyle information like:
            [
                {
                "name": "Седан",
                "value": 3
                },
                ...
            ]
        """
        url = '/categories/{}/bodystyles'.format(str(category))
        return self._make_request(url)

    def get_marks(self, category: int) -> Union[dict, list]:
        """Get available car marks from auto.ria.com.

        Args:
            category - needed category id.

        Returns:
            The list of dictionaries with marks information like:
            [
                {
                "name": "Acura",
                "value": 98
                },
                ...
            ]
        """
        url = '/categories/{}/marks'.format(str(category))
        return self._make_request(url)

    def get_models(self, category: int, mark: int) -> Union[dict, list]:
        """Get available models for selected mark from auto.ria.com.

        Args:
            category - needed category id.
            mark - needed mark id (since we're getting models of the mark)

        Returns:
            The list of dictionaries with models like:
            [
                {
                "name": "CL",
                "value": 953
                },
                ...
            ]
        """
        url = '/categories/{}/marks/{}/models'.format(str(category), str(mark))
        return self._make_request(url)

    def get_states(self) -> Union[dict, list]:
        """Get available states from auto.ria.com.

        Returns:
            The list of dictionaries with states like:
            [
                {
                "name": "Винницкая",
                "value": 1
                },
                ...
            ]
        """
        return self._make_request('/states')

    def get_gearboxes(self, category):
        """Get available gearbox types from auto.ria.com.

        Args:
            category - needed category id

        Returns:
            The list of dictionaries with gearboxes like:
            [
                {
                name: "Ручная / Механика",
                value: 1
                },
                ...
            ]
        """
        url = '/categories/{}/gearboxes'.format(str(category))
        return self._make_request(url)

    def get_driver_types(self, category):
        """Get available drive types from auto.ria.com.

        Args:
            category - needed category id.

        Returns:
            The list of dictionaries with drive types like:
            [
                {
                name: "Кардан",
                value: 4
                },
            ...
            ]

        """
        url = '/categories/{}/driverTypes'
        return self._make_request(url)

    def get_fuels(self):
        """Get available fuel types from auto.ria.com.

        Returns:
            The list of dictionaries with fuel types like:
            [
                {
                name: "Бензин",
                value: 1
                },
                ...
            ]
        """
        return self._make_request('/fuels')

    def get_options(self, category):
        """Get available options from auto.ria.com.

        Args:
            category - needed category id.

        Returns:
            The list of dictionaries with options like:
            [
                {
                name: "ABD",
                value: 354
                },
                ...
            ]
        """
        url = '/categories/{}/options'.format(str(category))
        return self._make_request(url)

    def get_colors(self):
        """Get available colors from auto.ria.com.

        Returns:
            The list of dictionaries with colors like:
            [
                {
                name: "Бежевый",
                value: 1
                },
                ...
            ]
        """
        return self._make_request('/colors')

    def average_price(self, parameters: dict) -> Union[dict, list]:
        """Make an API request for average price.

        Args:
            parametrs - search parameters, composed by
            RiaAverageCarPrice class, see help and the list
            of parameters there.

         Returns:
                Python dictionary with data as described here:
                https://goo.gl/WVCVi8
                An example:
                {'arithmeticMean': 6142.471428571429,
                 'classifieds': [19365865,
                                 17441252,
                                 ...
                                 ],
                 'interQuartileMean': 6749.941176470588,
                 'percentiles': {'1.0': 2591.3759999999997,
                                 '5.0': 2735,
                                 ...
                                 '99.0': 8236.5},
                 'prices': [3300,
                            3500,
                            ...],
                 'total': 28}
        """
        return self._make_request('/average', parameters)


class RiaAverageCarPrice:
    """Compose search parameters and get an average price.

    Search parametrs are composed during instance initialization,
    the request for average price is sent using RiaAPI class.
    """

    def __init__(self, category: str, mark: str, model: str,
                 bodystyle: str = None, years: list = None,
                 state: str = None, gears: list = None,
                 opts: list = None) -> Union[dict, list]:
        """Constructor.

        Compose parameters for GET request to auro.ria.com API.
        Acceps the following search parameters.

        Args:
            category - vehicle type, e.g. ''Легковые''
            mark - mark, like ''Renault''
            model - model, like ''Scenic''
            bodystyle - (optional) bodystyle, e.g. ''Седан''
            year - (optional) list with start and end manufacturing year,
                   e.g. ''[2005, 2006]'', also one of years could be
                   ''None'', e.g. ''[2005, None]''
                <== note: make this parameter behave like on auto.ria:
                if there's only start year end=current_year,
                vice versa - start=1950==>
            state - (optional) state (city), e.g. ''Харьков''
            gear_id - (optional) list with gearshift types,
                        e.g. ['Ручная', 'Автомат']

        The following search parameters are not in use right now.
        Are to be added.
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
        """
        self._api = RiaAPI()
        self._params = {}

        # Getting list of categories and selecting needed id
        categories_list = self._api.get_categories()
        selected_category = select_item(category, categories_list)
        self._params['main_category'] = selected_category

        # Getting list of bodysyles and selecting needed id
        bodystyles_list = self._api.get_bodystyles(selected_category)
        self._params['body_id'] = select_item(bodystyle, bodystyles_list)

        # Getting list of marks and selecting needed id
        marks_list = self._api.get_marks(selected_category)
        selected_mark = select_item(mark, marks_list)
        self._params['marka_id'] = selected_mark

        # Getting list of models and selecting needed id
        models_list = self._api.get_models(selected_category, selected_mark)
        self._params['model_id'] = select_item(model, models_list)

        # Getting list of states and selecting needed id
        states_list = self._api.get_states()
        self._params['state_id'] = select_item(state, states_list)

        # Creating a list from start and end years
        self._params['yers'] = years

        # Creating a list of gearbox ids
        gearboxes = self._api.get_gearboxes(selected_category)
        self._params['gear_id'] = select_list(gears, gearboxes)

        # Creatin a list of option ids
        options = self._api.get_options(selected_category)
        self._params['options'] = select_list(opts, options)

    def get_average(self) -> Union[dict, list]:
        """Get average price for composed search parameters."""
        return self._api.average_price(self._params)


def select_item(item_to_select: str, items_list: dict) -> int:
        """Select vehicle type, bodystyle, mark, model from the given list.

        This function is intended to convert human-readable search
        parameter, for instance, ''Винница'' into API-understandable
        state identifier, for the given example it would be 1.

        Args:
            item_to_select - could be not 100% accurate as it is in the
                auto.ria.ua lists, e.g. value ''Харьков'' is acceptable,
                because the parameter is wild-carded in comprasion like
                ''*Харьков*'', the function will find suitable name
                ''Харьковская'' and will return its id.
            items_list - JSON-formatted list of pairs ''name: value'',
                    obtained from one of the ''get_'' functions.

        Returns:
            needed item (category, bodystyle, mark etc.) identifyer.
        """
        if item_to_select is not None and items_list is not None:
            for item in items_list:
                if fnmatch(item['name'], '*' + item_to_select + '*'):
                    return item['value']
        else:
            return None


def select_list(list_to_select: list, items_list: dict) -> list:
    """Select a list of ids in the list of dictionaries.

    The function is intended to select a list of options inside
    the list of dictionaries returned by any ''get_'' method of
    RiaAPI.
    For example, we have:
        gears=['Ручная / Механика', 'Автомат']
    as a search parameter, we need to:
    1. Get a list of dictionaries (happens not in this function)
    2. Define ids of provided options (happens right here)

    Args:
        list_to_select - a list of options to select, for instance,
                ['Ручная / Механика', 'Автомат']
        items_list - list of dictionaries with option names and ids,
        for example:
            [
                {
                name: "Ручная / Механика",
                value: 1
                },
                ...
            ]

    Returns:
        The list of ids, ready-to-use in other methods, for example:
            [1, 2]
    """
    if list_to_select is not None:
        selected_list = []
        for item in list_to_select:
            selected_item = select_item(item, items_list)
            selected_list.append(selected_item)
        return selected_list
