"""
RefastGrid Premium Dashboard Demo

An interactive dashboard showcasing multiple advanced examples of the RefastGrid 
component, demonstrating:
1. Spreadsheet Editor (Standard & Bound Focus Methods)
2. Calculated Cells (Interactive Invoice with sticky bottom summary totals)
3. Collapsible Tree Grid (Department Organization & Budget Planner with Python state tracking)
4. Live Ticker (Simulated real-time Crypto price feeds with dynamic cell highlight styling)

All session states are managed using `ctx.state` to support isolated multi-user sessions.

Run this file with:
    python usage.py

Then open http://localhost:8085 in your browser.
"""
from hashlib import new

import asyncio
import random
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Card, CardHeader, CardTitle, CardContent, Text, Button, Row, Column, ThemeSwitcher, Badge, Tabs, TabItem

from refast_grid import RefastGrid

# Initialize the Refast application
ui = RefastApp(title="RefastGrid Showcase Hub")

# =====================================================================
# EXAMPLE 1: SPREADSHEET EDITOR HELPERS
# =====================================================================
spreadsheet_columns = [
    {"column_id": "id", "width": 60, "resizable": False},
    {"column_id": "name", "width": 160, "resizable": True, "reorderable": True},
    {"column_id": "age", "width": 80, "resizable": True, "reorderable": True},
    {"column_id": "active", "width": 85, "resizable": True, "reorderable": True},
    {"column_id": "birthday", "width": 130, "resizable": True, "reorderable": True},
    {"column_id": "notes", "width": 220, "resizable": True, "reorderable": True},
]

def make_spreadsheet_rows(data):
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
    
    rows = [header_row]
    for item in data:
        rows.append({
            "row_id": item["id"],
            "reorderable": True,
            "cells": [
                {"type": "text", "text": item["id"], "non_editable": True, "class_name": "bg-muted/40 font-mono text-center text-muted-foreground"},
                {"type": "text", "text": item["name"]},
                {"type": "number", "value": item["age"]},
                {"type": "checkbox", "checked": item["active"]},
                {"type": "text", "text": item["birthday"], "placeholder": "YYYY-MM-DD"},
                {"type": "text", "text": item["notes"]},
            ]
        })
    return rows

# =====================================================================
# EXAMPLE 2: CALCULATED CELLS (INVOICE GENERATOR) HELPERS
# =====================================================================
invoice_columns = [
    {"column_id": "desc", "width": 300, "resizable": True, "reorderable": True},
    {"column_id": "qty", "width": 80, "resizable": True},
    {"column_id": "price", "width": 140, "resizable": True},
    {"column_id": "subtotal", "width": 150, "resizable": True},
    {"column_id": "tax_rate", "width": 100, "resizable": True},
    {"column_id": "total", "width": 160, "resizable": True},
]

def make_invoice_rows(items):
    header_row = {
        "row_id": "header",
        "cells": [
            {"type": "header", "text": "Item Description"},
            {"type": "header", "text": "Qty"},
            {"type": "header", "text": "Unit Price ($)"},
            {"type": "header", "text": "Subtotal ($)"},
            {"type": "header", "text": "Tax Rate (%)"},
            {"type": "header", "text": "Total ($)"},
        ],
        "reorderable": False,
    }
    
    grid_rows = [header_row]
    sum_subtotal = 0.0
    sum_tax = 0.0
    sum_total = 0.0
    
    for item in items:
        qty = item["qty"]
        price = item["price"]
        subtotal = qty * price
        tax = subtotal * (item["tax_rate"] / 100.0)
        total = subtotal + tax
        
        sum_subtotal += subtotal
        sum_tax += tax
        sum_total += total
        
        grid_rows.append({
            "row_id": item["id"],
            "reorderable": True,
            "cells": [
                {"type": "text", "text": item["desc"]},
                {"type": "number", "value": qty},
                {"type": "number", "value": price},
                {"type": "number", "value": subtotal, "non_editable": True, "class_name": "bg-muted/30 font-medium text-muted-foreground font-mono"},
                {"type": "number", "value": item["tax_rate"]},
                {"type": "number", "value": total, "non_editable": True, "class_name": "bg-muted/30 font-bold text-foreground font-mono"},
            ]
        })
        
    # Sticky bottom subtotal summary row
    grid_rows.append({
        "row_id": "subtotal-summary",
        "cells": [
            {"type": "text", "text": "Subtotal Sum", "non_editable": True, "class_name": "font-semibold text-right bg-muted/40"},
            {"type": "text", "text": "", "non_editable": True, "class_name": "bg-muted/40"},
            {"type": "text", "text": "", "non_editable": True, "class_name": "bg-muted/40"},
            {"type": "number", "value": sum_subtotal, "non_editable": True, "class_name": "font-bold bg-muted/40 text-muted-foreground font-mono"},
            {"type": "text", "text": "", "non_editable": True, "class_name": "bg-muted/40"},
            {"type": "number", "value": sum_tax, "non_editable": True, "class_name": "font-semibold bg-muted/40 text-muted-foreground font-mono"},
        ]
    })
    
    # Sticky bottom grand total summary row
    grid_rows.append({
        "row_id": "total-summary",
        "cells": [
            {"type": "text", "text": "Grand Total (USD)", "non_editable": True, "class_name": "font-bold text-right bg-primary/5 dark:bg-primary/10"},
            {"type": "text", "text": "", "non_editable": True, "class_name": "bg-primary/5 dark:bg-primary/10"},
            {"type": "text", "text": "", "non_editable": True, "class_name": "bg-primary/5 dark:bg-primary/10"},
            {"type": "text", "text": "", "non_editable": True, "class_name": "bg-primary/5 dark:bg-primary/10"},
            {"type": "text", "text": "", "non_editable": True, "class_name": "bg-primary/5 dark:bg-primary/10"},
            {"type": "number", "value": sum_total, "non_editable": True, "class_name": "font-black bg-primary/10 dark:bg-primary/20 text-primary text-base font-mono"},
        ]
    })
    
    return grid_rows

# =====================================================================
# EXAMPLE 3: TREE GRID (BUDGET PLANNER) HELPERS
# =====================================================================
tree_columns = [
    {"column_id": "department", "width": 300, "resizable": True},
    {"column_id": "budget", "width": 150, "resizable": True},
    {"column_id": "headcount", "width": 110, "resizable": True},
    {"column_id": "spent", "width": 150, "resizable": True},
]

def compute_tree_totals(tree_data_list):
    # Reset parent nodes
    for node in tree_data_list:
        if node["has_children"]:
            node["budget"] = 0.0
            node["headcount"] = 0
            node["spent"] = 0.0

    # Cumulate values from children up to parents recursively
    def sum_node(node_id):
        node = next(n for n in tree_data_list if n["id"] == node_id)
        if not node["has_children"]:
            return node["budget"], node["headcount"], node["spent"]
        
        b_sum, h_sum, s_sum = 0.0, 0, 0.0
        for child in tree_data_list:
            if child["parent_id"] == node_id:
                b, h, s = sum_node(child["id"])
                b_sum += b
                h_sum += h
                s_sum += s
        
        node["budget"] = b_sum
        node["headcount"] = h_sum
        node["spent"] = s_sum
        return b_sum, h_sum, s_sum

    sum_node("root")

def get_visible_tree_nodes(tree_data_list):
    visible = []
    
    def add_children(parent_id):
        children = [n for n in tree_data_list if n["parent_id"] == parent_id]
        for child in children:
            visible.append(child)
            if child["is_expanded"] and child["has_children"]:
                add_children(child["id"])
                
    root = next(n for n in tree_data_list if n["id"] == "root")
    visible.append(root)
    if root["is_expanded"]:
        add_children("root")
        
    return visible

def make_tree_rows(nodes):
    header_row = {
        "row_id": "header",
        "cells": [
            {"type": "header", "text": "Department Name"},
            {"type": "header", "text": "Budget ($)"},
            {"type": "header", "text": "Headcount"},
            {"type": "header", "text": "Spent ($)"},
        ],
        "reorderable": False,
    }
    
    grid_rows = [header_row]
    for node in nodes:
        is_parent = node["has_children"]
        row_style_class = "bg-muted/20 font-semibold text-foreground" if is_parent else ""
        
        grid_rows.append({
            "row_id": node["id"],
            "reorderable": False,
            "cells": [
                {
                    "type": "chevron",
                    "text": node["name"],
                    "is_expanded": node["is_expanded"],
                    "has_children": node["has_children"],
                    "indent": node["level"],
                    "parent_id": node["parent_id"],
                    "class_name": row_style_class
                },
                {
                    "type": "number", 
                    "value": node["budget"], 
                    "non_editable": is_parent,
                    "class_name": f"{row_style_class} font-mono"
                },
                {
                    "type": "number", 
                    "value": node["headcount"], 
                    "non_editable": is_parent,
                    "class_name": f"{row_style_class} font-mono"
                },
                {
                    "type": "number", 
                    "value": node["spent"], 
                    "non_editable": is_parent,
                    "class_name": f"{row_style_class} text-muted-foreground font-mono" if is_parent else "font-mono"
                },
            ]
        })
    return grid_rows

# =====================================================================
# EXAMPLE 4: LIVE CRYPTO TICKER HELPERS
# =====================================================================
crypto_columns = [
    {"column_id": "name", "width": 160},
    {"column_id": "symbol", "width": 100},
    {"column_id": "price", "width": 150},
    {"column_id": "change", "width": 120},
    {"column_id": "volume", "width": 180},
]

def make_crypto_rows(data, flash_state=None):
    if flash_state is None:
        flash_state = {}
        
    header_row = {
        "row_id": "header",
        "cells": [
            {"type": "header", "text": "Cryptocurrency"},
            {"type": "header", "text": "Symbol"},
            {"type": "header", "text": "Price (USD)"},
            {"type": "header", "text": "24h Change (%)"},
            {"type": "header", "text": "24h Volume ($)"},
        ],
        "reorderable": False,
    }
    
    grid_rows = [header_row]
    for coin in data:
        coin_id = coin["id"]
        direction = flash_state.get(coin_id, "flat")
        
        # Color flash class for active updates
        price_class = "font-mono "
        if direction == "up":
            price_class += "bg-green-500/20 text-green-600 dark:text-green-400 font-bold transition-all duration-300"
        elif direction == "down":
            price_class += "bg-red-500/20 text-red-600 dark:text-red-400 font-bold transition-all duration-300"
        else:
            price_class += "transition-all duration-300 text-foreground"
            
        change_class = "font-mono font-medium "
        if coin["change_24h"] > 0:
            change_class += "text-green-600 dark:text-green-400"
        elif coin["change_24h"] < 0:
            change_class += "text-red-600 dark:text-red-400"
            
        grid_rows.append({
            "row_id": coin_id,
            "reorderable": False,
            "cells": [
                {"type": "text", "text": coin["name"], "non_editable": True, "class_name": "font-semibold"},
                {"type": "text", "text": coin["symbol"], "non_editable": True, "class_name": "text-muted-foreground text-center font-mono"},
                {"type": "number", "value": coin["price"], "non_editable": True, "class_name": price_class},
                {"type": "number", "value": coin["change_24h"], "non_editable": True, "class_name": change_class},
                {"type": "number", "value": coin["volume"], "non_editable": True, "class_name": "font-mono text-muted-foreground"},
            ]
        })
    return grid_rows

# =====================================================================
# BACKGROUND ASYNC LIVE UPDATES LOOP
# =====================================================================
async def run_live_updates(ctx: Context):
    try:
        while ctx.state.get("is_auto_refreshing", False):
            crypto_data = ctx.state.get("crypto_data", [])
            changes_made = []
            for coin in crypto_data:
                if random.random() < 0.7:  # 70% chance of ticking
                    change_pct = (random.random() - 0.48) * 1.5  # -0.72% to +0.78%
                    old_price = coin["price"]
                    coin["price"] = round(coin["price"] * (1 + change_pct / 100), 2 if coin["price"] > 1 else 4)
                    coin["change_24h"] = round(coin["change_24h"] + change_pct, 2)
                    coin["volume"] = int(coin["volume"] * (1 + (random.random() - 0.5) * 0.04))
                    
                    direction = "up" if coin["price"] > old_price else "down"
                    changes_made.append((coin["id"], direction))
                else:
                    changes_made.append((coin["id"], "flat"))

            # Save state update
            ctx.state["crypto_data"] = crypto_data

            # Render with high-contrast color flashes
            await ctx.update_props("crypto-grid", {"rows": make_crypto_rows(crypto_data, dict(changes_made))})
            await asyncio.sleep(1.2)
            
            # Revert background color back to normal
            await ctx.update_props("crypto-grid", {"rows": make_crypto_rows(crypto_data, {c["id"]: "flat" for c in crypto_data})})
            await asyncio.sleep(0.8)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Error in background update task: {e}")

# =====================================================================
# STATE INITIALIZATION HELPER
# =====================================================================
def init_state(ctx: Context):
    """Initialize session state keys if not already set."""
    if "active_tab" not in ctx.state:
        ctx.state["active_tab"] = "spreadsheet"
        
    if "spreadsheet_data" not in ctx.state:
        ctx.state["spreadsheet_data"] = [
            {"id": "1", "name": "Alice Smith", "age": 28, "active": True, "birthday": "1998-05-15", "notes": "Lead Designer"},
            {"id": "2", "name": "Bob Jones", "age": 34, "active": False, "birthday": "1992-11-20", "notes": "Senior Engineer"},
            {"id": "3", "name": "Charlie Brown", "age": 19, "active": True, "birthday": "2007-03-05", "notes": "Intern Developer"},
            {"id": "4", "name": "Diana Prince", "age": 31, "active": True, "birthday": "1995-08-28", "notes": "Product Manager"},
        ]
        
    if "invoice_data" not in ctx.state:
        ctx.state["invoice_data"] = [
            {"id": "inv-1", "desc": "Premium Web Design Service", "qty": 1, "price": 2500.0, "tax_rate": 15.0},
            {"id": "inv-2", "desc": "React SEO Optimization Consulting", "qty": 10, "price": 150.0, "tax_rate": 10.0},
            {"id": "inv-3", "desc": "SaaS Cloud Hosting (Annual Plan)", "qty": 2, "price": 450.0, "tax_rate": 5.0},
        ]
        
    if "tree_data" not in ctx.state:
        initial_tree = [
            {"id": "root", "name": "Company HQ", "parent_id": None, "level": 0, "budget": 0.0, "headcount": 0, "spent": 0.0, "is_expanded": True, "has_children": True},
            {"id": "eng", "name": "Engineering", "parent_id": "root", "level": 1, "budget": 0.0, "headcount": 0, "spent": 0.0, "is_expanded": True, "has_children": True},
            {"id": "eng-fe", "name": "Frontend Team", "parent_id": "eng", "level": 2, "budget": 120000.0, "headcount": 4, "spent": 95000.0, "is_expanded": False, "has_children": False},
            {"id": "eng-be", "name": "Backend Team", "parent_id": "eng", "level": 2, "budget": 180000.0, "headcount": 6, "spent": 172000.0, "is_expanded": False, "has_children": False},
            {"id": "eng-qa", "name": "QA & Testing", "parent_id": "eng", "level": 2, "budget": 50000.0, "headcount": 2, "spent": 42000.0, "is_expanded": False, "has_children": False},
            {"id": "mkt", "name": "Marketing", "parent_id": "root", "level": 1, "budget": 0.0, "headcount": 0, "spent": 0.0, "is_expanded": True, "has_children": True},
            {"id": "mkt-social", "name": "Social Media Campaign", "parent_id": "mkt", "level": 2, "budget": 45000.0, "headcount": 2, "spent": 38000.0, "is_expanded": False, "has_children": False},
            {"id": "mkt-seo", "name": "SEO & Growth", "parent_id": "mkt", "level": 2, "budget": 30000.0, "headcount": 1, "spent": 25000.0, "is_expanded": False, "has_children": False},
            {"id": "ops", "name": "Operations & Admin", "parent_id": "root", "level": 1, "budget": 95000.0, "headcount": 3, "spent": 91000.0, "is_expanded": False, "has_children": False},
        ]
        # Pre-compute budget totals
        compute_tree_totals(initial_tree)
        ctx.state["tree_data"] = initial_tree
        
    if "crypto_data" not in ctx.state:
        ctx.state["crypto_data"] = [
            {"id": "btc", "name": "Bitcoin", "symbol": "BTC", "price": 68250.00, "change_24h": 2.45, "volume": 28450000000},
            {"id": "eth", "name": "Ethereum", "symbol": "ETH", "price": 3520.50, "change_24h": -1.15, "volume": 14200000000},
            {"id": "sol", "name": "Solana", "symbol": "SOL", "price": 142.75, "change_24h": 5.82, "volume": 4120000000},
            {"id": "ada", "name": "Cardano", "symbol": "ADA", "price": 0.485, "change_24h": -0.85, "volume": 380000000},
            {"id": "doge", "name": "Dogecoin", "symbol": "DOGE", "price": 0.138, "change_24h": 12.40, "volume": 1850000000},
        ]
        
    if "is_auto_refreshing" not in ctx.state:
        ctx.state["is_auto_refreshing"] = False
        
    if "refresh_task" not in ctx.state:
        ctx.state["refresh_task"] = None

# =====================================================================
# CALLBACK EVENT HANDLERS
# =====================================================================

async def switch_tab(ctx: Context):
    if not ctx.event_data or not isinstance(ctx.event_data, dict):
        return
    new_tab = ctx.event_data.get("value")
    """Switch active view and update tab buttons dynamically."""
    init_state(ctx)
    active_tab = ctx.state.get("active_tab", "spreadsheet")
    if not new_tab or new_tab == active_tab:
        return
        
    ctx.state["active_tab"] = new_tab
    
    # Hide old container, show new container
    await ctx.update_props(f"container-{active_tab}", {"class_name": "space-y-4 hidden"})
    await ctx.update_props(f"container-{new_tab}", {"class_name": "space-y-4"})
    
    # Switch button active variants
    await ctx.update_props(f"tab-btn-{active_tab}", {"variant": "ghost"})
    await ctx.update_props(f"tab-btn-{new_tab}", {"variant": "default"})

# Example 1: Spreadsheet Callbacks
async def handle_spreadsheet_changed(ctx: Context):
    init_state(ctx)
    spreadsheet_data = ctx.state["spreadsheet_data"]
    changes = ctx.event_data.get("changes", [])
    
    for change in changes:
        row_id = str(change["rowId"])
        col_id = change["columnId"]
        new_cell = change["newCell"]
        
        item = next((x for x in spreadsheet_data if x["id"] == row_id), None)
        if not item:
            continue
            
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

    ctx.state["spreadsheet_data"] = spreadsheet_data
    
    await ctx.update_props("spreadsheet-grid", {"rows": make_spreadsheet_rows(spreadsheet_data)})
    change_details = ", ".join([f"{c['columnId']} in Row {c['rowId']}" for c in changes])
    await ctx.update_text("status-text", f"Cells Updated: {change_details}")

async def handle_spreadsheet_focus(ctx: Context):
    location = ctx.event_data.get("location")
    if location:
        row_id = location.get("rowId")
        col_id = location.get("columnId")
        if row_id == "header":
            return
        await ctx.update_text("focus-text", f"Focused cell: Row {row_id}, Column '{col_id}'")

async def handle_spreadsheet_resized(ctx: Context):
    col_id = ctx.event_data.get("columnId")
    width = ctx.event_data.get("width")
    await ctx.update_text("status-text", f"Column '{col_id}' resized to {width}px")

async def handle_spreadsheet_reordered(ctx: Context):
    init_state(ctx)
    spreadsheet_data = ctx.state["spreadsheet_data"]
    
    target_row_id = str(ctx.event_data.get("targetRowId"))
    row_ids = [str(rid) for rid in ctx.event_data.get("rowIds", [])]
    drop_position = ctx.event_data.get("dropPosition")
    
    moving_items = [x for x in spreadsheet_data if x["id"] in row_ids]
    remaining_items = [x for x in spreadsheet_data if x["id"] not in row_ids]
    
    target_idx = next((i for i, x in enumerate(remaining_items) if x["id"] == target_row_id), -1)
    if target_idx != -1:
        insert_idx = target_idx + 1 if drop_position == "after" else target_idx
        for item in reversed(moving_items):
            remaining_items.insert(insert_idx, item)
            
        ctx.state["spreadsheet_data"] = remaining_items
        await ctx.update_props("spreadsheet-grid", {"rows": make_spreadsheet_rows(remaining_items)})
        await ctx.update_text("status-text", f"Reordered rows: Moved {', '.join(row_ids)} {drop_position} row {target_row_id}")

async def handle_set_focus(ctx: Context):
    await ctx.call_bound_js("spreadsheet-grid", "setFocusLocation", {"rowId": "2", "columnId": "age"})
    await ctx.update_text("status-text", "Programmatically focused Bob's Age cell.")

# Example 2: Invoice Callbacks
async def handle_invoice_changed(ctx: Context):
    init_state(ctx)
    invoice_data = ctx.state["invoice_data"]
    changes = ctx.event_data.get("changes", [])
    
    for change in changes:
        row_id = str(change["rowId"])
        col_id = change["columnId"]
        new_cell = change["newCell"]
        
        item = next((x for x in invoice_data if x["id"] == row_id), None)
        if not item:
            continue
            
        if col_id == "desc":
            item["desc"] = new_cell.get("text", "")
        elif col_id == "qty":
            item["qty"] = max(0, int(new_cell.get("value", 0)))
        elif col_id == "price":
            item["price"] = max(0.0, float(new_cell.get("value", 0.0)))
        elif col_id == "tax_rate":
            item["tax_rate"] = max(0.0, float(new_cell.get("value", 0.0)))

    ctx.state["invoice_data"] = invoice_data
    await ctx.update_props("invoice-grid", {"rows": make_invoice_rows(invoice_data)})
    await ctx.update_text("invoice-status", f"Invoice updated (total: {len(invoice_data)} items)")

async def handle_add_invoice_row(ctx: Context):
    init_state(ctx)
    invoice_data = ctx.state["invoice_data"]
    
    new_id = f"inv-{len(invoice_data) + 1}"
    invoice_data.append({
        "id": new_id,
        "desc": "New Item Line",
        "qty": 1,
        "price": 0.0,
        "tax_rate": 10.0
    })
    
    ctx.state["invoice_data"] = invoice_data
    await ctx.update_props("invoice-grid", {"rows": make_invoice_rows(invoice_data)})
    await ctx.update_text("invoice-status", f"Added new item: {new_id}")

async def handle_clear_invoice(ctx: Context):
    init_state(ctx)
    ctx.state["invoice_data"] = []
    await ctx.update_props("invoice-grid", {"rows": make_invoice_rows([])})
    await ctx.update_text("invoice-status", "Invoice cleared")

# Example 3: Tree Grid Callbacks
async def handle_tree_changed(ctx: Context):
    init_state(ctx)
    tree_data = ctx.state["tree_data"]
    changes = ctx.event_data.get("changes", [])
    
    for change in changes:
        row_id = str(change["rowId"])
        col_id = change["columnId"]
        new_cell = change["newCell"]
        
        node = next((n for n in tree_data if n["id"] == row_id), None)
        if not node:
            continue
            
        if col_id == "department" and new_cell.get("type") == "chevron":
            node["is_expanded"] = new_cell.get("isExpanded", False)
        elif col_id == "budget" and not node["has_children"]:
            node["budget"] = max(0.0, float(new_cell.get("value", 0.0)))
        elif col_id == "headcount" and not node["has_children"]:
            node["headcount"] = max(0, int(new_cell.get("value", 0)))
        elif col_id == "spent" and not node["has_children"]:
            node["spent"] = max(0.0, float(new_cell.get("value", 0.0)))

    compute_tree_totals(tree_data)
    ctx.state["tree_data"] = tree_data
    
    visible = get_visible_tree_nodes(tree_data)
    await ctx.update_props("tree-grid", {"rows": make_tree_rows(visible)})
    await ctx.update_text("tree-status", "Tree grid updated dynamically")

async def handle_expand_all(ctx: Context):
    init_state(ctx)
    tree_data = ctx.state["tree_data"]
    for node in tree_data:
        if node["has_children"]:
            node["is_expanded"] = True
            
    ctx.state["tree_data"] = tree_data
    visible = get_visible_tree_nodes(tree_data)
    await ctx.update_props("tree-grid", {"rows": make_tree_rows(visible)})
    await ctx.update_text("tree-status", "All departments expanded")

async def handle_collapse_all(ctx: Context):
    init_state(ctx)
    tree_data = ctx.state["tree_data"]
    for node in tree_data:
        if node["has_children"]:
            node["is_expanded"] = False
            
    ctx.state["tree_data"] = tree_data
    visible = get_visible_tree_nodes(tree_data)
    await ctx.update_props("tree-grid", {"rows": make_tree_rows(visible)})
    await ctx.update_text("tree-status", "All departments collapsed")

# Example 4: Live Crypto Ticker Callbacks
async def toggle_auto_refresh(ctx: Context):
    init_state(ctx)
    is_auto_refreshing = ctx.state.get("is_auto_refreshing", False)
    refresh_task = ctx.state.get("refresh_task")
    
    if is_auto_refreshing:
        ctx.state["is_auto_refreshing"] = False
        if refresh_task:
            refresh_task.cancel()
            ctx.state["refresh_task"] = None
        await ctx.update_props("toggle-refresh-btn", {"variant": "default", "children": "Start Auto-Refresh"})
        await ctx.update_text("crypto-status", "Live updates paused")
    else:
        ctx.state["is_auto_refreshing"] = True
        task = asyncio.create_task(run_live_updates(ctx))
        ctx.state["refresh_task"] = task
        await ctx.update_props("toggle-refresh-btn", {"variant": "destructive", "children": "Stop Auto-Refresh"})
        await ctx.update_text("crypto-status", "Live updates active (prices flash every 2s)")

# =====================================================================
# LAYOUT RENDERING
# =====================================================================

@ui.page("/")
def home(ctx: Context):
    # Initialize the user connection state
    init_state(ctx)
    
    # Cancel background update task if page reload/re-rendered to avoid floating tasks
    is_auto_refreshing = ctx.state.get("is_auto_refreshing", False)
    refresh_task = ctx.state.get("refresh_task")
    if is_auto_refreshing:
        ctx.state["is_auto_refreshing"] = False
        if refresh_task:
            refresh_task.cancel()
            ctx.state["refresh_task"] = None

    active_tab = ctx.state["active_tab"]
    spreadsheet_data = ctx.state["spreadsheet_data"]
    invoice_data = ctx.state["invoice_data"]
    tree_data = ctx.state["tree_data"]
    crypto_data = ctx.state["crypto_data"]

    return Container(
        class_name="max-w-6xl mx-auto py-8 space-y-6",
        children=[
            # Elegant gradient title
            Card(
                class_name="border border-border/60 shadow-md bg-gradient-to-br from-card to-muted/20",
                children=[
                    CardContent(
                        class_name="p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4",
                        children=[
                            Column(
                                class_name="space-y-1",
                                children=[
                                    Row(
                                        [
                                            Text(
                                                "RefastGrid Premium Showcase Hub",
                                                class_name="text-3xl font-bold tracking-tight bg-gradient-to-r from-primary to-emerald-500 bg-clip-text text-transparent"
                                            ),
                                            Badge("v0.2.0")
                                        ],
                                        align="center",
                                        gap=3,
                                    ),
                                    Text(
                                        "Explore advanced spreadsheet, tree structure, live streams, and reactive grids built with Refast.",
                                        class_name="text-muted-foreground text-sm"
                                    ),
                                ]
                            ),
                            # Small status pill
                            ThemeSwitcher(),
                        ]
                    )
                ]
            ),
            
            # Tab Controls Row
            Row(
                children=[
                    Tabs(
                        [
                            TabItem(label="Spreadsheet Editor", value="spreadsheet"),
                            TabItem(label="Calculated Invoice", value="invoice"),
                            TabItem(label="Collapsible Tree Grid", value="tree"),
                            TabItem(label="Live Crypto Ticker", value="live"),
                        ],
                        value=active_tab,
                        on_value_change=ctx.callback(switch_tab)
                    )
                ]
            ),
            
            # TAB CONTENT 1: SPREADSHEET EDITOR
            Container(
                id="container-spreadsheet",
                class_name="space-y-4" if active_tab == "spreadsheet" else "space-y-4 hidden",
                children=[
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("1. Interactive Spreadsheet Editor"),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    Text(
                                        "Supports edit-in-place, column resizing, cell range selection, and row reordering (drag-and-drop rows by holding their ID column handles).",
                                        class_name="text-muted-foreground text-sm"
                                    ),
                                    RefastGrid(
                                        id="spreadsheet-grid",
                                        columns=spreadsheet_columns,
                                        rows=make_spreadsheet_rows(spreadsheet_data),
                                        sticky_top_rows=1,
                                        enable_fill_handle=True,
                                        enable_range_selection=True,
                                        enable_row_selection=True,
                                        enable_column_selection=True,
                                        on_cells_changed=ctx.callback(handle_spreadsheet_changed),
                                        on_focus_location_changed=ctx.callback(handle_spreadsheet_focus),
                                        on_column_resized=ctx.callback(handle_spreadsheet_resized),
                                        on_rows_reordered=ctx.callback(handle_spreadsheet_reordered),
                                        class_name="h-80 min-w-full my-2 border border-border shadow-inner"
                                    ),
                                    Row(
                                        class_name="justify-between items-center bg-muted/40 p-3 rounded-lg border border-border text-sm",
                                        children=[
                                            Text(
                                                "Focused cell: (No active focus)",
                                                id="focus-text",
                                                class_name="font-medium text-primary text-xs"
                                            ),
                                            Text(
                                                "Last Action: Grid loaded",
                                                id="status-text",
                                                class_name="text-muted-foreground text-xs italic"
                                            )
                                        ]
                                    ),
                                    Row(
                                        class_name="gap-3 pt-3 border-t border-border justify-end",
                                        children=[
                                            Button(
                                                "Focus Bob's Age (Server Bound Method)",
                                                on_click=ctx.callback(handle_set_focus),
                                                variant="outline",
                                                class_name="text-xs"
                                            ),
                                            Button(
                                                "Focus Charlie's Notes (Client Bound Method)",
                                                on_click=ctx.bound_js("spreadsheet-grid", "setFocusLocation", {"rowId": "3", "columnId": "notes"}),
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
            ),
            
            # TAB CONTENT 2: CALCULATED INVOICE
            Container(
                id="container-invoice",
                class_name="space-y-4" if active_tab == "invoice" else "space-y-4 hidden",
                children=[
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("2. Interactive Invoice & Calculated Cells"),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    Text(
                                        "Demonstrates reactive programming: edit Qty, Price, or Tax Rate cells. The grid instantly "
                                        "recomputes Subtotal and Total columns on the server, updating the sticky bottom summary rows.",
                                        class_name="text-muted-foreground text-sm"
                                    ),
                                    RefastGrid(
                                        id="invoice-grid",
                                        columns=invoice_columns,
                                        rows=make_invoice_rows(invoice_data),
                                        sticky_top_rows=1,
                                        sticky_bottom_rows=2,
                                        enable_range_selection=True,
                                        on_cells_changed=ctx.callback(handle_invoice_changed),
                                        class_name="h-80 min-w-full my-2 border border-border shadow-inner"
                                    ),
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Text(
                                                "Invoice Status: Fully calculated",
                                                id="invoice-status",
                                                class_name="text-xs text-muted-foreground font-medium"
                                            ),
                                            Row(
                                                class_name="gap-2",
                                                children=[
                                                    Button(
                                                        "Add Item Line",
                                                        on_click=ctx.callback(handle_add_invoice_row),
                                                        variant="outline",
                                                        class_name="text-xs"
                                                    ),
                                                    Button(
                                                        "Clear Invoice",
                                                        on_click=ctx.callback(handle_clear_invoice),
                                                        variant="destructive",
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
                ]
            ),
            
            # TAB CONTENT 3: COLLAPSIBLE TREE GRID
            Container(
                id="container-tree",
                class_name="space-y-4" if active_tab == "tree" else "space-y-4 hidden",
                children=[
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("3. Organization Budget Planner (Collapsible Tree Grid)"),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    Text(
                                        "Demonstrates tree nodes and grouping with Chevron cells. Click chevrons to fold/expand rows. "
                                        "Parent node values (Budgets, Headcount, Spent) are sum-aggregated dynamically from child teams.",
                                        class_name="text-muted-foreground text-sm"
                                    ),
                                    RefastGrid(
                                        id="tree-grid",
                                        columns=tree_columns,
                                        rows=make_tree_rows(get_visible_tree_nodes(tree_data)),
                                        sticky_top_rows=1,
                                        on_cells_changed=ctx.callback(handle_tree_changed),
                                        class_name="h-96 min-w-full my-2 border border-border shadow-inner"
                                    ),
                                    Row(
                                        class_name="justify-between items-center",
                                        children=[
                                            Text(
                                                "Tree Status: Root node expanded",
                                                id="tree-status",
                                                class_name="text-xs text-muted-foreground font-medium"
                                            ),
                                            Row(
                                                class_name="gap-2",
                                                children=[
                                                    Button(
                                                        "Expand All",
                                                        on_click=ctx.callback(handle_expand_all),
                                                        variant="outline",
                                                        class_name="text-xs"
                                                    ),
                                                    Button(
                                                        "Collapse All",
                                                        on_click=ctx.callback(handle_collapse_all),
                                                        variant="outline",
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
                ]
            ),
            
            # TAB CONTENT 4: LIVE TICKER
            Container(
                id="container-live",
                class_name="space-y-4" if active_tab == "live" else "space-y-4 hidden",
                children=[
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("4. Live Ticker (Real-Time Price Updates)"),
                                ]
                            ),
                            CardContent(
                                class_name="space-y-4",
                                children=[
                                    Text(
                                        "Demonstrates real-time server pushing updates. Start the simulator below to feed randomized market ticks. "
                                        "Cells will flash green or red dynamically depending on price tick direction, styled via Tailwind.",
                                        class_name="text-muted-foreground text-sm"
                                    ),
                                    RefastGrid(
                                        id="crypto-grid",
                                        columns=crypto_columns,
                                        rows=make_crypto_rows(crypto_data),
                                        sticky_top_rows=1,
                                        class_name="h-80 min-w-full my-2 border border-border shadow-inner"
                                    ),
                                    Row(
                                        class_name="justify-between items-center bg-muted/40 p-4 rounded-lg border border-border",
                                        children=[
                                            Text(
                                                "Status: Live updates paused",
                                                id="crypto-status",
                                                class_name="text-sm font-semibold text-muted-foreground"
                                            ),
                                            Button(
                                                "Start Auto-Refresh",
                                                id="toggle-refresh-btn",
                                                on_click=ctx.callback(toggle_auto_refresh),
                                                variant="default",
                                                class_name="text-xs font-semibold px-4"
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
        ]
    )

# Expose router to FastAPI app
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
