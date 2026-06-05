"""
Example usage of the RefastGrid component wrapping silevis/reactgrid.

Run this file with:
    python usage.py

Then open http://localhost:8000 in your browser.
"""

from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Card, CardHeader, CardTitle, CardContent, Text, Button, Row

from refast_grid import RefastGrid


# Define the Refast app
ui = RefastApp(title="RefastGrid Premium Demo")

# Initial data state
initial_data = [
    {"id": "1", "name": "Alice Smith", "age": 28, "active": True, "birthday": "1998-05-15", "notes": "Lead Designer"},
    {"id": "2", "name": "Bob Jones", "age": 34, "active": False, "birthday": "1992-11-20", "notes": "Senior Engineer"},
    {"id": "3", "name": "Charlie Brown", "age": 19, "active": True, "birthday": "2007-03-05", "notes": "Intern Developer"},
    {"id": "4", "name": "Diana Prince", "age": 31, "active": True, "birthday": "1995-08-28", "notes": "Product Manager"},
]

columns = [
    {"column_id": "id", "width": 60, "resizable": False},
    {"column_id": "name", "width": 150, "resizable": True, "reorderable": True},
    {"column_id": "age", "width": 80, "resizable": True, "reorderable": True},
    {"column_id": "active", "width": 80, "resizable": True, "reorderable": True},
    {"column_id": "birthday", "width": 120, "resizable": True, "reorderable": True},
    {"column_id": "notes", "width": 200, "resizable": True, "reorderable": True},
]


def make_rows(data_list):
    """Helper function to build ReactGrid compatible row definitions."""
    header_row = {
        "row_id": "header",
        "cells": [
            {"type": "header", "text": "ID"},
            {"type": "header", "text": "Name"},
            {"type": "header", "text": "Age"},
            {"type": "header", "text": "Active"},
            {"type": "header", "text": "Birthday"},
            {"type": "header", "text": "Notes"},
        ],
        "reorderable": False,
    }
    
    grid_rows = [header_row]
    for item in data_list:
        grid_rows.append({
            "row_id": item["id"],
            "reorderable": True,
            "cells": [
                {"type": "text", "text": item["id"], "non_editable": True, "class_name": "bg-muted/50 font-mono text-center text-muted-foreground"},
                {"type": "text", "text": item["name"]},
                {"type": "number", "value": item["age"]},
                {"type": "checkbox", "checked": item["active"]},
                {"type": "text", "text": item["birthday"], "placeholder": "YYYY-MM-DD"},
                {"type": "text", "text": item["notes"]},
            ]
        })
    return grid_rows


# Callback: Handle cell value edits
async def handle_cells_changed(ctx: Context):
    changes = ctx.event_data.get("changes", [])
    
    for change in changes:
        row_id = str(change["rowId"])
        col_id = change["columnId"]
        new_cell = change["newCell"]
        
        # Find item in database/state
        item = next((x for x in initial_data if x["id"] == row_id), None)
        if not item:
            continue
            
        # Update correct field
        if col_id == "name":
            item["name"] = new_cell.get("text", "")
        elif col_id == "age":
            item["age"] = new_cell.get("value", 0)
        elif col_id == "active":
            item["active"] = new_cell.get("checked", False)
        elif col_id == "birthday":
            item["birthday"] = new_cell.get("text", "")
        elif col_id == "notes":
            item["notes"] = new_cell.get("text", "")

    # Regenerate rows and update the UI
    new_rows = make_rows(initial_data)
    await ctx.update_props("my-grid", {"rows": new_rows})
    
    change_details = ", ".join([f"{c['columnId']} in Row {c['rowId']}" for c in changes])
    await ctx.update_text("status-text", f"Cells Updated: {change_details}")


# Callback: Cell focus tracking
async def handle_focus_changed(ctx: Context):
    location = ctx.event_data.get("location")
    if location:
        row_id = location.get("rowId")
        col_id = location.get("columnId")
        # Don't show header selection
        if row_id == "header":
            return
        await ctx.update_text("focus-text", f"Active Focus: Row ID: {row_id} | Column ID: {col_id}")


# Callback: Column resizing notification
async def handle_column_resized(ctx: Context):
    col_id = ctx.event_data.get("columnId")
    width = ctx.event_data.get("width")
    await ctx.update_text("status-text", f"Column '{col_id}' resized to {width}px")


# Callback: Drag-and-drop row reordering
async def handle_rows_reordered(ctx: Context):
    target_row_id = str(ctx.event_data.get("targetRowId"))
    row_ids = [str(rid) for rid in ctx.event_data.get("rowIds", [])]
    drop_position = ctx.event_data.get("dropPosition")
    
    global initial_data
    
    # Get items to move
    moving_items = [x for x in initial_data if x["id"] in row_ids]
    # Filter remaining items
    remaining_items = [x for x in initial_data if x["id"] not in row_ids]
    
    # Find insertion index
    target_idx = next((i for i, x in enumerate(remaining_items) if x["id"] == target_row_id), -1)
    if target_idx != -1:
        insert_idx = target_idx + 1 if drop_position == "after" else target_idx
        for item in reversed(moving_items):
            remaining_items.insert(insert_idx, item)
            
        initial_data = remaining_items
        
        # Redraw rows
        new_rows = make_rows(initial_data)
        await ctx.update_props("my-grid", {"rows": new_rows})
        await ctx.update_text("status-text", f"Reordered rows: Moved {', '.join(row_ids)} {drop_position} row {target_row_id}")


# Bound JS action: Programmatically set focus to Age column in row 2
async def handle_set_focus(ctx: Context):
    await ctx.call_bound_js("my-grid", "setFocusLocation", {"rowId": "2", "columnId": "age"})
    await ctx.update_text("status-text", "Programmatically set focus to Bob Jones's Age cell.")


@ui.page("/")
def home(ctx: Context):
    """Home page rendering the RefastGrid with control panel."""
    return Container(
        class_name="max-w-6xl mx-auto py-8 space-y-6",
        children=[
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("RefastGrid Spreadsheet Extension"),
                        ]
                    ),
                    CardContent(
                        class_name="space-y-4",
                        children=[
                            Text(
                                "An interactive spreadsheet wrapped in Refast. Try editing cells, resizing columns, "
                                "or dragging rows by their header cells to reorder them.",
                                class_name="text-muted-foreground text-sm"
                            ),
                            
                            RefastGrid(
                                id="my-grid",
                                columns=columns,
                                rows=make_rows(initial_data),
                                sticky_top_rows=1,
                                enable_fill_handle=True,
                                enable_range_selection=True,
                                enable_row_selection=True,
                                enable_column_selection=True,
                                on_cells_changed=ctx.callback(handle_cells_changed),
                                on_focus_location_changed=ctx.callback(handle_focus_changed),
                                on_column_resized=ctx.callback(handle_column_resized),
                                on_rows_reordered=ctx.callback(handle_rows_reordered),
                                class_name="h-96 min-w-full my-4",
                            ),
                            
                            Row(
                                class_name="justify-between items-center bg-muted/30 p-3 rounded-lg border border-border text-sm",
                                children=[
                                    Text(
                                        "Focus Status: (No cell focused)",
                                        id="focus-text",
                                        class_name="font-medium text-primary"
                                    ),
                                    Text(
                                        "Last Action: Grid initialized",
                                        id="status-text",
                                        class_name="text-muted-foreground text-xs italic"
                                    )
                                ]
                            ),
                            
                            Row(
                                class_name="gap-3 pt-4 border-t border-border justify-end",
                                children=[
                                    Button(
                                        "Focus Bob's Age (Server Bound Method)",
                                        on_click=ctx.callback(handle_set_focus),
                                        variant="outline",
                                        class_name="text-xs"
                                    ),
                                    Button(
                                        "Focus Charlie's Notes (Client Bound Method)",
                                        on_click=ctx.bound_js("my-grid", "setFocusLocation", {"rowId": "3", "columnId": "notes"}),
                                        variant="ghost",
                                        class_name="text-xs"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


# Create FastAPI application
app = FastAPI()
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
