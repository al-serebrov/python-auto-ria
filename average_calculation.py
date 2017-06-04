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
from autoria import RiaAPI, RiaAverageCarPrice, select_item
# not implemented yet
# VEHICLE_MIN_PRICE = '4000'
# VEHICLE_MAX_PRICE = '5000'

# Type, mark and model are required parameters
# the rest of them is optional

api = RiaAPI()
myCarAveragePrice = RiaAverageCarPrice(
    category='Легковые',
    mark='Renault',
    model='Sceni',
    # bodystyle=None,
    # years=[2006, 2007],
    # state='Харьковская',
    # city='Харьков',
    gears=['Механика'],
    # opts=['ABS'],
    # mileage=[10, 200],
    # fuels=['Дизель'],
    drives=['Полный'],
    # color='Серый',
    # engine_volume=1.5,
    # seats=5,
    # doors=3,
    # carrying=1500,
    custom=0,
    damage=0,
    under_credit=0,
    confiscated=0,
    on_repair_parts=0
)

pprint(myCarAveragePrice.get_average())
