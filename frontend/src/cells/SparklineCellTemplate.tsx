import React from 'react';
import { CellTemplate, Cell, Compatible, Uncertain, UncertainCompatible } from '@silevis/reactgrid';

export interface SparklineCell extends Cell {
  type: 'sparkline';
  values: number[];
  chartType?: 'line' | 'bar';
}

export class SparklineCellTemplate implements CellTemplate<SparklineCell> {
  getCompatibleCell(uncertainCell: Uncertain<SparklineCell>): Compatible<SparklineCell> {
    const values = Array.isArray(uncertainCell.values) ? uncertainCell.values : [];
    const chartType = uncertainCell.chartType || 'line';
    const text = values.join(',');
    return { ...uncertainCell, values, chartType, text };
  }

  update(cell: Compatible<SparklineCell>, cellToMerge: UncertainCompatible<SparklineCell>): Compatible<SparklineCell> {
    return this.getCompatibleCell(cellToMerge);
  }

  render(
    cell: Compatible<SparklineCell>,
    isInEditMode: boolean,
    onCellChanged: (cell: Compatible<SparklineCell>, commit: boolean) => void
  ): React.ReactNode {
    const { values, chartType } = cell;
    if (values.length === 0) {
      return <div className="text-muted-foreground text-xs italic px-0">No data</div>;
    }

    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;

    const height = 24;
    const width = 80;

    if (chartType === 'bar') {
      const barCount = values.length;
      const gap = 2;
      const barWidth = Math.max((width - (barCount - 1) * gap) / barCount, 1.5);

      return (
        <div className="flex items-center justify-center w-full h-full px-0">
          <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
            {values.map((val, i) => {
              const barHeight = Math.max(((val - min) / range) * (height - 4), 2);
              const x = i * (barWidth + gap);
              const y = height - barHeight - 2;
              return (
                <rect
                  key={i}
                  x={x}
                  y={y}
                  width={barWidth}
                  height={barHeight}
                  fill="hsl(var(--primary))"
                  rx={0.5}
                />
              );
            })}
          </svg>
        </div>
      );
    }

    // Line Chart
    const points = values.map((val, i) => {
      const x = values.length > 1 ? (i / (values.length - 1)) * (width - 4) + 2 : width / 2;
      const y = height - ((val - min) / range) * (height - 6) - 3;
      return { x, y };
    });

    const pathData = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');

    return (
      <div className="flex items-center justify-center w-full h-full px-0">
        <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
          <path
            d={pathData}
            fill="none"
            stroke="hsl(var(--primary))"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    );
  }
}
