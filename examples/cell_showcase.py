"""
RefastGrid All Cell Types Showcase

This example showcases all 17 cell templates available in RefastGrid:
- 6 Built-in/Default Templates: text, number, checkbox, date, time, email
- 11 Custom Premium Templates: badge, dropdown, button, progress, avatar, sparkline, rating, link, tags, color, slider

Run this file with:
    python examples/cell_showcase.py

Then open http://localhost:8085 in your browser.
"""

from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Card, CardHeader, CardTitle, CardContent, Text, Row, Column, ThemeSwitcher, Badge
from refast_grid import RefastGrid

# Initialize the Refast application
ui = RefastApp(title="RefastGrid Cell Templates Showcase")

# Columns definition
showcase_columns = [
    {"column_id": "type_name", "width": 120, "resizable": True},
    {"column_id": "description", "width": 320, "resizable": True},
    {"column_id": "demo_cell", "width": 260, "resizable": True},
]

# Initial rows generation
def get_initial_rows():
    rows = [
        {
            "row_id": "header",
            "cells": [
                {"type": "header", "text": "Cell Type"},
                {"type": "header", "text": "Description"},
                {"type": "header", "text": "Interactive Demo"},
            ]
        },
        # 1. Text
        {
            "row_id": "row-text",
            "cells": [
                {"type": "text", "text": "Text", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Standard editable plain text cell.", "non_editable": True},
                {"type": "text", "text": "Double-click to edit me!"},
            ]
        },
        # 2. Number
        {
            "row_id": "row-number",
            "cells": [
                {"type": "text", "text": "Number", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Editable cell restricted to float/int values.", "non_editable": True},
                {"type": "number", "value": 42.0},
            ]
        },
        # 3. Checkbox
        {
            "row_id": "row-checkbox",
            "cells": [
                {"type": "text", "text": "Checkbox", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Standard interactive checkbox input.", "non_editable": True},
                {"type": "checkbox", "checked": True},
            ]
        },
        # 4. Date
        {
            "row_id": "row-date",
            "cells": [
                {"type": "text", "text": "Date", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Standard date selector using browser date picker.", "non_editable": True},
                {"type": "date", "date": "2026-06-07"},
            ]
        },
        # 5. Time
        {
            "row_id": "row-time",
            "cells": [
                {"type": "text", "text": "Time", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Standard time selector.", "non_editable": True},
                {"type": "time", "time": "09:30:00"},
            ]
        },
        # 6. Email
        {
            "row_id": "row-email",
            "cells": [
                {"type": "text", "text": "Email", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Standard cell containing email with formatting.", "non_editable": True},
                {"type": "email", "text": "hello@refast.dev"},
            ]
        },
        # 7. Badge (Custom)
        {
            "row_id": "row-badge",
            "cells": [
                {"type": "text", "text": "Badge", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Styled pill tag reflecting shadcn HSL variables.", "non_editable": True},
                {"type": "badge", "text": "Completed", "variant": "success"},
            ]
        },
        # 8. Dropdown (Custom)
        {
            "row_id": "row-dropdown",
            "cells": [
                {"type": "text", "text": "Dropdown", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Option picker cell styled matching input lists.", "non_editable": True},
                {
                    "type": "dropdown",
                    "value": "in_progress",
                    "options": [
                        {"value": "todo", "label": "To Do"},
                        {"value": "in_progress", "label": "In Progress"},
                        {"value": "done", "label": "Done"},
                    ]
                },
            ]
        },
        # 9. Button (Custom)
        {
            "row_id": "row-button",
            "cells": [
                {"type": "text", "text": "Button", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Cell containing a button. Click registers server callback.", "non_editable": True},
                {"type": "button", "text": "Trigger Sync", "action_id": "sync_showcase", "variant": "primary"},
            ]
        },
        # 10. Progress (Custom)
        {
            "row_id": "row-progress",
            "cells": [
                {"type": "text", "text": "Progress", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Renders a visual gauge bar (0.0 to 1.0).", "non_editable": True},
                {"type": "progress", "value": 0.75},
            ]
        },
        # 11. Avatar (Custom)
        {
            "row_id": "row-avatar",
            "cells": [
                {"type": "text", "text": "Avatar", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Profile layouts with image/initials & subtext description.", "non_editable": True},
                {
                    "type": "avatar",
                    "name": "Sarah Connor",
                    "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=80",
                    "subtext": "Operations Leader"
                },
            ]
        },
        # 12. Sparkline (Custom)
        {
            "row_id": "row-sparkline",
            "cells": [
                {"type": "text", "text": "Sparkline", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "SVG trend charts (line or bar) rendered directly.", "non_editable": True},
                {"type": "sparkline", "values": [12, 18, 9, 25, 20, 35], "chart_type": "line"},
            ]
        },
        # 13. Rating (Custom)
        {
            "row_id": "row-rating",
            "cells": [
                {"type": "text", "text": "Rating", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Stars, dots, or hearts with hover & click capability.", "non_editable": True},
                {"type": "rating", "value": 4, "max": 5, "icon": "star"},
            ]
        },
        # 14. Link (Custom)
        {
            "row_id": "row-link",
            "cells": [
                {"type": "text", "text": "Link", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Hyperlink opening in new tab without focus theft.", "non_editable": True},
                {"type": "link", "text": "Refast Docs", "url": "https://github.com/idling-mind/refast"},
            ]
        },
        # 15. Tags (Custom)
        {
            "row_id": "row-tags",
            "cells": [
                {"type": "text", "text": "Tags", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Multiple tags in a single scrollable cell container.", "non_editable": True},
                {"type": "tags", "values": ["v1.0", "react", "fastapi"]},
            ]
        },
        # 16. Color (Custom)
        {
            "row_id": "row-color",
            "cells": [
                {"type": "text", "text": "Color", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Swatch dot showing hex code. Launches system color picker.", "non_editable": True},
                {"type": "color", "value": "#a855f7"},
            ]
        },
        # 17. Slider (Custom)
        {
            "row_id": "row-slider",
            "cells": [
                {"type": "text", "text": "Slider", "non_editable": True, "class_name": "font-bold text-primary"},
                {"type": "text", "text": "Range slider displaying tooltip on sliding action.", "non_editable": True},
                {"type": "slider", "value": 45, "min": 0, "max": 100, "step": 1},
            ]
        },
    ]
    for row in rows:
        row["height"] = 40
    return rows

# Callback handler for cells changes
async def handle_cells_changed(ctx: Context):
    changes = ctx.event_data.get("changes", [])
    rows = ctx.state.get("rows", [])
    
    for change in changes:
        row_id = change.get("rowId")
        col_id = change.get("columnId")
        new_cell = change.get("newCell", {})
        cell_type = new_cell.get("type", "unknown")
        
        # Check for button click action
        if cell_type == "button" and new_cell.get("clicked"):
            msg = f"💥 Button Clicked! Row: {row_id}, Action ID: {new_cell.get('actionId')}"
        else:
            val = (
                new_cell.get("value") 
                if new_cell.get("value") is not None 
                else new_cell.get("text") 
                if new_cell.get("text") is not None 
                else new_cell.get("checked") 
                if new_cell.get("checked") is not None 
                else new_cell.get("values")
            )
            msg = f"📝 Cell Changed: Row '{row_id}' ({cell_type}) updated to: {val}"
        
        ctx.state["last_log"] = msg
        
        # Update row state values to ensure changes persist on grid re-renders
        for row in rows:
            if row["row_id"] == row_id:
                cell = row["cells"][2] # The third cell is the demo cell
                if cell_type == "checkbox":
                    cell["checked"] = new_cell.get("checked")
                elif cell_type == "dropdown":
                    cell["value"] = new_cell.get("value")
                elif cell_type == "slider":
                    cell["value"] = new_cell.get("value")
                elif cell_type == "color":
                    cell["value"] = new_cell.get("value")
                elif cell_type == "rating":
                    cell["value"] = new_cell.get("value")
                elif cell_type == "text":
                    cell["text"] = new_cell.get("text")
                elif cell_type == "number":
                    cell["value"] = new_cell.get("value")
                elif cell_type == "date":
                    cell["date"] = new_cell.get("date")
                elif cell_type == "time":
                    cell["time"] = new_cell.get("time")

        # Save the updated rows back to session state
        ctx.state["rows"] = rows
        
        # Update UI elements
        await ctx.update_text("log-viewer", msg)
        await ctx.update_props("showcase-grid", {"rows": rows})

@ui.page("/")
def home(ctx: Context):
    # Initialize rows state if not set
    if "rows" not in ctx.state:
        ctx.state["rows"] = get_initial_rows()
    if "last_log" not in ctx.state:
        ctx.state["last_log"] = "Change any interactive cell to see live logs here..."
        
    return Container(
        class_name="max-w-6xl mx-auto py-8 space-y-6",
        children=[
            # Header Hub
            Card(
                class_name="border border-border/60 shadow-md bg-gradient-to-br from-card to-muted/20",
                children=[
                    CardContent(
                        class_name="p-6 flex justify-between items-center",
                        children=[
                            Column(
                                class_name="space-y-1",
                                children=[
                                    Row(
                                        children=[
                                            Text(
                                                "RefastGrid Cell Showcase",
                                                class_name="text-2xl font-bold tracking-tight bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent"
                                            ),
                                            Badge("17 Cell Templates", variant="secondary")
                                        ],
                                        align="center",
                                        gap=3,
                                    ),
                                    Text(
                                        "A comprehensive demo showcasing all default and custom cell templates in action.",
                                        class_name="text-muted-foreground text-sm"
                                    )
                                ]
                            ),
                            ThemeSwitcher(),
                        ]
                    )
                ]
            ),
            
            # Grid & Log Split Panel
            Row(
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start",
                children=[
                    # Left 2 columns: RefastGrid
                    Column(
                        class_name="lg:col-span-2 space-y-2",
                        children=[
                            RefastGrid(
                                id="showcase-grid",
                                columns=showcase_columns,
                                rows=ctx.state["rows"],
                                sticky_top_rows=1,
                                enable_range_selection=True,
                                on_cells_changed=ctx.callback(handle_cells_changed),
                                class_name="h-[520px] w-full border border-border shadow-inner rounded-lg"
                            )
                        ]
                    ),
                    
                    # Right 1 column: Reactive Logs Card
                    Column(
                        children=[
                            Card(
                                class_name="h-[520px] flex flex-col border border-border bg-card shadow-md",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Reactive Event Logger"),
                                        ]
                                    ),
                                    CardContent(
                                        class_name="flex-grow flex flex-col justify-between p-6",
                                        children=[
                                            Text(
                                                ctx.state["last_log"],
                                                id="log-viewer",
                                                class_name="font-mono text-xs p-4 bg-muted/50 rounded-lg border border-border text-foreground flex-grow whitespace-pre-wrap break-all"
                                            ),
                                            Text(
                                                "Interaction events (clicks, selections, input modifications, sliders) stream instantly to the Python backend and refresh the state dynamically.",
                                                class_name="text-xs text-muted-foreground mt-4 italic"
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

# Expose router to FastAPI app
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
