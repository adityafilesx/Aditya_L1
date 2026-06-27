import type { FC, ReactNode } from 'react';

interface MissionControlLayoutV2Props {
  pipelineFlow: ReactNode;
  forecastSummary: ReactNode;
  scientificIntelligence: ReactNode;
  missionForecastCore: ReactNode;
  operatorCommand: ReactNode;
  researchWorkspace: ReactNode;
  platformDiagnostics: ReactNode;
}

export const MissionControlLayoutV2: FC<MissionControlLayoutV2Props> = ({
  pipelineFlow,
  forecastSummary,
  scientificIntelligence,
  missionForecastCore,
  operatorCommand,
  researchWorkspace,
  platformDiagnostics
}) => {
  return (
    <div className="h-full w-full bg-surface-container-lowest/20 flex flex-col overflow-hidden text-foreground select-none">
      
      {/* 1. Top Pipeline Flow Banner */}
      <div className="w-full flex-shrink-0 z-30">
        {pipelineFlow}
      </div>

      {/* 2. Mission Forecast Summary Banner */}
      <div className="w-full flex-shrink-0 border-b border-border/40 z-20">
        {forecastSummary}
      </div>

      {/* 3. Workspace Grid */}
      <div className="flex-1 grid grid-cols-12 gap-3 p-3 min-h-0 overflow-hidden">
        
        {/* Left Column: Scientific Intelligence (Width 25%) */}
        <div className="col-span-3 flex flex-col min-h-0 overflow-hidden">
          {scientificIntelligence}
        </div>

        {/* Center Column: Forecast Core (Width 50%) */}
        <div className="col-span-6 flex flex-col min-h-0 overflow-hidden">
          {missionForecastCore}
        </div>

        {/* Right Column: Operator, ML Registry (Width 25%) */}
        <div className="col-span-3 flex flex-col gap-3 min-h-0 overflow-hidden">
          
          {/* Operator Intelligence - 56% height */}
          <div className="h-[56%] min-h-0 flex flex-col">
            {operatorCommand}
          </div>
          
          {/* Machine & Feature Registry - 44% height */}
          <div className="h-[44%] min-h-0 flex flex-col">
            {researchWorkspace}
          </div>

        </div>

      </div>

      {/* 4. Platform Operations Footer Strip */}
      <div className="w-full h-8 flex-shrink-0 border-t border-border/40 bg-surface-container-lowest/80 backdrop-blur-md z-30">
        {platformDiagnostics}
      </div>

    </div>
  );
};
export default MissionControlLayoutV2;
