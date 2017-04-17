"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""

from pprint import pprint
from autoria import RiaAPI

# not implemented yet
# VEHICLE_MIN_PRICE = '4000'
# VEHICLE_MAX_PRICE = '5000'

# Type, mark and model are required parameters
# the rest of them is optional

api = RiaAPI()

results = api.get_average(category='Легковые',
                          mark='Renault',
                          model='Scenic',
                          bodystyle=None,
                          years=[2014, ],
                          state=None
                          )

pprint(results)
