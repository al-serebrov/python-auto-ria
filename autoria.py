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

    Python implementation of API intended for calulating
    average used car prices that are sold on http://auto.ria.com
    """

    def __init__(self):
        """Initialize a class."""
        self._base_url = 'http://api.auto.ria.com'

    def _make_request(self, url: str) -> Union[dict, list]:
        """Send get request and return data in JSON.

        Args:
            url - url returning needed data

        Returns:
            JSON-formatted response text.
        """
        response = requests.get(self._base_url + url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print('Ups! Something went wrong in processing of {}'.format(url))

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

    def select_item(self, item_to_select: str, items_list: dict) -> int:
        """Select vehicle type, bodystyle, mark, model from the given list.

        This function is intended to convert human-readable search parameter,
        for instance, ''Винница'' into API-understandable state identifier,
        for the given example it would be 1.

        Args:
            item_to_select - string, could be not 100% accurate as it is in the
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

    def get_average(self, category: str, mark: str, model: str,
                    bodystyle: str = None, years: list = None,
                    state: str = None) -> Union[dict, list]:
        """Compose parameters for GET request and send it.

        Get average price using search parameters.

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


            Returns:
                JSON-formatted output with data as described here:
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
        params_dict = {}

        # Getting list of categories and selecting needed id
        categories_list = self.get_categories()
        selected_category = self.select_item(category, categories_list)
        params_dict['main_category'] = selected_category

        # Getting list of bodysyles and selecting needed id
        bodystyles_list = self.get_bodystyles(selected_category)
        selected_bodystyle = self.select_item(bodystyle, bodystyles_list)
        params_dict['body_id'] = selected_bodystyle

        # Getting list of marks and selecting needed id
        marks_list = self.get_marks(selected_category)
        selected_mark = self.select_item(mark, marks_list)
        params_dict['marka_id'] = selected_mark

        # Getting list of models and selecting needed id
        models_list = self.get_models(selected_category, selected_mark)
        selected_model = self.select_item(model, models_list)
        params_dict['model_id'] = selected_model

        # Getting list of states and selecting needed id
        states_list = self.get_states()
        selected_state = self.select_item(state, states_list)
        params_dict['state_id'] = selected_state

        # Creting a list from start and end years
        params_dict['yers'] = years

        # Getting average price
        url = 'http://api.auto.ria.com/average'
        # Senging GET request
        response = requests.get(url, params=params_dict)
        # Formatiing response into JSON for convenience
        average = json.loads(response.text)
        print('{}\n{}'.format(params_dict, response.url))
        return average
