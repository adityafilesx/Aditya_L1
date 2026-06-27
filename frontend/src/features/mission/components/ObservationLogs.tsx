import React from 'react';
import { BaseCard, Icon } from '@design-system/index';
import { formatTimestamp } from '@utils/formatters';
import { cn } from '@utils/cn';

interface Alert {
  id: string;
  type: string;
  level: string;
  timestamp: string;
  message: string;
}

interface TimelineWidgetProps {
  alerts: Alert[];
}

export const TimelineWidget: React.FC<TimelineWidgetProps> = ({ alerts }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="OBSERVATION LOG">
      <div className="flex flex-col gap-4 overflow-y-auto pr-2 max-h-[300px] hide-scrollbar">
        {(!alerts || alerts.length === 0) ? (
          <div className="text-xs text-on-surface-variant/50 text-center py-4">No recent alerts or events.</div>
        ) : (
          alerts.slice(0, 50).map((alert, i) => (
            <div key={alert.id || i} className="flex gap-3 text-xs border-b border-outline-variant/30 pb-3 last:border-0 last:pb-0">
              <div className="font-data-mono text-[10px] text-on-surface-variant w-[130px] shrink-0 mt-0.5">
                {formatTimestamp(alert.timestamp)}
              </div>
              <div className="flex flex-col gap-1">
                <span className={cn("font-bold tracking-wider text-[10px]", 
                  alert.level === 'CRITICAL' ? 'text-critical' : 
                  alert.level === 'WARNING' ? 'text-warning' : 'text-success'
                )}>
                  [{alert.level}] {alert.type}
                </span>
                <span className="text-on-surface leading-tight">{alert.message}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </BaseCard>
  );
};

interface TraceabilityMatrixCardProps {
  diagnostics: any;
  config: any;
}

export const TraceabilityMatrixCard: React.FC<TraceabilityMatrixCardProps> = ({ diagnostics, config }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="TRACEABILITY MATRIX">
      <div className="space-y-4">
        <div className="flex flex-col gap-2">
          <span className="text-[10px] font-label-caps text-on-surface-variant">Engines</span>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(diagnostics?.engines || {}).map(([name, data]: [string, any]) => (
              <div key={name} className="flex justify-between items-center p-2 bg-surface-container-low border border-outline-variant rounded">
                <span className="text-[10px] font-label-caps text-on-surface truncate pr-2">{name.replace('_', ' ')}</span>
                <span className={cn("text-[9px] font-bold tracking-wider", data?.status === 'ONLINE' ? 'text-success' : 'text-critical')}>
                  {data?.status || 'UNKNOWN'}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <span className="text-[10px] font-label-caps text-on-surface-variant">System Hardware</span>
          <div className="grid grid-cols-2 gap-2 text-[10px] font-data-mono">
            <div className="flex justify-between p-1">
              <span className="text-on-surface-variant">CPU:</span>
              <span>{diagnostics?.hardware?.cpu_percent?.toFixed(1) || '---'}%</span>
            </div>
            <div className="flex justify-between p-1">
              <span className="text-on-surface-variant">MEM:</span>
              <span>{diagnostics?.hardware?.memory_percent?.toFixed(1) || '---'}%</span>
            </div>
            <div className="flex justify-between p-1">
              <span className="text-on-surface-variant">DISK:</span>
              <span>{diagnostics?.hardware?.disk_percent?.toFixed(1) || '---'}%</span>
            </div>
            <div className="flex justify-between p-1">
              <span className="text-on-surface-variant">NET:</span>
              <span>{diagnostics?.hardware?.network_latency_ms || '---'}ms</span>
            </div>
          </div>
        </div>
      </div>
    </BaseCard>
  );
};
