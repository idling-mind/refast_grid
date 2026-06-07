import React, { useRef } from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface ColorCell extends Cell {
  type: 'color';
  value: string;
}

export class ColorCellTemplate implements CellTemplate<ColorCell> {
  getCompatibleCell(uncertainCell: Uncertain<ColorCell>): Compatible<ColorCell> {
    const value = uncertainCell.value || '#000000';
    return { ...uncertainCell, value, text: value };
  }

  update(cell: Compatible<ColorCell>, cellToMerge: UncertainCompatible<ColorCell>): Compatible<ColorCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<ColorCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<ColorCell>, commit: boolean) => void
  ): React.ReactNode {
    const inputRef = useRef<HTMLInputElement>(null);

    const handleSwatchClick = (e: React.MouseEvent) => {
      e.stopPropagation();
      inputRef.current?.click();
    };

    return (
      <div className="flex items-center w-full h-full px-0 gap-2 select-none relative">
        <div
          onClick={handleSwatchClick}
          className="w-5 h-5 rounded-full border border-border cursor-pointer shadow-sm flex-shrink-0 hover:scale-105 transition-transform"
          style={{ backgroundColor: cell.value }}
        />
        <span className="font-mono text-[11px] text-muted-foreground truncate">{cell.value}</span>
        
        {/* Hidden native color input */}
        <input
          ref={inputRef}
          type="color"
          value={cell.value}
          onChange={(e) => {
            onCellChanged(this.getCompatibleCell({ ...cell, value: e.target.value }), true);
          }}
          className="absolute opacity-0 pointer-events-none w-0 h-0"
        />
      </div>
    );
  }
}
