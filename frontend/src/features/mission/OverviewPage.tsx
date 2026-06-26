import type { FC } from 'react';
import { 
  PageLayout, 
  Header, 
  MetricCard, 
  ChartContainer, 
  BaseCard, 
  BaseBadge, 
  SeverityBadge, 
  Timeline, 
  EnterpriseTable, 
  ActionButton,
  Icon,
  PlotlyContainer
} from '@design-system/index';
import type { ColumnDef } from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

// Custom inline structures maintained for visual identity:
const SYSTEM_SERVICES = [
  { name: 'Telemetry', status: 'online', ok: true },
  { name: 'Physics', status: 'online', ok: true },
  { name: 'Models', status: 'degraded', ok: true },
  { name: 'Forecast', status: 'online', ok: true },
  { name: 'Twin', status: 'syncing', ok: true },
  { name: 'Graph', status: 'online', ok: true },
  { name: 'API', status: 'online', ok: true },
  { name: 'DB', status: 'online', ok: true },
];

export const OverviewPageContent: FC = () => {
  const missionState = useStreamStore(state => state.mission);
  const history = useStreamStore(state => state.history);
  const connectionStatus = useStreamStore(state => state.connectionStatus);

  const modelCols: ColumnDef<any>[] = [
    { header: 'Model', accessorKey: 'model', cell: (row) => row.model },
    { header: 'Confidence', accessorKey: 'confidence', cell: (row) => row.confidence, className: 'text-right' },
    { header: 'Latency', accessorKey: 'latency', cell: (row) => row.latency, className: 'text-right' },
    { 
      header: 'Status', 
      accessorKey: 'status', 
      cell: (row) => (
        <span className="flex items-center">
          <span className={`w-2 h-2 rounded-full inline-block mr-2 ${row.status === 'ONLINE' ? 'bg-success' : 'bg-warning'}`}></span>
          <span className="text-[12px]">{row.status}</span>
        </span>
      )
    },
  ];

  const sensorCols: ColumnDef<any>[] = [
    { header: 'Instrument', accessorKey: 'instrument', cell: (row) => <strong>{row.instrument}</strong> },
    { header: 'Packet Qlt.', accessorKey: 'packetQlt', cell: (row) => row.packetQlt, className: 'text-right' },
    { header: 'Latency', accessorKey: 'latency', cell: (row) => row.latency, className: 'text-right' },
    { 
      header: 'Health', 
      accessorKey: 'health', 
      cell: (row) => (
        <span className={`px-2 py-1 rounded text-[10px] font-bold ${row.health === 'ONLINE' || row.health === 'OPTIMAL' ? 'bg-success/10 text-success' : 'bg-warning/10 text-warning'}`}>
          {row.health}
        </span>
      )
    },
  ];

  const alertCols: ColumnDef<any>[] = [
    { header: 'Time', accessorKey: 'timestamp', cell: (row) => new Date(row.timestamp).toLocaleTimeString() },
    { 
      header: 'Severity', 
      accessorKey: 'severity', 
      cell: (row) => <SeverityBadge status={row.severity}>{row.severity}</SeverityBadge> 
    },
    { header: 'Subsystem', accessorKey: 'type', cell: (row) => <span className="font-body-sm">{row.type}</span> },
    { header: 'Description', accessorKey: 'description', cell: (row) => <span className="font-body-sm">{row.description}</span> },
    { 
      header: 'Action', 
      accessorKey: 'action', 
      cell: (row) => <ActionButton onClick={() => console.log('Action triggered', row.id)}>Review</ActionButton> 
    },
  ];

  if (!missionState && connectionStatus === 'connecting') {
    return (
      <div className="space-y-gutter p-8 text-center text-on-surface-variant animate-pulse">
        Connecting to Real-Time Streaming Bus...
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

  // Fallback to empty if not loaded yet but connected
  const state = missionState || {} as any;
  const physics = state.physics || {};
  const forecast = state.forecast || {};
  const sensors = state.sensors || {};
  const models = state.models || {};
  const alerts = state.alerts || [];
  
  const mappedMetricData = [
    { title: 'Mission State', value: state.state === 2 ? 'ALERT' : state.state === 1 ? 'WATCH' : 'NOMINAL', status: state.state > 0 ? 'warning' : 'success' },
    { title: 'Flare Prob.', value: `${((forecast.probability || 0) * 100).toFixed(1)}%`, status: (forecast.probability || 0) > 0.5 ? 'warning' : 'primary' },
    { title: 'Forecast Conf.', value: `${((forecast.confidence || 0) * 100).toFixed(0)}%`, status: 'primary' },
    { title: 'Target Class', value: forecast.estimated_goes_class || 'Quiet', status: 'success' },
    { title: 'Neupert', value: physics.neupert_score?.toFixed(2) || '0.0', status: 'success' },
    { title: 'Temp (MK)', value: physics.temperature_mk?.toFixed(1) || '0.0', status: 'primary' },
    { title: 'Entropy', value: physics.shannon_entropy?.toFixed(2) || '0.0', status: 'primary' },
  ];

  const mappedSensorData: any[] = Object.keys(sensors).map((key) => ({
    id: key,
    instrument: key.toUpperCase(),
    packetQlt: '100.0%', // Simulated
    latency: '10ms', // Simulated
    health: sensors[key]
  }));

  const mappedModelData: any[] = [
    { id: '1', model: 'Ensemble Forecaster', confidence: 'N/A', latency: 'N/A', status: models.ensemble_status || 'OFFLINE' },
    { id: '2', model: 'XGBoost', confidence: 'N/A', latency: 'N/A', status: models.xgb_status || 'OFFLINE' },
    { id: '3', model: 'AI Temporal', confidence: 'N/A', latency: 'N/A', status: models.ai_temporal_status || 'OFFLINE' },
  ];

  const mappedServices = SYSTEM_SERVICES.map(s => {
    if (s.name === 'Physics') return { ...s, ok: !!physics.temperature_mk };
    if (s.name === 'Forecast') return { ...s, ok: !!forecast.probability };
    if (s.name === 'API') return { ...s, ok: connectionStatus === 'connected' };
    return s;
  });

  return (
    <>
      <Header
        title="Mission Overview"
        subtitle="Real-Time Executive Solar Situation Awareness"
        actions={
          <div className="flex flex-wrap gap-x-6 gap-y-2 bg-white p-4 rounded-xl border border-outline-variant font-data-mono text-data-mono">
            <div className="flex flex-col">
              <span className="text-[10px] text-on-surface-variant uppercase">UTC Clock</span>
              <span className="text-primary font-bold">{state.clock_utc || '00:00:00'}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] text-on-surface-variant uppercase">Mission Elapsed</span>
              <span className="text-on-surface">T+ 145:12:04:22</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] text-on-surface-variant uppercase">Mode</span>
              <span className="text-success font-bold flex items-center gap-1">
                <span className="live-dot bg-success"></span> {state.mode || 'SCIENCE MODE'}
              </span>
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] text-on-surface-variant uppercase">Shift / Op</span>
              <span className="text-on-surface">{state.operator || 'Cmdr. Aditi'}</span>
            </div>
          </div>
        }
      />

      <div className="bg-white border border-outline-variant rounded-lg p-3 mb-gutter flex flex-wrap items-center gap-6 justify-between overflow-x-auto whitespace-nowrap">
        {mappedServices.map((serv) => (
          <div key={serv.name} className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${serv.ok === true ? 'bg-success' : serv.ok === false ? 'bg-warning' : 'bg-critical'}`}></span>
            <span className="font-label-caps text-label-caps">{serv.name}</span>
          </div>
        ))}
      </div>

      {/* Grid of Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-gutter mb-gutter">
        {mappedMetricData.map((data) => (
          <MetricCard
            key={data.title}
            title={data.title}
            value={data.value}
            status={data.status as any}
          />
        ))}
      </div>

      {/* Solar flux & Side panels */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-gutter mb-gutter">
        <div className="lg:col-span-2">
          <ChartContainer
            title="Solar X-Ray Flux"
            subtitle="Real-time spectral density monitoring"
            timeRange="L-24H"
            onTimeRangeChange={() => {}}
            onRefresh={() => {}}
            onFullscreen={() => {}}
            onExport={() => {}}
          >
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
          </ChartContainer>
        </div>

        <div className="space-y-gutter">
          <BaseCard variant="plain" size="md" className="border-l-4 border-l-primary">
            <div className="flex items-center gap-2 mb-4 text-primary">
              <Icon name="psychology" className="text-[18px]" />
              <h3 className="font-label-caps text-label-caps font-bold">Intelligence Feed</h3>
            </div>
            <div className="space-y-4">
              {state.recommendations?.map((rec: string, i: number) => (
                <div key={i} className="p-3 bg-surface-container-low rounded-lg">
                  <div className="flex justify-between items-start mb-1">
                    <BaseBadge variant={i === 0 ? "primary" : "offline"} size="sm">{i === 0 ? "Current" : "Queued"}</BaseBadge>
                    <span className="font-data-mono text-[10px] text-outline">LIVE</span>
                  </div>
                  <p className="font-body-sm text-body-sm font-semibold">{rec}</p>
                </div>
              ))}
            </div>
          </BaseCard>

          <BaseCard variant="plain" size="md">
            <h3 className="font-label-caps text-label-caps text-on-surface-variant mb-4">Physics Summary</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="block text-[10px] text-outline uppercase">Temperature</span>
                <span className="font-numeric-telemetry text-numeric-telemetry font-bold">{physics?.temperature_mk?.toFixed(2) || '0.0'} MK</span>
              </div>
              <div>
                <span className="block text-[10px] text-outline uppercase">Neupert Score</span>
                <span className="font-numeric-telemetry text-numeric-telemetry font-bold">{physics?.neupert_score?.toFixed(2) || '0.0'}</span>
              </div>
              <div className="col-span-2">
                <span className="block text-[10px] text-outline uppercase">Emission Measure</span>
                <span className="font-data-mono text-data-mono font-bold">{physics?.emission_measure_norm?.toExponential(2) || '0.0'} cm⁻³</span>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-outline-variant grid grid-cols-2 gap-x-4 gap-y-2 text-[11px] font-data-mono">
              <div className="flex justify-between"><span>Centroid</span> <span className="text-success">{physics?.spectral_centroid?.toFixed(2)}</span></div>
              <div className="flex justify-between"><span>Entropy</span> <span className="text-success">{physics?.shannon_entropy?.toFixed(2)}</span></div>
              <div className="flex justify-between"><span>Flatness</span> <span className="text-primary">{physics?.spectral_flatness?.toFixed(2)}</span></div>
              <div className="flex justify-between"><span>Rolloff</span> <span className="text-on-surface-variant">{physics?.spectral_rolloff?.toFixed(2)}</span></div>
            </div>
          </BaseCard>
        </div>
      </div>

      {/* AI Model Consensus & Health */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter mb-gutter">
        <EnterpriseTable
          title="AI Model Consensus"
          data={mappedModelData}
          columns={modelCols}
          actions={<div className="px-3 py-1 bg-primary-container/10 border border-primary text-primary rounded-full font-label-caps text-label-caps">LIVE</div>}
        />
        <EnterpriseTable
          title="Sensor Health Matrix"
          data={mappedSensorData}
          columns={sensorCols}
        />
      </div>

      {/* Digital Twin & Operational Timeline */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter mb-gutter">
        <BaseCard variant="plain" size="md" className="flex flex-col md:flex-row gap-6">
          <div className="md:w-1/3 aspect-square bg-inverse-surface rounded-lg relative overflow-hidden flex items-center justify-center">
            <img className="absolute inset-0 w-full h-full object-cover opacity-80" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC7bio_x30nXMd-EMAfLkPJK9CDrJ_kb72719jzU6VeGU3-TpU4GLcwFW8IHVAInENRY79suLvvMJyENirVk4d235eNxZPTUX4JjL2mgV6OA6nfU2OeWRPvmwijWdYbZ3yFgN2BDJicHqiRK8kZDmv09ICEfsQ-CyVwONVzT6gVKTjdFeLPoBOffRRFmLs4i5ZYLTWOnXglZ--eHMOr9vM7oh0398IfNJTotvUjKdAdaE70e_fADvQgVFfXtoyzzPQeDX2ihHoMUGfD" alt="Solar surface"/>
            <div className="absolute inset-0 border-[20px] border-transparent border-t-primary/20 border-l-primary/20"></div>
            <div className="z-10 text-white font-data-mono text-[10px] bg-black/50 p-2 rounded backdrop-blur">AR-3482 TARGET LOCK</div>
          </div>
          <div className="flex-1 flex flex-col">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="font-headline-md text-headline-md text-on-surface">Digital Twin Snapshot</h3>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Simulated physics-to-sensor validation</p>
              </div>
              <div className="text-right">
                <span className="text-[10px] text-outline uppercase block">Similarity Score</span>
                <span className="font-numeric-telemetry text-numeric-telemetry text-primary font-bold">0.982</span>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 flex-1">
              <div className="p-4 bg-surface-container-low rounded-lg border border-outline-variant">
                <span className="block text-[10px] text-outline uppercase mb-2">Active Region Info</span>
                <div className="space-y-1 font-data-mono text-[12px]">
                  <div className="flex justify-between"><span>Lat/Long:</span> <span className="text-on-surface">12N / 45E</span></div>
                  <div className="flex justify-between"><span>Area:</span> <span className="text-on-surface">1420 MH</span></div>
                  <div className="flex justify-between"><span>Class:</span> <span className="text-secondary font-bold">Beta-Gamma-Delta</span></div>
                </div>
              </div>
              <div className="p-4 bg-surface-container-low rounded-lg border border-outline-variant">
                <span className="block text-[10px] text-outline uppercase mb-2">Twin Discrepancy</span>
                <div className="space-y-1 font-data-mono text-[12px]">
                  <div className="flex justify-between"><span>Flux Δ:</span> <span className="text-success">{state.digital_twin?.flux_delta?.toFixed(4) || '0.000'}</span></div>
                  <div className="flex justify-between"><span>V-Field Δ:</span> <span className="text-warning">{state.digital_twin?.v_field_delta?.toFixed(3) || '0.00'}</span></div>
                  <div className="flex justify-between"><span>Temp Δ:</span> <span className="text-success">{state.digital_twin?.temp_delta?.toFixed(3) || '0.00'}</span></div>
                </div>
              </div>
            </div>
          </div>
        </BaseCard>

        <BaseCard variant="plain" size="md">
          <h3 className="font-label-caps text-label-caps text-on-surface-variant mb-4">Operational Timeline</h3>
          <Timeline
            items={(alerts || []).slice(0, 4).map((a: any) => ({
              time: new Date(a.timestamp).toLocaleTimeString(),
              title: a.description,
              status: a.severity === 'CRITICAL' ? 'active' : 'inactive'
            }))}
          />
        </BaseCard>
      </div>

      {/* Recent Alerts */}
      <EnterpriseTable
        title="Recent Alerts"
        data={alerts}
        columns={alertCols}
        actions={<button className="font-label-caps text-label-caps text-primary hover:underline bg-transparent border-none cursor-pointer">View All Logs</button>}
        className="mb-gutter"
      />

      {/* System Resources Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-gutter">
        {Object.keys(state.system_metrics || {}).map((key) => {
          const value = state.system_metrics[key];
          return (
            <div key={key} className="bg-white p-4 rounded-xl border border-outline-variant">
              <div className="flex justify-between items-start mb-2">
                <span className="text-[10px] text-outline uppercase font-bold">{key}</span>
                <span className={`w-2 h-2 rounded-full ${value < 90 ? 'bg-success' : 'bg-warning'}`}></span>
              </div>
              <div className="font-numeric-telemetry text-[14px] font-bold">{value}%</div>
              <div className="h-8 mt-2 w-full bg-surface-container flex items-end gap-0.5">
                {[...Array(5)].map((_, barIdx) => (
                  <div 
                    key={barIdx} 
                    className={`w-1 ${value < 90 ? 'bg-primary/40' : 'bg-warning/40'}`} 
                    style={{ height: `${(Math.random() * 0.4 + 0.6) * value}%` }} 
                  />
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
};

export const OverviewPage: FC = () => (
  <PageLayout className="p-gutter">
    <OverviewPageContent />
  </PageLayout>
);

export default OverviewPage;
