import React from 'react';
import { BaseCard } from '@design-system/index';
import { BaseBadge } from '@design-system/index';

interface ObservationHealthCardProps {
  isValid: boolean;
  missingPackets: number;
  duplicatePackets: number;
  freshnessMs: number;
}

export const ObservationHealthCard: React.FC<ObservationHealthCardProps> = ({
  isValid,
  missingPackets,
  duplicatePackets,
  freshnessMs,
}) => {
  return (
    <BaseCard title="Observation Validation" className="h-full">
      <div className="flex flex-col gap-4">
        <div className="flex justify-between items-center pb-2 border-b border-white/10">
          <span className="text-secondary text-sm">Integrity Status</span>
          <BaseBadge variant={isValid ? 'success' : 'critical'}>{isValid ? 'VALID' : 'INVALID'}</BaseBadge>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Missing Packets</div>
            <div className={`text-xl font-mono ${missingPackets > 0 ? 'text-red-400' : 'text-primary'}`}>
              {missingPackets}
            </div>
          </div>
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Duplicate Packets</div>
            <div className={`text-xl font-mono ${duplicatePackets > 0 ? 'text-yellow-400' : 'text-primary'}`}>
              {duplicatePackets}
            </div>
          </div>
        </div>
        
        <div className="mt-2 pt-2 border-t border-white/10">
          <div className="text-secondary text-xs uppercase tracking-wider">Data Freshness</div>
          <div className="text-lg font-mono text-primary">{freshnessMs.toFixed(2)} ms</div>
        </div>
      </div>
    </BaseCard>
  );
};
