import React from 'react';
import { useWorkspaceStore } from '../../../realtime/workspaceStore';
import { useGraphStore } from '../../knowledge-graph/store/graphStore';
import { BaseCard, BaseBadge, Icon } from '@design-system/index';

export const ScientificContextPanel: React.FC = () => {
  const { globalCursorTime, activeRegion } = useWorkspaceStore();
  const { selectedNodeId, nodes } = useGraphStore();

  const selectedNode = nodes.find(n => n.id === selectedNodeId);

  return (
    <div className="flex flex-col gap-4">
      <div className="text-on-surface-variant font-body-sm text-[12px] leading-relaxed">
        The AI Scientist automatically injects the following context into your queries. You do not need to manually specify IDs or timestamps.
      </div>

      {/* Global Time Context */}
      <BaseCard variant="plain" size="sm" className="shadow-sm border-primary/20 bg-primary/5">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded bg-primary text-white flex items-center justify-center shadow-sm">
            <Icon name="schedule" className="text-[18px]" />
          </div>
          <div>
            <div className="font-label-caps text-[10px] text-primary uppercase font-bold tracking-wider">Mission Timeline</div>
            <div className="font-data-mono text-[14px] text-on-surface font-bold mt-0.5">
              {globalCursorTime ? new Date(globalCursorTime).toISOString().replace('T', ' ').substring(0, 19) : 'LIVE'} UTC
            </div>
          </div>
        </div>
      </BaseCard>

      {/* Active Region Context */}
      {activeRegion ? (
        <BaseCard variant="plain" size="sm" className="shadow-sm border-secondary-container/20 bg-secondary-container/5 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-2">
            <BaseBadge variant="warning">Tracking</BaseBadge>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded bg-secondary-container text-white flex items-center justify-center shadow-sm">
              <Icon name="my_location" className="text-[18px]" />
            </div>
            <div>
              <div className="font-label-caps text-[10px] text-secondary-container uppercase font-bold tracking-wider">Digital Twin Region</div>
              <div className="font-display-sm text-[16px] text-on-surface font-bold mt-0.5">{activeRegion.id}</div>
              <div className="font-data-mono text-[11px] text-on-surface-variant mt-1">Lat: {activeRegion.lat.toFixed(1)}° | Lon: {activeRegion.lon.toFixed(1)}°</div>
            </div>
          </div>
        </BaseCard>
      ) : (
        <BaseCard variant="plain" size="sm" className="shadow-sm border-dashed border-outline-variant opacity-60">
          <div className="text-center p-2 text-on-surface-variant">
            <Icon name="public" className="text-[24px] mb-2 opacity-50" />
            <div className="font-label-caps text-[11px] uppercase">Full Disk Mode</div>
            <div className="font-body-sm text-[10px] mt-1">No region selected in Digital Twin.</div>
          </div>
        </BaseCard>
      )}

      {/* Knowledge Graph Context */}
      {selectedNode ? (
        <BaseCard variant="plain" size="sm" className="shadow-sm border-[#9c27b0]/20 bg-[#9c27b0]/5 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-[#9c27b0]" />
          <div className="flex items-start gap-3 pl-2">
            <div className="w-8 h-8 rounded bg-[#9c27b0] text-white flex items-center justify-center shadow-sm">
              <Icon name="schema" className="text-[18px]" />
            </div>
            <div>
              <div className="font-label-caps text-[10px] text-[#9c27b0] uppercase font-bold tracking-wider">Graph Node</div>
              <div className="font-display-sm text-[16px] text-on-surface font-bold mt-0.5">{selectedNode.data.label}</div>
              <div className="font-data-mono text-[11px] text-on-surface-variant mt-1">{selectedNode.data.type}</div>
            </div>
          </div>
          <div className="mt-3 pl-2">
            {selectedNode.data.metadata && Object.keys(selectedNode.data.metadata).length > 0 && (
              <div className="flex flex-wrap gap-1">
                {Object.entries(selectedNode.data.metadata).map(([k, v]) => (
                  <span key={k} className="bg-white/50 border border-[#9c27b0]/30 px-1.5 py-0.5 rounded font-body-sm text-[10px] text-on-surface truncate max-w-[120px]">
                    {k}: {String(v)}
                  </span>
                ))}
              </div>
            )}
          </div>
        </BaseCard>
      ) : (
        <BaseCard variant="plain" size="sm" className="shadow-sm border-dashed border-outline-variant opacity-60">
          <div className="text-center p-2 text-on-surface-variant">
            <Icon name="account_tree" className="text-[24px] mb-2 opacity-50" />
            <div className="font-label-caps text-[11px] uppercase">Graph Inactive</div>
            <div className="font-body-sm text-[10px] mt-1">No entity selected in Knowledge Graph.</div>
          </div>
        </BaseCard>
      )}
    </div>
  );
};
