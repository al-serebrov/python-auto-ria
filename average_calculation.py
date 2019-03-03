# -*- coding: utf-8 -*-

"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com

Sample API usage:
categories = api.get_categories()
cars_category = select_item('Легковые', categories)
print(api.get_gearboxes(cars_category))
print(api.get_driver_types(cars_category))
print(api.get_options(cars_category))

print(api.get_fuels())
print(api.get_colors())
"""

from math import ceil
from pprint import pprint

from autoria.api import RiaAPI, RiaAverageCarPrice

# not implemented yet
# VEHICLE_MIN_PRICE = '4000'
# VEHICLE_MAX_PRICE = '5000'

# Type, mark and model are required parameters
# the rest of them is optional

api = RiaAPI()
search_params = {
    'category': 'Легковые',
    'mark': 'Mazda',
    'model': 'CX-5',
    'bodystyle': 'Внедорожник / Кроссовер',
    'years': [2015, 2017],
    # 'state': 'Винницкая',
    # 'city': 'Винница',
    'gears': ['Автомат'],
    # 'opts': ['ABS'],
    # 'mileage': [10, 200],
    'fuels': ['Дизель'],
    # 'drives': ['Полный'],
    # 'color': 'Серый',
    # 'engine_volume': 1.5,
    # 'seats': 5,
    # 'doors': 3,
    # 'carrying': 1500,
    # 'custom': False,
    # 'damage': False,
    # 'under_credit': False,
    # 'confiscated': False,
    # 'on_repair_parts': False
}

myCarAveragePrice = RiaAverageCarPrice(**search_params)

base_url = "https://auto.ria.com/auto__{}.html"
average = myCarAveragePrice.get_average()

report = {
    'search_params': search_params,
    'average': average,
    'classifieds_urls': [
        ['${}'.format(ceil(price)), base_url.format(item)]
        for price, item in zip(
            average.get('prices'), average.get('classifieds'))]
}
pprint(report)
