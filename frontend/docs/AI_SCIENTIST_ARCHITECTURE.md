# AI Scientist Architecture

## 1. Overview
The AI Scientist is the intelligent reasoning layer of the Aditya-L1 platform. It leverages LangGraph and GraphRAG to traverse the entire application state (Knowledge Graph, Mission Timeline, Digital Twin) to provide scientifically grounded answers and predictions.

## 2. Technology Stack
- **Frontend Engine**: `react-markdown`, `remark-math`, `rehype-katex` for rendering complex equations and citations.
- **State Management**: `aiScientistStore.ts` utilizing Zustand. This store actively listens to `workspaceStore` and `graphStore` to maintain context.
- **Backend Infrastructure (Pending)**: LangGraph (Agentic flow), FastAPI (Streaming responses), Neo4j/VectorDB (Knowledge Retrieval).

## 3. UI Structure
- **Left Pane (Memory)**: Historic research sessions and experiment logs.
- **Center Pane (Workspace)**: The active module (Copilot, XAI, Experiment Manager, Literature, Report Builder).
- **Right Pane (Context)**: A real-time readout of what the AI currently "sees" in the platform.

## 4. Security & Transparency
- All AI responses must include a `confidence` metric.
- All AI responses must array `sources` (e.g., specific graph nodes, papers, or assets) used to form the conclusion.
- Direct integration with the Explainability Workspace guarantees that underlying model features (e.g., XGBoost feature importance) are accessible.
