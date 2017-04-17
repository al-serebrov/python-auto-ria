"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""

from pprint import pprint
from autoria import get_average

# not implemented yet
# VEHICLE_MIN_PRICE = '4000'
# VEHICLE_MAX_PRICE = '5000'

# Type, mark and model are required parameters
# the rest of them is optional
results = get_average(category='Легковые',
                      mark='Renault',
                      model='Scenic',
                      bodystyle=None,
                      years=[2005, 2006],
                      state=None
                      )

pprint(results)
