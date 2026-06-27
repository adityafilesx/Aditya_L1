import type { FC } from 'react';
import { BaseCard, Icon } from '@design-system/index';
import { useForecast } from '../../hooks/useForecast';
import { DataFreshnessCard } from '../../widgets/DataFreshnessCard';
import { FeatureSearchCard } from '../widgets/FeatureSearchCard';
import { FeatureReplayCard } from '../widgets/FeatureReplayCard';
import { FeatureStatisticsCard } from '../widgets/FeatureStatisticsCard';
import { FeatureVersionCard } from '../widgets/FeatureVersionCard';
import { FeatureRegistryCard } from '../widgets/FeatureRegistryCard';

// Milestone 5 ML Cards
import { TrainingStatusCard } from '../widgets/TrainingStatusCard';
import { ModelComparisonCard } from '../widgets/ModelComparisonCard';
import { ModelRegistryCard } from '../widgets/ModelRegistryCard';
import { ExperimentRegistryCard } from '../widgets/ExperimentRegistryCard';
import { DatasetRegistryCard } from '../widgets/DatasetRegistryCard';
import { ModelLeaderboardCard } from '../widgets/ModelLeaderboardCard';
import { AblationStudyCard } from '../widgets/AblationStudyCard';
import { PromotionStatusCard } from '../widgets/PromotionStatusCard';
import { ScientificEvidenceCard } from '../widgets/ScientificEvidenceCard';
import { ExplanationCard } from '../widgets/ExplanationCard';
import { TrustScoreCard } from '../widgets/TrustScoreCard';
import { PlatformHealthCard } from '../widgets/PlatformHealthCard';
import { DeploymentStatusCard } from '../widgets/DeploymentStatusCard';
import { DiagnosticsCard } from '../widgets/DiagnosticsCard';
import { TraceabilityMatrixCard } from '../widgets/TraceabilityMatrixCard';

export const ResearchWorkspace: FC = () => {
  const { currentObservation } = useForecast();

  return (
    <BaseCard
      variant="plain"
      size="md"
      className="card-shadow h-full flex flex-col"
      title={
        <span className="font-label-caps text-label-caps text-on-surface flex items-center gap-2">
          <Icon name="library_books" className="text-tertiary" /> Observation Research
        </span>
      }
    >
      <div className="flex-1 overflow-y-auto">
        {!currentObservation ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-4">
            <Icon name="history" className="text-4xl text-on-surface-variant/50 mb-2" />
            <p className="text-on-surface-variant font-label-caps">Awaiting Connection</p>
          </div>
        ) : (
          <div className="flex flex-col gap-4 pb-4 h-full">
            <DataFreshnessCard provenance={currentObservation.provenance} />

            <div className="border-t border-slate-800/80 pt-4 mt-2 space-y-4">
              <TrainingStatusCard />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <ModelLeaderboardCard />
                <PromotionStatusCard />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-slate-800/80 pt-4 mt-2">
                <ScientificEvidenceCard />
                <ExplanationCard />
                <TrustScoreCard />
              </div>
              <div className="grid grid-cols-2 gap-4 mt-4 border-t border-slate-800/80 pt-4">
                <PlatformHealthCard />
                <DeploymentStatusCard />
                <DiagnosticsCard />
                <TraceabilityMatrixCard />
              </div>
              <AblationStudyCard />
              <ModelComparisonCard />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <ModelRegistryCard />
                <ExperimentRegistryCard />
                <DatasetRegistryCard />
              </div>
            </div>
            
            <FeatureSearchCard />
            <FeatureReplayCard />
            
            <div className="grid grid-cols-2 gap-4">
              <FeatureStatisticsCard />
              <FeatureVersionCard />
            </div>

            <FeatureRegistryCard />
          </div>
        )}
      </div>
    </BaseCard>
  );
};
