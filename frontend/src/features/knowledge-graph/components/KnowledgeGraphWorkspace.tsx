import { useEffect, useCallback } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useReactFlow,
  ReactFlowProvider,
  BackgroundVariant,
} from '@xyflow/react';
import type { NodeMouseHandler } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import { useGraphStore } from '../store/graphStore';
import type { AppNode, AppEdge } from '../store/graphStore';
import type { NodeTypes, EdgeTypes } from '@xyflow/react';
import { ScientificNode } from './nodes/ScientificNode';
import { ScientificEdge } from './edges/ScientificEdge';
import { GraphToolbar } from './GraphToolbar';
import { getLayoutedElements } from '../utils/layout';

const nodeTypes: NodeTypes = {
  scientific: ScientificNode as any,
};

const edgeTypes: EdgeTypes = {
  scientific: ScientificEdge as any,
};

// Generate some dummy nodes for demonstration
const initialNodes: AppNode[] = [
  { id: 'mission-1', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'Mission', label: 'Aditya-L1', timestamp: '2023-09-02T11:50:00Z', metadata: { status: 'Active' }, confidence: 1.0 } },
  { id: 'sensor-1', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'Sensor', label: 'SUIT', timestamp: '2023-09-02T11:50:00Z', metadata: { state: 'Nominal' }, confidence: 0.99 } },
  { id: 'sensor-2', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'Sensor', label: 'SoLEXS', timestamp: '2023-09-02T11:50:00Z', metadata: { state: 'Nominal' }, confidence: 0.99 } },
  { id: 'ar-1', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'ActiveRegion', label: 'AR13872', timestamp: '2026-06-25T10:00:00Z', metadata: { class: 'Beta-Gamma', area: 450, regionId: 'AR13872', lat: 15, lon: -25 }, confidence: 0.95 } },
  { id: 'feat-1', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'PhysicsFeature', label: 'Magnetic Shear', timestamp: '2026-06-25T11:00:00Z', metadata: { value: 'High', threshold: 0.8 }, confidence: 0.88 } },
  { id: 'pred-1', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'Prediction', label: 'M-Class Probability', timestamp: '2026-06-25T11:30:00Z', metadata: { model: 'XGBoost', prob: 0.85 }, confidence: 0.85 } },
  { id: 'flare-1', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'Flare', label: 'M4.2 Flare', timestamp: '2026-06-25T14:12:00Z', metadata: { peakFlux: '4.2e-5', duration: '35m' }, confidence: 0.98 } },
  { id: 'cme-1', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'CME', label: 'Halo CME', timestamp: '2026-06-25T14:45:00Z', metadata: { velocity: '1200 km/s', width: 360 }, confidence: 0.92 } },
  { id: 'asset-1', type: 'scientific', position: { x: 0, y: 0 }, data: { type: 'ScientificImage', label: 'Spectral Fit (Hardness)', timestamp: '2026-06-25T14:20:00Z', metadata: { event: 'M4.2' }, confidence: 1.0 } },
];

const initialEdges: AppEdge[] = [
  { id: 'e1', source: 'mission-1', target: 'sensor-1', type: 'scientific', data: { type: 'PHYSICAL', weight: 1, confidence: 1, timestamp: '', direction: 'directed', source: 'system', metadata: {} } },
  { id: 'e2', source: 'mission-1', target: 'sensor-2', type: 'scientific', data: { type: 'PHYSICAL', weight: 1, confidence: 1, timestamp: '', direction: 'directed', source: 'system', metadata: {} } },
  { id: 'e3', source: 'sensor-1', target: 'ar-1', type: 'scientific', data: { type: 'OBSERVATION' as any, weight: 1, confidence: 0.9, timestamp: '', direction: 'directed', source: 'system', metadata: {} } },
  { id: 'e4', source: 'ar-1', target: 'feat-1', type: 'scientific', data: { type: 'PHYSICS', weight: 2, confidence: 0.9, timestamp: '', direction: 'directed', source: 'pipeline', metadata: {} } },
  { id: 'e5', source: 'feat-1', target: 'pred-1', type: 'scientific', data: { type: 'CAUSAL', weight: 3, confidence: 0.85, timestamp: '', direction: 'directed', source: 'ai', metadata: {} } },
  { id: 'e6', source: 'pred-1', target: 'flare-1', type: 'scientific', data: { type: 'PREDICTION', weight: 4, confidence: 0.85, timestamp: '', direction: 'directed', source: 'ai', metadata: {} } },
  { id: 'e7', source: 'flare-1', target: 'cme-1', type: 'scientific', data: { type: 'CAUSAL', weight: 3, confidence: 0.92, timestamp: '', direction: 'directed', source: 'physics', metadata: {} } },
  { id: 'e8', source: 'sensor-2', target: 'flare-1', type: 'scientific', data: { type: 'OBSERVATION' as any, weight: 1, confidence: 0.98, timestamp: '', direction: 'directed', source: 'pipeline', metadata: {} } },
  { id: 'e9', source: 'flare-1', target: 'asset-1', type: 'scientific', data: { type: 'RESEARCH', weight: 1, confidence: 1, timestamp: '', direction: 'directed', source: 'pipeline', metadata: {} } },
];

const WorkspaceInner: React.FC = () => {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect, setNodes, setEdges, setSelectedNode } = useGraphStore();
  const { fitView } = useReactFlow();

  const handleLayout = useCallback(async () => {
    const { layoutedNodes, layoutedEdges } = await getLayoutedElements(nodes, edges, 'RIGHT');
    setNodes([...layoutedNodes]);
    setEdges([...layoutedEdges]);
    window.requestAnimationFrame(() => {
      fitView({ padding: 0.2, duration: 800 });
    });
  }, [nodes, edges, setNodes, setEdges, fitView]);

  // Initial load
  useEffect(() => {
    if (nodes.length === 0) {
      getLayoutedElements(initialNodes, initialEdges, 'RIGHT').then(({ layoutedNodes, layoutedEdges }) => {
        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
        setTimeout(() => fitView({ padding: 0.2 }), 100);
      });
    }
  }, []);

  const onNodeClick: NodeMouseHandler = useCallback((_, node) => {
    setSelectedNode(node.id);
  }, [setSelectedNode]);

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
  }, [setSelectedNode]);

  return (
    <div className="w-full h-full relative bg-surface-container-highest">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        minZoom={0.1}
        maxZoom={1.5}
        className="scientific-graph"
      >
        <Background variant={BackgroundVariant.Dots} gap={24} size={2} color="#c7c4d7" />
        <Controls showInteractive={false} className="bg-surface border-surface-variant shadow-sm" />
        <MiniMap 
          nodeColor={(n) => {
            const t = n.data?.type as string;
            return t === 'Flare' ? '#fe693c' : t === 'CME' ? '#9c27b0' : t === 'Prediction' ? '#4140d1' : '#c7c4d7';
          }}
          maskColor="rgba(17, 19, 24, 0.7)"
          className="bg-surface border-surface-variant rounded shadow-sm" 
        />
        <GraphToolbar onLayout={handleLayout} />
      </ReactFlow>
    </div>
  );
};

export const KnowledgeGraphWorkspace: React.FC = () => {
  return (
    <ReactFlowProvider>
      <WorkspaceInner />
    </ReactFlowProvider>
  );
};
