import type { FC } from 'react';
import { useForecast } from '../hooks/useForecast';

interface Stage {
  id: string;
  name: string;
  shortName: string;
  status: 'ACTIVE' | 'PROCESSING' | 'WARNING' | 'IDLE';
  latency?: string;
  description: string;
}

export const PipelineFlow: FC = () => {
  const { currentObservation, nowcastState, latestForecast } = useForecast();

  const getStages = (): Stage[] => {
    const obsStatus = currentObservation ? 'ACTIVE' : 'IDLE';
    const valStatus = currentObservation?.validation ? (currentObservation.validation.is_valid ? 'ACTIVE' : 'WARNING') : 'IDLE';
    const calStatus = currentObservation?.calibration ? (currentObservation.calibration.is_calibrated ? 'ACTIVE' : 'WARNING') : 'IDLE';
    const syncStatus = currentObservation?.synchronization ? (currentObservation.synchronization.is_synchronized ? 'ACTIVE' : 'WARNING') : 'IDLE';
    const qualStatus = currentObservation?.quality ? (currentObservation.quality.overall_scientific_confidence >= 0.8 ? 'ACTIVE' : 'WARNING') : 'IDLE';
    const nowcastStatus = nowcastState ? 'PROCESSING' : 'IDLE';
    const physicsStatus = nowcastState?.latest_physics ? 'ACTIVE' : 'IDLE';
    const featureStatus = nowcastState?.latest_features ? 'ACTIVE' : 'IDLE';
    const mlStatus = latestForecast ? 'ACTIVE' : 'IDLE';
    const forecastStatus = latestForecast ? 'ACTIVE' : 'IDLE';
    const decisionStatus = latestForecast?.state ? (latestForecast.state === 'ALERT' || latestForecast.state === 'WARNING' ? 'WARNING' : 'ACTIVE') : 'IDLE';
    const xaiStatus = latestForecast ? 'ACTIVE' : 'IDLE';
    const opsStatus = nowcastState ? 'ACTIVE' : 'IDLE';

    return [
      { id: 'obs', name: 'Observation', shortName: 'OBS', status: obsStatus, description: 'Raw Soft/Hard X-Ray telemetry stream ingestion.' },
      { id: 'val', name: 'Validation', shortName: 'VAL', status: valStatus, description: 'Ingress packet integrity and timestamp continuity validation.' },
      { id: 'cal', name: 'Calibration', shortName: 'CAL', status: calStatus, description: 'Detector gain correction and offset adjustments.' },
      { id: 'sync', name: 'Synchronization', shortName: 'SYNC', status: syncStatus, description: 'Multi-instrument clock alignment and sync delay processing.' },
      { id: 'qual', name: 'Quality Assessment', shortName: 'QA', status: qualStatus, description: 'Scientific signal-to-noise ratio confidence scoring.' },
      { id: 'now', name: 'Nowcasting', shortName: 'NOW', status: nowcastStatus, description: 'Real-time solar event detection and tracking.' },
      { id: 'phys', name: 'Physics Characterization', shortName: 'PHYS', status: physicsStatus, description: 'Plasma profile extraction and Neupert effect matching.' },
      { id: 'feat', name: 'Feature Engineering', shortName: 'FEAT', status: featureStatus, description: 'ML-ready feature vector registry compilation.' },
      { id: 'ml', name: 'Machine Learning', shortName: 'ML', status: mlStatus, description: 'Ensemble model inference and conformal calibration.' },
      { id: 'fore', name: 'Forecast Generation', shortName: 'FORE', status: forecastStatus, description: 'Multi-horizon probability projection calculations.' },
      { id: 'dec', name: 'Decision Intelligence', shortName: 'DEC', status: decisionStatus, description: 'Mission mode recommendation engine evaluation.' },
      { id: 'xai', name: 'Explainable AI', shortName: 'XAI', status: xaiStatus, description: 'LIME/SHAP feature weights and reasoning chain construction.' },
      { id: 'ops', name: 'Mission Operations', shortName: 'OPS', status: opsStatus, description: 'Manual override validations and payload safe-mode triggering.' }
    ];
  };

  const stages = getStages();

  const getStatusClasses = (status: Stage['status']) => {
    switch (status) {
      case 'ACTIVE':
        return {
          bg: 'bg-success/20 border-success/80 text-success',
          text: 'text-success font-bold',
          line: 'bg-success/80'
        };
      case 'PROCESSING':
        return {
          bg: 'bg-primary/20 border-primary text-primary animate-pulse',
          text: 'text-primary font-bold',
          line: 'bg-primary/80'
        };
      case 'WARNING':
        return {
          bg: 'bg-warning/20 border-warning text-warning',
          text: 'text-warning font-bold',
          line: 'bg-warning/80'
        };
      default:
        return {
          bg: 'bg-surface border-border/40 text-muted-foreground',
          text: 'text-muted-foreground',
          line: 'bg-border/20'
        };
    }
  };

  return (
    <div className="w-full h-full px-4 flex items-center justify-between gap-2 overflow-x-auto select-none custom-scrollbar">
      <div className="flex items-center pr-3 border-r border-border/50 flex-shrink-0">
        <span className="font-bold text-label tracking-widest uppercase text-muted-foreground">PIPELINE TRACE</span>
      </div>

      <div className="flex-1 flex items-center justify-between min-w-0 px-2 h-full">
        {stages.map((stage, idx) => {
          const colors = getStatusClasses(stage.status);
          return (
            <div key={stage.id} className="flex items-center flex-1 last:flex-initial h-full relative group cursor-help">
              <div className="flex items-center gap-1.5">
                <div className={`w-5 h-5 rounded-full border flex items-center justify-center font-mono text-[9px] font-bold transition-all duration-300 ${colors.bg}`}>
                  {stage.shortName.charAt(0)}
                </div>
                <span className={`text-label uppercase whitespace-nowrap transition-colors duration-300 ${colors.text} hidden xl:block`}>
                  {stage.shortName}
                </span>
              </div>

              {/* Connecting Line */}
              {idx < stages.length - 1 && (
                <div className="flex-1 h-[1px] mx-1 relative min-w-[10px]">
                  <div className={`absolute inset-0 transition-colors duration-300 ${colors.line}`} />
                </div>
              )}

              {/* Tooltip */}
              <div className="absolute bottom-8 left-0 hidden group-hover:block bg-surface-container-highest border border-border/80 p-2 rounded shadow-xl text-label z-50 pointer-events-none min-w-[200px]">
                <p className="font-bold text-foreground mb-1">{stage.name}</p>
                <p className="text-muted-foreground">{stage.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
export default PipelineFlow;
