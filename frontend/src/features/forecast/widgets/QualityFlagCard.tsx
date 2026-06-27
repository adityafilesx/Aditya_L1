import React from 'react';
import { BaseCard } from '@design-system/index';
import { BaseBadge } from '@design-system/index';

interface QualityFlagCardProps {
  flags: { status: string; description: string; severity: string }[];
}

export const QualityFlagCard: React.FC<QualityFlagCardProps> = ({ flags }) => {
  return (
    <BaseCard title="Observation Quality Flags" className="h-full">
      <div className="flex flex-col gap-2">
        {flags.length === 0 ? (
          <div className="text-secondary text-sm">No flags present. Observation is clean.</div>
        ) : (
          flags.map((flag, idx) => (
            <div key={idx} className="flex items-center justify-between p-2 bg-surface-elevated rounded">
              <div className="flex items-center gap-3">
                <BaseBadge variant={
                    flag.severity === 'CRITICAL' ? 'critical' : 
                    flag.severity === 'WARNING' ? 'warning' : 'primary'
                  }>{flag.status}</BaseBadge>
                <span className="text-sm text-primary">{flag.description}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </BaseCard>
  );
};
