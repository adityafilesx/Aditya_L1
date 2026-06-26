import { Fragment } from 'react';
import type { FC } from 'react';
import { cn } from '@utils/cn';
import { 
  PageLayout, 
  Header, 
  EnterpriseTable, 
  SeverityBadge,
  Icon,
  PlotlyContainer
} from '@design-system/index';
import type { ColumnDef } from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

interface ConsensusRow {
  id: string;
  architecture: string;
  prediction: string;
  confidence: string;
  latency: string;
  accuracy: string;
  calibration: string;
  status: string;
}

const CONSENSUS_DATA: ConsensusRow[] = [
  { id: '1', architecture: 'XGBoost (Ensemble)', prediction: 'M-Class', confidence: '96.2%', latency: '4ms', accuracy: '96%', calibration: 'Perfect', status: 'NOMINAL' },
  { id: '2', architecture: 'LightGBM', prediction: 'M-Class', confidence: '94.8%', latency: '3ms', accuracy: '95%', calibration: 'High', status: 'NOMINAL' },
  { id: '3', architecture: 'Temporal CNN (TCN)', prediction: 'C-Class', confidence: '82.1%', latency: '18ms', accuracy: '89%', calibration: 'Drifting', status: 'WARNING' },
  { id: '4', architecture: 'Transformer-XL', prediction: 'M-Class', confidence: '91.5%', latency: '42ms', accuracy: '92%', calibration: 'Stable', status: 'NOMINAL' },
  { id: '5', architecture: 'Physics-Informed NN', prediction: 'M-Class', confidence: '98.9%', latency: '22ms', accuracy: '97%', calibration: 'Optimal', status: 'NOMINAL' },
];

interface ExperimentRow {
  id: string;
  runId: string;
  timestamp: string;
  epochs: number;
  loss: string;
  auc: string;
  tags: string;
}

const EXPERIMENT_DATA: ExperimentRow[] = [
  { id: '1', runId: 'solar-flare-v4.2.1', timestamp: '2023-10-27 12:45', epochs: 500, loss: '0.038', auc: '0.982', tags: 'PRODUCTION' },
  { id: '2', runId: 'experiment-tcn-02', timestamp: '2023-10-27 10:12', epochs: 250, loss: '0.051', auc: '0.914', tags: 'TESTING' },
  { id: '3', runId: 'hyper-opt-r4', timestamp: '2023-10-26 23:55', epochs: 1000, loss: '0.044', auc: '0.955', tags: 'ARCHIVED' },
];

export const AiWorkspacePageSection1: FC = () => (
  <>
    <Header
      title="AI Intelligence"
      subtitle="Explainable Artificial Intelligence • Forecast Validation • Model Diagnostics"
      actions={
        <div className="flex items-center gap-gutter">
          <div className="hidden lg:flex items-center gap-4 bg-surface-container-high px-4 py-2 rounded-lg">
            <div className="flex flex-col">
              <span className="font-label-caps text-[10px] text-on-surface-variant">MODEL VERSION</span>
              <span className="font-data-mono text-data-mono text-primary">v4.2.1-alpha.rc2</span>
            </div>
            <div className="w-px h-8 bg-outline-variant"></div>
            <div className="flex flex-col">
              <span className="font-label-caps text-[10px] text-on-surface-variant">INFERENCE</span>
              <span className="font-data-mono text-data-mono text-secondary">REAL-TIME</span>
            </div>
            <div className="w-px h-8 bg-outline-variant"></div>
            <div className="flex flex-col">
              <span className="font-label-caps text-[10px] text-on-surface-variant">EXPERIMENT</span>
              <span className="font-data-mono text-data-mono text-on-surface">FLARE_DYNAMICS_99</span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined p-2 hover:bg-surface-container-high rounded-full cursor-pointer">timer</span>
            <span className="material-symbols-outlined p-2 hover:bg-surface-container-high rounded-full cursor-pointer">public</span>
            <span className="material-symbols-outlined p-2 hover:bg-surface-container-high rounded-full cursor-pointer">settings</span>
            <div className="w-8 h-8 rounded-full bg-primary-container flex items-center justify-center text-on-primary-container font-bold text-xs">FD</div>
          </div>
        </div>
      }
    />
  </>
);

export const AiWorkspacePageSection2: FC = () => {
  const consensusCols: ColumnDef<ConsensusRow>[] = [
    { header: 'MODEL ARCHITECTURE', accessorKey: 'architecture', cell: (row) => <strong>{row.architecture}</strong> },
    { header: 'PREDICTION', accessorKey: 'prediction' },
    { header: 'CONFIDENCE', accessorKey: 'confidence', className: 'font-data-mono' },
    { header: 'LATENCY', accessorKey: 'latency', className: 'font-data-mono' },
    { header: 'ACCURACY', accessorKey: 'accuracy', cell: (row) => <span className="text-primary">{row.accuracy}</span> },
    { header: 'CALIBRATION', accessorKey: 'calibration' },
    { header: 'STATUS', accessorKey: 'status', cell: (row) => <SeverityBadge status={row.status}>{row.status}</SeverityBadge> },
  ];

  const experimentCols: ColumnDef<ExperimentRow>[] = [
    { header: 'RUN ID', accessorKey: 'runId', cell: (row) => <span className="font-data-mono">{row.runId}</span> },
    { header: 'TIMESTAMP', accessorKey: 'timestamp' },
    { header: 'EPOCHS', accessorKey: 'epochs' },
    { header: 'LOSS', accessorKey: 'loss', cell: (row) => <span className="font-data-mono text-primary">{row.loss}</span> },
    { header: 'AUC', accessorKey: 'auc', className: 'font-data-mono' },
    { 
      header: 'TAGS', 
      accessorKey: 'tags', 
      cell: (row) => (
        <span className={cn(
          'px-2 rounded text-[10px]',
          row.tags === 'PRODUCTION' ? 'bg-primary/10 text-primary' : row.tags === 'TESTING' ? 'bg-secondary/10 text-secondary' : 'bg-outline-variant/30 text-on-surface-variant'
        )}>
          {row.tags}
        </span>
      ) 
    },
  ];

  const history = useStreamStore(state => state.history);
  const timeAxis = history.telemetry.map(t => new Date(t.timestamp).getTime());
  const probAxis = history.telemetry.map(t => (t as any).forecast?.probability ?? Math.random());
  
  return (
    <>
      <div className="max-w-[1800px] grid grid-cols-12 gap-gutter">
        
        {/* Live Prediction Box */}
        <section className="col-span-12 lg:col-span-8 bento-card p-6 flex flex-col gap-6">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="font-label-caps text-label-caps text-on-surface-variant">LIVE AI PREDICTION</h2>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="font-display-lg text-display-lg text-primary">20.8%</span>
                <span className="font-body-lg text-on-surface-variant">Flare Probability</span>
              </div>
            </div>
            <div className="text-right">
              <span className="font-label-caps text-label-caps text-on-surface-variant">CONFIDENCE INTERVAL</span>
              <div className="font-numeric-telemetry text-headline-md text-secondary font-bold">96%</div>
            </div>
          </div>
          
          <div className="h-48 w-full bg-surface-container-low rounded-xl flex items-end p-4 gap-1 relative overflow-hidden">
            <div className="absolute top-4 left-4 flex flex-col gap-1 z-10">
              <span className="font-label-caps text-[10px] text-on-surface-variant">PREDICTION HISTORY (24H)</span>
              <span className="font-data-mono text-xs text-primary">SENSITIVITY: HIGH</span>
            </div>
            <div className="w-full h-full pt-8">
              <PlotlyContainer 
                data={[{
                  x: timeAxis,
                  y: probAxis,
                  type: 'scatter',
                  mode: 'lines',
                  line: { color: '#4140d1', shape: 'spline' },
                  fill: 'tozeroy'
                }]}
                layout={{
                  xaxis: { visible: false },
                  yaxis: { visible: false },
                  margin: { t: 0, b: 0, l: 0, r: 0 },
                  paper_bgcolor: 'transparent',
                  plot_bgcolor: 'transparent'
                }}
                syncCursor
              />
            </div>
          </div>
          <div className="flex justify-between items-center border-t border-outline-variant pt-4">
            <div className="flex gap-8">
              <div>
                <span className="font-label-caps text-[10px] text-on-surface-variant uppercase">Expected Class</span>
                <p className="font-headline-md text-xl">M-CLASS (MODERATE)</p>
              </div>
              <div>
                <span className="font-label-caps text-[10px] text-on-surface-variant uppercase">Time to Peak</span>
                <p className="font-headline-md text-xl">~14:22 UTC</p>
              </div>
            </div>
            <div className="flex gap-2">
              <button className="px-4 py-2 bg-surface-container-high rounded-lg font-label-caps text-label-caps hover:bg-surface-container-highest transition-colors cursor-pointer border-none">COMPARE MODELS</button>
              <button className="px-4 py-2 bg-primary text-on-primary rounded-lg font-label-caps text-label-caps hover:opacity-90 transition-opacity cursor-pointer border-none">VIEW EXPLANATION</button>
            </div>
          </div>
        </section>
        
        {/* Feature Importance Box */}
        <section className="col-span-12 lg:col-span-4 bento-card p-6 flex flex-col gap-4">
          <div className="flex justify-between items-center mb-2">
            <h2 className="font-label-caps text-label-caps text-on-surface-variant">FEATURE IMPORTANCE</h2>
            <div className="flex gap-2">
              <span className="text-[10px] font-label-caps bg-primary-container text-on-primary-container px-2 py-0.5 rounded">SHAP</span>
              <span className="text-[10px] font-label-caps bg-surface-container-high text-on-surface-variant px-2 py-0.5 rounded">GAIN</span>
            </div>
          </div>
          <div className="space-y-4">
            {[
              { name: 'Magnetic Flux Density', val: '+0.24 SHAP', p: 80, isPos: true },
              { name: 'Plasma Velocity', val: '+0.18 SHAP', p: 60, isPos: true },
              { name: 'Proton Density', val: '-0.05 SHAP', p: 15, isPos: false },
              { name: 'Sunspot Group Area', val: '+0.12 SHAP', p: 40, isPos: true },
            ].map((feat) => (
              <div key={feat.name} className="flex flex-col gap-1">
                <div className="flex justify-between font-label-caps text-[11px]">
                  <span>{feat.name}</span>
                  <span className={feat.isPos ? 'text-primary' : 'text-secondary'}>{feat.val}</span>
                </div>
                <div className={cn('h-2 bg-surface-container-low rounded-full overflow-hidden flex', !feat.isPos && 'justify-end')}>
                  <div className={cn('h-full', feat.isPos ? 'bg-primary' : 'bg-secondary')} style={{ width: `${feat.p}%` }}></div>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-auto pt-4 border-t border-outline-variant">
            <p className="font-body-sm text-on-surface-variant italic">"Current prediction heavily influenced by Magnetic Flux anomaly in AR-2934."</p>
          </div>
        </section>
        
        {/* Model Consensus Table */}
        <div className="col-span-12">
          <EnterpriseTable
            title="MODEL CONSENSUS MATRIX"
            data={CONSENSUS_DATA}
            columns={consensusCols}
            actions={<span className="font-data-mono text-[11px] text-on-surface-variant">POLLING RATE: 100HZ</span>}
          />
        </div>
        
        {/* Inference Pipeline */}
        <section className="col-span-12 lg:col-span-7 bento-card p-6">
          <h2 className="font-label-caps text-label-caps text-on-surface-variant mb-6">AI INFERENCE PIPELINE</h2>
          <div className="flex items-center justify-between gap-2">
            {[
              { label: 'TELEMETRY\nINGESTION', icon: 'sensors', isLive: true },
              { label: 'DATA\nCLEANING', icon: 'cleaning_services' },
              { label: 'PHYSICS\nENGINE', icon: 'auto_fix_high' },
              { label: 'MODEL\nINFERENCE', icon: 'psychology', isCenter: true },
              { label: 'ACTION\nTRIGGER', icon: 'campaign' },
            ].map((step, idx) => (
              <Fragment key={idx}>
                {idx > 0 && (
                  <div className="flex-1 h-px bg-outline-variant relative">
                    {idx === 1 && <div className="absolute -top-1 left-1/2 w-2 h-2 rounded-full bg-primary animate-ping"></div>}
                  </div>
                )}
                <div className="flex flex-col items-center gap-2">
                  <div className={cn(
                    'w-16 h-16 rounded-xl flex items-center justify-center border border-outline-variant bg-surface-container-low',
                    step.isCenter && 'bg-primary border-none shadow-lg text-white'
                  )}>
                    <Icon name={step.icon} className={step.isCenter ? 'text-white text-[24px]' : 'text-primary text-[24px]'} />
                  </div>
                  <span className={cn('font-label-caps text-[9px] text-center whitespace-pre-line', step.isCenter && 'font-bold')}>
                    {step.label}
                  </span>
                </div>
              </Fragment>
            ))}
          </div>
        </section>
        
        {/* Training Metrics */}
        <section className="col-span-12 lg:col-span-5 bento-card p-6 flex flex-col gap-4">
          <h2 className="font-label-caps text-label-caps text-on-surface-variant">TRAINING METRICS</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-surface-container-low rounded-lg">
              <span className="font-label-caps text-[10px] text-on-surface-variant">TOTAL SAMPLES</span>
              <div className="font-numeric-telemetry text-xl text-on-surface font-bold">102,252</div>
            </div>
            <div className="p-4 bg-surface-container-low rounded-lg">
              <span className="font-label-caps text-[10px] text-on-surface-variant">TSS (TRUE SKILL)</span>
              <div className="font-numeric-telemetry text-xl text-primary font-bold">0.91</div>
            </div>
            <div className="p-4 bg-surface-container-low rounded-lg">
              <span className="font-label-caps text-[10px] text-on-surface-variant">HSS (HEIDKE)</span>
              <div className="font-numeric-telemetry text-xl text-primary font-bold">0.84</div>
            </div>
            <div className="p-4 bg-surface-container-low rounded-lg">
              <span className="font-label-caps text-[10px] text-on-surface-variant">LOSS (LOG)</span>
              <div className="font-numeric-telemetry text-xl text-on-surface font-bold">0.042</div>
            </div>
          </div>
          <div className="mt-2">
            <span className="font-label-caps text-[10px] text-on-surface-variant uppercase">Calibration Curve</span>
            <div className="h-24 w-full bg-surface-container-low rounded border border-outline-variant mt-1 relative overflow-hidden">
              <div className="absolute inset-0 border-b border-r border-outline-variant/20"></div>
              <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none">
                <path d="M 0 100 Q 50 40 100 0" fill="none" stroke="#4140d1" strokeWidth="2"></path>
              </svg>
            </div>
          </div>
        </section>
        
        {/* Experiment Tracker */}
        <div className="col-span-12 lg:col-span-8">
          <EnterpriseTable
            title="EXPERIMENT TRACKER (W&B)"
            data={EXPERIMENT_DATA}
            columns={experimentCols}
            actions={<button className="text-primary font-label-caps text-[11px] font-bold bg-transparent border-none cursor-pointer hover:underline">OPEN FULL DASHBOARD</button>}
          />
        </div>
        
        {/* Model Registry */}
        <section className="col-span-12 lg:col-span-4 bento-card p-6 flex flex-col gap-4">
          <h2 className="font-label-caps text-label-caps text-on-surface-variant font-bold">MODEL REGISTRY</h2>
          <div className="space-y-3">
            {[
              { v: 'v4.2.1 (Active)', t: 'PRODUCTION ENCLAVE', icon: 'verified', active: true },
              { v: 'v4.3.0-rc1', t: 'STAGING GATE', icon: 'hourglass_empty', opacity: true },
              { v: 'v5.0.0-alpha', t: 'RESEARCH LAB', icon: 'science', opacity: true },
            ].map((reg, idx) => (
              <div key={idx} className={cn(
                'p-3 border rounded-lg flex items-center justify-between',
                reg.active ? 'border-primary bg-primary/5' : 'border-outline-variant',
                reg.opacity && 'opacity-70'
              )}>
                <div className="flex items-center gap-3">
                  <Icon name={reg.icon} className={reg.active ? 'text-primary' : 'text-on-surface-variant'} />
                  <div>
                    <p className="font-bold text-sm text-on-surface">{reg.v}</p>
                    <p className="text-[10px] font-label-caps text-on-surface-variant">{reg.t}</p>
                  </div>
                </div>
                <Icon name="more_vert" className="text-on-surface-variant cursor-pointer" />
              </div>
            ))}
          </div>
          <button className="w-full mt-2 border border-outline border-dashed p-3 rounded-lg text-on-surface-variant font-label-caps text-label-caps hover:bg-surface-container-low transition-colors bg-transparent cursor-pointer">
            + REGISTER NEW MODEL
          </button>
        </section>
        
        {/* System log terminal view */}
        <section className="col-span-12 bg-terminal-bg rounded-xl p-4 font-data-mono text-[11px] overflow-hidden shadow-2xl border border-[#30363d]">
          <div className="flex items-center justify-between border-b border-[#30363d] pb-2 mb-3">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span className="ml-4 text-[#8b949e]">AI_SYSTEM_LOGS_STREAM</span>
            </div>
            <span className="text-[#8b949e]">Uptime: 1422:05:12</span>
          </div>
          <div className="space-y-1 text-[#c9d1d9] h-32 overflow-y-auto no-scrollbar">
            <p><span className="text-[#8b949e]">[14:22:01]</span> <span className="text-green-400">INFO:</span> Inference engine cold start successful. Model v4.2.1 loaded on GPU_0.</p>
            <p><span className="text-[#8b949e]">[14:22:02]</span> <span className="text-green-400">INFO:</span> Telemetry stream synchronized. Latency offset: -1.2ms.</p>
            <p><span className="text-[#8b949e]">[14:22:03]</span> <span className="text-yellow-400">WARN:</span> Drifting detected in Temporal AI feature vectors (Proton Density).</p>
            <p><span className="text-[#8b949e]">[14:22:04]</span> <span className="text-blue-400">DEBUG:</span> SHAP values recalculated for current frame. Dominant feature: AR_2934_MAG_FLUX.</p>
            <p><span className="text-[#8b949e]">[14:22:05]</span> <span className="text-green-400">INFO:</span> Prediction broadcasted to Command Uplink. Probability: 20.8%.</p>
            <p><span className="text-[#8b949e]">[14:22:06]</span> <span className="text-purple-400">CMD:</span> Executing automated uncertainty re-calibration on Ensemble node...</p>
          </div>
        </section>
      </div>
    </>
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
