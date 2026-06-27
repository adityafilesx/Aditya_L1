import type { FC } from 'react';
import { useMemo } from 'react';
import { BaseCard, Icon } from '../../../design-system';
import { useForecast } from '../hooks/useForecast';

const TRUST_SPARK = [40, 50, 45, 60, 55, 70, 75, 80, 78, 85, 90, 88, 92, 94];

// Local presentational helpers — keep every section visually consistent.
const Row: FC<{ label: string; value: string; valueClass?: string; truncate?: boolean }> = ({
  label,
  value,
  valueClass = 'text-foreground',
  truncate,
}) => (
  <div className="flex justify-between items-center gap-2">
    <span className="text-label text-muted-foreground flex-shrink-0">{label}:</span>
    <span className={`text-primary-metric ${valueClass} ${truncate ? 'truncate max-w-[90px]' : ''}`}>{value}</span>
  </div>
);

const Tile: FC<{ label: string; value: string; valueClass?: string }> = ({
  label,
  value,
  valueClass = 'text-foreground',
}) => (
  <div className="bg-surface/30 border border-border/20 rounded p-1.5 flex flex-col justify-center">
    <span className="text-[10px] text-muted-foreground uppercase tracking-widest">{label}</span>
    <span className={`text-primary-metric mt-0.5 ${valueClass}`}>{value}</span>
  </div>
);

const SectionHeader: FC<{ title: string; aside?: string }> = ({ title, aside }) => (
  <div className="flex justify-between items-center">
    <span className="text-label font-bold text-muted-foreground uppercase tracking-widest">{title}</span>
    {aside && <span className="text-label text-muted-foreground italic">{aside}</span>}
  </div>
);

export const OperationsIntelligence: FC = () => {
  const { selectedModel, nowcastState, latestForecast, forecastWindow } = useForecast();

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

  const trust = useMemo(() => {
    let score = 94;
    let delta = '+2';

    if (forecastWindow === '24h') {
      score = 86;
      delta = '-1';
    } else if (forecastWindow === '7d') {
      score = 72;
      delta = '-5';
    }

    return { score, delta, isPositive: !delta.startsWith('-') };
  }, [forecastWindow]);

  const repo = useMemo(() => ({
    forecastId: latestForecast?.forecast_id || 'F-3910A',
    version: 'v4.1.2',
    verification: 'PENDING',
    replay: 'AVAILABLE',
    stored: 'S3-ARCHIVE'
  }), [latestForecast]);

  return (
    <BaseCard className="flex flex-col h-full bg-surface-container-lowest/40 border border-border/20 backdrop-blur-md overflow-hidden p-3">

      {/* Header */}
      <div className="flex justify-between items-center flex-shrink-0 mb-3 border-b border-border/20 pb-2">
        <div className="flex items-center gap-1.5 min-w-0">
          <Icon name="database" className="text-primary flex-shrink-0" />
          <h2 className="text-heading text-foreground truncate">Operations Intelligence</h2>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
          <span className="text-label text-success font-bold uppercase">NOMINAL</span>
        </div>
      </div>

      <div className="flex-1 flex flex-col gap-3 min-h-0 overflow-y-auto custom-scrollbar pr-1">

        {/* Section 1: Feature Store + Dataset Registry */}
        <section className="grid grid-cols-2 gap-3 flex-shrink-0 border-b border-border/20 pb-3">
          <div className="flex flex-col gap-1">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest mb-1">Feature Store</span>
            <Row label="Vector ID" value={data.featureStore.vectorId} />
            <Row label="Active Feats" value={data.featureStore.activeCount} />
            <Row label="Readiness" value={data.featureStore.readiness} valueClass="text-success" />
          </div>
          <div className="flex flex-col gap-1 border-l border-border/20 pl-3">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest mb-1">Dataset Registry</span>
            <Row label="Target" value={data.datasetRegistry.target} truncate />
            <Row label="Dataset" value={data.datasetRegistry.dataset} truncate />
            <Row label="Window" value={data.datasetRegistry.window} />
          </div>
        </section>

        {/* Section 2: Model Registry & Governance */}
        <section className="flex flex-col gap-1 flex-shrink-0 border-b border-border/20 pb-3">
          <span className="text-label font-bold text-muted-foreground uppercase tracking-widest mb-1">Model Registry &amp; Governance</span>
          <div className="grid grid-cols-2 gap-x-4 gap-y-1">
            <Row label="Active" value={data.modelRegistry.activeModel} truncate />
            <Row label="Select Score" value={data.modelRegistry.selectionScore} />
            <Row label="Version" value={data.modelRegistry.version} truncate />
            <Row label="Calib" value={data.modelRegistry.calibration} truncate />
            <Row label="Stage" value={data.modelRegistry.stage} valueClass="text-success" truncate />
            <Row label="Inference" value={data.inference.latency} />
            <Row label="Impl" value={data.modelRegistry.implType} truncate />
            <Row label="Throughput" value={data.inference.throughput} />
          </div>
        </section>

        {/* Section 3: Verification */}
        <section className="flex flex-col gap-2 flex-shrink-0 border-b border-border/20 pb-3">
          <SectionHeader title="Verification Engine" aside={`Queue: ${data.verification.queue}`} />
          <div className="grid grid-cols-5 gap-2 text-center">
            <Tile label="CSI" value={data.verification.csi} />
            <Tile label="Hit Rate" value={data.verification.hitRate} valueClass="text-success" />
            <Tile label="Brier" value={data.verification.brier} />
            <Tile label="Reliab" value={data.verification.reliability} />
            <Tile label="Cal Err" value={data.verification.calibrationErr} />
          </div>
        </section>

        {/* Section 4: Trust & Repository */}
        <section className="flex gap-3 flex-shrink-0">
          {/* Trust history */}
          <div className="flex-1 flex flex-col border-r border-border/20 pr-3">
            <div className="flex justify-between items-center mb-1">
              <span className="text-label font-bold text-muted-foreground uppercase tracking-widest">Trust Score</span>
              <span className="text-label text-muted-foreground">24h</span>
            </div>
            <div className="flex items-end gap-2 mb-2">
              <span className="text-hero text-foreground leading-none">{trust.score}%</span>
              <span className={`text-label font-bold pb-0.5 ${trust.isPositive ? 'text-success' : 'text-error'}`}>
                {trust.isPositive ? '▲' : '▼'} {trust.delta}%
              </span>
            </div>
            <div className="h-6 w-full flex items-end gap-[2px] opacity-70 mt-auto">
              {TRUST_SPARK.map((h, i) => (
                <div key={i} className="flex-1 bg-primary rounded-t-sm transition-all" style={{ height: `${h}%` }} />
              ))}
            </div>
          </div>

          {/* Forecast repository */}
          <div className="flex-1 flex flex-col">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest mb-1">Repository</span>
            <div className="flex flex-col gap-1">
              <Row label="ID" value={repo.forecastId} truncate />
              <Row label="Ver" value={repo.version} />
              <Row label="Verif" value={repo.verification} valueClass="text-warning" />
              <Row label="Replay" value={repo.replay} valueClass="text-success" />
              <Row label="Stored" value={repo.stored} truncate />
            </div>
          </div>
        </section>

      </div>
    </BaseCard>
  );
};
export default OperationsIntelligence;
