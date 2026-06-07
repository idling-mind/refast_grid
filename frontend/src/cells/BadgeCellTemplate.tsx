import React from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface BadgeCell extends Cell {
  type: 'badge';
  text: string;
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'destructive' | 'info';
}

export class BadgeCellTemplate implements CellTemplate<BadgeCell> {
  getCompatibleCell(uncertainCell: Uncertain<BadgeCell>): Compatible<BadgeCell> {
    const text = uncertainCell.text || '';
    const variant = uncertainCell.variant || 'primary';
    return { ...uncertainCell, text, variant, value: NaN };
  }

  update(cell: Compatible<BadgeCell>, cellToMerge: UncertainCompatible<BadgeCell>): Compatible<BadgeCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<BadgeCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<BadgeCell>, commit: boolean) => void
  ): React.ReactNode {
    return (
      <div className="flex items-center justify-center w-full h-full px-0">
        <span className={`rg-badge rg-badge-${cell.variant || 'primary'}`}>
          {cell.text}
        </span>
      </div>
    );
  }
}
