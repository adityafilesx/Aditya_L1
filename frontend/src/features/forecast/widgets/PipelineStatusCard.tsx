import React from 'react';
import { BaseCard } from '@design-system/index';
import { BaseBadge } from '@design-system/index';
import type { PipelineStatus } from '../types/ForecastTypes';

export const PipelineStatusCard: React.FC<{ status: PipelineStatus | null }> = ({ status }) => {
  if (!status) {
    return (
      <BaseCard title="Pipeline Status" className="h-full flex flex-col justify-center items-center p-8">
        <div className="animate-pulse flex flex-col items-center">
          <span className="text-secondary text-sm">Awaiting Pipeline Status...</span>
        </div>
      </BaseCard>
    );
  }
  return (
    <BaseCard title="Pipeline Status" className="h-full">
      <div className="flex flex-col gap-4">
        <div className="flex justify-between items-center pb-2 border-b border-white/10">
          <span className="text-secondary text-sm">System Health</span>
          <BaseBadge variant={status.status === 'GREEN' ? 'success' : status.status === 'YELLOW' ? 'warning' : 'critical'}>{status.system_health}</BaseBadge>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Stream Rate</div>
            <div className="text-xl font-mono text-primary">
              {status.observation_rate_hz.toFixed(1)} <span className="text-sm">Hz</span>
            </div>
          </div>
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">End-to-End Latency</div>
            <div className={`text-xl font-mono ${status.current_latency_ms > 200 ? 'text-yellow-400' : 'text-primary'}`}>
              {status.current_latency_ms.toFixed(0)} <span className="text-sm">ms</span>
            </div>
          </div>
        </div>

        <div className="mt-2 pt-2 border-t border-white/10">
          <div className="text-secondary text-xs uppercase tracking-wider">Active Payloads</div>
          <div className="text-sm text-primary flex gap-2 mt-1">
            {status.active_instruments.map((inst, i) => (
              <span key={i} className="px-2 py-1 bg-surface-elevated rounded text-xs">{inst}</span>
            ))}
          </div>
        </div>
      </div>
    </BaseCard>
  );
};
