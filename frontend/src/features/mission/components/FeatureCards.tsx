import React from 'react';
import { BaseCard, Icon } from '@design-system/index';

interface FeatureStoreCardProps {
  features: any[];
}

export const FeatureStoreCard: React.FC<FeatureStoreCardProps> = ({ features }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title="FEATURE STORE">
      <div className="space-y-3">
        {(!features || features.length === 0) ? (
          <div className="text-xs text-on-surface-variant/50 text-center py-4">No active features found.</div>
        ) : (
          features.map((feature, idx) => (
            <div key={idx} className="flex flex-col gap-1 p-2 bg-surface-container-low border border-outline-variant rounded">
              <span className="text-[11px] font-bold text-on-surface">{feature.name}</span>
              <div className="flex justify-between items-center">
                <span className="text-[9px] font-label-caps text-on-surface-variant">V{feature.version || '1.0'}</span>
                <span className="text-[9px] font-label-caps text-secondary bg-secondary/10 px-1 rounded">{feature.dtype || 'float32'}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </BaseCard>
  );
};
