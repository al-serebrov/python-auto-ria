from autoria.utils import select_item


class TestSelect:
    """Tests for ``select_item`` function."""

    def test_select_exact(self, select_data):
        """Item can be found by exact name match."""
        assert select_item('one', select_data) == 1
        assert select_item('two', select_data) == 2

    def test_select_inexact(self, select_data):
        """Item can be found by inexact name match."""
        assert select_item('on', select_data) == 1
        assert select_item('tw', select_data) == 2
