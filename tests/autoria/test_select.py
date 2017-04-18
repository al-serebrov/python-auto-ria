from autoria.api import select_item


class TestSelect:
    """Tests for ``select_item`` function."""

    def test_select_exact(self):
        """Item can be found by exact name match."""
        data = [{
            'name': 'one',
            'value': 1,
        }, {
            'name': 'two',
            'value': 2,
        }]
        assert select_item('one', data) == 1
        assert select_item('two', data) == 2
