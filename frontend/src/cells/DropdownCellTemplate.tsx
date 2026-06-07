import React, { useState, useRef, useEffect } from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface DropdownOption {
  value: string;
  label: string;
}

export interface DropdownCell extends Cell {
  type: 'dropdown';
  value: string;
  options: DropdownOption[];
}

const DropdownCellComponent: React.FC<{
  cell: Compatible<DropdownCell>;
  onCellChanged: (cell: Compatible<DropdownCell>, commit: boolean) => void;
}> = ({ cell, onCellChanged }) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const selectedOption = cell.options.find(o => o.value === cell.value);
  const label = selectedOption ? selectedOption.label : cell.value;

  useEffect(() => {
    if (!isOpen) return;
    const handleOutsideClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    // Use mousedown with capture to intercept clicks early
    document.addEventListener('mousedown', handleOutsideClick, true);
    return () => document.removeEventListener('mousedown', handleOutsideClick, true);
  }, [isOpen]);

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    setIsOpen(!isOpen);
  };

  const handleSelect = (optionValue: string, e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    setIsOpen(false);
    
    const template = new DropdownCellTemplate();
    onCellChanged(template.getCompatibleCell({ ...cell, value: optionValue }), true);
  };

  return (
    <div
      ref={containerRef}
      className="relative flex items-center justify-between w-full h-full px-3 select-none"
    >
      <div
        onClick={handleToggle}
        className="flex items-center justify-between w-full h-full cursor-pointer"
      >
        <span className="truncate">{label}</span>
        <span className="text-muted-foreground/45 text-[9px] ml-1 flex-shrink-0">▼</span>
      </div>

      {isOpen && (
        <div
          className="absolute left-0 w-full min-w-[120px] bg-popover text-popover-foreground border border-border rounded-md shadow-md z-50 py-1"
          style={{ top: '100%', marginTop: '2px' }}
        >
          {cell.options.map((opt) => (
            <div
              key={opt.value}
              onClick={(e) => handleSelect(opt.value, e)}
              className={`px-3 py-1.5 text-xs cursor-pointer truncate transition-colors hover:bg-accent hover:text-accent-foreground ${
                opt.value === cell.value ? 'bg-accent/50 font-medium' : ''
              }`}
            >
              {opt.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export class DropdownCellTemplate implements CellTemplate<DropdownCell> {
  getCompatibleCell(uncertainCell: Uncertain<DropdownCell>): Compatible<DropdownCell> {
    const value = uncertainCell.value || '';
    const options = uncertainCell.options || [];
    const option = options.find(o => o.value === value);
    const text = option ? option.label : value;
    return { ...uncertainCell, value, options, text };
  }

  update(cell: Compatible<DropdownCell>, cellToMerge: UncertainCompatible<DropdownCell>): Compatible<DropdownCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<DropdownCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<DropdownCell>, commit: boolean) => void
  ): React.ReactNode {
    return <DropdownCellComponent cell={cell} onCellChanged={onCellChanged} />;
  }
}
