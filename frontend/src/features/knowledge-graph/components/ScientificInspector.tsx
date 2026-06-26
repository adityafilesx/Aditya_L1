import React from 'react';
import { useGraphStore } from '../store/graphStore';
import { useWorkspaceStore } from '../../../realtime/workspaceStore';
import { BaseCard, Icon, BaseBadge } from '@design-system/index';

export const ScientificInspector: React.FC = () => {
  const { selectedNodeId, nodes } = useGraphStore();
  const setDigitalTwinCursor = useWorkspaceStore((state: any) => state.setCursorTime);
  const setActiveRegion = useWorkspaceStore((state: any) => state.setActiveRegion);

  const selectedNode = nodes.find(n => n.id === selectedNodeId);

  if (!selectedNode) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-on-surface-variant/50 p-8 text-center">
        <Icon name="hub" className="text-[48px] mb-4 opacity-50" />
        <div className="font-body-lg">Select a node in the graph to view its scientific properties and reasoning chains.</div>
      </div>
    );
  }

  const { data } = selectedNode;

  const handleSyncDigitalTwin = () => {
    // Synchronize global workspace with this node's timeline and region (if any)
    const time = new Date(data.timestamp).getTime();
    setDigitalTwinCursor(time);
    
    if (data.metadata?.regionId) {
      // Mock AR metadata
      setActiveRegion({
        id: data.metadata.regionId,
        lat: Number(data.metadata.lat || 15),
        lon: Number(data.metadata.lon || -25),
      });
    }
  };

  return (
    <div className="h-full flex flex-col gap-4 overflow-y-auto pr-2">
      {/* Header Info */}
      <div className="bg-surface border border-surface-variant rounded-xl p-4 shadow-sm relative overflow-hidden">
        <div className="absolute top-0 left-0 w-1 h-full bg-primary" />
        <div className="flex justify-between items-start mb-2">
          <BaseBadge variant="primary">{data.type}</BaseBadge>
          {data.confidence && (
            <span className="font-numeric-telemetry font-bold text-[14px] text-on-surface">
              {(data.confidence * 100).toFixed(1)}% Conf
            </span>
          )}
        </div>
        <h2 className="font-display-md text-[20px] font-bold text-on-surface mt-2">{data.label}</h2>
        <div className="font-data-mono text-[11px] text-on-surface-variant mt-1">
          {new Date(data.timestamp).toLocaleString()}
        </div>
      </div>

      {/* Actions */}
      <div className="grid grid-cols-2 gap-2">
        <button 
          onClick={handleSyncDigitalTwin}
          className="bg-primary text-white py-2 rounded-lg font-label-caps text-[11px] font-bold shadow-sm hover:shadow-md transition-all flex items-center justify-center gap-2 border border-primary/20"
        >
          <Icon name="travel_explore" className="text-[16px]" /> SYNC TWIN
        </button>
        <button className="bg-surface-container text-on-surface py-2 rounded-lg font-label-caps text-[11px] font-bold border border-surface-variant hover:bg-surface-container-high transition-colors flex items-center justify-center gap-2">
          <Icon name="history" className="text-[16px]" /> REASONING
        </button>
      </div>

      {/* Metadata */}
      <BaseCard variant="plain" size="sm" title="Scientific Metadata" icon="data_object" className="shadow-sm">
        <div className="mt-2 space-y-2">
          {data.metadata && Object.entries(data.metadata).map(([key, value]) => (
            <div key={key} className="flex justify-between items-end border-b border-surface-variant/50 pb-1">
              <span className="font-body-sm text-on-surface-variant text-[12px]">{key}</span>
              <span className="font-data-mono font-bold text-[12px] text-on-surface truncate max-w-[150px]">{String(value)}</span>
            </div>
          ))}
        </div>
      </BaseCard>

      {/* Similarity Engine Hook */}
      <BaseCard variant="plain" size="sm" title="Historical Similarity" icon="auto_graph" className="shadow-sm">
        <div className="text-[11px] text-on-surface-variant mb-3 leading-relaxed">
          Top historical events matching this node's physical and morphological signature.
        </div>
        <div className="space-y-2">
          <div className="flex items-center justify-between bg-surface-container-lowest border border-surface-variant rounded p-2 cursor-pointer hover:border-primary transition-colors">
            <div>
              <div className="font-bold text-[12px] text-on-surface">AR12673 X8.2</div>
              <div className="font-data-mono text-[10px] text-on-surface-variant">2017-09-10</div>
            </div>
            <div className="font-numeric-telemetry text-secondary-container font-bold">94.2%</div>
          </div>
          <div className="flex items-center justify-between bg-surface-container-lowest border border-surface-variant rounded p-2 cursor-pointer hover:border-primary transition-colors">
            <div>
              <div className="font-bold text-[12px] text-on-surface">AR12192 X3.1</div>
              <div className="font-data-mono text-[10px] text-on-surface-variant">2014-10-24</div>
            </div>
            <div className="font-numeric-telemetry text-secondary-container font-bold">88.5%</div>
          </div>
        </div>
      </BaseCard>
    </div>
  );
};
