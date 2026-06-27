import React from 'react';
import { BaseCard, ProgressBar } from '@design-system/index';
import { formatLatency, formatPercent } from '@utils/formatters';

interface PipelineStatusCardProps {
  latencyMs?: number;
  cpu?: number;
  memory?: number;
  disk?: number;
  status?: string;
}

export const PipelineStatusCard: React.FC<PipelineStatusCardProps> = ({
  latencyMs,
  cpu,
  memory,
  disk,
  status
}) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="PIPELINE STATUS">
      <div className="flex justify-between items-center mb-6">
        <span className="text-[10px] font-label-caps text-on-surface-variant">System Health</span>
        <span className="px-2 py-0.5 bg-success/10 text-success text-[10px] font-bold tracking-wider rounded border border-success/20">
          {status || 'ONLINE'}
        </span>
      </div>

      <div className="flex flex-col gap-1 mb-6">
        <span className="text-[10px] font-label-caps text-on-surface-variant">End-to-End Latency</span>
        <span className="font-numeric-telemetry text-xl font-bold">{formatLatency(latencyMs)}</span>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {[
          { name: 'CPU', value: cpu },
          { name: 'RAM', value: memory },
          { name: 'DISK IO', value: disk },
        ].map((perf) => (
          <div key={perf.name} className="flex flex-col gap-1">
            <div className="flex justify-between">
              <span className="text-[10px] font-label-caps text-on-surface-variant">{perf.name}</span>
              <span className="text-[10px] font-data-mono">{formatPercent((perf.value || 0) / 100, 1)}</span>
            </div>
            <ProgressBar value={perf.value || 0} className="h-1.5" />
          </div>
        ))}
      </div>
    </BaseCard>
  );
};

interface InstrumentMetadataCardProps {
  sensors: Record<string, string>;
  uptimeSec?: number;
}

export const InstrumentMetadataCard: React.FC<InstrumentMetadataCardProps> = ({ sensors, uptimeSec }) => {
  const sensorEntries = Object.entries(sensors || {});

  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="INSTRUMENT METADATA">
      <div className="flex justify-between items-center mb-6">
        <span className="text-[10px] font-label-caps text-on-surface-variant">Uptime</span>
        <span className="font-data-mono text-xs text-on-surface">{uptimeSec ? `${(uptimeSec / 3600).toFixed(1)} hrs` : '---'}</span>
      </div>

      <div className="space-y-3">
        {sensorEntries.length === 0 ? (
          <div className="text-xs text-on-surface-variant/50 text-center py-4">No sensor data available.</div>
        ) : (
          sensorEntries.map(([sensor, status]) => (
            <div key={sensor} className="flex justify-between items-center p-2 bg-surface-container-low border border-outline-variant rounded">
              <span className="text-[11px] font-label-caps text-on-surface uppercase">{sensor}</span>
              <span className={`text-[10px] font-bold tracking-wider ${
                status === 'ONLINE' ? 'text-success' : 
                status === 'DEGRADED' ? 'text-warning' : 'text-critical'
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
