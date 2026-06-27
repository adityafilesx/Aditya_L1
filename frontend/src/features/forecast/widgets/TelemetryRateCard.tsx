import React from 'react';
import { BaseCard } from '@design-system/index';

export const TelemetryRateCard: React.FC<{ rate: number }> = ({ rate }) => {
  return (
    <BaseCard title="Telemetry Stream Rate" className="h-full">
      <div className="flex flex-col gap-4 items-center justify-center h-full">
        <div className="text-4xl font-mono text-primary flex items-baseline gap-2">
          {rate.toFixed(1)} <span className="text-sm text-secondary">Hz</span>
        </div>
        <div className="text-sm text-secondary">
          Live Connection
        </div>
      </div>
    </BaseCard>
  );
};
