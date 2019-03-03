from typing import Any, Dict, List
from fnmatch import fnmatch
 

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
