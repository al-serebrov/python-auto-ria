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
    'mark': 'Mitsubishi',
    'model': 'ASX',
    # 'bodystyle': '',
    'years': [2015, 2017],
    # 'state': 'Винницкая',
    # 'city': 'Винница',
    'gears': ['Автомат'],
    # 'opts': ['ABS'],
    # 'mileage': [10, 200],
    # 'fuels': ['Дизель'],
    # 'drives': ['Полный'],
    # 'color': 'Серый',
    # 'engine_volume': 1.5,
    # 'seats': 5,
    # 'doors': 3,
    # 'carrying': 1500,
    'custom': False,
    'damage': False,
    'under_credit': False,
    'confiscated': False,
    'on_repair_parts': False
}
myCarAveragePrice = RiaAverageCarPrice(
    category=search_params.get('category'),
    mark=search_params.get('mark'),
    model=search_params.get('model'),
    bodystyle=search_params.get('bodystyle'),
    years=search_params.get('years'),
    state=search_params.get('state'),
    city=search_params.get('city'),
    gears=search_params.get('gears'),
    opts=search_params.get('opts'),
    mileage=search_params.get('mileage'),
    fuels=search_params.get('fuels'),
    drives=search_params.get('drives'),
    color=search_params.get('color'),
    engine_volume=search_params.get('engine_volume'),
    seats=search_params.get('seats'),
    doors=search_params.get('doors'),
    carrying=search_params.get('carrying'),
    custom=search_params.get('custom'),
    damage=search_params.get('damage'),
    under_credit=search_params.get('under_credit'),
    confiscated=search_params.get('confiscated'),
    on_repair_parts=search_params.get('on_repair_parts')
)

base_url = "https://auto.ria.com/auto__{}.html"
average = myCarAveragePrice.get_average()

report = {
    'search_params': search_params,
    'average': average,
    'classifieds_urls': [
        base_url.format(item)
        for item in average.get('classifieds')]
}
pprint(report)
