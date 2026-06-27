import type { FC } from 'react';
import { useForecastStore } from '../../store/forecastStore';
import { DetectorWidget } from '../widgets/DetectorWidget';
import { TimelineWidget } from '../widgets/TimelineWidget';
import { ThermalCard } from '../widgets/ThermalCard';
import { SpectralCard } from '../widgets/SpectralCard';
import { PlasmaCard } from '../widgets/PlasmaCard';
import { NeupertCard } from '../widgets/NeupertCard';
import { CharacterizationCard } from '../widgets/CharacterizationCard';
import { IndicesCard } from '../widgets/IndicesCard';
import { FeatureStoreCard } from '../widgets/FeatureStoreCard';
import { FeatureRegistryCard } from '../widgets/FeatureRegistryCard';
import { FeatureDependencyGraph } from '../widgets/FeatureDependencyGraph';
import { FeatureValidationCard } from '../widgets/FeatureValidationCard';
import { FeatureQualityCard } from '../widgets/FeatureQualityCard';
import { FeatureNormalizationCard } from '../widgets/FeatureNormalizationCard';
import { PredictionTargetCard } from '../widgets/PredictionTargetCard';
import { LineageExplorer } from '../widgets/LineageExplorer';

// Milestone 5 ML Cards
import { ModelRegistryCard } from '../widgets/ModelRegistryCard';
import { ServingStatusCard } from '../widgets/ServingStatusCard';
import { InferenceCard } from '../widgets/InferenceCard';
import { CalibrationCard } from '../widgets/CalibrationCard';

export const ScientificWorkspace: FC = () => {
  const { nowcastState } = useForecastStore();
  
  return (
    <div className="flex flex-col gap-gutter h-full overflow-y-auto pb-4 pr-1">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter flex-shrink-0">
        <DetectorWidget detector={nowcastState?.solexs_detector} instrumentName="SoLEXS" />
        <DetectorWidget detector={nowcastState?.helios_detector} instrumentName="HEL1OS" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-gutter flex-shrink-0 border-t border-slate-800/60 pt-4">
        <ServingStatusCard />
        <ModelRegistryCard />
        <InferenceCard />
        <CalibrationCard />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-gutter flex-shrink-0 border-t border-slate-800/60 pt-4">
        <ThermalCard physics={nowcastState?.latest_physics || null} />
        <SpectralCard physics={nowcastState?.latest_physics || null} />
        <PlasmaCard physics={nowcastState?.latest_physics || null} />
        <NeupertCard physics={nowcastState?.latest_physics || null} />
        <CharacterizationCard physics={nowcastState?.latest_physics || null} />
        <IndicesCard physics={nowcastState?.latest_physics || null} />
        <FeatureStoreCard nowcastState={nowcastState} />
        <FeatureRegistryCard />
        <FeatureDependencyGraph />
        <FeatureValidationCard nowcastState={nowcastState} />
        <FeatureQualityCard nowcastState={nowcastState} />
        <FeatureNormalizationCard nowcastState={nowcastState} />
        <PredictionTargetCard />
      </div>

      <div className="w-full flex-shrink-0">
        <LineageExplorer />
      </div>
      
      <div className="flex-shrink-0">
        <TimelineWidget />
      </div>
    </div>
  );
};
