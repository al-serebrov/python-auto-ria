import pytest


@pytest.fixture()
def ria_categories():
    return [{
        "name": "Легковые",
        "value": 1
    }]


@pytest.fixture()
def ria_marks():
    return [{
        "name": "Renault",
        "value": 1
    }]


@pytest.fixture()
def ria_models():
    return [{
        "name": "Scenic",
        "value": 1
    }]


@pytest.fixture()
def ria_bodystyles():
    return [{
        "name": "Седан",
        "value": 3
    }]


@pytest.fixture()
def ria_states():
    return [{
        "name": "Винницкая",
        "value": 1
    }]


@pytest.fixture()
def ria_cities():
    return [{
        "name": "Винница",
        "value": 1
    }]


@pytest.fixture()
def ria_gearboxes():
    return [{
        "name": "Ручная / Механика",
        "value": 1
    }]


@pytest.fixture()
def ria_options():
    return [{
        "name": "ABD",
        "value": 354
    }]


@pytest.fixture()
def ria_fuels():
    return [{
        "name": "Бензин",
        "value": 1
    }]


@pytest.fixture()
def ria_driver_types():
    return [{
        "name": "Кардан",
        "value": 4
    }]


@pytest.fixture()
def ria_colors():
    return [{
        "name": "Бежевый",
        "value": 1
    }]


@pytest.fixture()
def ria_average():
    return {
        'arithmeticMean': 10415.65375,
        'classifieds': [19335039,
                        19810663,
                        18442214,
                        19639867,
                        19522880,
                        18911900,
                        19519819,
                        19673969],
        'interQuartileMean': 10800,
        'percentiles': {'1.0': 6433,
                        '25.0': 8500,
                        '5.0': 6965,
                        '50.0': 11300,
                        '75.0': 12124.75,
                        '95.0': 12906.699499999999,
                        '99.0': 13082.3239},
        'prices': [13126.23,
                   12499,
                   10600,
                   6300,
                   8600,
                   12000,
                   8200,
                   12000],
        'total': 8
    }


@pytest.fixture()
def select_data():
    return [{
            'name': 'one',
            'value': 1,
            }, {
            'name': 'two',
            'value': 2,
            }]


@pytest.fixture()
def list_to_select():
    return ['Ручная / Механика', 'Автомат']


@pytest.fixture()
def items_list():
    return [
                {
                    'name': "Ручная / Механика",
                    'value': 1
                },
                {
                    'name': "Автомат",
                    'value': 2
                }
           ]
  
