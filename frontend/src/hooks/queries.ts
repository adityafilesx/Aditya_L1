import { useQuery } from "@tanstack/react-query";
import { api } from "../api/endpoints";

export const useDashboard = () => {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: api.dashboard.getDashboard,
    refetchInterval: 1000, // Fetch every second for live feel
  });
};

export const useOperationsTelemetry = () => {
  return useQuery({
    queryKey: ["operations", "telemetry"],
    queryFn: api.operations.getTelemetry,
    refetchInterval: 1000,
  });
};

export const useOperationsPhysics = () => {
  return useQuery({
    queryKey: ["operations", "physics"],
    queryFn: api.operations.getPhysics,
    refetchInterval: 1000,
  });
};

export const useOperationsModels = () => {
  return useQuery({
    queryKey: ["operations", "models"],
    queryFn: api.operations.getModels,
    refetchInterval: 5000,
  });
};

export const useOperationsHealth = () => {
  return useQuery({
    queryKey: ["operations", "health"],
    queryFn: api.operations.getHealth,
    refetchInterval: 5000,
  });
};

export const useForecastCurrent = () => {
  return useQuery({
    queryKey: ["forecast", "current"],
    queryFn: api.forecast.getCurrent,
    refetchInterval: 5000,
  });
};

export const usePhysicsSummary = () => {
  return useQuery({
    queryKey: ["physics", "summary"],
    queryFn: api.physics.getSummary,
    refetchInterval: 1000,
  });
};

export const useDecisionState = () => {
  return useQuery({
    queryKey: ["decision", "state"],
    queryFn: api.decision.getState,
    refetchInterval: 1000,
  });
};

export const useDigitalTwinState = () => {
  return useQuery({
    queryKey: ["digitalTwin", "state"],
    queryFn: api.digitalTwin.getState,
    refetchInterval: 5000,
  });
};

export const useKnowledgeGraphSummary = () => {
  return useQuery({
    queryKey: ["knowledgeGraph", "summary"],
    queryFn: api.knowledgeGraph.getSummary,
    refetchInterval: 10000,
  });
};

export const useIntelligenceRisk = () => {
  return useQuery({
    queryKey: ["intelligence", "risk"],
    queryFn: api.intelligence.getRisk,
    refetchInterval: 5000,
  });
};

export const useIntelligenceRecommendations = () => {
  return useQuery({
    queryKey: ["intelligence", "recommendations"],
    queryFn: api.intelligence.getRecommendations,
    refetchInterval: 5000,
  });
};

export const useSystemHealth = () => {
  return useQuery({
    queryKey: ["system", "health"],
    queryFn: api.system.getHealth,
    refetchInterval: 2000,
  });
};

export const useTimelineEvents = () => {
  return useQuery({
    queryKey: ["timeline", "events"],
    queryFn: api.timeline.getEvents,
    refetchInterval: 5000,
  });
};

export const useResearchBenchmarks = () => {
  return useQuery({
    queryKey: ["research", "benchmarks"],
    queryFn: api.research.getBenchmarks,
  });
};
