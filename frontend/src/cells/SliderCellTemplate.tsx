import React, { useState, useRef } from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface SliderCell extends Cell {
  type: 'slider';
  value: number;
  min?: number;
  max?: number;
  step?: number;
}

export class SliderCellTemplate implements CellTemplate<SliderCell> {
  getCompatibleCell(uncertainCell: Uncertain<SliderCell>): Compatible<SliderCell> {
    const value = typeof uncertainCell.value === 'number' ? uncertainCell.value : 0;
    const min = uncertainCell.min ?? 0;
    const max = uncertainCell.max ?? 100;
    const step = uncertainCell.step ?? 1;
    return { ...uncertainCell, value, min, max, step, text: value.toString() };
  }

  update(cell: Compatible<SliderCell>, cellToMerge: UncertainCompatible<SliderCell>): Compatible<SliderCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<SliderCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<SliderCell>, commit: boolean) => void
  ): React.ReactNode {
    const [isSliding, setIsSliding] = useState(false);
    const [currentVal, setCurrentVal] = useState(cell.value);
    const containerRef = useRef<HTMLDivElement>(null);

    const min = cell.min ?? 0;
    const max = cell.max ?? 100;
    const percent = ((currentVal - min) / (max - min)) * 100;

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const val = parseFloat(e.target.value);
      setCurrentVal(val);
    };

    const handleMouseUp = () => {
      setIsSliding(false);
      onCellChanged(this.getCompatibleCell({ ...cell, value: currentVal }), true);
    };

    return (
      <div ref={containerRef} className="relative flex items-center w-full h-full px-0 select-none">
        {/* Tooltip */}
        {isSliding && (
          <div
            className="absolute -top-7 z-30 px-2 py-0.5 text-[10px] font-semibold text-popover-foreground bg-popover border border-border rounded shadow-md pointer-events-none transform -translate-x-1/2 transition-all"
            style={{ left: `${percent}%` }}
          >
            {currentVal}
          </div>
        )}
        
        {/* Custom Range Input matching Shadcn Slider track/thumb */}
        <input
          type="range"
          min={min}
          max={max}
          step={cell.step ?? 1}
          value={currentVal}
          onChange={handleInputChange}
          onMouseDown={() => setIsSliding(true)}
          onMouseUp={handleMouseUp}
          onTouchStart={() => setIsSliding(true)}
          onTouchEnd={handleMouseUp}
          className="w-full h-1 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary focus:outline-none [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary [&::-webkit-slider-thumb]:shadow [&::-webkit-slider-thumb]:transition-transform [&::-webkit-slider-thumb]:hover:scale-110 [&::-moz-range-thumb]:h-3 [&::-moz-range-thumb]:w-3 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-primary [&::-moz-range-thumb]:border-none [&::-moz-range-thumb]:shadow [&::-moz-range-thumb]:transition-transform [&::-moz-range-thumb]:hover:scale-110"
        />
      </div>
    );
  }
}
