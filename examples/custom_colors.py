"""
RefastGrid Custom Colors Example

This example showcases how RefastGrid automatically adapts to themeswitching out of the box,
and demonstrates how you can customize its colors using CSS custom properties via the `style` dictionary.
"""

from refast import RefastApp, Context
from refast.components import Container, Card, CardHeader, CardTitle, CardContent, Text, Column, ThemeSwitcher

from refast_grid import RefastGrid

# Initialize the Refast application
ui = RefastApp(title="RefastGrid Color Customization Demo")

# Define columns
columns = [
    {"column_id": "id", "width": 80, "resizable": False},
    {"column_id": "item", "width": 200, "resizable": True},
    {"column_id": "status", "width": 120, "resizable": True},
    {"column_id": "priority", "width": 120, "resizable": True},
]

# Helper to generate rows
def make_rows():
    return [
        {
            "row_id": "header",
            "cells": [
                {"type": "header", "text": "Task ID"},
                {"type": "header", "text": "Task Item"},
                {"type": "header", "text": "Status"},
                {"type": "header", "text": "Priority"},
            ],
        },
        {
            "row_id": "1",
            "cells": [
                {"type": "text", "text": "TASK-101", "non_editable": True, "class_name": "font-mono text-center text-muted-foreground"},
                {"type": "text", "text": "Implement themeswitching support"},
                {"type": "text", "text": "Completed", "class_name": "text-green-600 dark:text-green-400 font-semibold"},
                {"type": "text", "text": "High"},
            ],
        },
        {
            "row_id": "2",
            "cells": [
                {"type": "text", "text": "TASK-102", "non_editable": True, "class_name": "font-mono text-center text-muted-foreground"},
                {"type": "text", "text": "Add color override flexibility"},
                {"type": "text", "text": "In Progress", "class_name": "text-amber-600 dark:text-amber-400 font-semibold"},
                {"type": "text", "text": "Medium"},
            ],
        },
        {
            "row_id": "3",
            "cells": [
                {"type": "text", "text": "TASK-103", "non_editable": True, "class_name": "font-mono text-center text-muted-foreground"},
                {"type": "text", "text": "Write usage documentation"},
                {"type": "text", "text": "Pending", "class_name": "text-muted-foreground"},
                {"type": "text", "text": "Low"},
            ],
        },
    ]

@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="max-w-4xl mx-auto py-8 space-y-8",
        children=[
            # Header card
            Card(
                class_name="border border-border/60 shadow-md bg-gradient-to-br from-card to-muted/20",
                children=[
                    CardContent(
                        class_name="p-6 flex justify-between items-center",
                        children=[
                            Column(
                                class_name="space-y-1",
                                children=[
                                    Text(
                                        "RefastGrid Custom Colors Demo",
                                        class_name="text-2xl font-bold tracking-tight bg-gradient-to-r from-primary to-emerald-500 bg-clip-text text-transparent"
                                    ),
                                    Text(
                                        "Explore themeswitching integration and flexible style overrides.",
                                        class_name="text-muted-foreground text-sm"
                                    )
                                ]
                            ),
                            ThemeSwitcher(),
                        ]
                    )
                ]
            ),
            
            # Example 1: Default theme
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("1. Default Theme Integration (Auto-Adapting)"),
                        ]
                    ),
                    CardContent(
                        class_name="space-y-4",
                        children=[
                            Text(
                                "This grid uses default settings. It automatically adapts colors (cell backgrounds, text, borders, input focus, highlights) to light and dark modes when using the ThemeSwitcher.",
                                class_name="text-muted-foreground text-sm"
                            ),
                            RefastGrid(
                                id="default-grid",
                                columns=columns,
                                rows=make_rows(),
                                enable_range_selection=True,
                                class_name="h-44 min-w-full my-2 border border-border shadow-inner"
                            ),
                        ]
                    )
                ]
            ),

            # Example 2: Slate Theme Override
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("2. Custom Slate/Steel Styling (CSS Variable Overrides)"),
                        ]
                    ),
                    CardContent(
                        class_name="space-y-4",
                        children=[
                            Text(
                                "This grid overrides the default colors with custom steel/slate shades using CSS variables passed via the `style` prop.",
                                class_name="text-muted-foreground text-sm"
                            ),
                            RefastGrid(
                                id="slate-grid",
                                columns=columns,
                                rows=make_rows(),
                                enable_range_selection=True,
                                style={
                                    "--rg-background": "#334155",        # Slate 700 background
                                    "--rg-foreground": "#f8fafc",        # Slate 50 text
                                    "--rg-border-color": "#475569",      # Slate 600 borders
                                    "--rg-primary": "#38bdf8",           # Sky 400 focus & selection
                                    "--rg-selection-bg": "rgba(56, 189, 248, 0.15)",  # Sky 400 selection area with 15% opacity
                                    "--rg-muted-bg": "#1e293b",          # Slate 800 background for task ID column
                                },
                                class_name="h-44 min-w-full my-2 border border-slate-600 shadow-inner rounded-lg"
                            ),
                        ]
                    )
                ]
            ),

            # Example 3: Cyberpunk Neon Theme (Extreme Customization)
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("3. Cyberpunk Neon Theme (Extreme Customization)"),
                        ]
                    ),
                    CardContent(
                        class_name="space-y-4",
                        children=[
                            Text(
                                "Demonstrates a vibrant dark-only look with neon borders, dark backgrounds, and purple/pink selection indicators.",
                                class_name="text-muted-foreground text-sm"
                            ),
                            RefastGrid(
                                id="neon-grid",
                                columns=columns,
                                rows=make_rows(),
                                enable_range_selection=True,
                                style={
                                    "--rg-background": "#0f172a",        # Very dark blue
                                    "--rg-foreground": "#38bdf8",        # Cyan text
                                    "--rg-border-color": "#ec4899",      # Pink borders
                                    "--rg-primary": "#a855f7",           # Purple highlights & focus
                                    "--rg-selection-bg": "rgba(168, 85, 247, 0.15)",  # Purple selection area
                                    "--rg-muted-bg": "#1e1b4b",          # Indigo dark background
                                },
                                class_name="h-44 min-w-full my-2 border border-pink-500 shadow-lg shadow-pink-500/10 rounded-lg"
                            ),
                        ]
                    )
                ]
            ),
        ]
    )

from fastapi import FastAPI

# Expose router to FastAPI app
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
