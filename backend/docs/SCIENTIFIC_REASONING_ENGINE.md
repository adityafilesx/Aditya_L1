# Scientific Reasoning Engine (SRE) Architecture

## Overview
The SRE is the intelligence layer of the Aditya-L1 platform. It transforms the AI Scientist UI from a mocked prototype into a production-grade multi-agent reasoning system.

## Pipeline
```
User Query → Context Builder → Planner → Router → Agents → Reviewer → Response Builder → Frontend (SSE)
```

## Core Modules

| Module | File | Purpose |
|---|---|---|
| Context Builder | `reasoning/context_builder.py` | Gathers full platform state from AppState |
| Planner | `reasoning/planner.py` | Classifies intent, decomposes into SubTasks |
| Router | `reasoning/router.py` | Dispatches SubTasks to agents with timeouts |
| Reasoner | `reasoning/reasoner.py` | Top-level orchestrator (sync + streaming) |
| Memory | `reasoning/memory.py` | In-memory conversation store |
| Workflow | `reasoning/workflow.py` | Pre-defined multi-step scientific workflows |

## Intent Classification
The Planner classifies user queries into: `explain`, `predict`, `compare`, `report`, `literature`, `experiment`, `mission`, `general`.

## Agent Architecture
10 specialized agents, all extending `BaseAgent`:
- Physics, Prediction, Digital Twin, Knowledge Graph, Mission
- Spectral, Literature, Experiment, Report, Review

## Streaming
The `/api/reasoning/chat` endpoint streams responses via SSE. Each agent result is yielded as a separate event, enabling progressive rendering in the frontend.

## Future Hooks
The architecture is designed for:
- **GraphRAG**: Replace keyword-based KG search with vector similarity
- **LangGraph**: Replace the Planner with an LLM-based agentic planner
- **MCP/A2A**: External model and agent integration via tool registry
- **PINNs/GNNs**: Physics-informed neural networks as additional agents
