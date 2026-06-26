# Scientific Knowledge Graph Architecture

## 1. Overview
The Scientific Knowledge Graph serves as the mission memory for Aditya-L1. It unifies all data streams into a single queryable graph.

## 2. Technology Stack
- **Graph Visualization**: `React Flow` with `elkjs` for hierarchical layout rendering.
- **State Management**: `Zustand` (`graphStore.ts`).
- **Graph Schema**: Strongly typed generic graph structure built for direct mapping to Neo4j.
- **AI Compatibility**: Each node contains an `embeddings` property reserved for PyTorch Geometric (GNNs) and GraphRAG text embeddings.

## 3. Data Integration Strategy
- **Digital Twin**: Directly integrated via `workspaceStore.activeRegion` and `cursorTime`. Selecting a graph node physically alters the WebGL canvas.
- **Mission Timeline**: Graph interactions synchronize timestamps globally.

## 4. Performance Limits
- Max simultaneous virtualized nodes (React Flow limits): ~20,000.
- Server-side bounding box culling required beyond this limit.
