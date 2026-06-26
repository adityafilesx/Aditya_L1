import { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import type { NodeProps } from '@xyflow/react';
import type { AppNode } from '../../store/graphStore';
import { Icon } from '@design-system/index';

const TYPE_ICONS: Record<string, string> = {
  Flare: 'wb_sunny',
  CME: 'storm',
  Prediction: 'batch_prediction',
  ActiveRegion: 'my_location',
  Telemetry: 'monitor_heart',
  ScientificImage: 'image',
  Sensor: 'sensors',
  MissionState: 'flag',
  PhysicsFeature: 'analytics',
};

const TYPE_COLORS: Record<string, string> = {
  Flare: 'bg-secondary-container text-white border-secondary-fixed',
  CME: 'bg-[#9c27b0] text-white border-[#e1bee7]',
  Prediction: 'bg-primary text-white border-[#c5cae9]',
  ActiveRegion: 'bg-surface-container-high text-on-surface border-outline',
  ScientificImage: 'bg-tertiary-container text-on-tertiary-container border-tertiary-fixed',
  Default: 'bg-surface border-outline-variant text-on-surface',
};

export const ScientificNode = memo(({ data, selected }: NodeProps<AppNode>) => {
  const icon = TYPE_ICONS[data.type] || 'schema';
  const colorClass = TYPE_COLORS[data.type] || TYPE_COLORS.Default;

  return (
    <>
      <Handle type="target" position={Position.Left} className="w-2 h-4 !bg-outline rounded-sm border-none" />
      
      <div className={`w-[280px] shadow-sm rounded-xl border-2 transition-all ${
        selected ? 'border-primary shadow-[0_0_0_2px_rgba(65,64,209,0.2)]' : 'border-transparent'
      }`}>
        <div className={`p-3 rounded-xl flex flex-col gap-2 ${colorClass}`}>
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-2">
              <Icon name={icon} className="text-[18px]" />
              <span className="font-label-caps text-[11px] font-bold uppercase tracking-wider">{data.type}</span>
            </div>
            {data.confidence && (
              <span className="font-numeric-telemetry text-[11px] opacity-90">{Math.round(data.confidence * 100)}%</span>
            )}
          </div>
          
          <div>
            <div className="font-display-sm text-[16px] font-bold truncate leading-tight">{data.label}</div>
            <div className="font-data-mono text-[10px] opacity-80 mt-1">{new Date(data.timestamp).toLocaleTimeString()} UTC</div>
          </div>
          
          {data.metadata && Object.keys(data.metadata).length > 0 && (
            <div className="flex flex-wrap gap-1 mt-1">
              {Object.entries(data.metadata).slice(0, 2).map(([k, v]) => (
                <span key={k} className="bg-black/10 px-1.5 py-0.5 rounded font-body-sm text-[10px] truncate max-w-[120px]">
                  {k}: {String(v)}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      <Handle type="source" position={Position.Right} className="w-2 h-4 !bg-outline rounded-sm border-none" />
    </>
  );
});

ScientificNode.displayName = 'ScientificNode';
