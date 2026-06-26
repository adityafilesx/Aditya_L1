import React, { useState } from 'react';
import { useAiScientistStore } from '../store/aiScientistStore';
import { ScientificContextPanel } from './ScientificContextPanel';
import { CommandConsole } from './CommandConsole';
import { ResearchConversation } from './ResearchConversation';
import { ExplainableAiWorkspace } from './ExplainableAiWorkspace';
import { ExperimentManager } from './ExperimentManager';
import { PublicationBuilder } from './PublicationBuilder';
import { Icon } from '@design-system/index';

export const AiWorkspaceLayout: React.FC = () => {
  const { activeMode, setMode } = useAiScientistStore();
  const [historyOpen, setHistoryOpen] = useState(true);
  const [contextOpen, setContextOpen] = useState(true);

  return (
    <div className="flex w-full h-[calc(100vh-140px)] bg-surface-container-lowest overflow-hidden">
      
      {/* LEFT: History Panel */}
      <div className={`transition-all duration-300 border-r border-surface-variant flex flex-col bg-surface ${historyOpen ? 'w-[250px]' : 'w-[50px] items-center'}`}>
        <div className="p-3 border-b border-surface-variant flex items-center justify-between">
          {historyOpen && <span className="font-label-caps text-label-caps uppercase text-on-surface font-bold">Research Memory</span>}
          <button onClick={() => setHistoryOpen(!historyOpen)} className="text-on-surface-variant hover:text-primary transition-colors cursor-pointer border-none bg-transparent">
            <Icon name={historyOpen ? 'keyboard_double_arrow_left' : 'menu'} />
          </button>
        </div>
        {historyOpen && (
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            <div className="p-2 bg-surface-container-low hover:bg-surface-container rounded-lg cursor-pointer border border-surface-variant">
              <div className="font-body-sm font-bold text-on-surface truncate">M4.2 Flare Analysis</div>
              <div className="font-data-mono text-[10px] text-on-surface-variant mt-1">2 hours ago</div>
            </div>
            <div className="p-2 hover:bg-surface-container rounded-lg cursor-pointer border border-transparent">
              <div className="font-body-sm font-bold text-on-surface truncate">Spectral Fitting (AR13872)</div>
              <div className="font-data-mono text-[10px] text-on-surface-variant mt-1">Yesterday</div>
            </div>
            <div className="p-2 hover:bg-surface-container rounded-lg cursor-pointer border border-transparent">
              <div className="font-body-sm font-bold text-on-surface truncate">CME Prediction Explainability</div>
              <div className="font-data-mono text-[10px] text-on-surface-variant mt-1">Jun 23, 2026</div>
            </div>
          </div>
        )}
      </div>

      {/* CENTER: Main Workspace */}
      <div className="flex-1 flex flex-col min-w-0 bg-surface-container-lowest relative">
        {/* Mode Selector */}
        <div className="h-[48px] border-b border-surface-variant bg-surface flex items-center px-4 gap-4 overflow-x-auto hide-scrollbar">
          {[
            { id: 'chat', label: 'Copilot', icon: 'forum' },
            { id: 'xai', label: 'Explainability', icon: 'model_training' },
            { id: 'experiment', label: 'Experiments', icon: 'science' },
            { id: 'literature', label: 'Literature', icon: 'menu_book' },
            { id: 'report', label: 'Publish', icon: 'picture_as_pdf' },
          ].map(m => (
            <button
              key={m.id}
              onClick={() => setMode(m.id as any)}
              className={`flex items-center gap-2 font-label-caps text-[11px] font-bold uppercase transition-colors px-3 py-1.5 rounded-lg border cursor-pointer ${
                activeMode === m.id 
                  ? 'bg-primary text-white border-primary shadow-[0_2px_8px_rgba(65,64,209,0.3)]' 
                  : 'bg-transparent text-on-surface-variant border-transparent hover:bg-surface-container hover:text-on-surface'
              }`}
            >
              <Icon name={m.icon} className="text-[16px]" /> {m.label}
            </button>
          ))}
        </div>
        
        {/* Workspace Content */}
        <div className="flex-1 overflow-hidden relative">
          {activeMode === 'chat' && <ResearchConversation />}
          {activeMode === 'xai' && <ExplainableAiWorkspace />}
          {activeMode === 'experiment' && <ExperimentManager />}
          {activeMode === 'literature' && <div className="p-8 text-on-surface-variant">Literature Engine (Under Construction)</div>}
          {activeMode === 'report' && <PublicationBuilder />}
        </div>

        {/* Command Console */}
        {activeMode === 'chat' && (
          <div className="border-t border-surface-variant bg-surface p-4">
            <CommandConsole />
          </div>
        )}
      </div>

      {/* RIGHT: Context Panel */}
      <div className={`transition-all duration-300 border-l border-surface-variant flex flex-col bg-surface ${contextOpen ? 'w-[320px]' : 'w-[50px] items-center'}`}>
        <div className="p-3 border-b border-surface-variant flex items-center justify-between">
          {contextOpen && <span className="font-label-caps text-label-caps uppercase text-on-surface font-bold flex items-center gap-2"><Icon name="account_tree" className="text-primary text-[16px]" /> Scientific Context</span>}
          <button onClick={() => setContextOpen(!contextOpen)} className="text-on-surface-variant hover:text-primary transition-colors cursor-pointer border-none bg-transparent">
            <Icon name={contextOpen ? 'keyboard_double_arrow_right' : 'dock'} />
          </button>
        </div>
        {contextOpen && (
          <div className="flex-1 overflow-y-auto p-4">
            <ScientificContextPanel />
          </div>
        )}
      </div>
    </div>
  );
};
