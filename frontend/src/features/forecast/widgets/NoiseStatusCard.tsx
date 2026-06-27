import React from 'react';
import { BaseCard } from '@design-system/index';
import type { NoiseBackgroundResult } from '../types/ForecastTypes';

export const NoiseStatusCard: React.FC<{ result: NoiseBackgroundResult }> = ({ result }) => {
  return (
    <BaseCard title="Noise & Background Assessment" className="h-full">
      <div className="flex flex-col gap-4">
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Signal Stability</div>
            <div className="text-xl font-mono text-primary">
              {result.signal_stability.toFixed(1)}%
            </div>
          </div>
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Noise Ratio</div>
            <div className={`text-xl font-mono ${result.noise_percentage > 3 ? 'text-yellow-400' : 'text-primary'}`}>
              {result.noise_percentage.toFixed(2)}%
            </div>
          </div>
        </div>
        
        <div className="pt-2 border-t border-white/10 grid grid-cols-2 gap-4">
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Soft X-Ray Base</div>
            <div className="text-sm font-mono text-primary truncate">
              {result.soft_xray_background.toExponential(2)} <span className="text-xs text-secondary">cps</span>
            </div>
          </div>
          <div>
            <div className="text-secondary text-xs uppercase tracking-wider">Hard X-Ray Base</div>
            <div className="text-sm font-mono text-primary truncate">
              {result.hard_xray_background.toExponential(2)} <span className="text-xs text-secondary">cps</span>
            </div>
          </div>
        </div>

      </div>
    </BaseCard>
  );
};
