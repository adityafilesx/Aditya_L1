# Agent Architecture

## Base Interface
All agents extend `BaseAgent` and implement `async execute(subtask, context) -> AgentResult`.

## AgentResult
```python
@dataclass
class AgentResult:
    agent_name: str
    content: str          # Markdown-formatted output
    confidence: float     # 0.0 to 1.0
    sources: List[Source]  # Traceable sources
    data: Dict            # Raw structured data
    warnings: List[str]   # Uncertainty flags
```

## Registered Agents

| Agent | Module | Responsibilities |
|---|---|---|
| PhysicsAgent | `physics_engine/` | Temperature, EM, entropy, Neupert, wavelets |
| PredictionAgent | `ai_engine/`, `decision/` | Forecast, calibration, ensemble agreement |
| DigitalTwinAgent | `digital_twin/` | Region state, similarity, 3D state |
| KnowledgeGraphAgent | `knowledge_graph/` | Search, relationships, communities |
| MissionAgent | `mission_intelligence/` | Risk indices, recommendations |
| SpectralAgent | `physics_engine/spectral` | Spectral fits, thermal models |
| LiteratureAgent | (mocked) | NASA ADS, arXiv (stub) |
| ExperimentAgent | `ai_engine/` | Benchmarks, model registry |
| ReportAgent | All modules | Multi-section report generation |
| ReviewAgent | All results | Evidence validation, confidence check |
