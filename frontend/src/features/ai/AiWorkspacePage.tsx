import type { FC } from 'react';
import { 
  PageLayout, 
  Header
} from '@design-system/index';

// Milestone 5 ML Cards
import { TrainingStatusCard } from '../forecast/components/widgets/TrainingStatusCard';
import { ModelComparisonCard } from '../forecast/components/widgets/ModelComparisonCard';
import { EvaluationCard } from '../forecast/components/widgets/EvaluationCard';
import { CalibrationCard } from '../forecast/components/widgets/CalibrationCard';
import { LearningCurveCard } from '../forecast/components/widgets/LearningCurveCard';
import { ROCViewer } from '../forecast/components/widgets/ROCViewer';
import { ConfusionMatrixViewer } from '../forecast/components/widgets/ConfusionMatrixViewer';
import { ExperimentRegistryCard } from '../forecast/components/widgets/ExperimentRegistryCard';
import { ModelLeaderboardCard } from '../forecast/components/widgets/ModelLeaderboardCard';
import { PromotionStatusCard } from '../forecast/components/widgets/PromotionStatusCard';
import { AblationStudyCard } from '../forecast/components/widgets/AblationStudyCard';

export const AiWorkspacePageSection1: FC = () => (
  <>
    <Header
      title="AI Intelligence Workspace"
      subtitle="Explainable Artificial Intelligence • Forecast Validation • Model Diagnostics"
      actions={
        <div className="flex items-center gap-gutter">
          <div className="hidden lg:flex items-center gap-4 bg-slate-800/60 px-4 py-2 rounded-lg">
            <div className="flex flex-col">
              <span className="font-label-caps text-[10px] text-slate-400">PLATFORM STATUS</span>
              <span className="font-data-mono text-xs text-green-400">NOMINAL</span>
            </div>
            <div className="w-px h-8 bg-slate-700"></div>
            <div className="flex flex-col">
              <span className="font-label-caps text-[10px] text-slate-400">ACTIVE ENSEMBLE</span>
              <span className="font-data-mono text-xs text-primary">ONLINE</span>
            </div>
          </div>
        </div>
      }
    />
  </>
);

export const AiWorkspacePageSection2: FC = () => {
  return (
    <div className="max-w-[1800px] flex flex-col gap-6">
      <div className="grid grid-cols-12 gap-gutter">
        {/* Left Column - Pipeline Control & Comparisons */}
        <div className="col-span-12 lg:col-span-6 xl:col-span-4 flex flex-col gap-gutter">
          <TrainingStatusCard />
          <ModelComparisonCard />
        </div>

        {/* Center Column - Metrics & Calibration */}
        <div className="col-span-12 lg:col-span-6 xl:col-span-4 flex flex-col gap-gutter">
          <EvaluationCard />
          <CalibrationCard />
          <ConfusionMatrixViewer />
        </div>

        {/* Right Column - Plots & Visualizers */}
        <div className="col-span-12 xl:col-span-4 flex flex-col gap-gutter">
          <LearningCurveCard />
          <ROCViewer />
          <PromotionStatusCard />
        </div>
      </div>

      <div className="grid grid-cols-12 gap-gutter mb-6">
        <div className="col-span-12 xl:col-span-6 flex flex-col">
          <ModelLeaderboardCard />
        </div>
        <div className="col-span-12 xl:col-span-6 flex flex-col">
          <AblationStudyCard />
        </div>
      </div>

      {/* Full Width Bottom - Logged Experiments */}
      <div className="w-full">
        <ExperimentRegistryCard />
      </div>

      {/* System log terminal view */}
      <section className="bg-slate-950 rounded-xl p-4 font-data-mono text-[11px] overflow-hidden shadow-2xl border border-slate-800">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="ml-4 text-slate-400">AI_SYSTEM_LOGS_STREAM</span>
          </div>
          <span className="text-slate-400">Uptime: 1422:05:12</span>
        </div>
        <div className="space-y-1 text-slate-300 h-32 overflow-y-auto no-scrollbar">
          <p><span className="text-slate-500">[14:22:01]</span> <span className="text-green-400">INFO:</span> Training orchestrator loaded. Model registry initialized.</p>
          <p><span className="text-slate-500">[14:22:02]</span> <span className="text-green-400">INFO:</span> Loaded features from ScientificFeatureStore.</p>
          <p><span className="text-slate-500">[14:22:03]</span> <span className="text-yellow-400">WARN:</span> Class imbalance ratio above threshold for training splits.</p>
          <p><span className="text-slate-500">[14:22:04]</span> <span className="text-blue-400">DEBUG:</span> Cross-validation strategy configured to walk_forward.</p>
          <p><span className="text-slate-500">[14:22:05]</span> <span className="text-green-400">INFO:</span> Calibration complete. Platt Scaling coefficients registered.</p>
        </div>
      </section>
    </div>
  );
};

export const AiWorkspacePageContent: FC = () => (
  <>
    <AiWorkspacePageSection1 />
    <AiWorkspacePageSection2 />
  </>
);

export const AiWorkspacePage: FC = () => (
  <PageLayout className="px-container-margin py-6">
    <AiWorkspacePageContent />
  </PageLayout>
);

export default AiWorkspacePage;
