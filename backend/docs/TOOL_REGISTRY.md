# Tool Registry

## Purpose
The Tool Registry wraps existing `AppState` methods into a discoverable interface that agents can call.

## Available Tools

| Tool | Description | Module |
|---|---|---|
| `physics_summary` | Current physics parameters | physics_engine |
| `forecast_current` | Latest flare prediction | ai_engine |
| `digital_twin_state` | Full Digital Twin state | digital_twin |
| `digital_twin_regions` | Active regions | digital_twin |
| `digital_twin_similarity` | Historical similarity | digital_twin |
| `knowledge_graph_summary` | KG summary | knowledge_graph |
| `knowledge_graph_events` | All KG nodes | knowledge_graph |
| `decision_state` | Operational state | decision |
| `decision_thresholds` | Dynamic thresholds | decision |

## Adding New Tools
```python
TOOL_REGISTRY["my_tool"] = Tool(
    name="my_tool",
    description="Does something useful",
    fn=my_callable,
    module="my_module",
)
```
