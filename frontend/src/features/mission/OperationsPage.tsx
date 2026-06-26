import type { FC } from 'react';
import { cn } from '@utils/cn';
import { 
  PageLayout, 
  Header, 
  BaseCard, 
  BaseBadge, 
  SeverityBadge, 
  EnterpriseTable, 
  SecondaryButton, 
  DangerButton, 
  ProgressBar,
  Icon,
  PlotlyContainer
} from '@design-system/index';
import type { ColumnDef } from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

const Skeleton: FC<{ className?: string }> = ({ className }) => (
  <div className={cn("animate-pulse bg-surface-container-high rounded", className)} />
);

const DataDisplay: FC<{ label: string, value: string | number, unit?: string, size?: 'sm' | 'md' | 'lg', trend?: 'up' | 'down' | 'flat', className?: string }> = ({ label, value, unit, size = 'sm', trend, className }) => (
  <div className={cn("flex flex-col gap-1", className)}>
    <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">{label}</span>
    <div className="flex items-baseline gap-1">
      <span className={cn("font-numeric-telemetry font-bold", size === 'lg' ? 'text-2xl' : size === 'md' ? 'text-xl' : 'text-sm')}>{value}</span>
      {unit && <span className="text-[10px] text-on-surface-variant font-data-mono">{unit}</span>}
      {trend && <Icon name={trend === 'up' ? 'trending_up' : trend === 'down' ? 'trending_down' : 'trending_flat'} className={trend === 'up' ? 'text-warning' : trend === 'down' ? 'text-success' : 'text-on-surface-variant'} />}
    </div>
  </div>
);


interface ModelComparisonRow {
  id: string;
  model: string;
  pred: string;
  conf: string;
  latency: string;
  status?: string;
}

const COMPARISON_DATA: ModelComparisonRow[] = [
  { id: '1', model: 'XGBoost-V4', pred: 'M1.2', conf: '88%', latency: '12ms' },
  { id: '2', model: 'Temporal-CN', pred: 'M1.4', conf: '94%', latency: '45ms' },
  { id: '3', model: 'Transformer-S', pred: 'M1.1', conf: '91%', latency: '110ms' },
  { id: '4', model: 'Hybrid-Alpha', pred: 'M1.3', conf: '96%', latency: '68ms' },
];

export const OperationsPageContent: FC = () => {
  const missionState = useStreamStore(state => state.mission);
  const history = useStreamStore(state => state.history);
  const connectionStatus = useStreamStore(state => state.connectionStatus);

  if (!missionState && connectionStatus === 'connecting') {
    return (
      <div className="space-y-gutter">
        <Skeleton className="h-16 w-full rounded-xl" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-gutter">
           <Skeleton className="lg:col-span-2 h-96 w-full rounded-xl" />
           <Skeleton className="h-96 w-full rounded-xl" />
        </div>
      </div>
    );
  }

  if (!missionState && connectionStatus === 'disconnected') {
    return (
      <div className="p-8 text-center border border-critical rounded-lg bg-critical/5 text-critical">
        <h2 className="text-xl font-bold mb-2">System Offline</h2>
        <p>Failed to connect to Mission Control Gateway. Re-establishing telemetry link...</p>
      </div>
    );
  }

  const state = missionState || {} as any;
  const telemetry = state.telemetry || {};
  const physics = state.physics || {};
  const timelineData = state.alerts || [];

  const timelineCols: ColumnDef<any>[] = [
    { header: 'TIME (UTC)', accessorKey: 'timestamp', cell: (row) => new Date(row.timestamp).toLocaleTimeString() },
    { header: 'SEVERITY', accessorKey: 'severity', cell: (row) => <SeverityBadge status={row.severity?.toUpperCase() || 'INFO'}>{row.severity?.toUpperCase() || 'INFO'}</SeverityBadge> },
    { header: 'TYPE', accessorKey: 'type' },
    { header: 'DESCRIPTION', accessorKey: 'description' },
  ];

  return (
    <>
      <Header
        title="Operations Center"
        subtitle="Real-Time Mission Operations & Scientific Investigation"
        actions={
          <div className="flex items-center gap-6 bg-surface-container-low p-4 rounded-xl border border-outline-variant">
            <div className="flex flex-col border-r border-outline-variant pr-6">
              <span className="font-label-caps text-label-caps text-on-surface-variant">Mission State</span>
              <span className={cn("font-numeric-telemetry text-numeric-telemetry font-bold", state.state > 0 ? "text-warning" : "text-success")}>{state.state === 2 ? 'ALERT' : state.state === 1 ? 'WATCH' : 'NOMINAL'}</span>
            </div>
            <div className="flex flex-col border-r border-outline-variant pr-6">
              <span className="font-label-caps text-label-caps text-on-surface-variant">Operator</span>
              <span className="font-numeric-telemetry text-numeric-telemetry text-on-surface">Cmdr. Aditi</span>
            </div>
            <div className="flex flex-col">
              <span className="font-label-caps text-label-caps text-on-surface-variant">UTC Clock</span>
              <span className="font-data-mono text-data-mono text-on-surface">Live</span>
            </div>
          </div>
        }
      />
      
      <section className="bg-surface rounded-xl border border-outline-variant p-3 flex justify-between items-center mb-gutter">
        <div className="flex items-center gap-2">
          <div className="flex bg-surface-container-highest rounded border border-outline-variant p-1">
            <button className="px-3 py-1 text-label-caps font-label-caps hover:bg-surface-container-low rounded">30m</button>
            <button className="px-3 py-1 bg-primary text-on-primary text-label-caps font-label-caps rounded">1h</button>
            <button className="px-3 py-1 text-label-caps font-label-caps hover:bg-surface-container-low rounded">6h</button>
            <button className="px-3 py-1 text-label-caps font-label-caps hover:bg-surface-container-low rounded">24h</button>
            <button className="px-3 py-1 text-label-caps font-label-caps hover:bg-surface-container-low rounded">7d</button>
          </div>
          <div className="h-6 w-px bg-outline-variant mx-2"></div>
          <div className="flex items-center gap-1">
            <button className="p-2 hover:bg-surface-container-high rounded text-on-surface-variant"><Icon name="play_arrow" /></button>
            <button className="p-2 hover:bg-surface-container-high rounded text-on-surface-variant"><Icon name="pause" /></button>
            <button className="p-2 hover:bg-surface-container-high rounded text-on-surface-variant"><Icon name="replay" /></button>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-1 bg-surface-container-low rounded border border-outline-variant">
            <span className="blinking-dot"></span>
            <span className="font-label-caps text-label-caps text-on-surface">L1 LINK: NOMINAL</span>
          </div>
          <SecondaryButton icon="download" size="sm">Export CSV</SecondaryButton>
          <SecondaryButton icon="image" size="sm">PNG</SecondaryButton>
        </div>
      </section>

      <div className="grid grid-cols-12 gap-gutter">
        <div className="col-span-12 xl:col-span-8 flex flex-col gap-gutter">
          <div className="grid grid-cols-1 gap-4">
            <BaseCard variant="glass" className="p-4" title={
              <span className="font-label-caps text-label-caps text-on-surface-variant flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-primary"></span> Soft X-Ray Flux (0.1–0.8 nm)
              </span>
            }>
              <div className="h-48 bg-surface-container-low rounded border border-outline-variant border-dashed flex items-center justify-center">
                 <PlotlyContainer 
                   data={[{
                     x: history.telemetry.map(t => new Date(t.timestamp).getTime()),
                     y: history.telemetry.map(t => t.solexs_sdd2_ctr),
                     type: 'scatter',
                     mode: 'lines',
                     fill: 'tozeroy',
                     line: { color: '#8884d8' },
                     name: 'SoLEXS SDD2'
                   }]} 
                   layout={{ showlegend: false, margin: {t:0,b:0,l:40,r:10} }}
                   syncCursor
                 />
              </div>
            </BaseCard>
            <BaseCard variant="glass" className="p-4" title={
              <span className="font-label-caps text-label-caps text-on-surface-variant flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-secondary"></span> Hard X-Ray Flux (10–100 keV)
              </span>
            }>
              <div className="h-48 bg-surface-container-low rounded border border-outline-variant border-dashed flex items-center justify-center">
                <PlotlyContainer 
                   data={[{
                     x: history.telemetry.map(t => new Date(t.timestamp).getTime()),
                     y: history.telemetry.map(t => t.helios_czt_broad_ctr),
                     type: 'scatter',
                     mode: 'lines',
                     line: { color: '#82ca9d' },
                     name: 'HEL1OS Broad'
                   }]} 
                   layout={{ showlegend: false, margin: {t:0,b:0,l:40,r:10} }}
                   syncCursor
                 />
              </div>
            </BaseCard>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
            <BaseCard variant="plain" size="md" className="card-shadow" title={
              <span className="font-label-caps text-label-caps text-on-surface flex items-center gap-2">
                <Icon name="psychology" className="text-primary" /> AI DECISION ENGINE
              </span>
            } badge={<span className="px-2 py-0.5 bg-green-100 text-green-700 text-[10px] font-bold rounded">AUTONOMOUS</span>}>
              <div className="flex justify-between items-center mb-6">
                <DataDisplay 
                  label="System State" 
                  value={state.state === 2 ? 'ALERT' : state.state === 1 ? 'WATCH' : 'NOMINAL'} 
                  size="md" 
                  className={state.state > 0 ? "text-warning" : "text-success"} 
                />
                <BaseBadge variant={state.state > 0 ? "warning" : "primary"}>Conformal Conf: {(state.forecast?.confidence * 100)?.toFixed(1) || '0.0'}%</BaseBadge>
              </div>
              
              <div className="space-y-4">
                <div className="bg-surface p-3 rounded border border-outline-variant">
                  <span className="font-label-caps text-label-caps block mb-1">Recommended Action</span>
                  <span className="font-body-sm font-bold text-on-surface">{state.recommendations?.[0] || 'Maintain Science Operations'}</span>
                </div>
                
                <div className="bg-surface p-3 rounded border border-outline-variant">
                  <span className="font-label-caps text-label-caps block mb-1">Predicted Class</span>
                  <span className="font-body-sm font-bold text-on-surface">{state.forecast?.estimated_goes_class || 'Quiet'}</span>
                </div>
              </div>
            </BaseCard>
            
            <EnterpriseTable
              title="MODEL COMPARISON"
              data={COMPARISON_DATA}
              columns={[
                { header: 'MODEL', accessorKey: 'model' },
                { header: 'PRED', accessorKey: 'pred' },
                { header: 'CONF', accessorKey: 'conf' },
                { header: 'LATENCY', accessorKey: 'latency' },
              ]}
              className="p-5 shadow-sm border border-outline-variant"
            />
          </div>
        </div>
        
        <div className="col-span-12 xl:col-span-4 flex flex-col gap-gutter">
          <BaseCard variant="glass" className="p-5 shadow-sm bg-surface-bright" title={
            <span className="font-label-caps text-label-caps text-on-surface mb-6 flex items-center gap-2">
              <Icon name="flash_on" className="text-secondary" /> LIVE EVENT INSPECTOR
            </span>
          }>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1 p-3 bg-white rounded border border-outline-variant">
                <DataDisplay label="Current" value={telemetry.solexs_sdd2_ctr?.toFixed(1) || '0.0'} unit="cps" size="lg" />
              </div>
              <div className="flex flex-col gap-1 p-3 bg-white rounded border border-outline-variant">
                <DataDisplay label="Current" value={telemetry.helios_czt_broad_ctr?.toFixed(1) || '0.0'} unit="cps" size="lg" />
              </div>
              <div className="flex flex-col gap-1 p-3 bg-white rounded border border-outline-variant">
                <span className="text-[10px] font-label-caps text-on-surface-variant">GOES XRS-B (W/m²)</span>
                <span className="font-numeric-telemetry text-numeric-telemetry font-bold text-secondary">{telemetry.goes_xrs_b ? telemetry.goes_xrs_b.toExponential(2) : 0}</span>
              </div>
              <div className="flex flex-col gap-1 p-3 bg-white rounded border border-outline-variant">
                <span className="text-[10px] font-label-caps text-on-surface-variant">PROTON FLUX &gt;10MeV</span>
                <span className="font-numeric-telemetry text-numeric-telemetry font-bold text-primary">{telemetry.proton_flux_10MeV ? telemetry.proton_flux_10MeV.toFixed(2) : 0}</span>
              </div>
            </div>
          </BaseCard>
          
          <BaseCard variant="plain" size="md" className="card-shadow" title="PHYSICS ENGINE METRICS">
            <DataDisplay label="Neupert Score" value={physics.neupert_score?.toFixed(2) || '0.0'} trend="up" />
            <DataDisplay label="Temperature" value={physics.temperature_mk?.toFixed(1) || '0.0'} unit="MK" />
            <div className="pt-4 mt-4 border-t border-outline-variant space-y-2">
              <div className="flex justify-between font-data-mono text-[11px]">
                <span className="text-on-surface-variant">Spectral Centroid</span>
                <span className="text-primary">{physics.spectral_centroid?.toFixed(3) || '0.0'}</span>
              </div>
              <div className="flex justify-between font-data-mono text-[11px]">
                <span className="text-on-surface-variant">Shannon Entropy</span>
                <span className="text-primary">{physics.shannon_entropy?.toFixed(3) || '0.0'}</span>
              </div>
              <div className="flex justify-between font-data-mono text-[11px]">
                <span className="text-on-surface-variant">Emission Measure</span>
                <span className="text-primary">{physics.emission_measure_norm?.toExponential(2) || '0.00e0'}</span>
              </div>
            </div>
          </BaseCard>
          
          <BaseCard variant="plain" size="md" className="card-shadow" title="SYSTEM PERFORMANCE">
            <div className="grid grid-cols-2 gap-4">
              {[
                { name: 'CPU', value: 42, color: 'primary' },
                { name: 'RAM', value: 68, color: 'primary' },
                { name: 'GPU', value: 91, color: 'secondary' },
                { name: 'DISK IO', value: 14, color: 'primary' },
              ].map((perf) => (
                <div key={perf.name} className="p-3 bg-surface-container-low rounded border border-outline-variant">
                  <div className="flex justify-between mb-1">
                    <span className="text-[10px] font-label-caps text-on-surface-variant">{perf.name}</span>
                    <span className="text-[10px] font-data-mono">{perf.value}%</span>
                  </div>
                  <ProgressBar value={perf.value} />
                </div>
              ))}
            </div>
          </BaseCard>
        </div>
      </div>
      
      {/* Lower Timeline & Commands layout */}
      <div className="grid grid-cols-12 gap-gutter mt-gutter mb-20">
        <div className="col-span-12 xl:col-span-9 flex flex-col gap-gutter">
          <EnterpriseTable
            title="MISSION TIMELINE & RECENT EVENTS"
            data={timelineData || []}
            columns={timelineCols}
            actions={
              <div className="flex gap-2">
                <span className="bg-surface-container-highest text-on-surface-variant px-3 py-1 rounded text-[10px] font-bold">LIVE UPDATE</span>
              </div>
            }
          />
        </div>
        
        <div className="col-span-12 xl:col-span-3 flex flex-col gap-4">
          <BaseCard variant="plain" size="md" className="card-shadow h-full" title={
            <span className="font-label-caps text-label-caps text-on-surface mb-6 flex items-center gap-2">
              <Icon name="terminal" className="text-on-surface-variant" /> OPERATOR COMMANDS
            </span>
          }>
            <div className="flex flex-col gap-3">
              <button className="w-full flex items-center justify-between p-4 bg-surface-container border border-outline-variant rounded-lg hover:bg-surface-container-high transition-colors">
                <span className="font-label-caps text-label-caps font-bold">GENERATE REPORT</span>
                <Icon name="description" />
              </button>
              <button className="w-full flex items-center justify-between p-4 bg-surface-container border border-outline-variant rounded-lg hover:bg-surface-container-high transition-colors">
                <span className="font-label-caps text-label-caps font-bold">EXPORT SESSION</span>
                <Icon name="cloud_upload" />
              </button>
              <DangerButton className="w-full flex items-center justify-between p-4 bg-error/10 border border-error/20 rounded-lg text-error hover:bg-error/20 transition-colors">
                <span className="font-label-caps text-label-caps font-bold text-left">EMERGENCY PROCEDURES</span>
                <Icon name="report_problem" />
              </DangerButton>
            </div>
            <div className="mt-8 p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Icon name="info" className="text-primary text-[18px]" />
                <span className="text-[11px] font-bold text-primary uppercase">Manual Override</span>
              </div>
              <p className="text-[12px] text-on-surface-variant">Press <kbd className="px-1 bg-surface-variant rounded">Ctrl+Shift+L</kbd> to unlock full instrument command console.</p>
            </div>
          </BaseCard>
        </div>
      </div>
    </>
  );
};


export const OperationsPage: FC = () => (
  <PageLayout className="p-gutter">
    <OperationsPageContent />
  </PageLayout>
);

export default OperationsPage;
