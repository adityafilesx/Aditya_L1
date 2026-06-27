import React from 'react';
import { BaseCard } from '@design-system/index';
import type { ObservationProvenance } from '../types/ForecastTypes';

export const DataFreshnessCard: React.FC<{ provenance: ObservationProvenance }> = ({ provenance }) => {
  return (
    <BaseCard title="Observation Provenance & Latency" className="h-full">
      <div className="flex flex-col gap-4">
        <div className="flex justify-between items-center text-sm border-b border-white/10 pb-2">
          <span className="text-secondary">Observation ID</span>
          <span className="text-primary font-mono text-xs truncate max-w-[150px]">{provenance.observation_id}</span>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col">
            <span className="text-[10px] text-secondary uppercase">Acquisition</span>
            <span className="text-xs text-primary font-mono">{provenance.acquisition_latency_ms.toFixed(1)} ms</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] text-secondary uppercase">Validation</span>
            <span className="text-xs text-primary font-mono">{provenance.validation_latency_ms.toFixed(1)} ms</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] text-secondary uppercase">Calibration</span>
            <span className="text-xs text-primary font-mono">{provenance.calibration_latency_ms.toFixed(1)} ms</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] text-secondary uppercase">Processing</span>
            <span className="text-xs text-primary font-mono">{provenance.processing_latency_ms.toFixed(1)} ms</span>
          </div>
        </div>

        <div className="mt-2 pt-2 border-t border-white/10 flex justify-between items-center">
          <span className="text-secondary text-xs uppercase tracking-wider">Total Pipeline Latency</span>
          <span className={`text-lg font-mono ${provenance.total_latency_ms > 200 ? 'text-yellow-400' : 'text-primary'}`}>
            {provenance.total_latency_ms.toFixed(1)} <span className="text-sm">ms</span>
          </span>
        </div>
      </div>
    </BaseCard>
  );
};
