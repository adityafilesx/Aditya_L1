import React from 'react';
import { BaseCard } from '@design-system/index';
import type { QualityResult } from '../types/ForecastTypes';

export const ObservationConfidenceCard: React.FC<{ result: QualityResult }> = ({ result }) => {
  return (
    <BaseCard title="Scientific Confidence" className="h-full">
      <div className="flex flex-col gap-4">
        
        <div className="flex flex-col gap-1">
          <div className="flex justify-between items-center text-sm">
            <span className="text-secondary">Overall Confidence</span>
            <span className="text-primary font-mono">{(result.overall_scientific_confidence * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full bg-surface-container rounded-full h-2">
            <div 
              className={`h-2 rounded-full ${result.overall_scientific_confidence > 0.9 ? 'bg-green-500' : result.overall_scientific_confidence > 0.7 ? 'bg-yellow-500' : 'bg-red-500'}`} 
              style={{ width: `${result.overall_scientific_confidence * 100}%` }}
            />
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mt-2">
          <div className="flex flex-col gap-1">
            <span className="text-secondary text-xs uppercase">Observation</span>
            <span className="text-sm font-mono">{(result.observation_quality * 100).toFixed(1)}%</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-secondary text-xs uppercase">Calibration</span>
            <span className="text-sm font-mono">{(result.calibration_confidence * 100).toFixed(1)}%</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-secondary text-xs uppercase">Sync</span>
            <span className="text-sm font-mono">{(result.sync_confidence * 100).toFixed(1)}%</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-secondary text-xs uppercase">Noise</span>
            <span className="text-sm font-mono">{(result.noise_confidence * 100).toFixed(1)}%</span>
          </div>
        </div>

      </div>
    </BaseCard>
  );
};
