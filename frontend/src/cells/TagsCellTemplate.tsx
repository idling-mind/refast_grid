import React from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface TagsCell extends Cell {
  type: 'tags';
  values: string[];
}

export class TagsCellTemplate implements CellTemplate<TagsCell> {
  getCompatibleCell(uncertainCell: Uncertain<TagsCell>): Compatible<TagsCell> {
    const values = Array.isArray(uncertainCell.values) ? uncertainCell.values : [];
    const text = values.join(', ');
    return { ...uncertainCell, values, text };
  }

  update(cell: Compatible<TagsCell>, cellToMerge: UncertainCompatible<TagsCell>): Compatible<TagsCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<TagsCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<TagsCell>, commit: boolean) => void
  ): React.ReactNode {
    return (
      <div className="flex items-center gap-1.5 w-full h-full px-0 overflow-x-auto select-none no-scrollbar">
        {cell.values.map((tag, i) => (
          <span
            key={i}
            className="inline-flex items-center px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground border border-border text-[10px] font-medium leading-none whitespace-nowrap"
          >
            {tag}
          </span>
        ))}
      </div>
    );
  }
}
