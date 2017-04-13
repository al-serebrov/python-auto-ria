"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""

from pprint import pprint
from api_methods import get_average

PARAMETERS = {
    'VEHICLE_TYPE': 'Легковые',
    'VEHICLE_MARK': 'Ford',
    'VEHICLE_MODEL': 'Focus',
    'VEHICLE_BODY': None,
    'VEHICLE_YEAR_START': 2000,
    'VEHICLE_YEAR_END': 2006,
    'VEHICLE_REGION': 'Харьков',
    # not implemented yet
    # VEHICLE_MIN_PRICE = '4000'
    # VEHICLE_MAX_PRICE = '5000'
    # end
}

results = get_average(PARAMETERS)

print('{}\n{}'.format(results[0], results[1]))
pprint(results[2])
