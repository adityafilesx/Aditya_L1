import type { FC } from 'react';
import { BaseCard, Icon } from '@design-system/index';
import { useForecast } from '../../hooks/useForecast';
import { useForecastStore } from '../../store/forecastStore';
import { InstrumentStatusCard } from '../../widgets/InstrumentStatusCard';
import { TelemetryRateCard } from '../../widgets/TelemetryRateCard';
import { PipelineStatusCard } from '../../widgets/PipelineStatusCard';
import { MLReadinessCard } from '../widgets/MLReadinessCard';
import { FeatureQualityCard } from '../widgets/FeatureQualityCard';
import { FeatureValidationCard } from '../widgets/FeatureValidationCard';

// Milestone 5 ML Cards
import { ServingStatusCard } from '../widgets/ServingStatusCard';
import { ModelHealthCard } from '../widgets/ModelHealthCard';
import { InferenceCard } from '../widgets/InferenceCard';

export const OperatorWorkspace: FC = () => {
  const { currentObservation, pipelineStatus } = useForecast();
  const { nowcastState } = useForecastStore();

  return (
    <BaseCard
      variant="plain"
      size="md"
      className="card-shadow h-full flex flex-col"
      title={
        <span className="font-label-caps text-label-caps text-on-surface flex items-center gap-2">
          <Icon name="admin_panel_settings" className="text-error" /> Pipeline Operations
        </span>
      }
    >
      <div className="flex-1 overflow-y-auto">
        {!currentObservation ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-4">
            <Icon name="sensors_off" className="text-4xl text-on-surface-variant/50 mb-2" />
            <p className="text-on-surface-variant font-label-caps">Awaiting Connection</p>
          </div>
        ) : (
          <div className="flex flex-col gap-4 pb-4">
            <PipelineStatusCard status={pipelineStatus} />
            <div className="grid grid-cols-2 gap-4">
              <InstrumentStatusCard metadata={currentObservation.metadata} />
              <TelemetryRateCard rate={pipelineStatus?.observation_rate_hz || 0} />
            </div>

            <div className="border-t border-slate-800/80 pt-4 mt-2 space-y-4">
              <MLReadinessCard />
              <div className="grid grid-cols-2 gap-4">
                <ServingStatusCard />
                <ModelHealthCard />
              </div>
              <InferenceCard />
              <div className="grid grid-cols-2 gap-4">
                <FeatureQualityCard nowcastState={nowcastState} />
                <FeatureValidationCard nowcastState={nowcastState} />
              </div>
            </div>
          </div>
        )}
      </div>
    </BaseCard>
  );
};
