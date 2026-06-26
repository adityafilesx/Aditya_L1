import { memo } from 'react';
import { BaseEdge, EdgeLabelRenderer, getBezierPath } from '@xyflow/react';
import type { EdgeProps } from '@xyflow/react';
import type { AppEdge } from '../../store/graphStore';

const EDGE_COLORS: Record<string, string> = {
  CAUSAL: '#fe693c', // Secondary (orange)
  TEMPORAL: '#4140d1', // Primary
  SIMILARITY: '#10b981', // Green
  PHYSICAL: '#9c27b0', // Purple
  Default: '#c7c4d7',
};

export const ScientificEdge = memo(({
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  data,
  markerEnd,
  selected,
}: EdgeProps<AppEdge>) => {
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const edgeColor = EDGE_COLORS[data?.type || ''] || EDGE_COLORS.Default;
  const strokeWidth = (data?.weight || 1) * (selected ? 2 : 1.5);
  const opacity = selected ? 1 : (data?.confidence || 1);
  const animated = data?.type === 'CAUSAL' || data?.type === 'PREDICTION';

  return (
    <>
      <BaseEdge 
        path={edgePath} 
        markerEnd={markerEnd} 
        style={{
          ...style,
          strokeWidth,
          stroke: edgeColor,
          opacity,
          animation: animated ? 'dash 1s linear infinite' : 'none',
          strokeDasharray: animated ? '4 4' : 'none'
        }} 
      />
      <EdgeLabelRenderer>
        <div
          className="absolute bg-surface/80 backdrop-blur border border-surface-variant px-2 py-0.5 rounded font-data-mono text-[9px] text-on-surface-variant font-bold shadow-sm pointer-events-auto cursor-pointer hover:text-primary transition-colors z-20"
          style={{
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
          }}
        >
          {data?.type}
          {data?.confidence && <span className="ml-1 opacity-70">{(data.confidence * 100).toFixed(0)}%</span>}
        </div>
      </EdgeLabelRenderer>
      
      {/* Invisible thicker edge for easier clicking/hovering */}
      <BaseEdge 
        path={edgePath} 
        style={{ strokeWidth: 15, stroke: 'transparent', cursor: 'pointer' }} 
      />
    </>
  );
});

ScientificEdge.displayName = 'ScientificEdge';
