"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""


import requests
import json
# from fnmatch import fnmatch
from typing import Any, Dict, List
from collections import namedtuple
from .utils import select_item, select_list


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


RiaAverageCarPriceParams = namedtuple('RiaAverageCarPriceParams', [
    'main_category',
    'marka_id',
    'model_id',
    'state_id',
    'body_id',
    'city_id',
    'yers',
    'raceInt',
    'gear_id',
    'options',
    'fuel_id',
    'drive_id',
    'color_id',
    'engineVolume',
    'seats',
    'door',
    'carrying',
    'custom',
    'damage',
    'under_credit',
    'confiscated_car',
    'onRepairParts',
])


class RiaAverageCarPrice:
    """Compose search parameters and get an average price.

    Search parametrs are composed during instance initialization,
    the request for average price is sent using RiaAPI class.
    """

    def __init__(self, category: str, mark: str, model: str,
                 bodystyle: str = None, years: list = None,
                 state: str = None, city: str = None,
                 gears: list = None, opts: list = None,
                 mileage: list = None, fuels: list = None,
                 drives: list = None, color: str = None,
                 engine_volume: float = None,
                 seats: int = None, doors: int = None,
                 carrying: int = None, custom: bool = False,
                 damage: bool = False, under_credit: bool = False,
                 confiscated: bool = False, on_repair_parts: bool = False
                 ) -> None:
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
            custom - is custom clearance needed for the car?
            damage - is the car damaged in car accident?
            credit - is the car under credit?
            confiscated - is the car confiscated?
            on_repair_parts - is the car is broken?
        """
        self._api = RiaAPI()
        # Processing required args
        # Getting the list of categories and selecting needed id
        category_id = select_item(category, self._api.get_categories())
        # Getting the list of marks and selecting needed id
        mark_id = select_item(mark, self._api.get_marks(category_id))
        # Getting the list of models and selecting neede id
        model_id = select_item(
            model,
            self._api.get_models(category_id, mark_id)
        )

        # Processing the rest of args, those which are defaulted to None
        # are processed below
        self._params = RiaAverageCarPriceParams(
            main_category=category_id,
            marka_id=mark_id,
            model_id=model_id,
            state_id=None,
            body_id=None,
            city_id=None,
            yers=years,
            raceInt=mileage,
            gear_id=None,
            options=None,
            fuel_id=None,
            drive_id=None,
            color_id=None,
            engineVolume=engine_volume,
            seats=seats,
            door=doors,
            carrying=carrying,
            custom=custom,
            damage=damage,
            under_credit=under_credit,
            confiscated_car=confiscated,
            onRepairParts=on_repair_parts,
        )

        if state is not None:
            # state_id variable is needed below, whice selecting a city
            state_id = select_item(state, self._api.get_states())
            self._params = self._params._replace(state_id=state_id)

        if bodystyle is not None:
            self._params = self._params._replace(body_id=select_item(
                bodystyle,
                self._api.get_bodystyles(category_id)
            ))

        if city is not None and state is not None:
            self._params = self._params._replace(city_id=select_item(
                city,
                self._api.get_cities(state_id)
            ))

        if gears is not None:
            self._params = self._params._replace(gear_id=select_list(
                gears,
                self._api.get_gearboxes(category_id)
            ))

        if opts is not None:
            self._params = self._params._replace(options=select_list(
                opts,
                self._api.get_options(category_id)
            ))

        if fuels is not None:
            self._params = self._params._replace(fuel_id=select_list(
                fuels, self._api.get_fuels()
            ))

        if drives is not None:
            self._params = self._params._replace(drive_id=select_list(
                drives,
                self._api.get_driver_types(category_id)
            ))

        if color is not None:
            self._params = self._params._replace(color_id=select_item(
                color,
                self._api.get_colors()
            ))

    def get_average(self) -> dict:
        """Get average price for composed search parameters."""
        return self._api.average_price(self._params._asdict())



