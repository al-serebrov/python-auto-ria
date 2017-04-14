"""Python auto.ria.com API.

Python implementation of API intended for calulating
average used car prices that are sold on http://auto.ria.com
"""

from pprint import pprint
from autoria import get_average

# Search parameters
# Type, mark and model are required parameters
# the rest of them is optional
CATEGORY = 'Легковые'
MARK = 'Renaul'
MODEL = 'Scenic'
BODY = None
YEAR_START = 2005
YEAR_END = 2006
REGION = None
# not implemented yet
# VEHICLE_MIN_PRICE = '4000'
# VEHICLE_MAX_PRICE = '5000'
# end

results = get_average(category=CATEGORY,
                      mark=MARK,
                      model=MODEL,
                      bodystyle=BODY,
                      year_start=YEAR_START,
                      year_end=YEAR_END,
                      state=REGION
                      )

print('{}\n{}'.format(results[0], results[1]))
pprint(results[2])
