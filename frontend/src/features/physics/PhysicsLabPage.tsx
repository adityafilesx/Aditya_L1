import { Fragment } from 'react';
import type { FC } from 'react';
import { cn } from '@utils/cn';
import { 
  PageLayout, 
  BaseCard, 
  PrimaryButton, 
  SecondaryButton,
  Icon,
  PlotlyContainer
} from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

const PHYSICS_STATS = [
  { title: 'Peak Temperature', value: '14.2', unit: 'MK', icon: 'thermostat', isSec: true },
  { title: 'Emission Measure', value: '1.2e48', unit: 'cm⁻³', icon: 'waves', isPri: true },
  { title: 'Heating Rate', value: '4.5e28', unit: 'erg/s', icon: 'local_fire_department' },
  { title: 'Neupert Score', value: '0.71', unit: 'σ = 0.05', icon: 'score', isSubText: true },
  { title: 'AI Confidence', value: '94.2', unit: '%', icon: 'psychology', isBordered: true },
];

export const PhysicsLabPageContent: FC = () => {
  const history = useStreamStore(state => state.history);
  const currentPhysics = useStreamStore(state => state.mission?.physics);
  const currentTime = useStreamStore(state => state.mission?.clock_utc);

  const tHistory = history.physics.map(p => p.temperature_mk);
  const emHistory = history.physics.map(p => p.emission_measure_norm);
  const timeAxis = history.telemetry.map(t => new Date(t.timestamp).getTime());

  // Update dynamic values in PHYSICS_STATS
  const currentStats = PHYSICS_STATS.map(stat => {
    if (stat.title === 'Peak Temperature') return { ...stat, value: currentPhysics?.temperature_mk?.toFixed(1) || '0.0' };
    if (stat.title === 'Emission Measure') return { ...stat, value: currentPhysics?.emission_measure_norm?.toExponential(2) || '0.00e0' };
    if (stat.title === 'Neupert Score') return { ...stat, value: currentPhysics?.neupert_score?.toFixed(2) || '0.00' };
    return stat;
  });

  return (
    <>
      <div className="max-w-[1800px] mx-auto grid grid-cols-12 gap-gutter">
        
        {/* Title Section */}
        <div className="col-span-12 mb-4 flex justify-between items-end border-b border-outline-variant pb-4">
          <div>
            <h2 className="font-headline-md text-headline-md text-on-surface mb-1">Physics Laboratory</h2>
            <p className="font-data-mono text-[12px] text-on-surface-variant">Thermodynamic Diagnostics • Spectral Analysis • Plasma Evolution • Physics Intelligence</p>
          </div>
          <div className="flex items-center gap-6">
            <div className="flex gap-4 font-data-mono text-[12px]">
              <div><span className="text-on-surface-variant">T:</span> <span className="text-on-surface font-semibold">{currentTime || 'Waiting...'}</span></div>
              <div><span className="text-on-surface-variant">Exp:</span> <span className="text-on-surface font-semibold">1.0s</span></div>
              <div><span className="text-on-surface-variant">Inst:</span> <span className="text-primary font-semibold">SUIT / VELC</span></div>
            </div>
            <div className="flex gap-2">
              <SecondaryButton size="sm">Export Data</SecondaryButton>
              <PrimaryButton size="sm">Run Model</PrimaryButton>
            </div>
          </div>
        </div>
        
        {/* Stats Grid */}
        <div className="col-span-12 grid grid-cols-5 gap-4 mb-2">
          {currentStats.map((stat, idx) => (
            <div 
              key={idx} 
              className={cn(
                'lab-card p-4 flex flex-col justify-between',
                stat.isBordered && 'border-l-4 border-l-primary-container'
              )}
            >
              <div className="flex justify-between items-start mb-2">
                <span className={cn('font-label-caps text-[11px]', stat.isBordered ? 'text-primary' : 'text-on-surface-variant')}>{stat.title}</span>
                <Icon 
                  name={stat.icon} 
                  className={cn(
                    'text-[16px]', 
                    stat.isSec ? 'text-secondary' : stat.isPri ? 'text-primary' : stat.isBordered ? 'text-primary-container' : 'text-on-surface-variant'
                  )} 
                />
              </div>
              <div className="flex items-baseline gap-1">
                <span className={cn(
                  'font-numeric-telemetry text-numeric-telemetry',
                  stat.isSec ? 'text-secondary' : stat.isPri ? 'text-primary' : stat.isBordered ? 'text-primary-container' : 'text-on-surface'
                )}>
                  {stat.value}
                </span>
                {stat.isSubText ? (
                  <span className="text-[10px] text-on-surface-variant ml-2">{stat.unit}</span>
                ) : (
                  <span className="text-on-surface-variant text-body-sm ml-1">{stat.unit}</span>
                )}
              </div>
            </div>
          ))}
        </div>
        
        {/* Chart Panels */}
        <div className="col-span-8 flex flex-col gap-6">
          <BaseCard variant="lab" className="p-0 overflow-hidden flex flex-col h-[400px]">
            <div className="flex border-b border-outline-variant bg-surface-container-lowest px-4 pt-3">
              <div className="px-4 py-2 border-b-2 border-primary text-primary font-label-caps text-[11px] cursor-pointer">T-Evolution</div>
              <div className="px-4 py-2 border-b-2 border-transparent text-on-surface-variant font-label-caps text-[11px] cursor-pointer hover:text-on-surface">EM-Evolution</div>
              <div className="px-4 py-2 border-b-2 border-transparent text-on-surface-variant font-label-caps text-[11px] cursor-pointer hover:text-on-surface">Pressure</div>
              <div className="px-4 py-2 border-b-2 border-transparent text-on-surface-variant font-label-caps text-[11px] cursor-pointer hover:text-on-surface">Density</div>
            </div>
            <div className="flex-1 p-4 relative">
              <div className="absolute top-4 right-4 flex gap-2">
                <span className="bg-white/80 px-2 py-1 border border-outline-variant rounded text-[10px] font-data-mono text-on-surface-variant">Log Scale</span>
              </div>
              <div className="w-full h-full">
                <PlotlyContainer 
                  data={[{
                    x: timeAxis,
                    y: tHistory,
                    type: 'scatter',
                    mode: 'lines',
                    line: { color: '#e85d04', width: 2 },
                    name: 'Temperature (MK)'
                  }]}
                  layout={{
                    yaxis: { title: { text: 'Temperature (MK)' }, gridcolor: 'rgba(255,255,255,0.05)' },
                    showlegend: false,
                    margin: { t: 20, r: 20, b: 30, l: 50 }
                  }}
                  syncCursor
                />
              </div>
            </div>
          </BaseCard>

          <BaseCard variant="lab" className="p-0 flex flex-col h-[450px]" title={
            <span className="font-label-caps text-[12px] text-on-surface flex items-center gap-2">
              <Icon name="graphic_eq" className="text-[16px]" /> Spectral Analysis (XSPEC)
            </span>
          } badge={
            <div className="flex gap-2">
              <span className="px-2 py-0.5 bg-green-50 text-green-700 border border-green-200 rounded text-[10px] font-data-mono">χ² = 1.08</span>
              <span className="px-2 py-0.5 border border-outline-variant rounded text-[10px] font-data-mono text-on-surface-variant">dof = 124</span>
            </div>
          }>
            <div className="flex flex-1 overflow-hidden border-t border-outline-variant/30">
              <div className="flex-1 flex flex-col border-r border-outline-variant">
                <div className="flex bg-surface-container-lowest px-2 border-b border-outline-variant">
                  <div className="px-3 py-1.5 border-b-2 border-primary text-primary font-label-caps text-[10px] cursor-pointer">Counts/Energy</div>
                  <div className="px-3 py-1.5 border-b-2 border-transparent text-on-surface-variant font-label-caps text-[10px] cursor-pointer">Residuals</div>
                  <div className="px-3 py-1.5 border-b-2 border-transparent text-on-surface-variant font-label-caps text-[10px] cursor-pointer">DEM</div>
                </div>
                <div className="flex-1 p-4">
                  <div className="w-full h-full border border-dashed border-outline-variant flex items-center justify-center text-on-surface-variant font-data-mono text-sm">
                    [XSPEC Spectral Plot Render]
                  </div>
                </div>
              </div>
              <div className="w-[280px] bg-surface-bright p-4 flex flex-col gap-4 overflow-y-auto">
                <h4 className="font-label-caps text-[11px] text-on-surface-variant mb-1">Model Parameters</h4>
                <div className="space-y-3">
                  {[
                    { n: 'vth.kT', v: '1.24 keV', d: '40' },
                    { n: 'vth.norm', v: '0.054', d: '20' },
                    { n: 'powerlaw.PhoIndex', v: '3.4', d: '70', isSec: true },
                  ].map((p, idx) => (
                    <div key={idx} className="flex flex-col gap-1">
                      <div className="flex justify-between text-[11px] font-data-mono">
                        <span className="text-on-surface">{p.n}</span>
                        <span className={p.isSec ? 'text-secondary' : 'text-primary'}>{p.v}</span>
                      </div>
                      <input className="w-full accent-primary cursor-pointer" type="range" defaultValue={p.d} />
                    </div>
                  ))}
                </div>
                <div className="mt-auto">
                  <button className="w-full py-2 bg-surface border border-outline-variant rounded font-label-caps text-[11px] text-on-surface hover:bg-surface-variant transition-colors cursor-pointer">Re-Fit Data</button>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>
        
        {/* Right sidebars */}
        <div className="col-span-4 flex flex-col gap-6">
          <BaseCard variant="lab" className="p-4 flex flex-col h-[280px]" title={
            <span className="font-label-caps text-[12px] text-on-surface flex items-center gap-2">
              <Icon name="change_history" className="text-[16px]" /> Thermodynamic Phase Diagram
            </span>
          }>
            <div className="flex-1 border border-outline-variant rounded bg-surface-container-lowest relative mt-3">
              <div className="absolute inset-0">
                <PlotlyContainer 
                  data={[{
                    x: tHistory,
                    y: emHistory,
                    type: 'scatter',
                    mode: 'lines+markers',
                    marker: { color: timeAxis, colorscale: 'Viridis', size: 6 },
                    line: { color: 'rgba(255,255,255,0.2)' },
                  }]}
                  layout={{
                    xaxis: { title: { text: 'Temperature (MK)' } },
                    yaxis: { title: { text: 'Emission Measure' }, type: 'log' },
                    margin: { t: 10, r: 10, b: 40, l: 50 },
                    showlegend: false
                  }}
                />
              </div>
            </div>
          </BaseCard>

          <BaseCard variant="lab" className="p-4 flex flex-col flex-1 min-h-[300px]" title={
            <span className="font-label-caps text-[12px] text-on-surface flex items-center gap-2">
              <Icon name="timeline" className="text-[16px]" /> Event Morphology
            </span>
          }>
            <div className="flex justify-between mb-4 px-2 mt-3">
              {[
                { name: 'Pre-flare', isCurrent: false },
                { name: 'Rise', isCurrent: true },
                { name: 'Peak', isCurrent: false },
                { name: 'Decay', isCurrent: false },
              ].map((step, idx) => (
                <Fragment key={idx}>
                  {idx > 0 && <div className="h-px bg-outline-variant flex-1 mt-1.5 mx-1"></div>}
                  <div className="text-center">
                    <div className={cn(
                      'w-3 h-3 rounded-full mx-auto mb-1',
                      step.isCurrent 
                        ? 'bg-secondary-container animate-pulse' 
                        : 'bg-surface-variant border border-outline-variant'
                    )}></div>
                    <span className={cn('font-data-mono text-[9px]', step.isCurrent ? 'text-secondary' : 'text-on-surface-variant')}>{step.name}</span>
                  </div>
                </Fragment>
              ))}
            </div>
            <div className="flex-1 overflow-y-auto pr-2 space-y-3">
              <div className="border-l-2 border-outline-variant pl-3 pb-2 relative">
                <div className="absolute w-2 h-2 rounded-full bg-outline-variant -left-[5px] top-1"></div>
                <div className="font-data-mono text-[10px] text-on-surface-variant mb-0.5">14:30:12Z</div>
                <div className="font-body-sm text-[12px] text-on-surface">Initial flux increase detected in SUIT 1700Å.</div>
              </div>
              <div className="border-l-2 border-secondary-container pl-3 pb-2 relative">
                <div className="absolute w-2 h-2 rounded-full bg-secondary-container -left-[5px] top-1"></div>
                <div className="font-data-mono text-[10px] text-secondary mb-0.5">14:32:00Z</div>
                <div className="font-body-sm text-[12px] text-on-surface font-medium">Impulsive phase onset. Hard X-ray emission rise.</div>
              </div>
              <div className="border-l-2 border-outline-variant pl-3 relative opacity-60">
                <div className="absolute w-2 h-2 rounded-full bg-surface -left-[5px] top-1 border border-outline-variant"></div>
                <div className="font-data-mono text-[10px] text-on-surface-variant mb-0.5">Pending...</div>
              </div>
            </div>
          </BaseCard>
        </div>

      </div>
    </>
  );
};

export const PhysicsLabPage: FC = () => (
  <PageLayout className="p-gutter bg-surface">
    <PhysicsLabPageContent />
  </PageLayout>
);

export default PhysicsLabPage;
