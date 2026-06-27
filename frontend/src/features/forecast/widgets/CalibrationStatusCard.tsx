import React from 'react';
import { BaseCard } from '@design-system/index';
import { BaseBadge } from '@design-system/index';
import type { CalibrationResult } from '../types/ForecastTypes';

export const CalibrationStatusCard: React.FC<{ result: CalibrationResult }> = ({ result }) => {
  return (
    <BaseCard title="Calibration Status" className="h-full">
      <div className="flex flex-col gap-4">
        <div className="flex justify-between items-center pb-2 border-b border-white/10">
          <span className="text-secondary text-sm">Status</span>
          <BaseBadge variant={result.is_calibrated ? 'success' : 'warning'}>{result.is_calibrated ? 'CALIBRATED' : 'UNVERIFIED'}</BaseBadge>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-secondary text-sm">Gain Correction</span>
          <span className={`text-sm ${result.gain_correction_applied ? 'text-green-400' : 'text-red-400'}`}>
            {result.gain_correction_applied ? 'APPLIED' : 'MISSING'}
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-secondary text-sm">Offset Correction</span>
          <span className={`text-sm ${result.offset_correction_applied ? 'text-green-400' : 'text-red-400'}`}>
            {result.offset_correction_applied ? 'APPLIED' : 'MISSING'}
          </span>
        </div>

        <div className="mt-2 pt-2 border-t border-white/10 flex justify-between items-center">
          <span className="text-secondary text-xs uppercase tracking-wider">Confidence</span>
          <span className="text-lg font-mono text-primary">{(result.calibration_confidence * 100).toFixed(1)}%</span>
        </div>
      </div>
    </BaseCard>
  );
};
