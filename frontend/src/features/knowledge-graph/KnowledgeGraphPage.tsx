import type { FC } from 'react';
import { 
  PageLayout, 
  Header, 
  BaseCard
} from '@design-system/index';

import { KnowledgeGraphWorkspace } from './components/KnowledgeGraphWorkspace';
import { ScientificInspector } from './components/ScientificInspector';

export const KnowledgeGraphPageContent: FC = () => {
  return (
    <>
      <Header
        title="Knowledge Graph"
        subtitle="Scientific Event Intelligence • Causal Analysis • Mission Knowledge Base"
        actions={
          <div className="flex items-center gap-6 bg-surface p-4 rounded-[18px] border border-surface-variant shadow-sm">
            <div className="text-right">
              <div className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1">Events Indexed</div>
              <div className="font-numeric-telemetry text-numeric-telemetry font-bold text-on-surface">12,458</div>
            </div>
            <div className="w-px h-10 bg-surface-variant"></div>
            <div className="text-right">
              <div className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1">Relationships</div>
              <div className="font-numeric-telemetry text-numeric-telemetry font-bold text-on-surface">98,341</div>
            </div>
          </div>
        }
      />
      
      <div className="grid grid-cols-12 gap-gutter">
        {/* Left Side (Graph Workspace) */}
        <div className="col-span-12 lg:col-span-9 flex flex-col gap-gutter h-[calc(100vh-200px)]">
          <BaseCard variant="plain" className="h-full flex flex-col p-0 overflow-hidden shadow-sm border border-outline-variant/30">
            <KnowledgeGraphWorkspace />
          </BaseCard>
        </div>
        
        {/* Right Side (Inspector) */}
        <div className="col-span-12 lg:col-span-3 flex flex-col gap-gutter h-[calc(100vh-200px)]">
          <ScientificInspector />
        </div>
      </div>
      
      {/* Timeline */}
      <BaseCard variant="plain" size="md" className="mt-gutter shadow-sm" title="Graph Ingestion Timeline" icon="update">
        <div className="flex gap-4 overflow-x-auto hide-scrollbar pb-2 mt-4">
          <div className="flex-none w-64 border-l-2 border-primary pl-3">
            <div className="font-data-mono text-[10px] text-on-surface-variant/60 mb-1">10:42:15 UTC</div>
            <div className="font-body-sm text-on-surface">Node <span className="font-data-mono text-primary bg-primary/10 px-1 rounded">AR13872</span> updated properties</div>
          </div>
          
          <div className="flex-none w-64 border-l-2 border-secondary-container pl-3">
            <div className="font-data-mono text-[10px] text-on-surface-variant/60 mb-1">10:38:02 UTC</div>
            <div className="font-body-sm text-on-surface">New edge formed: <span className="font-data-mono text-[12px]">Flare_M1.2 -&gt; CME_094</span></div>
          </div>
          
          <div className="flex-none w-64 border-l-2 border-surface-variant pl-3 opacity-60">
            <div className="font-data-mono text-[10px] text-on-surface-variant/60 mb-1">10:15:00 UTC</div>
            <div className="font-body-sm text-on-surface">Telemetry sync complete (9,402 metrics)</div>
          </div>
          
          <div className="flex-none w-64 border-l-2 border-surface-variant pl-3 opacity-60">
            <div className="font-data-mono text-[10px] text-on-surface-variant/60 mb-1">09:00:00 UTC</div>
            <div className="font-body-sm text-on-surface">Daily model re-training executed.</div>
          </div>
        </div>
      </BaseCard>
    </>
  );
};

export const KnowledgeGraphPage: FC = () => (
  <PageLayout className="p-gutter">
    <KnowledgeGraphPageContent />
  </PageLayout>
);

export default KnowledgeGraphPage;
