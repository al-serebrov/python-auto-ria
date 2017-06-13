"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""


import requests
import json
from collections import OrderedDict
from fnmatch import fnmatch
from typing import Any, Dict, List


class RiaAPI:
    """Python auto.ria.com API.

    This class contains methods to work with auto.ria.com API:
    get categories, bodystyles, states etc. lists with identifiers,
    send a request to calculate average price
    """

    def __init__(self):
        """Constructor."""
        self._api_url = 'http://api.auto.ria.com{method}'
        self._params = {
            'CATEGORY': 'main_category',
            'MARK': 'marka_id',
            'MODEL': 'model_id',
            'STATE': 'state_id',
            'BODY': 'body_id',
            'CITY': 'city_id',
            'YEARS': 'yers',
            'MILEAGE': 'race_int',
            'GEAR': 'gear_id',
            'OPTIONS': 'options',
            'FUEL': 'fuel_id',
            'DRIVE': 'drive_id',
            'COLOR': 'color_id',
            'ENGINEVOLUME': 'engineVolume',
            'SEATS': 'seats',
            'DOOR': 'door',
            'CARRYING': 'carrying',
            'CUSTOM': 'custom',
            'DAMAGE': 'damage',
            'CREDIT': 'under_credit',
            'CONFISCATED': 'confiscated_car',
            'REPAIR': 'onRepairParts'
        }

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

    def get_params(self) -> Dict:
        """Get Auto RIA API parameter names from constants.

        Returns:
            Ready to use dictionary with API parameters.
        """
        return self._params

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

    def __init__(self, category: str, mark: str, model: str,
                 bodystyle: str = None, years: list = None,
                 state: str = None, city: str = None,
                 gears: list = None, opts: list = None,
                 mileage: list = None, fuels: list = None,
                 drives: list = None, color: str = None,
                 engine_volume: float = None,
                 seats: int = None, doors: int = None,
                 carrying: int = None, custom: int = None,
                 damage: int = None, under_credit: int = None,
                 confiscated: int = None, on_repair_parts: int = None
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
            custom - is custom clearance needed for the car? 1 - YES, 0 - NO
            damage - is the car damaged in car accident? 1 - YES, 0 - NO
            credit - is the car under credit? 1 - YES, 0 - NO
            confiscated - is the car confiscated? 1 - YES, 0 - NO
            on_repair_parts - is the car is broken? 1 - YES, 0 - NO
        """
        self._api = RiaAPI()

        self._api_params = self._api.get_params()

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
        # Processing the rest of args

        if state is not None:
            # state_id variable is needed below, whice selecting a city
            state_id = select_item(state, self._api.get_states())
        else:
            state_id = None

        if bodystyle is not None:
            bodystyle_id = select_item(
                bodystyle,
                self._api.get_bodystyles(category_id)
            )
        else:
            bodystyle_id = None

        if city is not None and state is not None:
            city_id = select_item(
                city,
                self._api.get_cities(state_id)
            )
        else:
            city_id = None

        if gears is not None:
            gear_id = select_list(
                gears,
                self._api.get_gearboxes(category_id)
            )
        else:
            gear_id = None

        if opts is not None:
            options_id = select_list(
                opts,
                self._api.get_options(category_id)
            )
        else:
            options_id = None

        if fuels is not None:
            fuel_id = select_list(fuels, self._api.get_fuels())
        else:
            fuel_id = None

        if drives is not None:
            drive_id = select_list(
                drives,
                self._api.get_driver_types(category_id)
            )
        else:
            drive_id = None

        if color is not None:
            color_id = select_item(
                color,
                self._api.get_colors()
            )
        else:
            color_id = None

        self._params = self.assign_parameters_to_dict(
            api_params=self._api_params, category=category_id,
            mark=mark_id, model=model_id, bodystyle=bodystyle_id, years=years,
            state=state_id, city=city_id, gears=gear_id, opts=options_id,
            mileage=mileage, fuels=fuel_id, drives=drive_id, color=color_id,
            engine_volume=engine_volume, seats=seats, doors=doors,
            carrying=carrying, custom=custom, damage=damage,
            under_credit=under_credit, confiscated=confiscated,
            on_repair_parts=on_repair_parts
        )
        print(self._params)

    def get_average(self) -> dict:
        """Get average price for composed search parameters."""
        return self._api.average_price(self._params)

    def assign_parameters_to_dict(
        self, api_params: dict, category: str, mark: str, model: str,
        bodystyle: str = None, years: list = None,
        state: str = None, city: str = None,
        gears: list = None, opts: list = None,
        mileage: list = None, fuels: list = None,
        drives: list = None, color: str = None,
        engine_volume: float = None,
        seats: int = None, doors: int = None,
        carrying: int = None, custom: int = None,
        damage: int = None, under_credit: int = None,
        confiscated: int = None, on_repair_parts: int = None
    ) -> Dict:
        """Add docsring here."""
        params_list = [
            bodystyle, carrying, category, city, color,
            confiscated, under_credit, custom, damage, doors,
            drives, engine_volume, fuels, gears, mark, mileage,
            model, opts, on_repair_parts, seats, state, years
        ]
        api_params_processed = OrderedDict(
            sorted(api_params.items(),
                   key=lambda t: t[0])
        )
        assigned_dict = {}
        for i, (key, value) in enumerate(api_params_processed.items()):
            assigned_dict[value] = params_list[i]
        return assigned_dict


def select_item(item_to_select: str, items_list: list) -> int:
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


def select_list(list_to_select: list, items_list: list) -> list:
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
