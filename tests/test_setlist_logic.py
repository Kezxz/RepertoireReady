# tests/test_setlist_logic.py

import unittest
from io import StringIO
from contextlib import redirect_stdout

from app.setlist_logic import (
    create_setlist,
    add_piece_to_setlist,
    remove_piece_from_setlist,
    view_setlist,
)

class TestSetlistLogic(unittest.TestCase):
    def test_add_piece_order(self):
        setlist_items = []
        performance_id = 1

        add_piece_to_setlist(setlist_items, performance_id, piece_id=101)
        add_piece_to_setlist(setlist_items, performance_id, piece_id=202)
        add_piece_to_setlist(setlist_items, performance_id, piece_id=303)

        items = [it for it in setlist_items if it.performance_id == performance_id]
        items.sort(key=lambda it: it.order_index)

        self.assertEqual([it.order_index for it in items], [1, 2, 3])
        self.assertEqual([it.piece_id for it in items], [101, 202, 303])

    def test_remove_piece_renumber(self):
        setlist_items = []
        performance_id = 1

        add_piece_to_setlist(setlist_items, performance_id, piece_id=111)  # order 1
        add_piece_to_setlist(setlist_items, performance_id, piece_id=222)  # order 2
        add_piece_to_setlist(setlist_items, performance_id, piece_id=333)  # order 3

        removed = remove_piece_from_setlist(setlist_items, performance_id, order_index=2)
        self.assertTrue(removed)

        items = [it for it in setlist_items if it.performance_id == performance_id]
        items.sort(key=lambda it: it.order_index)

        self.assertEqual([it.order_index for it in items], [1, 2])
        self.assertEqual([it.piece_id for it in items], [111, 333])

    def test_view_setlist_empty_message(self):
        setlist_items = []
        setlist = create_setlist(
            performance_id=1,
            title="Test Show",
            date="2026-02-13",
            location="Chicago",
            user_id=42
        )

        buf = StringIO()
        with redirect_stdout(buf):
            view_setlist(setlist, setlist_items)

        output = buf.getvalue()
        self.assertIn("(no pieces yet)", output)

if __name__ == "__main__":
    unittest.main()