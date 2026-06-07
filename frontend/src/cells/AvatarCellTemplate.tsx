import React from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface AvatarCell extends Cell {
  type: 'avatar';
  name: string;
  avatarUrl?: string;
  subtext?: string;
}

export class AvatarCellTemplate implements CellTemplate<AvatarCell> {
  getCompatibleCell(uncertainCell: Uncertain<AvatarCell>): Compatible<AvatarCell> {
    const name = uncertainCell.name || 'User';
    const avatarUrl = uncertainCell.avatarUrl || '';
    const subtext = uncertainCell.subtext || '';
    return { ...uncertainCell, name, avatarUrl, subtext, text: name };
  }

  update(cell: Compatible<AvatarCell>, cellToMerge: UncertainCompatible<AvatarCell>): Compatible<AvatarCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  getInitials(name: string): string {
    const parts = name.trim().split(/\s+/);
    if (parts.length === 0 || !parts[0]) return '?';
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }

  render(
    cell: Compatible<AvatarCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<AvatarCell>, commit: boolean) => void
  ): React.ReactNode {
    const initials = this.getInitials(cell.name);

    return (
      <div className="flex items-center w-full h-full px-0 gap-2 select-none overflow-hidden">
        {/* Avatar container */}
        <div className="relative flex-shrink-0 w-7 h-7 rounded-full bg-muted border border-border flex items-center justify-center overflow-hidden">
          {cell.avatarUrl ? (
            <img
              src={cell.avatarUrl}
              alt={cell.name}
              className="w-full h-full object-cover z-10"
              onError={(e) => {
                // If image fails, hide image element
                (e.target as HTMLElement).style.display = 'none';
              }}
            />
          ) : null}
          {/* Initials fallback (rendered underneath the image) */}
          <span className="text-[10px] font-bold text-muted-foreground absolute">
            {initials}
          </span>
        </div>
        
        {/* Text Details */}
        <div className="flex flex-col min-w-0 leading-none">
          <span className="text-xs font-semibold truncate text-foreground mb-0.5">{cell.name}</span>
          {cell.subtext && (
            <span className="text-[10px] text-muted-foreground truncate">{cell.subtext}</span>
          )}
        </div>
      </div>
    );
  }
}
