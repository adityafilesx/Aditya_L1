import React from 'react';
import { BaseCard, Icon } from '@design-system/index';

interface ServingStatusCardProps {
  modelsStatus: Record<string, string>;
}

export const ServingStatusCard: React.FC<ServingStatusCardProps> = ({ modelsStatus }) => {
  const models = Object.entries(modelsStatus || {});

  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="SERVING STATUS">
      <div className="space-y-3">
        {models.length === 0 ? (
          <div className="text-xs text-on-surface-variant/50 text-center py-4">No model serving data.</div>
        ) : (
          models.map(([model, status]) => (
            <div key={model} className="flex justify-between items-center p-2 bg-surface-container-low border border-outline-variant rounded">
              <span className="text-[11px] font-label-caps text-on-surface uppercase">{model.replace('_status', '')}</span>
              <span className={`text-[10px] font-bold tracking-wider ${
                status === 'ONLINE' ? 'text-success' : 
                status === 'OFFLINE' ? 'text-on-surface-variant' : 'text-warning'
              }`}>
                {status}
              </span>
            </div>
          ))
        )}
      </div>
    </BaseCard>
  );
};

interface ModelRegistryCardProps {
  models: any[];
}

export const ModelRegistryCard: React.FC<ModelRegistryCardProps> = ({ models }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="MODEL REGISTRY">
      <div className="space-y-3">
        {(!models || models.length === 0) ? (
          <div className="text-xs text-on-surface-variant/50 text-center py-4">No registered models found.</div>
        ) : (
          models.map((model, idx) => (
            <div key={idx} className="flex flex-col gap-2 p-3 bg-surface-container-low border border-outline-variant rounded">
              <div className="flex justify-between items-center">
                <span className="text-[11px] font-bold text-on-surface">{model.model_id}</span>
                <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                  model.deployment_stage === 'PRODUCTION' ? 'bg-success/10 text-success border border-success/20' : 
                  'bg-surface-container-highest text-on-surface-variant'
                }`}>
                  {model.deployment_stage}
                </span>
              </div>
              <div className="flex justify-between items-center text-[10px]">
                <span className="font-label-caps text-on-surface-variant">Architecture</span>
                <span className="font-data-mono">{model.architecture}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </BaseCard>
  );
};

interface InferenceReadinessCardProps {
  metrics: any[];
}

export const InferenceReadinessCard: React.FC<InferenceReadinessCardProps> = ({ metrics }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="INFERENCE READINESS">
      <div className="space-y-3">
        {(!metrics || metrics.length === 0) ? (
          <div className="text-xs text-on-surface-variant/50 text-center py-4">No inference metrics available.</div>
        ) : (
          metrics.map((metric, idx) => (
            <div key={idx} className="flex flex-col gap-2 p-3 bg-surface-container-low border border-outline-variant rounded">
              <div className="flex justify-between items-center">
                <span className="text-[11px] font-bold text-on-surface">{metric.model_id}</span>
              </div>
              <div className="grid grid-cols-2 gap-2 mt-1">
                <div className="flex flex-col gap-0.5">
                  <span className="text-[9px] font-label-caps text-on-surface-variant">Accuracy</span>
                  <span className="font-data-mono text-[11px]">{(metric.accuracy * 100).toFixed(1)}%</span>
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-[9px] font-label-caps text-on-surface-variant">Brier Score</span>
                  <span className="font-data-mono text-[11px]">{metric.brier?.toFixed(4) || '---'}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </BaseCard>
  );
};

interface ConformalCalibrationCardProps {
  calibration: any;
}

export const ConformalCalibrationCard: React.FC<ConformalCalibrationCardProps> = ({ calibration }) => {
  if (!calibration) {
    return (
      <BaseCard variant="plain" size="md" className="card-shadow h-full" title="CONFORMAL CALIBRATION">
        <div className="text-xs text-on-surface-variant/50 text-center py-4">No calibration data available.</div>
      </BaseCard>
    );
  }

  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="CONFORMAL CALIBRATION">
      <div className="flex justify-between items-center mb-4">
        <span className="text-[10px] font-label-caps text-on-surface-variant">Status</span>
        <span className="px-2 py-0.5 bg-success/10 text-success text-[10px] font-bold tracking-wider rounded border border-success/20">
          {calibration.calibration_status || 'UNKNOWN'}
        </span>
      </div>
      <div className="space-y-3">
        <div className="flex justify-between items-center p-2 bg-surface-container-low border border-outline-variant rounded">
          <span className="text-[11px] font-label-caps text-on-surface-variant">Method</span>
          <span className="text-[10px] font-bold text-on-surface text-right max-w-[120px]">{calibration.active_method}</span>
        </div>
        <div className="flex justify-between items-center p-2 bg-surface-container-low border border-outline-variant rounded">
          <span className="text-[11px] font-label-caps text-on-surface-variant">Expected Error</span>
          <span className="font-data-mono text-[11px] text-on-surface">{calibration.expected_calibration_error?.toFixed(3)}</span>
        </div>
        <div className="flex justify-between items-center p-2 bg-surface-container-low border border-outline-variant rounded">
          <span className="text-[11px] font-label-caps text-on-surface-variant">Quantile Threshold</span>
          <span className="font-data-mono text-[11px] text-warning">{calibration.conformal_quantile_threshold?.toFixed(3)}</span>
        </div>
      </div>
    </BaseCard>
  );
};

interface PredictionTargetCardProps {
  targets: any[];
}

export const PredictionTargetCard: React.FC<PredictionTargetCardProps> = ({ targets }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="PREDICTION TARGETS">
      <div className="space-y-3">
        {(!targets || targets.length === 0) ? (
          <div className="text-xs text-on-surface-variant/50 text-center py-4">No active targets found.</div>
        ) : (
          targets.map((target, idx) => (
            <div key={idx} className="flex flex-col gap-1 p-2 bg-surface-container-low border border-outline-variant rounded">
              <span className="text-[11px] font-bold text-on-surface">{target.name}</span>
              <div className="flex justify-between items-center">
                <span className="text-[9px] font-label-caps text-on-surface-variant">ID: {target.id}</span>
                <span className="text-[9px] font-label-caps text-primary bg-primary/10 px-1 rounded">{target.type}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </BaseCard>
  );
};
