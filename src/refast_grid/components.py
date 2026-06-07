"""Component definitions for RefastGrid (wrapping silevis/reactgrid) component for refast."""

from typing import Any
from refast.components.base import Component
from refast.components.registry import register_component


@register_component(
    name="RefastGrid",
    package="refast_grid",
    module="components",
)
class RefastGrid(Component):
    """
    RefastGrid component.

    A powerful grid/spreadsheet component for Refast based on silevis/reactgrid.
    It supports multiple cell types:
    - Default built-in types:
        - "header": Static column headers.
        - "text": Simple text.
        - "number": Numeric value.
        - "checkbox": Boolean checkbox.
        - "date": Date selector.
        - "time": Time selector.
        - "email": Email-validated field.
        - "chevron": Collapsible tree indent cell.
    - Custom premium types:
        - "badge": Styled status tags with 'text' and 'variant' ("primary", "secondary", "success", "warning", "destructive", "info").
        - "dropdown": Option dropdowns with 'value' and 'options' list of dicts with 'value' and 'label'.
        - "button": Interactive click buttons with 'text', 'action_id', and 'variant' ("primary", "secondary", "destructive", "outline"). Triggers cell change callback on click.
        - "progress": Completion gauges with numeric 'value' (0.0 to 1.0).
        - "avatar": Profile cards with 'name', 'avatar_url', and optional 'subtext'.
        - "sparkline": Inline SVG micro-charts with 'values' (number list) and 'chart_type' ("line" or "bar").
        - "rating": Selectable rating scales with 'value', 'max' (default 5), and 'icon' ("star", "dot", "heart").
        - "link": styled navigation anchor links with 'text', 'url', and optional 'new_tab' (boolean).
        - "tags": Inline list of multiple string labels with 'values' (string list).
        - "color": Color swathes with hex/rgb 'value'. Opens picker when clicked.
        - "slider": range sliders with 'value', 'min', 'max', and 'step'. Shows tooltip when dragging.

    column resizing, sticky rows/columns, cell selection, drag-and-drop reordering,
    and server-side callbacks.


    Args:
        columns: List of column definitions. Each column is a dict:
            - column_id: Unique identifier (string/number)
            - width: Optional initial width in pixels (number)
            - resizable: Optional boolean to enable resizing for this column
            - reorderable: Optional boolean to enable reordering of this column
        rows: List of row definitions. Each row is a dict:
            - row_id: Unique identifier (string/number)
            - cells: List of cell definitions (dicts)
            - height: Optional row height in pixels (number)
            - reorderable: Optional boolean to enable drag-and-drop reordering
        enable_column_resize_on_all_headers: If True, enables column resizing on all header cells.
        highlights: Optional list of cell coordinates to highlight:
            - row_id: Id of the row
            - column_id: Id of the column
            - color: Optional color (hex/rgb/hsl string)
            - border_color: Optional border color
        sticky_top_rows: Number of rows pinned at the top.
        sticky_bottom_rows: Number of rows pinned at the bottom.
        sticky_left_columns: Number of columns pinned on the left.
        sticky_right_columns: Number of columns pinned on the right.
        enable_fill_handle: Enables cell fill handle (copy/drag behavior).
        enable_range_selection: Enables selection of multiple cell ranges.
        enable_row_selection: Enables selecting entire rows.
        enable_column_selection: Enables selecting entire columns.
        focus_location: Dict with `row_id` and `column_id` to programmatically focus a cell.
        initial_focus_location: Dict with `row_id` and `column_id` for initial cell focus.
        can_reorder_rows: If False, prevents dragging/reordering rows.
        can_reorder_columns: If False, prevents dragging/reordering columns.
        
        on_cells_changed: Callback triggered when cell edits are committed.
            Receives `changes` in `ctx.event_data` where each change contains:
            - rowId: Row ID of the changed cell
            - columnId: Column ID of the changed cell
            - type: Cell type
            - previousCell: Previous cell state dict
            - newCell: New cell state dict
        on_focus_location_changed: Callback triggered when active cell focus shifts.
            Receives `location` in `ctx.event_data`.
        on_column_resized: Callback triggered when column resizing finishes.
            Receives `columnId`, `width`, and `selectedColIds` in `ctx.event_data`.
        on_rows_reordered: Callback triggered when rows are drag-and-drop reordered.
            Receives `targetRowId`, `rowIds`, and `dropPosition` in `ctx.event_data`.
        on_columns_reordered: Callback triggered when columns are drag-and-drop reordered.
            Receives `targetColumnId`, `columnIds`, and `dropPosition` in `ctx.event_data`.

    Example:
        ```python
        from refast import RefastApp, Context
        from refast_grid import RefastGrid

        ui = RefastApp()

        async def handle_cells_changed(ctx: Context):
            changes = ctx.event_data.get("changes", [])
            for change in changes:
                print(f"Cell changed: Row {change['rowId']}, Col {change['columnId']}")
                print(f"New Value: {change['newCell'].get('text')}")

        @ui.page("/")
        def home(ctx: Context):
            columns = [
                {"column_id": "name", "width": 150},
                {"column_id": "age", "width": 80},
                {"column_id": "active", "width": 80},
            ]
            rows = [
                # Header Row
                {
                    "row_id": "header",
                    "cells": [
                        {"type": "header", "text": "Name"},
                        {"type": "header", "text": "Age"},
                        {"type": "header", "text": "Active"},
                    ]
                },
                # Data Row
                {
                    "row_id": "row-1",
                    "cells": [
                        {"type": "text", "text": "Alice"},
                        {"type": "number", "value": 25},
                        {"type": "checkbox", "checked": True},
                    ]
                }
            ]
            return RefastGrid(
                id="my-grid",
                columns=columns,
                rows=rows,
                sticky_top_rows=1,
                on_cells_changed=ctx.callback(handle_cells_changed),
            )
        ```

    Bound Methods:
        - setFocusLocation(location): Programmatically sets focus to a cell.
            E.g. `ctx.call_bound_js("my-grid", "setFocusLocation", {"rowId": "row-1", "columnId": "age"})`
    """

    component_type = "RefastGrid"

    def __init__(
        self,
        columns: list[dict[str, Any]],
        rows: list[dict[str, Any]],
        enable_column_resize_on_all_headers: bool = True,
        highlights: list[dict[str, Any]] | None = None,
        sticky_top_rows: int = 0,
        sticky_bottom_rows: int = 0,
        sticky_left_columns: int = 0,
        sticky_right_columns: int = 0,
        enable_fill_handle: bool = False,
        enable_range_selection: bool = False,
        enable_row_selection: bool = False,
        enable_column_selection: bool = False,
        focus_location: dict[str, Any] | None = None,
        initial_focus_location: dict[str, Any] | None = None,
        can_reorder_rows: bool = True,
        can_reorder_columns: bool = True,
        on_cells_changed: Any = None,
        on_focus_location_changed: Any = None,
        on_column_resized: Any = None,
        on_rows_reordered: Any = None,
        on_columns_reordered: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.columns = columns
        self.rows = rows
        self.enable_column_resize_on_all_headers = enable_column_resize_on_all_headers
        self.highlights = highlights
        self.sticky_top_rows = sticky_top_rows
        self.sticky_bottom_rows = sticky_bottom_rows
        self.sticky_left_columns = sticky_left_columns
        self.sticky_right_columns = sticky_right_columns
        self.enable_fill_handle = enable_fill_handle
        self.enable_range_selection = enable_range_selection
        self.enable_row_selection = enable_row_selection
        self.enable_column_selection = enable_column_selection
        self.focus_location = focus_location
        self.initial_focus_location = initial_focus_location
        self.can_reorder_rows = can_reorder_rows
        self.can_reorder_columns = can_reorder_columns
        
        # Callbacks
        self.on_cells_changed = on_cells_changed
        self.on_focus_location_changed = on_focus_location_changed
        self.on_column_resized = on_column_resized
        self.on_rows_reordered = on_rows_reordered
        self.on_columns_reordered = on_columns_reordered

    def render(self) -> dict[str, Any]:
        """Render the component to a dictionary for the frontend."""
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "columns": self.columns,
                "rows": self.rows,
                "enable_column_resize_on_all_headers": self.enable_column_resize_on_all_headers,
                "highlights": self.highlights,
                "sticky_top_rows": self.sticky_top_rows,
                "sticky_bottom_rows": self.sticky_bottom_rows,
                "sticky_left_columns": self.sticky_left_columns,
                "sticky_right_columns": self.sticky_right_columns,
                "enable_fill_handle": self.enable_fill_handle,
                "enable_range_selection": self.enable_range_selection,
                "enable_row_selection": self.enable_row_selection,
                "enable_column_selection": self.enable_column_selection,
                "focus_location": self.focus_location,
                "initial_focus_location": self.initial_focus_location,
                "can_reorder_rows": self.can_reorder_rows,
                "can_reorder_columns": self.can_reorder_columns,
                
                # Serialized callbacks (ComponentRenderer converts to JS functions)
                "on_cells_changed": self.on_cells_changed.serialize() if self.on_cells_changed else None,
                "on_focus_location_changed": self.on_focus_location_changed.serialize() if self.on_focus_location_changed else None,
                "on_column_resized": self.on_column_resized.serialize() if self.on_column_resized else None,
                "on_rows_reordered": self.on_rows_reordered.serialize() if self.on_rows_reordered else None,
                "on_columns_reordered": self.on_columns_reordered.serialize() if self.on_columns_reordered else None,
                
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
