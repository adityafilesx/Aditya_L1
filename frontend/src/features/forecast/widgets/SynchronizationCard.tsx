import React from 'react';
import { BaseCard } from '@design-system/index';
import { BaseBadge } from '@design-system/index';
import type { SynchronizationResult } from '../types/ForecastTypes';

export const SynchronizationCard: React.FC<{ result: SynchronizationResult }> = ({ result }) => {
  return (
    <BaseCard title="Payload Synchronization" className="h-full">
      <div className="flex flex-col gap-4">
        <div className="flex justify-between items-center pb-2 border-b border-white/10">
          <span className="text-secondary text-sm">Sync State</span>
          <BaseBadge variant={result.is_synchronized ? 'success' : 'critical'}>{result.is_synchronized ? 'LOCKED' : 'DRIFTING'}</BaseBadge>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Sync Delay</div>
            <div className={`text-xl font-mono ${result.sync_delay_ms > 10 ? 'text-yellow-400' : 'text-primary'}`}>
              {result.sync_delay_ms.toFixed(2)} <span className="text-sm">ms</span>
            </div>
          </div>
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Time Offset</div>
            <div className={`text-xl font-mono ${result.time_offset_ms > 1.0 ? 'text-yellow-400' : 'text-primary'}`}>
              {result.time_offset_ms.toFixed(3)} <span className="text-sm">ms</span>
            </div>
          </div>
        </div>
        
        <div className="mt-2 pt-2 border-t border-white/10 flex justify-between items-center">
          <span className="text-secondary text-xs uppercase tracking-wider">Sync Confidence</span>
          <span className="text-lg font-mono text-primary">{(result.sync_confidence * 100).toFixed(1)}%</span>
        </div>
      </div>
    </BaseCard>
  );
};
