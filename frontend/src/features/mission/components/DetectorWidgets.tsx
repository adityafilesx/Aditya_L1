import React from 'react';
import { BaseCard, Icon } from '@design-system/index';
import { formatScientific, formatFlux } from '@utils/formatters';
import { cn } from '@utils/cn';

interface DetectorWidgetProps {
  title: string;
  iconColor: string;
  flux: number | null | undefined;
  unit: string;
  status: string; // ONLINE, IDLE, DEGRADED, OFFLINE
  baseline?: number;
  triggerThreshold?: number;
  eventCount?: number;
}

export const DetectorWidget: React.FC<DetectorWidgetProps> = ({
  title,
  iconColor,
  flux,
  unit,
  status,
  baseline,
  triggerThreshold,
  eventCount
}) => {
  const getStatusColor = (st: string) => {
    switch (st?.toUpperCase()) {
      case 'ONLINE':
      case 'ACTIVE':
        return 'text-success border-success bg-success/10';
      case 'RISING':
      case 'MONITORING':
        return 'text-warning border-warning bg-warning/10';
      case 'DEGRADED':
      case 'ERROR':
        return 'text-critical border-critical bg-critical/10';
      default:
        return 'text-on-surface-variant border-outline-variant bg-surface-container-low';
    }
  };

  const statusColor = getStatusColor(status);

  return (
    <BaseCard variant="glass" className="p-4" title={
      <span className="font-label-caps text-[11px] text-on-surface-variant flex items-center justify-between w-full">
        <span className="flex items-center gap-2">
          <span className={cn("w-2 h-2 rounded-full", iconColor)}></span> {title}
        </span>
        <span className={cn("px-2 py-0.5 rounded border text-[9px] font-bold tracking-wider", statusColor)}>
          {status || 'UNKNOWN'}
        </span>
      </span>
    }>
      <div className="flex flex-col gap-4 mt-2">
        <div className="flex justify-between items-end bg-surface-container-low p-3 rounded border border-outline-variant">
          <div className="flex flex-col gap-1">
            <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">Current Flux</span>
            <div className="flex items-baseline gap-1">
              <span className="font-numeric-telemetry text-2xl font-bold">{formatScientific(flux)}</span>
              <span className="text-[10px] text-on-surface-variant font-data-mono">{unit}</span>
            </div>
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className="text-[9px] font-label-caps text-on-surface-variant flex items-center gap-1" title="Configured Reference Threshold">
              Threshold <Icon name="info" className="text-[10px]" />
            </span>
            <span className="font-numeric-telemetry text-xs text-warning">{formatScientific(triggerThreshold)}</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="flex flex-col gap-1 p-2 bg-surface-container-highest rounded">
            <span className="text-[9px] font-label-caps text-on-surface-variant">Baseline Flux</span>
            <span className="font-numeric-telemetry text-xs text-on-surface">{formatScientific(baseline)}</span>
          </div>
          <div className="flex flex-col gap-1 p-2 bg-surface-container-highest rounded">
            <span className="text-[9px] font-label-caps text-on-surface-variant">Event Count</span>
            <span className="font-numeric-telemetry text-xs text-on-surface">{formatFlux(eventCount, 0)}</span>
          </div>
        </div>
      </div>
    </BaseCard>
  );
};
