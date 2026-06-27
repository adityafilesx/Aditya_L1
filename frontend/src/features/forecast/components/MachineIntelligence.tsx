import type { FC } from 'react';
import { useMemo } from 'react';
import { BaseCard, Icon } from '../../../design-system';
import { useForecast } from '../hooks/useForecast';

export const MachineIntelligence: FC = () => {
  const { selectedModel, nowcastState } = useForecast();

  const data = useMemo(() => {
    const isEnsemble = selectedModel === 'Ensemble Consensus';
    
    return {
      featureStore: {
        vectorId: nowcastState?.latest_feature_vector_id ? nowcastState.latest_feature_vector_id.slice(0, 8) : 'FV-9204A',
        activeCount: '124',
        readiness: 'READY',
      },
      datasetRegistry: {
        dataset: 'Aditya-GTI-2024.1',
        target: 'Soft X-Ray Flux',
        window: 'Last 15m'
      },
      modelRegistry: {
        activeModel: selectedModel || 'Temporal-CN',
        version: isEnsemble ? 'v2.4.1 (Ensemble)' : 'v1.12.0',
        stage: 'PROMOTED (Production)',
        selectionScore: isEnsemble ? '94.2' : '88.5',
        calibration: 'Isotonic Regression',
        implType: 'PyTorch / XGBoost'
      },
      inference: {
        latency: isEnsemble ? '24ms (Batch)' : '8ms',
        throughput: '120 req/s'
      },
      verification: {
        brier: '0.124',
        csi: '0.782',
        hitRate: '0.941',
        reliability: '0.92',
        calibrationErr: '0.04',
        queue: 'Idle (0 active)',
      }
    };
  }, [selectedModel, nowcastState]);

  return (
    <BaseCard className="flex flex-col h-full bg-surface-container-lowest/40 border border-border/20 backdrop-blur-md overflow-hidden p-3">
      
      {/* Component Contract Header */}
      <div className="flex justify-between items-center flex-shrink-0 mb-3 border-b border-border/20 pb-2">
        <div className="flex items-center gap-1.5">
          <Icon name="Database" className="text-primary" />
          <h2 className="text-heading text-foreground">Machine Intelligence</h2>
        </div>
        
        {/* Component Contract Status */}
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
          <span className="text-label text-success font-bold uppercase">NOMINAL</span>
        </div>
      </div>

      <div className="flex-1 flex flex-col gap-3 min-h-0 pr-1">
        
        {/* Row 1: Feature & Dataset */}
        <div className="grid grid-cols-2 gap-3 flex-shrink-0 border-b border-border/20 pb-3">
          <div className="flex flex-col gap-1">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest mb-1">Feature Store</span>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Vector ID:</span><span className="text-primary-metric text-foreground">{data.featureStore.vectorId}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Active Feats:</span><span className="text-primary-metric text-foreground">{data.featureStore.activeCount}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Readiness:</span><span className="text-primary-metric text-success">{data.featureStore.readiness}</span></div>
          </div>
          <div className="flex flex-col gap-1 border-l border-border/20 pl-3">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest mb-1">Dataset Registry</span>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Target:</span><span className="text-primary-metric text-foreground truncate max-w-[80px]">{data.datasetRegistry.target}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Dataset:</span><span className="text-primary-metric text-foreground truncate max-w-[80px]">{data.datasetRegistry.dataset}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Window:</span><span className="text-primary-metric text-foreground">{data.datasetRegistry.window}</span></div>
          </div>
        </div>

        {/* Row 2: Model Registry & Governance */}
        <div className="flex flex-col gap-1 flex-shrink-0 border-b border-border/20 pb-3">
          <span className="text-label font-bold text-muted-foreground uppercase tracking-widest mb-1">Model Registry & Governance</span>
          <div className="grid grid-cols-2 gap-x-4 gap-y-1">
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Active:</span><span className="text-primary-metric text-foreground truncate max-w-[80px]">{data.modelRegistry.activeModel}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Select Score:</span><span className="text-primary-metric text-foreground">{data.modelRegistry.selectionScore}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Version:</span><span className="text-primary-metric text-foreground">{data.modelRegistry.version}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Calib:</span><span className="text-primary-metric text-foreground truncate max-w-[80px]">{data.modelRegistry.calibration}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Stage:</span><span className="text-primary-metric text-success truncate max-w-[80px]">{data.modelRegistry.stage}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Inference:</span><span className="text-primary-metric text-foreground">{data.inference.latency}</span></div>
          </div>
        </div>

        {/* Row 3: Verification */}
        <div className="flex flex-col gap-2 flex-shrink-0 mt-auto pt-1">
          <div className="flex justify-between items-center">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest">Verification Engine</span>
            <span className="text-label text-muted-foreground italic">Queue: {data.verification.queue}</span>
          </div>
          
          <div className="grid grid-cols-5 gap-2 text-center mt-1">
            <div className="bg-surface/30 border border-border/20 rounded p-1.5 flex flex-col justify-center">
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest">CSI</span>
              <span className="text-primary-metric text-foreground mt-0.5">{data.verification.csi}</span>
            </div>
            <div className="bg-surface/30 border border-border/20 rounded p-1.5 flex flex-col justify-center">
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Hit Rate</span>
              <span className="text-primary-metric text-success mt-0.5">{data.verification.hitRate}</span>
            </div>
            <div className="bg-surface/30 border border-border/20 rounded p-1.5 flex flex-col justify-center">
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Brier</span>
              <span className="text-primary-metric text-foreground mt-0.5">{data.verification.brier}</span>
            </div>
            <div className="bg-surface/30 border border-border/20 rounded p-1.5 flex flex-col justify-center">
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Reliab</span>
              <span className="text-primary-metric text-foreground mt-0.5">{data.verification.reliability}</span>
            </div>
            <div className="bg-surface/30 border border-border/20 rounded p-1.5 flex flex-col justify-center">
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest">Cal Err</span>
              <span className="text-primary-metric text-foreground mt-0.5">{data.verification.calibrationErr}</span>
            </div>
          </div>
        </div>

      </div>
    </BaseCard>
  );
};
export default MachineIntelligence;
