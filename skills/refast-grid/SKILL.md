---
name: refast-grid
description: Guide for utilizing the RefastGrid extension component (wrapping silevis/reactgrid) within Refast applications.
---

# Skill: RefastGrid extension component

Use this skill when developing or extending applications using the `refast_grid` package, a custom React spreadsheet extension built for **Refast** using `@silevis/reactgrid`.

`refast_grid` allows you to render spreadsheet-like components directly from Python, supporting editing in place, range selections, columns/rows frozen header/footer, custom highlight markers, drag-and-drop row/column reordering, collapsible tree nodes, and server-driven reactive calculations.

---

## 1. Quick Setup & Integration

Refast's extension system supports **auto-discovery via entry points**. To make `RefastGrid` available in your Refast application:

1. Install the extension in your virtual environment:
   ```bash
   pip install -e .
   ```
2. Refast will automatically detect and load the extension.
3. Import the component and extension class:
   ```python
   from refast import RefastApp, Context
   from refast_grid import RefastGrid, RefastGridExtension
   
   # Explicit registration (if not using auto-discovery)
   ui = RefastApp(
       title="My Grid App",
       extensions=[RefastGridExtension()]
   )
   ```

---

## 2. API Reference: `RefastGrid`

The `RefastGrid` component can be configured with the following properties:

### Core Configuration Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | `list[dict]` | **Required** | Column configuration definitions. |
| `rows` | `list[dict]` | **Required** | Rows containing cell content definitions. |
| `enable_column_resize_on_all_headers` | `bool` | `True` | Allow dragging all header boundaries to resize columns. |
| `highlights` | `list[dict]` | `None` | Highlight cell coordinates: `[{"row_id": "r1", "column_id": "c1", "color": "hex", "border_color": "hex"}]`. |
| `sticky_top_rows` | `int` | `0` | Frozen top headers count. |
| `sticky_bottom_rows` | `int` | `0` | Frozen bottom footers count (e.g. summaries). |
| `sticky_left_columns` | `int` | `0` | Frozen left columns count. |
| `sticky_right_columns` | `int` | `0` | Frozen right columns count. |
| `enable_fill_handle` | `bool` | `False` | Enables cell fill-handle (drag-to-copy/drag-to-fill). |
| `enable_range_selection` | `bool` | `False` | Enables selecting multi-cell rectangular ranges. |
| `enable_row_selection` | `bool` | `False` | Enables clicking row headers to highlight entire rows. |
| `enable_column_selection` | `bool` | `False` | Enables clicking column headers to highlight entire columns. |
| `focus_location` | `dict` | `None` | Controlled cell location to focus programmatically: `{"row_id": "...", "column_id": "..."}`. |
| `initial_focus_location` | `dict` | `None` | Uncontrolled initial cell focus. |
| `can_reorder_rows` | `bool` | `True` | Allow dragging rows to reorder. |
| `can_reorder_columns` | `bool` | `True` | Allow dragging columns to reorder. |

### Callbacks (Server-Side)

Register callbacks using `ctx.callback(...)`. Python receives the parameters under `ctx.event_data`.

* **`on_cells_changed`**: Fired when cell edit is committed.
  * `ctx.event_data["changes"]` is a list of changes, each containing:
    * `rowId` (str/int): Row key.
    * `columnId` (str/int): Column key.
    * `type` (str): Cell type (e.g., `'text'`, `'number'`).
    * `previousCell` (dict): Previous cell dict state.
    * `newCell` (dict): Newly entered cell dict state.
* **`on_focus_location_changed`**: Fired when active focus shifts.
  * `ctx.event_data["location"]`: `{"rowId": "...", "columnId": "..."}`.
* **`on_column_resized`**: Fired when column resizing finishes.
  * `ctx.event_data`: `{"columnId": "...", "width": int, "selectedColIds": [...]}`.
* **`on_rows_reordered`**: Fired after drag-and-drop row swap.
  * `ctx.event_data`: `{"targetRowId": "...", "rowIds": [...], "dropPosition": "before" | "after"}`.
* **`on_columns_reordered`**: Fired after drag-and-drop column swap.
  * `ctx.event_data`: `{"targetColumnId": "...", "columnIds": [...], "dropPosition": "before" | "after"}`.

---

## 3. Data Schema: Columns, Rows & Cells

### Column Definition
```python
columns = [
    {
        "column_id": "age",      # Unique identifier
        "width": 100,            # Initial width in pixels
        "resizable": True,       # Can user drag resize this column?
        "reorderable": True      # Can user drag reorder this column?
    }
]
```

### Row Definition
```python
rows = [
    {
        "row_id": "row-1",       # Unique identifier
        "height": 35,            # Optional row height in px
        "reorderable": True,     # Can user drag this row?
        "cells": [ ... ]         # Cell definitions
    }
]
```

### Cell Definitions (by Type)

All cells can accept `non_editable=True` to lock edits, and `class_name="..."` for Tailwind styling.

#### 1. Header Cell (`"header"`)
Read-only title cells, styled differently.
```python
{"type": "header", "text": "Age"}
```

#### 2. Text Cell (`"text"`)
Standard text input cell.
```python
{
    "type": "text", 
    "text": "Alice", 
    "placeholder": "Enter name...", 
    "non_editable": False, 
    "class_name": "bg-muted text-foreground"
}
```

#### 3. Number Cell (`"number"`)
Handles numeric input, float/int.
```python
{
    "type": "number", 
    "value": 42.5, 
    "format": None,              # Optional Python number format
    "non_editable": False
}
```

#### 4. Checkbox Cell (`"checkbox"`)
Boolean checkbox selector.
```python
{"type": "checkbox", "checked": True, "non_editable": False}
```

#### 5. Chevron Cell (`"chevron"`)
Used to build tree-grids. Clicking the chevron toggle fires `on_cells_changed` with the updated expansion state.
```python
{
    "type": "chevron",
    "text": "Engineering Team",  # Row Label
    "is_expanded": True,         # Expansion state
    "has_children": True,        # Renders expansion indicator
    "indent": 1,                 # Indentation level (0 is root)
    "parent_id": "root-dept"     # Parent node key
}
```

#### 6. Date Cell (`"date"`)
Date inputs. Accepts ISO date string representation.
```python
{"type": "date", "date": "1998-05-15"}
```

#### 7. Time Cell (`"time"`)
Time inputs. Accepts ISO datetime string representation.
```python
{"type": "time", "time": "2026-06-06T22:00:00Z"}
```

---

## 4. Programmatic Methods (Bound JS Commands)

You can trigger imperative UI commands (like setting cell focus) programmatically. Use the component's `id` to target it:

### Set Cell Focus
* **From Python Callback (Server-side)**:
  ```python
  async def focus_action(ctx: Context):
      await ctx.call_bound_js(
          "my-grid-id", 
          "setFocusLocation", 
          {"rowId": "row-2", "columnId": "name"}
      )
  ```
* **From Client-Side Click Event (Zero-latency)**:
  ```python
  Button(
      "Focus Cell", 
      on_click=ctx.bound_js(
          "my-grid-id", 
          "setFocusLocation", 
          {"rowId": "row-2", "columnId": "name"}
      )
  )
  ```

---

## 5. Themes, Colors & Custom Styles

RefastGrid adapts automatically to light/dark modes by mapping its CSS variables to Refast's Tailwind semantic HSL color tokens (`--border`, `--card`, `--foreground`, etc.).

### Variable Theme Overrides

You can supply style customizations to the `style` dictionary prop. The component respects the following CSS variable names:

```python
RefastGrid(
    id="custom-grid",
    columns=columns,
    rows=rows,
    style={
        "--rg-background": "#0f172a",        # Background of cells
        "--rg-foreground": "#f8fafc",        # Text color
        "--rg-border-color": "#475569",      # Grid gridlines
        "--rg-primary": "#38bdf8",           # Focus border & handle color
        "--rg-selection-bg": "rgba(56, 189, 248, 0.15)",  # Multi-cell range selection bg
        "--rg-muted-bg": "#1e293b",          # Background for static columns (e.g. key/headers)
        "--rg-accent-bg": "#a855f7",         # Action cell hover/highlights
        "--rg-accent-fg": "#ffffff",         # Accent text
        "--rg-header-bg": "#1e293b",         # Row/column header cell background
        "--rg-header-fg": "#38bdf8",         # Header text color
    }
)
```

---

## 6. Common Design Patterns

### Pattern A: Standard Interactive Data Grid

```python
from refast import RefastApp, Context
from refast_grid import RefastGrid

ui = RefastApp()

# Session-safe state setup
def get_user_data(ctx: Context):
    if "grid_data" not in ctx.state:
        ctx.state["grid_data"] = [
            {"id": "r1", "name": "Alice", "age": 28},
            {"id": "r2", "name": "Bob", "age": 34},
        ]
    return ctx.state["grid_data"]

# Handler for cell updates
async def on_cells_changed(ctx: Context):
    data = get_user_data(ctx)
    changes = ctx.event_data.get("changes", [])
    
    for change in changes:
        row_id = change["rowId"]
        col_id = change["columnId"]
        new_val = change["newCell"].get("text") if col_id == "name" else change["newCell"].get("value")
        
        # Apply edits to state
        for item in data:
            if item["id"] == row_id:
                item[col_id] = new_val

    # Re-render rows to push changes back to frontend
    await ctx.update_props("main-grid", {"rows": make_rows(data)})

def make_rows(data):
    rows = [
        # Header Row
        {
            "row_id": "header",
            "cells": [
                {"type": "header", "text": "Name"},
                {"type": "header", "text": "Age"},
            ]
        }
    ]
    # Body Rows
    for item in data:
        rows.append({
            "row_id": item["id"],
            "cells": [
                {"type": "text", "text": item["name"]},
                {"type": "number", "value": item["age"]},
            ]
        })
    return rows

@ui.page("/")
def index(ctx: Context):
    data = get_user_data(ctx)
    columns = [
        {"column_id": "name", "width": 150},
        {"column_id": "age", "width": 80},
    ]
    return RefastGrid(
        id="main-grid",
        columns=columns,
        rows=make_rows(data),
        on_cells_changed=ctx.callback(on_cells_changed),
        enable_range_selection=True
    )
```

### Pattern B: Calculated Invoice with Footers

Ensure totals are recalculated whenever quantity or price is updated, leveraging `sticky_bottom_rows` for total rollups.

```python
def make_invoice_rows(items):
    headers = {
        "row_id": "header",
        "cells": [{"type": "header", "text": "Item"}, {"type": "header", "text": "Subtotal"}]
    }
    
    rows = [headers]
    grand_total = 0.0
    for item in items:
        sub = item["qty"] * item["price"]
        grand_total += sub
        rows.append({
            "row_id": item["id"],
            "cells": [
                {"type": "text", "text": item["item_name"]},
                {"type": "number", "value": sub, "non_editable": True}
            ]
        })
        
    # Frozen bottom total
    rows.append({
        "row_id": "total-summary",
        "cells": [
            {"type": "text", "text": "Grand Total", "non_editable": True, "class_name": "font-bold text-right"},
            {"type": "number", "value": grand_total, "non_editable": True, "class_name": "font-bold text-primary"}
        ]
    })
    return rows
```

### Pattern C: Collapsible Tree Grid

Maintain node visibility based on expansion state in `ctx.state`. 

```python
def get_visible_nodes(tree_nodes):
    visible = []
    
    def recurse(parent_id):
        children = [n for n in tree_nodes if n["parent_id"] == parent_id]
        for child in children:
            visible.append(child)
            if child["is_expanded"] and child["has_children"]:
                recurse(child["id"])
                
    root = next(n for n in tree_nodes if n["parent_id"] is None)
    visible.append(root)
    if root["is_expanded"]:
        recurse(root["id"])
    return visible

async def handle_tree_changes(ctx: Context):
    tree_nodes = ctx.state["tree_nodes"]
    changes = ctx.event_data.get("changes", [])
    
    for change in changes:
        row_id = change["rowId"]
        new_cell = change["newCell"]
        
        node = next(n for n in tree_nodes if n["id"] == row_id)
        if change["columnId"] == "name" and new_cell.get("type") == "chevron":
            node["is_expanded"] = new_cell.get("isExpanded")
            
    ctx.state["tree_nodes"] = tree_nodes
    visible = get_visible_nodes(tree_nodes)
    await ctx.update_props("tree-grid", {"rows": make_tree_rows(visible)})
```

### Pattern D: Live Real-Time Ticker Flashing

Apply server-side styling and push targeted row props over the websocket. Apply temporary "flashing colors" using Tailwind, then reset:

```python
async def run_live_updates(ctx: Context):
    # Simulated stock ticks
    while ctx.state.get("is_active"):
        stock_data = ctx.state["stocks"]
        
        # 1. Update prices with tick direction
        flash_state = {}
        for stock in stock_data:
            old_price = stock["price"]
            stock["price"] *= (1 + (random.random() - 0.5) * 0.02)
            flash_state[stock["id"]] = "up" if stock["price"] > old_price else "down"
            
        # 2. Render rows with high-contrast color classes
        await ctx.update_props("ticker-grid", {"rows": make_rows(stock_data, flash_state)})
        await asyncio.sleep(1.0)
        
        # 3. Revert classes to normal (clearing green/red background flashes)
        await ctx.update_props("ticker-grid", {"rows": make_rows(stock_data, {})})
        await asyncio.sleep(1.0)
```
