import React from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface ButtonCell extends Cell {
  type: 'button';
  text: string;
  actionId: string;
  variant?: 'primary' | 'secondary' | 'destructive' | 'outline';
  clicked?: boolean;
}

export class ButtonCellTemplate implements CellTemplate<ButtonCell> {
  getCompatibleCell(uncertainCell: Uncertain<ButtonCell>): Compatible<ButtonCell> {
    const text = uncertainCell.text || 'Button';
    const actionId = uncertainCell.actionId || '';
    const variant = uncertainCell.variant || 'primary';
    const clicked = !!uncertainCell.clicked;
    return { ...uncertainCell, text, actionId, variant, clicked, value: NaN };
  }

  update(cell: Compatible<ButtonCell>, cellToMerge: UncertainCompatible<ButtonCell>): Compatible<ButtonCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<ButtonCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<ButtonCell>, commit: boolean) => void
  ): React.ReactNode {
    const variantClasses = {
      primary: 'bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm',
      secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
      destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90 shadow-sm',
      outline: 'border border-input bg-background text-foreground hover:bg-accent hover:text-accent-foreground',
    };

    const handleClick = (e: React.MouseEvent) => {
      e.stopPropagation();
      // Set clicked to true and trigger onCellChanged to send the event to the server
      onCellChanged(this.getCompatibleCell({ ...cell, clicked: true }), true);
    };

    return (
      <div className="flex items-center justify-center w-full h-full px-0">
        <button
          onClick={handleClick}
          className={`inline-flex items-center justify-center rounded-[var(--radius)] text-xs font-medium transition-colors h-7 w-full py-1 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring ${variantClasses[cell.variant || 'primary']}`}
        >
          {cell.text}
        </button>
      </div>
    );
  }
}
