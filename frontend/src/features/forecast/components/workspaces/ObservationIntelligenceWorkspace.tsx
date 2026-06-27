import type { FC } from 'react';
import { BaseCard, Icon } from '@design-system/index';
import { useForecast } from '../../hooks/useForecast';
import { useForecastStore } from '../../store/forecastStore';
import { ObservationHealthCard } from '../../widgets/ObservationHealthCard';
import { ObservationConfidenceCard } from '../../widgets/ObservationConfidenceCard';
import { QualityFlagCard } from '../../widgets/QualityFlagCard';
import { NoiseStatusCard } from '../../widgets/NoiseStatusCard';
import { DetectorBenchmarkCard } from '../widgets/DetectorBenchmarkCard';
import { FeatureValidationCard } from '../widgets/FeatureValidationCard';
import { FeatureNormalizationCard } from '../widgets/FeatureNormalizationCard';
import { FeatureQualityCard } from '../widgets/FeatureQualityCard';
import { FeatureStatisticsCard } from '../widgets/FeatureStatisticsCard';

export const ObservationIntelligenceWorkspace: FC = () => {
  const { currentObservation } = useForecast();
  const { nowcastState } = useForecastStore();

  return (
    <BaseCard
      variant="plain"
      size="md"
      className="card-shadow h-full flex flex-col"
      title={
        <span className="font-label-caps text-label-caps text-on-surface flex items-center gap-2">
          <Icon name="auto_awesome" className="text-primary" /> Observation Intelligence
        </span>
      }
    >
      <div className="flex-1 overflow-y-auto">
        {!currentObservation ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-4">
            <Icon name="model_training" className="text-4xl text-on-surface-variant/50 mb-2" />
            <p className="text-on-surface-variant font-label-caps">Awaiting Observation Context</p>
            <p className="text-xs text-on-surface-variant/70 mt-2">Observation metrics will appear once telemetry begins streaming.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pb-4">
            <ObservationHealthCard 
              isValid={currentObservation.validation.is_valid}
              missingPackets={currentObservation.validation.missing_packets}
              duplicatePackets={currentObservation.validation.duplicate_packets}
              freshnessMs={currentObservation.validation.freshness_ms}
            />
            <ObservationConfidenceCard result={currentObservation.quality} />
            <NoiseStatusCard result={currentObservation.noise_background} />
            <QualityFlagCard flags={currentObservation.quality.flags} />
            
            <div className="md:col-span-2">
              <DetectorBenchmarkCard nowcastState={nowcastState} />
            </div>

            <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4 border-t border-slate-800/80 pt-4 mt-2">
              <FeatureValidationCard nowcastState={nowcastState} />
              <FeatureNormalizationCard nowcastState={nowcastState} />
              <FeatureQualityCard nowcastState={nowcastState} />
              <FeatureStatisticsCard />
            </div>
          </div>
        )}
      </div>
    </BaseCard>
  );
};
