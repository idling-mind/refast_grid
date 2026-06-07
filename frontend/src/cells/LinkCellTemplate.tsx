import React from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface LinkCell extends Cell {
  type: 'link';
  text: string;
  url: string;
  newTab?: boolean;
}

export class LinkCellTemplate implements CellTemplate<LinkCell> {
  getCompatibleCell(uncertainCell: Uncertain<LinkCell>): Compatible<LinkCell> {
    const text = uncertainCell.text || '';
    const url = uncertainCell.url || '#';
    const newTab = uncertainCell.newTab !== false;
    return { ...uncertainCell, text, url, newTab };
  }

  update(cell: Compatible<LinkCell>, cellToMerge: UncertainCompatible<LinkCell>): Compatible<LinkCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<LinkCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<LinkCell>, commit: boolean) => void
  ): React.ReactNode {
    return (
      <div className="flex items-center w-full h-full px-0 overflow-hidden select-none">
        <a
          href={cell.url}
          target={cell.newTab ? '_blank' : undefined}
          rel={cell.newTab ? 'noopener noreferrer' : undefined}
          onClick={(e) => {
            // Stop propagation to prevent cell selection on link click
            e.stopPropagation();
          }}
          className="text-primary hover:underline font-medium truncate"
        >
          {cell.text}
        </a>
      </div>
    );
  }
}
