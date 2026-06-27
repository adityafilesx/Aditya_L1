import type { FC } from 'react';

import { MissionControlLayoutV5 } from './layouts/MissionControlLayoutV5';
import { PipelineFlow } from './components/PipelineFlow';
import { MissionForecastSummary } from './components/MissionForecastSummary';
import { ScientificIntelligence } from './components/ScientificIntelligence';
import { MissionForecastCore } from './components/MissionForecastCore';
import { OperatorCommand } from './components/OperatorCommand';
import { MachineIntelligence } from './components/MachineIntelligence';
import { TrustAndRepository } from './components/TrustAndRepository';
import { PlatformDiagnostics } from './components/PlatformDiagnostics';

import { useObservationStream } from './hooks/useObservationStream';
import { useNowcastStream } from './hooks/useNowcastStream';
import { useForecastPolling } from './hooks/useForecastPolling';

export const ForecastingPageContent: FC = () => {
  // Start all realtime streams and polling
  useObservationStream();
  useNowcastStream();
  useForecastPolling();

  return (
    <MissionControlLayoutV5
      missionForecastSummary={<MissionForecastSummary />}
      missionForecastCore={<MissionForecastCore />}
      scientificIntelligence={<ScientificIntelligence />}
      decisionIntelligence={<OperatorCommand />}
      machineIntelligence={<MachineIntelligence />}
      trustAndRepository={<TrustAndRepository />}
      pipelineFlow={<PipelineFlow />}
      platformDiagnostics={<PlatformDiagnostics />}
    />
  );
};

export const ForecastingPage: FC = () => (
  <ForecastingPageContent />
);

export default ForecastingPage;
