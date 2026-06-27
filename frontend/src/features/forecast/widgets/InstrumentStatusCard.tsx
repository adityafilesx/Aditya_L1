import React from 'react';
import { BaseCard } from '@design-system/index';
import { BaseBadge } from '@design-system/index';
import type { InstrumentMetadata } from '../types/ForecastTypes';

export const InstrumentStatusCard: React.FC<{ metadata: Record<string, InstrumentMetadata> }> = ({ metadata }) => {
  return (
    <BaseCard title="Payload Status" className="h-full">
      <div className="flex flex-col gap-4">
        {Object.values(metadata).map((inst) => (
          <div key={inst.instrument_id} className="flex flex-col gap-2 p-3 bg-surface-elevated rounded">
            <div className="flex justify-between items-center">
              <span className="text-sm font-bold text-primary">{inst.instrument_id}</span>
              <BaseBadge variant={inst.detector_state === 'ACTIVE' ? 'success' : 'warning'}>{inst.detector_state}</BaseBadge>
            </div>
            <div className="grid grid-cols-2 gap-2 mt-1">
              <div className="flex flex-col">
                <span className="text-[10px] text-secondary uppercase">Energy Range</span>
                <span className="text-xs text-primary">{inst.energy_range}</span>
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] text-secondary uppercase">Cadence</span>
                <span className="text-xs text-primary font-mono">{inst.cadence_hz} Hz</span>
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] text-secondary uppercase">Mode</span>
                <span className="text-xs text-primary">{inst.operational_mode}</span>
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] text-secondary uppercase">Units</span>
                <span className="text-xs text-primary">{inst.units}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </BaseCard>
  );
};
