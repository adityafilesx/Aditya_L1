import React from 'react';
import { Panel } from '@xyflow/react';
import { Icon } from '@design-system/index';

interface GraphToolbarProps {
  onLayout: () => void;
}

export const GraphToolbar: React.FC<GraphToolbarProps> = ({ onLayout }) => {
  return (
    <Panel position="top-left" className="m-4">
      <div className="flex gap-2 bg-surface/90 backdrop-blur-md p-2 rounded-xl shadow-lg border border-surface-variant">
        <div className="relative">
          <Icon name="search" className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[16px]" />
          <input 
            type="text" 
            placeholder="Search Mission Memory..." 
            className="pl-9 pr-4 py-1.5 w-64 bg-surface-container border border-surface-variant rounded-lg font-body-sm outline-none focus:border-primary transition-colors text-on-surface"
          />
        </div>
        
        <div className="w-px bg-surface-variant mx-1 my-1" />
        
        <button 
          onClick={onLayout}
          className="px-3 py-1.5 bg-surface-container hover:bg-surface-container-high rounded-lg font-label-caps text-[11px] font-bold text-on-surface flex items-center gap-2 border border-surface-variant transition-colors"
          title="Auto-Layout (ELK)"
        >
          <Icon name="schema" className="text-[16px]" />
          LAYOUT
        </button>

        <button 
          className="px-3 py-1.5 bg-surface-container hover:bg-surface-container-high rounded-lg font-label-caps text-[11px] font-bold text-on-surface flex items-center gap-2 border border-surface-variant transition-colors"
        >
          <Icon name="filter_list" className="text-[16px]" />
          FILTER
        </button>
        
        <button 
          className="px-3 py-1.5 bg-surface-container hover:bg-surface-container-high rounded-lg font-label-caps text-[11px] font-bold text-on-surface flex items-center gap-2 border border-surface-variant transition-colors"
        >
          <Icon name="download" className="text-[16px]" />
          EXPORT
        </button>
      </div>
    </Panel>
  );
};
