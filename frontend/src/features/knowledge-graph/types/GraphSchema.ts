// Neo4j & NetworkX compatible graph schema

export type ScientificNodeType = 
  | 'Mission' | 'MissionState' | 'Telemetry' | 'Prediction' 
  | 'PhysicsFeature' | 'Wavelet' | 'SpectralFit' | 'Temperature' 
  | 'EmissionMeasure' | 'Entropy' | 'Neupert' | 'Sensor' 
  | 'SoLEXS' | 'HEL1OS' | 'GOES' | 'HMI' | 'AIA' | 'SWIS'
  | 'Flare' | 'CME' | 'SEP' | 'ActiveRegion' | 'DigitalTwin'
  | 'MissionRecommendation' | 'KnowledgeAsset' | 'ScientificImage'
  | 'ResearchPaper' | 'Notebook' | 'Experiment' | 'Model'
  | 'Dataset' | 'Benchmark' | 'Operator' | 'MissionReport'
  | 'Alert' | 'TimelineEvent' | 'SystemEvent';

export type ScientificEdgeType = 
  | 'TEMPORAL' | 'SPATIAL' | 'PHYSICAL' | 'CAUSAL' 
  | 'CORRELATION' | 'PREDICTION' | 'SIMILARITY' 
  | 'HISTORICAL' | 'SCIENTIFIC' | 'OPERATIONAL' 
  | 'SENSOR' | 'AI' | 'PHYSICS' | 'MISSION' 
  | 'RESEARCH' | 'CONFIDENCE';

export interface GraphNodeProperties {
  label: string;
  timestamp: string; // ISO 8601
  metadata: Record<string, any>;
  embeddings?: number[]; // Placeholder for GraphRAG/GNN
  source?: string;
  confidence?: number; // 0.0 to 1.0
  status?: 'nominal' | 'degraded' | 'critical' | 'info';
}

export interface GraphEdgeProperties {
  weight: number;
  confidence: number;
  timestamp: string;
  direction: 'directed' | 'undirected' | 'bidirectional';
  source: string;
  metadata: Record<string, any>;
}

export interface NodeData extends GraphNodeProperties, Record<string, unknown> {
  type: ScientificNodeType;
}

export interface EdgeData extends GraphEdgeProperties, Record<string, unknown> {
  type: ScientificEdgeType;
}
