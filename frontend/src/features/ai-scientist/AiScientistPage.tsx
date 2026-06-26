import type { FC } from 'react';
import { PageLayout, Header } from '@design-system/index';
import { AiWorkspaceLayout } from './components/AiWorkspaceLayout';

export const AiScientistPage: FC = () => {
  return (
    <>
      <Header
        title="AI Scientist Workspace"
        subtitle="GraphRAG Intelligence • Mission Analytics • Explainable AI"
        actions={
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-success shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse"></span>
            <span className="font-label-caps text-[10px] uppercase text-success tracking-widest font-bold">Agents Active</span>
          </div>
        }
      />
      <PageLayout className="p-0 overflow-hidden">
        <AiWorkspaceLayout />
      </PageLayout>
    </>
  );
};
