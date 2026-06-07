import React, { useState } from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface RatingCell extends Cell {
  type: 'rating';
  value: number;
  max?: number;
  icon?: 'star' | 'dot' | 'heart';
}

export class RatingCellTemplate implements CellTemplate<RatingCell> {
  getCompatibleCell(uncertainCell: Uncertain<RatingCell>): Compatible<RatingCell> {
    const value = typeof uncertainCell.value === 'number' ? uncertainCell.value : 0;
    const max = uncertainCell.max || 5;
    const icon = uncertainCell.icon || 'star';
    return { ...uncertainCell, value, max, icon, text: value.toString() };
  }

  update(cell: Compatible<RatingCell>, cellToMerge: UncertainCompatible<RatingCell>): Compatible<RatingCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<RatingCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<RatingCell>, commit: boolean) => void
  ): React.ReactNode {
    const [hoverValue, setHoverValue] = useState<number | null>(null);
    const max = cell.max || 5;
    const activeValue = hoverValue !== null ? hoverValue : cell.value;

    const renderIcon = (index: number) => {
      const isFilled = index <= activeValue;
      const size = "w-4 h-4 cursor-pointer transition-all duration-150 hover:scale-125";
      
      switch (cell.icon) {
        case 'heart':
          return (
            <svg
              className={size}
              viewBox="0 0 24 24"
              stroke={isFilled ? "hsl(var(--destructive))" : "hsl(var(--muted-foreground) / 0.35)"}
              fill={isFilled ? "hsl(var(--destructive))" : "none"}
              strokeWidth="2"
            >
              <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
            </svg>
          );
        case 'dot':
          return (
            <svg
              className={size}
              viewBox="0 0 24 24"
            >
              <circle
                cx="12"
                cy="12"
                r="6"
                fill={isFilled ? "hsl(var(--primary))" : "hsl(var(--muted-foreground) / 0.2)"}
              />
            </svg>
          );
        case 'star':
        default:
          return (
            <svg
              className={size}
              viewBox="0 0 24 24"
              stroke={isFilled ? "hsl(var(--primary))" : "hsl(var(--muted-foreground) / 0.35)"}
              fill={isFilled ? "hsl(var(--primary))" : "none"}
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
          );
      }
    };

    return (
      <div className="flex items-center justify-center w-full h-full gap-0.5 px-0 select-none">
        {Array.from({ length: max }).map((_, i) => {
          const index = i + 1;
          return (
            <div
              key={index}
              onMouseEnter={() => setHoverValue(index)}
              onMouseLeave={() => setHoverValue(null)}
              onClick={() => onCellChanged(this.getCompatibleCell({ ...cell, value: index }), true)}
            >
              {renderIcon(index)}
            </div>
          );
        })}
      </div>
    );
  }
}
