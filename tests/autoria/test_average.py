import requests_mock
import json

from autoria.api import RiaAverageCarPrice


class TestAverage:
    """Tests for autoria average car price calculation."""

    def test_average_minimal(self, ria_categories, ria_marks, ria_states,
                             ria_bodystyles, ria_models, ria_cities,
                             ria_gearboxes, ria_options, ria_fuels,
                             ria_driver_types, ria_colors, ria_average):
        """Car price can be calculated with minimal set of parameters."""
        with requests_mock.Mocker() as mock:
            mock.get('/categories',
                     text=json.dumps(ria_categories))
            mock.get('/categories/1/marks',
                     text=json.dumps(ria_marks))
            mock.get('/states',
                     text=json.dumps(ria_states))
            mock.get('/categories/1/bodystyles',
                     text=json.dumps(ria_bodystyles))
            mock.get('/categories/1/marks/1/models',
                     text=json.dumps(ria_models))
            mock.get('/categories/1/gearboxes',
                     text=json.dumps(ria_gearboxes))
            mock.get('/categories/1/options',
                     text=json.dumps(ria_options))
            mock.get('/fuels',
                     text=json.dumps(ria_fuels))
            mock.get('/categories/1/driverTypes',
                     text=json.dumps(ria_driver_types))
            mock.get('/colors',
                     text=json.dumps(ria_colors))
            mock.get('/states/None/cities',
                     text=json.dumps(ria_cities))
            myCarAveragePrice = RiaAverageCarPrice(
                category='Легковые',
                mark='Renault',
                model='Scenic'
            )
            # We only have 3 parameters here, do we actually need to
            # make all 11 requests above?
            mock.get(
                '/average?model_id=1&main_category=1&marka_id=1',
                text=json.dumps(ria_average))
            result = myCarAveragePrice.get_average()
            assert result == ria_average
