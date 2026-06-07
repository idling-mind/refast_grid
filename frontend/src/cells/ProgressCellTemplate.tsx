import React from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface ProgressCell extends Cell {
  type: 'progress';
  value: number;
}

export class ProgressCellTemplate implements CellTemplate<ProgressCell> {
  getCompatibleCell(uncertainCell: Uncertain<ProgressCell>): Compatible<ProgressCell> {
    const rawValue = typeof uncertainCell.value === 'number' ? uncertainCell.value : 0;
    // Normalize: if value is greater than 1, assume it's a percentage (e.g. 75 instead of 0.75)
    const value = rawValue > 1 ? rawValue / 100 : rawValue;
    const text = `${Math.round(value * 100)}%`;
    return { ...uncertainCell, value, text };
  }

  update(cell: Compatible<ProgressCell>, cellToMerge: UncertainCompatible<ProgressCell>): Compatible<ProgressCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<ProgressCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<ProgressCell>, commit: boolean) => void
  ): React.ReactNode {
    const percent = Math.min(Math.max(cell.value * 100, 0), 100);

    return (
      <div className="flex flex-col justify-center w-full h-full px-0 select-none">
        <div className="flex justify-between items-center text-[10px] text-muted-foreground mb-0.5">
          <span>{Math.round(percent)}%</span>
        </div>
        <div className="w-full h-1.5 bg-secondary rounded-full overflow-hidden">
          <div
            className="h-full bg-primary transition-all duration-300 rounded-full"
            style={{ width: `${percent}%` }}
          />
        </div>
      </div>
    );
  }
}
