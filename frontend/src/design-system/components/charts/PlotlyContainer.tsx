import React, { memo } from 'react';
import Plot from 'react-plotly.js';
import type { Layout, Data, Config } from 'plotly.js';
import { useWorkspaceStore } from '../../../realtime/workspaceStore';

interface PlotlyContainerProps {
  data: Data[];
  layout?: Partial<Layout>;
  config?: Partial<Config>;
  className?: string;
  onHover?: (data: any) => void;
  syncCursor?: boolean;
}

export const PlotlyContainer: React.FC<PlotlyContainerProps> = memo(({
  data,
  layout = {},
  config = {},
  className = "",
  onHover,
  syncCursor = false
}) => {
  const setGlobalCursor = useWorkspaceStore(state => state.setCursorTime);
  const globalCursorTime = useWorkspaceStore(state => state.globalCursorTime);

  const defaultLayout: Partial<Layout> = {
    autosize: true,
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { family: 'Inter, sans-serif', color: '#a0a0a0' },
    margin: { t: 20, r: 20, b: 40, l: 40 },
    xaxis: {
      gridcolor: 'rgba(255,255,255,0.05)',
      zerolinecolor: 'rgba(255,255,255,0.1)',
      showline: true,
      linecolor: 'rgba(255,255,255,0.1)'
    },
    yaxis: {
      gridcolor: 'rgba(255,255,255,0.05)',
      zerolinecolor: 'rgba(255,255,255,0.1)',
      showline: true,
      linecolor: 'rgba(255,255,255,0.1)'
    },
    showlegend: true,
    legend: {
      orientation: 'h',
      y: 1.1,
      font: { color: '#ffffff' }
    },
    shapes: syncCursor && globalCursorTime ? [
      {
        type: 'line',
        x0: globalCursorTime,
        x1: globalCursorTime,
        y0: 0,
        y1: 1,
        yref: 'paper',
        line: { color: 'rgba(255,0,0,0.5)', width: 2, dash: 'dot' }
      }
    ] : [],
    ...layout
  };

  const defaultConfig: Partial<Config> = {
    displaylogo: false,
    responsive: true,
    modeBarButtonsToRemove: ['lasso2d'],
    ...config
  };

  return (
    <div className={`w-full h-full relative ${className}`}>
      <Plot
        data={data}
        layout={defaultLayout}
        config={defaultConfig}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
        onHover={(e) => {
          if (syncCursor && e.points.length > 0) {
            // Plotly gives strings for dates, convert to timestamp if needed
            const x = e.points[0].x;
            if (typeof x === 'number') {
              setGlobalCursor(x);
            } else if (typeof x === 'string') {
              setGlobalCursor(new Date(x).getTime());
            }
          }
          if (onHover) onHover(e);
        }}
      />
    </div>
  );
});

PlotlyContainer.displayName = 'PlotlyContainer';
