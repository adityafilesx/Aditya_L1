import ELK from 'elkjs/lib/elk.bundled.js';
import type { AppNode, AppEdge } from '../store/graphStore';

const elk = new ELK();

// Node dimensions for ELK calculation
const NODE_WIDTH = 280;
const NODE_HEIGHT = 100;

export const getLayoutedElements = async (nodes: AppNode[], edges: AppEdge[], direction: 'RIGHT' | 'DOWN' = 'RIGHT') => {
  
  const graph = {
    id: 'root',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': direction,
      'elk.spacing.nodeNode': '60',
      'elk.layered.spacing.nodeNodeBetweenLayers': '100',
    },
    children: nodes.map((node) => ({
      ...node,
      width: NODE_WIDTH,
      height: NODE_HEIGHT,
    })),
    edges: edges.map((edge) => ({
      id: edge.id,
      sources: [edge.source],
      targets: [edge.target],
    })),
  };

  try {
    const layoutedGraph = await elk.layout(graph);
    
    // Map back ELK coordinates to React Flow nodes
    const layoutedNodes = nodes.map((node) => {
      const elkNode = layoutedGraph.children?.find((n) => n.id === node.id);
      if (!elkNode || elkNode.x === undefined || elkNode.y === undefined) {
        return node;
      }
      
      return {
        ...node,
        position: {
          x: elkNode.x,
          y: elkNode.y,
        },
      };
    });

    return { layoutedNodes, layoutedEdges: edges };
  } catch (err) {
    console.error('ELK Layout Error', err);
    return { layoutedNodes: nodes, layoutedEdges: edges };
  }
};
