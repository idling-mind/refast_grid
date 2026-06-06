/**
 * RefastGrid React Component
 *
 * This component wraps `@silevis/reactgrid` and maps its properties and callbacks
 * to the Refast system, enabling a feature-rich spreadsheet/grid component.
 */

import React, { useRef, useEffect, useState, useCallback } from 'react';
import {
  ReactGrid,
  Column,
  Row,
  Cell,
  CellChange,
  CellLocation,
  Highlight,
  Id,
  DropPosition
} from '@silevis/reactgrid';
import '@silevis/reactgrid/styles.css';
import './RefastGrid.css';
import { cn } from './utils';

export interface RefastGridProps {
  /** Component ID - used for targeting with ctx.bound_js() */
  id?: string;
  /** CSS classes to apply */
  className?: string;
  /** Additional inline styles */
  style?: React.CSSProperties;
  /** Refast internal ID for tracking */
  'data-refast-id'?: string;

  // ReactGrid Props
  /** Column definitions */
  columns: Column[];
  /** Row definitions with cells */
  rows: Row<Cell>[];
  /** Enables resizing on all header columns */
  enableColumnResizeOnAllHeaders?: boolean;
  /** Array of cells to highlight */
  highlights?: Highlight[];
  /** Number of sticky rows at the top */
  stickyTopRows?: number;
  /** Number of sticky rows at the bottom */
  stickyBottomRows?: number;
  /** Number of sticky columns on the left */
  stickyLeftColumns?: number;
  /** Number of sticky columns on the right */
  stickyRightColumns?: number;
  /** Enables fill handle feature */
  enableFillHandle?: boolean;
  /** Enables selecting range of cells */
  enableRangeSelection?: boolean;
  /** Enables row selection */
  enableRowSelection?: boolean;
  /** Enables column selection */
  enableColumnSelection?: boolean;
  
  // Focus positioning (controlled / initial)
  /** Controlled focus location */
  focusLocation?: CellLocation;
  /** Initial focus location */
  initialFocusLocation?: CellLocation;

  // Gating properties for drag-and-drop
  /** Allow reordering of rows (default is true if onRowsReordered is set) */
  canReorderRows?: boolean;
  /** Allow reordering of columns (default is true if onColumnsReordered is set) */
  canReorderColumns?: boolean;

  // Callbacks
  /** Triggered when cell values change */
  onCellsChanged?: (eventData: { changes: Array<{
    rowId: Id;
    columnId: Id;
    type: string;
    previousCell: Cell;
    newCell: Cell;
  }> }) => void;
  /** Triggered when active cell focus location changes */
  onFocusLocationChanged?: (eventData: { location: CellLocation }) => void;
  /** Triggered when column resizing finishes */
  onColumnResized?: (eventData: { columnId: Id; width: number; selectedColIds: Id[] }) => void;
  /** Triggered when row reordering finishes */
  onRowsReordered?: (eventData: { targetRowId: Id; rowIds: Id[]; dropPosition: DropPosition }) => void;
  /** Triggered when column reordering finishes */
  onColumnsReordered?: (eventData: { targetColumnId: Id; columnIds: Id[]; dropPosition: DropPosition }) => void;
}

export function RefastGrid({
  id,
  className,
  style,
  'data-refast-id': dataRefastId,
  columns,
  rows,
  enableColumnResizeOnAllHeaders = true,
  highlights,
  stickyTopRows = 0,
  stickyBottomRows = 0,
  stickyLeftColumns = 0,
  stickyRightColumns = 0,
  enableFillHandle = false,
  enableRangeSelection = false,
  enableRowSelection = false,
  enableColumnSelection = false,
  focusLocation,
  initialFocusLocation,
  canReorderRows = true,
  canReorderColumns = true,
  onCellsChanged,
  onFocusLocationChanged,
  onColumnResized,
  onRowsReordered,
  onColumnsReordered,
}: RefastGridProps): React.ReactElement {
  const wrapperRef = useRef<HTMLDivElement>(null);
  
  // Track visibility to handle initially hidden container rendering
  const [visibleKey, setVisibleKey] = useState(0);
  const wasVisibleRef = useRef(false);

  useEffect(() => {
    const element = wrapperRef.current;
    if (!element) return;

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const isVisibleNow = entry.contentRect.width > 0;
        if (isVisibleNow && !wasVisibleRef.current) {
          setVisibleKey(prev => prev + 1);
        }
        wasVisibleRef.current = isVisibleNow;
      }
    });

    observer.observe(element);
    return () => {
      observer.disconnect();
    };
  }, []);

  // Focus location override (used for programmatic changes)
  const [focusOverride, setFocusOverride] = useState<CellLocation | undefined>(
    focusLocation || initialFocusLocation
  );

  // Sync state when controlled prop changes from the server
  useEffect(() => {
    if (focusLocation) {
      setFocusOverride(focusLocation);
    }
  }, [focusLocation]);

  // Clear focus override after a short timeout so ReactGrid goes back to uncontrolled mode
  useEffect(() => {
    if (focusOverride) {
      const timer = setTimeout(() => {
        setFocusOverride(undefined);
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [focusOverride]);

  // Handle focus changes
  const handleFocusLocationChanged = useCallback((location: CellLocation) => {
    if (onFocusLocationChanged) {
      onFocusLocationChanged({ location });
    }
  }, [onFocusLocationChanged]);

  // Handle cell changes
  const handleCellsChanged = useCallback((changes: CellChange[]) => {
    if (onCellsChanged) {
      // Map changes into a clean serializable array for the server
      const mappedChanges = changes.map(change => ({
        rowId: change.rowId,
        columnId: change.columnId,
        type: change.type,
        previousCell: change.previousCell,
        newCell: change.newCell,
      }));
      onCellsChanged({ changes: mappedChanges });
    }
  }, [onCellsChanged]);

  // Handle column resize
  const handleColumnResized = useCallback((columnId: Id, width: number, selectedColIds: Id[]) => {
    setLocalColumns((prevColumns) => {
      return prevColumns.map(col => {
        if (col.columnId === columnId) {
          return { ...col, width };
        }
        return col;
      });
    });

    if (onColumnResized) {
      onColumnResized({ columnId, width, selectedColIds });
    }
  }, [onColumnResized]);

  // Handle row reorder
  const handleRowsReordered = useCallback((targetRowId: Id, rowIds: Id[], dropPosition: DropPosition) => {
    if (onRowsReordered) {
      onRowsReordered({ targetRowId, rowIds, dropPosition });
    }
  }, [onRowsReordered]);

  // Handle column reorder
  const handleColumnsReordered = useCallback((targetColumnId: Id, columnIds: Id[], dropPosition: DropPosition) => {
    if (onColumnsReordered) {
      onColumnsReordered({ targetColumnId, columnIds, dropPosition });
    }
  }, [onColumnsReordered]);

  // Validation functions for drag and drop reordering
  const handleCanReorderRows = useCallback((targetRowId: Id, rowIds: Id[], dropPosition: DropPosition): boolean => {
    return canReorderRows;
  }, [canReorderRows]);

  const handleCanReorderColumns = useCallback((targetColumnId: Id, columnIds: Id[], dropPosition: DropPosition): boolean => {
    return canReorderColumns;
  }, [canReorderColumns]);

  // Normalize helper for columns to support both snake_case and camelCase
  const normalizeColumns = useCallback((cols: Column[]): Column[] => {
    if (!cols) return [];
    return cols.map(c => ({
      columnId: c.columnId ?? (c as any).column_id,
      width: c.width,
      resizable: c.resizable,
      reorderable: c.reorderable,
    }));
  }, []);

  // Local state for column configuration and widths to support resizing
  const [localColumns, setLocalColumns] = useState<Column[]>(() => normalizeColumns(columns));
  const prevColumnsPropRef = useRef<Column[]>(normalizeColumns(columns));

  // Sync state when controlled columns prop changes from the server
  useEffect(() => {
    const nextNormalized = normalizeColumns(columns);
    const prevColumns = prevColumnsPropRef.current;
    
    setLocalColumns((currentLocal) => {
      return nextNormalized.map(nextCol => {
        const prevCol = prevColumns.find(c => c.columnId === nextCol.columnId);
        const currentLocalCol = currentLocal.find(c => c.columnId === nextCol.columnId);
        
        // If the column wasn't in the previous prop list, it's new, so use it as is
        if (!prevCol) {
          return nextCol;
        }
        
        // If the server explicitly updated this column's width prop, use the new width
        if (nextCol.width !== prevCol.width) {
          return nextCol;
        }
        
        // If we have a local version of this column (which might be resized), preserve it
        if (currentLocalCol) {
          return {
            ...nextCol,
            width: currentLocalCol.width,
          };
        }
        
        return nextCol;
      });
    });
    
    prevColumnsPropRef.current = nextNormalized;
  }, [columns, normalizeColumns]);

  // Normalize rows and cells to support both snake_case and camelCase
  const normalizedRows = React.useMemo(() => {
    if (!rows) return [];
    return rows.map(r => ({
      rowId: r.rowId ?? (r as any).row_id,
      height: r.height,
      reorderable: r.reorderable,
      cells: (r.cells || []).map((c: any) => {
        const normalizedCell: any = {
          type: c.type || 'text',
          style: c.style,
          className: c.className ?? c.class_name,
          nonEditable: c.nonEditable ?? c.non_editable,
        };

        if ('text' in c) normalizedCell.text = c.text;
        if ('value' in c) normalizedCell.value = c.value;
        if ('checked' in c) normalizedCell.checked = c.checked;
        if ('placeholder' in c) normalizedCell.placeholder = c.placeholder;
        if ('format' in c) normalizedCell.format = c.format;

        // Date and Time cells require JavaScript Date objects
        if ('date' in c) {
          normalizedCell.date = typeof c.date === 'string' && c.date ? new Date(c.date) : c.date;
        }
        if ('time' in c) {
          normalizedCell.time = typeof c.time === 'string' && c.time ? new Date(c.time) : c.time;
        }

        // Chevron cell support
        const isExpanded = c.isExpanded ?? c.is_expanded;
        if (isExpanded !== undefined) normalizedCell.isExpanded = isExpanded;

        const hasChildren = c.hasChildren ?? c.has_children;
        if (hasChildren !== undefined) normalizedCell.hasChildren = hasChildren;

        const parentId = c.parentId ?? c.parent_id;
        if (parentId !== undefined) normalizedCell.parentId = parentId;

        const indent = c.indent;
        if (indent !== undefined) normalizedCell.indent = indent;

        // Copy other fields
        for (const key of Object.keys(c)) {
          if (![
            'column_id', 'columnId', 'row_id', 'rowId', 
            'class_name', 'className', 'non_editable', 'nonEditable', 
            'style', 'type', 'isExpanded', 'is_expanded', 
            'hasChildren', 'has_children', 'parentId', 'parent_id', 
            'indent', 'date', 'time'
          ].includes(key)) {
            normalizedCell[key] = c[key];
          }
        }
        return normalizedCell;
      }),
    }));
  }, [rows]);

  // Expose bound methods on the DOM element for Refast client/server actions
  useEffect(() => {
    const wrapper = wrapperRef.current;
    if (!wrapper) return;

    // Set focus location programmatically
    (wrapper as any).setFocusLocation = (newLoc: CellLocation) => {
      setFocusOverride(newLoc);
    };

    // Cleanup: remove methods when component unmounts
    return () => {
      delete (wrapper as any).setFocusLocation;
    };
  }, []);

  return (
    <div
      ref={wrapperRef}
      id={id}
      className={cn(
        'refast_grid w-full overflow-auto bg-card text-card-foreground border border-border rounded-[var(--radius)]',
        className
      )}
      data-refast-id={dataRefastId}
      style={style}
    >
      {visibleKey > 0 && (
        <ReactGrid
          key={visibleKey}
          columns={localColumns}
          rows={normalizedRows}
          enableColumnResizeOnAllHeaders={enableColumnResizeOnAllHeaders}
          highlights={highlights}
          stickyTopRows={stickyTopRows}
          stickyBottomRows={stickyBottomRows}
          stickyLeftColumns={stickyLeftColumns}
          stickyRightColumns={stickyRightColumns}
          enableFillHandle={enableFillHandle}
          enableRangeSelection={enableRangeSelection}
          enableRowSelection={enableRowSelection}
          enableColumnSelection={enableColumnSelection}
          focusLocation={focusOverride}
          onFocusLocationChanged={handleFocusLocationChanged}
          onCellsChanged={handleCellsChanged}
          onColumnResized={handleColumnResized}
          onRowsReordered={handleRowsReordered}
          onColumnsReordered={handleColumnsReordered}
          canReorderRows={handleCanReorderRows}
          canReorderColumns={handleCanReorderColumns}
        />
      )}
    </div>
  );
}

RefastGrid.displayName = 'RefastGrid';
