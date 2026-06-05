import unittest
from refast_grid import RefastGrid


class MockCallback:
    """Mock callback for testing."""
    def serialize(self):
        return {"callbackId": "test-callback-id"}


class TestRefastGrid(unittest.TestCase):
    def test_render_basic(self):
        columns = [{"column_id": "col1", "width": 100}]
        rows = [
            {
                "row_id": "header",
                "cells": [{"type": "header", "text": "Col 1"}]
            },
            {
                "row_id": "row1",
                "cells": [{"type": "text", "text": "Val 1"}]
            }
        ]
        grid = RefastGrid(id="grid-1", columns=columns, rows=rows)
        result = grid.render()
        
        self.assertEqual(result["type"], "RefastGrid")
        self.assertEqual(result["id"], "grid-1")
        self.assertEqual(result["props"]["columns"], columns)
        self.assertEqual(result["props"]["rows"], rows)
        self.assertEqual(result["props"]["sticky_top_rows"], 0)
        self.assertTrue(result["props"]["enable_column_resize_on_all_headers"])
    
    def test_render_with_callbacks(self):
        columns = [{"column_id": "col1"}]
        rows = []
        cb = MockCallback()
        grid = RefastGrid(
            id="grid-2", 
            columns=columns, 
            rows=rows,
            on_cells_changed=cb,
            on_focus_location_changed=cb
        )
        result = grid.render()
        
        self.assertEqual(result["props"]["on_cells_changed"], {"callbackId": "test-callback-id"})
        self.assertEqual(result["props"]["on_focus_location_changed"], {"callbackId": "test-callback-id"})

    def test_render_with_extra_props(self):
        columns = []
        rows = []
        grid = RefastGrid(
            id="grid-3",
            columns=columns,
            rows=rows,
            class_name="custom-class",
            enable_fill_handle=True,
            sticky_top_rows=2
        )
        result = grid.render()
        
        self.assertEqual(result["props"]["class_name"], "custom-class")
        self.assertTrue(result["props"]["enable_fill_handle"])
        self.assertEqual(result["props"]["sticky_top_rows"], 2)


if __name__ == "__main__":
    unittest.main()
