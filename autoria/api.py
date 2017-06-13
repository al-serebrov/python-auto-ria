"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""


import requests
import json
from fnmatch import fnmatch
from typing import Any, Dict, List, Optional


class RiaAPI:
    """Python auto.ria.com API.

    This class contains methods to work with auto.ria.com API:
    get categories, bodystyles, states etc. lists with identifiers,
    send a request to calculate average price
    """

    def __init__(self):
        """Constructor."""
        self._api_url = 'http://api.auto.ria.com{method}'

    def _make_request(
            self, url: str, parameters: dict = None) -> Any:
        """Send get request and return data in JSON.

        Args:
            url - url returning needed data
            parameters - request GET parameters (if any)

        Returns:
            List of dictionaries with response text.
        """
        req_url = self._api_url.format(method=url)
        response = requests.get(url=req_url, params=parameters)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(
                'Error making a request to: {}, response: {}, {}'
                .format(url, response.status_code, response.text))

    def get_categories(self) -> List[Dict[str, Any]]:
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

    def get_bodystyles(self, category: int) -> List[Dict[str, Any]]:
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

    def get_marks(self, category: int) -> List[Any]:
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

    def get_models(self, category: int, mark: int) -> List[Dict[str, Any]]:
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

    def get_states(self) -> List[Dict[str, Any]]:
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

    def get_cities(self, state: int) -> List[Dict[str, Any]]:
        """Get the list of cities for selected state.

        Args:
            state - identifier with selected state id.

        Returns:
            The list of dictionaries with cities of the selected
            state. E.g. if we pass 1 (Vinnitsa state) the result is:
            [
                {
                name: "Винница",
                value: 1
                },
                {
                name: "Жмеринка",
                value: 27
                },
                ...
            ]
        """
        url = '/states/{}/cities'.format(str(state))
        return self._make_request(url)

    def get_gearboxes(self, category: int) -> List[Dict[str, Any]]:
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

    def get_driver_types(self, category: int) -> List[Dict[str, Any]]:
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
        url = '/categories/{}/driverTypes'.format(category)
        return self._make_request(url)

    def get_fuels(self) -> List[Dict[str, Any]]:
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

    def get_options(self, category: int) -> List[Dict[str, Any]]:
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

    def get_colors(self) -> List[Dict[str, Any]]:
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

    def average_price(self, parameters: dict) -> dict:
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

    def __init__(self, category: str, mark: str, model: str, **kwargs) -> None:
        """Constructor.

        Compose parameters for GET request to auro.ria.com API.
        Acceps the following search parameters.

        Args:
            category - vehicle type, e.g. ''Легковые''
            mark - mark, like ''Renault''
            model - model, like ''Scenic''
        All following args are optional:
            bodystyle - bodystyle, e.g. ''Седан''
            year - list with start and end manufacturing year,
                   e.g. ''[2005, 2006]'', also one of years could be
                   ''None'', e.g. ''[2005, None]''
            state - state, e.g. ''Харьковская''
            city - city inside of state, e.g. ''Харьков'', if
                the state is not selected (state=None), city won't be
                selected too, and won't have any influence on search results
            gears - list with gearshift types,
                        e.g. ['Ручная', 'Автомат']
            opts - list with neede options, like
                ['ABS', 'ABD']
            mileage - list with start and end mileage, e.g.:
                [10, 100]
            fuels - list with gasoline types,
                    e.g. ''[Бензин, Газ/Бензин]''
            drives - list with drive types,
                    e.g. ''[Передний, Полный]''
            color - car color like ''Бежевый''
            engineVolume - e.g. 1.5
            seats - quantity of seats, e.g. 5
            doors - quantity of doors, e.g. 3
            carrying - how much is the car able to carry, e.g. 1500
            custom - is custom clearance needed for the car? 1 - YES, 0 - NO
            damage - is the car damaged in car accident? 1 - YES, 0 - NO
            credit - is the car under credit? 1 - YES, 0 - NO
            confiscated - is the car confiscated? 1 - YES, 0 - NO
            on_repair_parts - is the car is broken? 1 - YES, 0 - NO
        """
        # Init all the parameters.
        self._category_id = None
        self._mark_id = None
        self._model_id = None
        self._state_id = None
        self._body_id = None
        self._city_id = None
        self._years = None
        self._mileage = None
        self._gear_id = None
        self._options = None
        self._fuel_id = None
        self._drive_id = None
        self._color_id = None
        self._engine_volume = None
        self._seats = None
        self._doors = None
        self._carrying = None
        self._custom = None
        self._damage = None
        self._under_credit = None
        self._confiscated = None
        self._on_repair_parts = None

        # Create API client.
        self._api = RiaAPI()

        # Processing required arguments: category, mark, model.
        # Getting the list of categories and selecting needed id.
        self._category(category)
        # Getting the list of marks and selecting needed id
        self._mark(mark)
        # Getting the list of models and selecting neede id
        self._model(model)

        # Processing optional arguments.
        state = None
        city = None
        for key in kwargs:
            # To shorten the code we call the setter method by name,
            # this is same as if we did this:
            #
            # for key in kwargs:
            #     if key == 'state':
            #         self.state(kwargs['state'])
            #     if key == 'bodystyle':
            #         self.bodystyle(kwargs['bodystyle'])
            #      ... and so on
            if not hasattr(self, key):
                raise Exception('Unknown parameter: {}'.format(key))
            # We have special handling for state and city as we need to
            # process them together.
            if key == 'state':
                state = kwargs['state']
            elif key == 'city':
                city = kwargs['city']
            else:
                getattr(self, key)(kwargs[key])

        if state and city:
            self.city(state, city)
        elif state:
            self.state(state)

    def get_average(self) -> dict:
        """Get average price for composed search parameters."""
        return self._api.average_price(self.as_dict())

    def _category(self, category):
        """Set category.

        The method is private because category is a required constructor parameter.
        """
        self._category_id = select_item(category, self._api.get_categories())

    def _mark(self, mark):
        """Set mark.

        The method is private because mark is a required constructor parameter.
        """
        self._mark_id = select_item(
            mark, self._api.get_marks(self._category_id))

    def _model(self, model):
        """Set model.

        The method is private because model is a required constructor parameter.
        """
        self._model_id = select_item(
            model,
            self._api.get_models(self._category_id, self._mark_id)
        )

    def bodystyle(self, bodystyle):
        """Set bodystyle."""
        self._body_id = select_item(
            bodystyle,
            self._api.get_bodystyles(self._category_id)
        )
        return self

    def state(self, state):
        """Set state."""
        self._state_id = select_item(state, self._api.get_states())

    def city(self, state, city):
        """Set state and city."""
        self.state(state)
        self._city_id = select_item(
            city,
            self._api.get_cities(self._state_id)
        )
        return self

    def gears(self, gears):
        """Set gears."""
        self._gear_id = select_list(
            gears,
            self._api.get_gearboxes(self._category_id)
        )
        return self

    def opts(self, opts):
        """Set opts."""
        self._options = select_list(
            opts,
            self._api.get_options(self._category_id)
        )
        return self

    def fuels(self, fuels):
        """Set fuels."""
        self._fuel_id = select_list(fuels, self._api.get_fuels())
        return self

    def drives(self, drives):
        """Set drives."""
        self._drive_id = select_list(
            drives,
            self._api.get_driver_types(self._category_id)
        )
        return self

    def color(self, color):
        """Set color."""
        self._color_id = select_item(
            color,
            self._api.get_colors()
        )
        return self

    def as_dict(self):
        return {
            'main_category': self._category_id,
            'marka_id': self._mark_id,
            'model_id': self._model_id,
            'state_id': self._state_id,
            'body_id': self._body_id,
            'city_id': self._city_id,
            'yers': self._years,
            'raceInt': self._mileage,
            'gear_id': self._gear_id,
            'options': self._options,
            'fuel_id': self._fuel_id,
            'drive_id': self._drive_id,
            'color_id': self._color_id,
            'engineVolume': self._engine_volume,
            'seats': self._seats,
            'door': self._doors,
            'carrying': self._carrying,
            'custom': self._custom,
            'damage': self._damage,
            'under_credit': self._under_credit,
            'confiscated_car': self._confiscated,
            'onRepairParts': self._on_repair_parts
        }


def select_item(item_to_select: str, items_list: list) -> Optional[int]:
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
                if fnmatch(item['name'], item_to_select):
                    return item['value']
            for item in items_list:
                if fnmatch(item['name'], '{}*'.format(item_to_select)):
                    return item['value']
            for item in items_list:
                if fnmatch(item['name'], '*{}*'.format(item_to_select)):
                    return item['value']


def select_list(list_to_select: list, items_list: list) -> Optional[list]:
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
