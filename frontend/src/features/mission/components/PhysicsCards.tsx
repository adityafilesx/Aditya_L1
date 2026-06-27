import React from 'react';
import { BaseCard, Icon } from '@design-system/index';
import { formatScientific } from '@utils/formatters';
import { cn } from '@utils/cn';

interface PhysicsCardProps {
  physics: any;
}

const MetricRow: React.FC<{ label: string; value: string; unit?: string; highlight?: boolean }> = ({ label, value, unit, highlight }) => (
  <div className="flex justify-between items-center p-2 bg-surface-container-low border border-outline-variant rounded">
    <span className="text-[11px] font-label-caps text-on-surface-variant">{label}</span>
    <div className="flex items-baseline gap-1">
      <span className={cn("font-data-mono text-[11px]", highlight ? "text-primary font-bold" : "text-on-surface")}>{value}</span>
      {unit && <span className="text-[9px] text-on-surface-variant font-label-caps">{unit}</span>}
    </div>
  </div>
);

export const ThermalProfileCard: React.FC<PhysicsCardProps> = ({ physics }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title={
      <span className="flex items-center gap-2 font-label-caps text-[11px] text-on-surface">
        <Icon name="thermostat" className="text-[14px] text-error" /> THERMAL PROFILE
      </span>
    }>
      <div className="space-y-3">
        <MetricRow 
          label="Temperature" 
          value={physics?.temperature_mk?.toFixed(2) ?? '---'} 
          unit="MK" 
          highlight 
        />
        <MetricRow 
          label="Emission Measure" 
          value={formatScientific(physics?.emission_measure_norm)} 
          unit="cm⁻³" 
        />
      </div>
    </BaseCard>
  );
};

export const SpectralProfileCard: React.FC<PhysicsCardProps> = ({ physics }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title={
      <span className="flex items-center gap-2 font-label-caps text-[11px] text-on-surface">
        <Icon name="graphic_eq" className="text-[14px] text-secondary" /> SPECTRAL PROFILE
      </span>
    }>
      <div className="space-y-3">
        <MetricRow 
          label="Spectral Centroid" 
          value={physics?.spectral_centroid?.toFixed(3) ?? '---'} 
          highlight 
        />
        <MetricRow 
          label="Spectral Flatness" 
          value={physics?.spectral_flatness?.toFixed(3) ?? '---'} 
        />
        <MetricRow 
          label="Spectral Rolloff" 
          value={physics?.spectral_rolloff?.toFixed(2) ?? '---'} 
        />
      </div>
    </BaseCard>
  );
};

export const PlasmaStateCard: React.FC<PhysicsCardProps> = ({ physics }) => {
  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title={
      <span className="flex items-center gap-2 font-label-caps text-[11px] text-on-surface">
        <Icon name="lens_blur" className="text-[14px] text-primary" /> PLASMA STATE
      </span>
    }>
      <div className="space-y-3">
        <MetricRow 
          label="Shannon Entropy" 
          value={physics?.shannon_entropy?.toFixed(3) ?? '---'} 
          highlight 
        />
      </div>
    </BaseCard>
  );
};

export const NeupertConsistencyCard: React.FC<PhysicsCardProps> = ({ physics }) => {
  const score = physics?.neupert_score;
  const isConsistent = score !== undefined && score !== null && score > 0;

  return (
    <BaseCard variant="plain" size="md" className="card-shadow h-full" title={
      <span className="flex items-center gap-2 font-label-caps text-[11px] text-on-surface">
        <Icon name="timeline" className="text-[14px] text-warning" /> NEUPERT EFFECT
      </span>
    }>
      <div className="flex flex-col items-center justify-center h-full min-h-[80px] gap-2">
        <span className={cn("text-3xl font-numeric-telemetry font-bold", isConsistent ? "text-success" : "text-on-surface-variant")}>
          {score?.toFixed(3) ?? '---'}
        </span>
        <span className="text-[10px] font-label-caps text-on-surface-variant">Consistency Score</span>
      </div>
    </BaseCard>
  );
};
