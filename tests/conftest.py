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
        'arithmeticMean': 6142,
        'classifieds': [
            19365865,
            17441252,
        ],
        'interQuartileMean': 6749.941176470588,
        'percentiles': {
            '1.0': 2591.3759999999997,
            '5.0': 2735,
            '99.0': 8236.5
        },
        'prices': [
            3300,
            3500,
        ],
        'total': 28
    }
