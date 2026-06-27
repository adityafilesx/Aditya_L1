import type { FC, ReactNode } from 'react';

interface MissionControlLayoutV5Props {
  missionForecastSummary: ReactNode;
  missionForecastCore: ReactNode;
  scientificIntelligence: ReactNode;
  decisionIntelligence: ReactNode;
  machineIntelligence: ReactNode;
  trustAndRepository: ReactNode;
  pipelineFlow: ReactNode;
  platformDiagnostics: ReactNode;
}

export const MissionControlLayoutV5: FC<MissionControlLayoutV5Props> = ({
  missionForecastSummary,
  missionForecastCore,
  scientificIntelligence,
  decisionIntelligence,
  machineIntelligence,
  trustAndRepository,
  pipelineFlow,
  platformDiagnostics
}) => {
  return (
    <div className="h-full w-full bg-surface-container-lowest/20 flex flex-col overflow-hidden text-foreground select-none">
      
      {/* 1. Zone 1: Mission Forecast Summary (Global Status, Context & Alert Ladder) */}
      <div className="w-full flex-shrink-0 border-b border-border/40 z-20 bg-surface-container-low/50 backdrop-blur-md">
        {missionForecastSummary}
      </div>

      {/* 2. Workspace Grid (Zones 2-6) - Scrollable on small screens */}
      <div className="flex-1 overflow-y-auto min-h-0 custom-scrollbar pb-4">
        <div className="grid grid-cols-12 gap-3 p-3 min-h-full h-fit">
          
          {/* Zone 3: Scientific Intelligence (Width 25%) */}
          <div className="col-span-3 flex flex-col h-full">
            {scientificIntelligence}
          </div>

          {/* Zone 2: Forecast Core (Width 50%) */}
          <div className="col-span-6 flex flex-col h-full">
            {missionForecastCore}
          </div>

          {/* Right Column: Decision, Machine, Trust & Repository (Width 25%) */}
          <div className="col-span-3 flex flex-col gap-3 h-full">
            
            {/* Zone 4: Decision Intelligence */}
            <div className="flex-1 flex flex-col min-h-[300px]">
              {decisionIntelligence}
            </div>
            
            {/* Zone 5: Machine Intelligence */}
            <div className="flex-shrink-0 flex flex-col min-h-[320px]">
              {machineIntelligence}
            </div>

            {/* Zone 6: Trust & Repository */}
            <div className="flex-shrink-0 flex flex-col min-h-[140px]">
              {trustAndRepository}
            </div>

          </div>

        </div>
      </div>

      {/* 3. Footer Stack (Zones 7) */}
      <div className="w-full h-8 flex-shrink-0 flex items-center justify-between border-t border-border/40 bg-surface-container-lowest/95 backdrop-blur-md z-30 overflow-hidden">
        {/* Pipeline Stepper (Left) */}
        <div className="flex-[1.3] min-w-0 h-full">
          {pipelineFlow}
        </div>
        
        {/* Platform Diagnostics Footer Strip (Right) */}
        <div className="flex-1 min-w-0 h-full flex justify-end">
          {platformDiagnostics}
        </div>
      </div>

    </div>
  );
};
export default MissionControlLayoutV5;
