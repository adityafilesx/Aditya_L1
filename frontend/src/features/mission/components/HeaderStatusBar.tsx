import React from 'react';
import { cn } from '@utils/cn';
import { formatTimestamp } from '@utils/formatters';

interface HeaderStatusBarProps {
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'reconnecting';
  operator: string;
  clockUtc: string;
  systemConfig?: any;
  lastUpdated: string | null;
  missionStateNum: number;
}

export const HeaderStatusBar: React.FC<HeaderStatusBarProps> = ({
  connectionStatus,
  operator,
  clockUtc,
  systemConfig,
  lastUpdated,
  missionStateNum
}) => {
  const isOnline = connectionStatus === 'connected';
  const stateLabels = ['NOMINAL', 'WATCH', 'ALERT'];
  const stateColors = ['text-success', 'text-warning', 'text-critical'];
  const missionStateLabel = stateLabels[missionStateNum] || 'UNKNOWN';
  const missionStateColor = stateColors[missionStateNum] || 'text-on-surface-variant';

  return (
    <div className="flex items-center gap-6 bg-surface-container-low p-4 rounded-xl border border-outline-variant w-full overflow-x-auto hide-scrollbar">
      <div className="flex items-center gap-2 border-r border-outline-variant pr-6 shrink-0">
        <span className={cn("w-3 h-3 rounded-full", isOnline ? "bg-success animate-pulse" : "bg-critical")} />
        <div className="flex flex-col">
          <span className="font-label-caps text-[10px] text-on-surface-variant">L1 LINK</span>
          <span className={cn("font-bold text-xs tracking-wider", isOnline ? "text-success" : "text-critical")}>
            {isOnline ? 'ONLINE' : 'OFFLINE'}
          </span>
        </div>
      </div>
      
      <div className="flex flex-col border-r border-outline-variant pr-6 shrink-0">
        <span className="font-label-caps text-[10px] text-on-surface-variant">MISSION STATE</span>
        <span className={cn("font-bold text-xs tracking-wider", missionStateColor)}>{missionStateLabel}</span>
      </div>

      <div className="flex flex-col border-r border-outline-variant pr-6 shrink-0">
        <span className="font-label-caps text-[10px] text-on-surface-variant">OPERATOR</span>
        <span className="font-numeric-telemetry text-xs text-on-surface">{operator || '---'}</span>
      </div>

      <div className="flex flex-col border-r border-outline-variant pr-6 shrink-0">
        <span className="font-label-caps text-[10px] text-on-surface-variant">PLATFORM ENV</span>
        <span className="font-data-mono text-xs text-on-surface">{systemConfig?.system_env?.toUpperCase() || '---'}</span>
      </div>

      <div className="flex flex-col border-r border-outline-variant pr-6 shrink-0">
        <span className="font-label-caps text-[10px] text-on-surface-variant">LAST UPDATED</span>
        <span className="font-data-mono text-xs text-on-surface">{formatTimestamp(lastUpdated)}</span>
      </div>

      <div className="flex flex-col shrink-0">
        <span className="font-label-caps text-[10px] text-on-surface-variant">UTC CLOCK</span>
        <span className="font-data-mono text-xs text-on-surface">{clockUtc || '---'}</span>
      </div>
    </div>
  );
};
