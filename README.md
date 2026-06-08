# refast_grid

Spreadsheet component for refast

A [Refast](https://github.com/idling-mind/refast) extension that provides the `RefastGrid` component.

## Installation

```bash
pip install refast_grid
```

## Usage

### Option 1: Auto-Discovery (Recommended)

When you install the package, Refast will automatically discover and load the extension:

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container
from refast_grid import RefastGrid

# Extension is auto-discovered, no need to manually register
ui = RefastApp(title="RefastGrid Demo")


@ui.page("/")
def home(ctx: Context):
    columns = [
        {"column_id": "name", "width": 150},
        {"column_id": "age", "width": 80},
        {"column_id": "active", "width": 80},
    ]
    
    rows = [
        {
            "row_id": "header",
            "cells": [
                {"type": "header", "text": "Name"},
                {"type": "header", "text": "Age"},
                {"type": "header", "text": "Active"},
            ]
        },
        {
            "row_id": "row-1",
            "cells": [
                {"type": "text", "text": "Alice"},
                {"type": "number", "value": 25},
                {"type": "checkbox", "checked": True},
            ]
        }
    ]

    return Container(
        class_name="p-8 max-w-2xl mx-auto",
        children=[
            RefastGrid(
                id="my-grid",
                columns=columns,
                rows=rows,
                sticky_top_rows=1,
            ),
        ]
    )

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Option 2: Manual Registration

If you want to disable auto-discovery and register extensions manually:

```python
from refast import RefastApp
from refast_grid import RefastGrid, RefastGridExtension

ui = RefastApp(
    title="RefastGrid Demo",
    auto_discover_extensions=False,
    extensions=[RefastGridExtension()],
)
```

## Component Props

Here are the primary props for `RefastGrid` (see `components.py` for the full list):

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | list[dict] | **Required** | Column definitions (`column_id`, `width`, `resizable`, etc.) |
| `rows` | list[dict] | **Required** | Row definitions (`row_id`, `cells` list) |
| `enable_column_resize_on_all_headers` | bool | True | Enable column resizing on all header cells |
| `highlights` | list[dict] | None | Cell coordinates to highlight (`row_id`, `column_id`, `color`) |
| `sticky_top_rows` | int | 0 | Number of rows pinned at the top |
| `sticky_bottom_rows` | int | 0 | Number of rows pinned at the bottom |
| `sticky_left_columns` | int | 0 | Number of columns pinned on the left |
| `sticky_right_columns` | int | 0 | Number of columns pinned on the right |
| `enable_fill_handle` | bool | False | Enables Excel-like cell fill handle (copy/drag behavior) |
| `enable_range_selection` | bool | False | Enables selection of multiple cell ranges |
| `enable_row_selection` | bool | False | Enables selecting entire rows |
| `enable_column_selection` | bool | False | Enables selecting entire columns |
| `focus_location` | dict | None | Dict with `row_id` and `column_id` to programmatically focus a cell |
| `initial_focus_location` | dict | None | Dict with `row_id` and `column_id` for initial cell focus |
| `can_reorder_rows` | bool | True | Prevents dragging/reordering rows if False |
| `can_reorder_columns` | bool | True | Prevents dragging/reordering columns if False |
| `on_cells_changed` | Callback | None | Triggered when cell edits are committed |
| `on_focus_location_changed` | Callback | None | Triggered when active cell focus shifts |
| `on_column_resized` | Callback | None | Triggered when column resizing finishes |
| `on_rows_reordered` | Callback | None | Triggered when rows are drag-and-drop reordered |
| `on_columns_reordered` | Callback | None | Triggered when columns are drag-and-drop reordered |
| `id` | str | None | Component ID |
| `class_name` | str | "" | CSS classes to apply |

## Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### Building the Frontend

```bash
cd frontend
npm install
npm run build
```

This builds the UMD bundle to `src/refast_grid/static/`.

### Installing Locally

```bash
# Install with automatic frontend build (via hatch hook)
pip install -e .

# Or build frontend first, then install
cd frontend && npm install && npm run build && cd ..
pip install -e .
```

### Running the Example

```bash
python usage.py
```

Then open http://localhost:8000 in your browser.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
