# Graph Schema Definition

## Nodes
Every node implements `GraphNodeProperties`:
```typescript
interface GraphNodeProperties {
  id: string; // UUID or unique hash
  label: string;
  type: ScientificNodeType; // Specific taxonomy class
  timestamp: string; // ISO 8601
  metadata: Record<string, any>; // Flexible JSON
  embeddings?: number[]; // Vector embedding of metadata
  source?: string;
  confidence?: number;
}
```

## Edges
Every edge implements `GraphEdgeProperties`:
```typescript
interface GraphEdgeProperties {
  id: string;
  source: string;
  target: string;
  type: ScientificEdgeType;
  weight: number;
  confidence: number;
  timestamp: string;
  direction: 'directed' | 'undirected' | 'bidirectional';
  metadata: Record<string, any>;
}
```
