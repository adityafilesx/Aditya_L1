import type { FC } from 'react';
import { cn } from '@utils/cn';
import { 
  BaseCard, 
  BaseBadge, 
  EnterpriseTable, 
  Icon
} from '@design-system/index';
import type { ColumnDef } from '@design-system/index';

interface AssetMatrixRow {
  id: string;
  asset: string;
  charging: string;
  radiation: string;
  comms: string;
}

const ASSET_MATRIX_DATA: AssetMatrixRow[] = [
  { id: 'aditya', asset: 'Aditya-L1', charging: 'LOW', radiation: 'NOMINAL', comms: '100%' },
  { id: 'insat', asset: 'INSAT-3DR', charging: 'ELEV', radiation: 'NOMINAL', comms: '98%' },
  { id: 'navic', asset: 'NavIC Fleet', charging: 'LOW', radiation: 'NOMINAL', comms: '100%' },
];

export const IntelligencePageContent: FC = () => {
  const assetCols: ColumnDef<AssetMatrixRow>[] = [
    { header: 'ASSET', accessorKey: 'asset', cell: (row) => <span className={cn(row.asset === 'Aditya-L1' && 'font-bold text-primary')}>{row.asset}</span> },
    { 
      header: 'CHARGING', 
      accessorKey: 'charging', 
      cell: (row) => (
        <span className="flex items-center">
          <span className={`w-2 h-2 rounded-full inline-block mr-2 ${row.charging === 'LOW' ? 'bg-green-500' : 'bg-yellow-500'}`} />
          {row.charging}
        </span>
      )
    },
    { 
      header: 'RADIATION', 
      accessorKey: 'radiation', 
      cell: (row) => (
        <span className="flex items-center">
          <span className="w-2 h-2 rounded-full inline-block bg-green-500 mr-2" />
          {row.radiation}
        </span>
      )
    },
    { header: 'COMMS', accessorKey: 'comms' },
  ];

  return (
    <>
      <header className="flex justify-between items-center w-full px-container-margin py-component-padding-y bg-surface-container-lowest dark:bg-surface-dim border-b border-outline-variant dark:border-outline shadow-sm z-40 sticky top-0">
        <div className="flex items-center space-x-8">
          <h1 className="font-display-lg text-[18px] tracking-tighter text-primary dark:text-primary-fixed">MISSION CONTROL PRECISION SYSTEM</h1>
          <nav className="hidden md:flex space-x-6">
            <a className="text-on-surface-variant font-medium font-label-caps text-label-caps hover:text-primary-container transition-colors duration-150" href="#">LIVE FEED</a>
            <a className="text-primary font-bold border-b-2 border-primary pb-1 font-label-caps text-label-caps transition-colors duration-150 opacity-80 scale-95" href="#">TELEMETRY</a>
            <a className="text-on-surface-variant font-medium font-label-caps text-label-caps hover:text-primary-container transition-colors duration-150" href="#">ANALYSIS</a>
          </nav>
        </div>
        <div className="flex items-center space-x-4">
          <div className="hidden lg:flex items-center space-x-2 text-primary dark:text-primary-fixed-dim font-label-caps text-label-caps px-3 py-1 bg-primary-fixed/10 rounded-full">
            <div className="w-2 h-2 rounded-full bg-primary blinking-dot"></div>
            <span>MISSION STATUS: NOMINAL</span>
          </div>
          <button className="text-on-surface-variant hover:text-primary-container transition-colors duration-150 bg-transparent border-none cursor-pointer">
            <Icon name="schedule" />
          </button>
          <button className="text-on-surface-variant hover:text-primary-container transition-colors duration-150 bg-transparent border-none cursor-pointer">
            <Icon name="language" />
          </button>
          <button className="text-on-surface-variant hover:text-primary-container transition-colors duration-150 bg-transparent border-none cursor-pointer">
            <Icon name="settings" />
          </button>
        </div>
      </header>

      <div className="p-container-margin space-y-section-gap flex-1">
        <section className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-outline-variant pb-6">
          <div>
            <h2 className="font-headline-md text-headline-md text-on-surface">Mission Intelligence</h2>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Global Space Weather Impact Assessment</p>
          </div>
          <div className="flex space-x-6 text-right">
            <div className="flex flex-col">
              <span className="font-label-caps text-label-caps text-tertiary">UTC TIME</span>
              <span className="font-data-mono text-data-mono text-on-surface" id="utc-clock">14:22:05 Z</span>
            </div>
            <div className="flex flex-col">
              <span className="font-label-caps text-label-caps text-tertiary">MISSION MODE</span>
              <span className="font-data-mono text-data-mono text-primary font-bold">NOMINAL</span>
            </div>
            <div className="flex flex-col">
              <span className="font-label-caps text-label-caps text-tertiary">FORECAST HORIZON</span>
              <span className="font-data-mono text-data-mono text-on-surface">72H</span>
            </div>
          </div>
        </section>

        {/* Overview metric panels */}
        <section className="grid grid-cols-2 md:grid-cols-6 gap-gutter bg-surface-container-lowest p-component-padding-x rounded-card border border-outline-variant shadow-card">
          <div className="flex flex-col border-r border-outline-variant last:border-0 pr-4">
            <span className="font-label-caps text-label-caps text-tertiary mb-1">MISSION RISK</span>
            <div className="flex items-baseline space-x-2">
              <span className="font-numeric-telemetry text-numeric-telemetry text-on-surface">21%</span>
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
            </div>
          </div>
          <div className="flex flex-col border-r border-outline-variant last:border-0 px-4">
            <span className="font-label-caps text-label-caps text-tertiary mb-1">SPACE WEATHER</span>
            <span className="font-numeric-telemetry text-numeric-telemetry text-on-surface">R1 / S1</span>
          </div>
          <div className="flex flex-col border-r border-outline-variant last:border-0 px-4">
            <span className="font-label-caps text-label-caps text-tertiary mb-1">SOLAR ACTIVITY</span>
            <span className="font-body-sm text-body-sm text-on-surface font-medium">Moderate</span>
          </div>
          <div className="flex flex-col border-r border-outline-variant last:border-0 px-4">
            <span className="font-label-caps text-label-caps text-tertiary mb-1">RADIATION</span>
            <span className="font-body-sm text-body-sm text-green-600 font-medium">Quiet</span>
          </div>
          <div className="flex flex-col border-r border-outline-variant last:border-0 px-4">
            <span className="font-label-caps text-label-caps text-tertiary mb-1">HF COMMS</span>
            <span className="font-body-sm text-body-sm text-on-surface font-medium">Nominal</span>
          </div>
          <div className="flex flex-col pl-4">
            <span className="font-label-caps text-label-caps text-tertiary mb-1">SAT HEALTH</span>
            <span className="font-body-sm text-body-sm text-primary font-medium">Optimal</span>
          </div>
        </section>

        {/* Hazard forecasts & interactive map mock */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
          <div className="lg:col-span-4 flex flex-col gap-gutter">
            <BaseCard variant="plain" size="md" className="shadow-card hover:border-primary transition-colors" title="MISSION RISK INDEX">
              <div className="space-y-4 mt-2">
                <div className="flex justify-between items-center">
                  <span className="font-body-sm text-body-sm text-on-surface-variant">Aggregate Risk</span>
                  <span className="font-numeric-telemetry text-numeric-telemetry text-on-surface">21%</span>
                </div>
                <div className="w-full h-8 bg-surface-container rounded flex items-end px-1 pb-1 space-x-1">
                  <div className="w-1/6 bg-primary/40 h-2 rounded-t"></div>
                  <div className="w-1/6 bg-primary/60 h-3 rounded-t"></div>
                  <div className="w-1/6 bg-primary/80 h-4 rounded-t"></div>
                  <div className="w-1/6 bg-primary h-6 rounded-t"></div>
                  <div className="w-1/6 bg-primary h-5 rounded-t"></div>
                  <div className="w-1/6 bg-primary h-7 rounded-t"></div>
                </div>
                <div className="border-t border-outline-variant pt-3 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-body-sm text-body-sm text-tertiary">Radiation Context</span>
                    <BaseBadge variant="success">Nominal</BaseBadge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-body-sm text-body-sm text-tertiary">HF Blackout</span>
                    <BaseBadge variant="warning">Elevated</BaseBadge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-body-sm text-body-sm text-tertiary">Satellite Risk</span>
                    <BaseBadge variant="success">Low</BaseBadge>
                  </div>
                </div>
              </div>
            </BaseCard>

            <BaseCard variant="plain" size="md" className="shadow-card hover:border-primary transition-colors" title="HAZARD FORECAST">
              <div className="grid grid-cols-2 gap-4 mt-2">
                <div className="bg-surface-container p-3 rounded-lg">
                  <span className="block font-label-caps text-label-caps text-tertiary mb-1">CME PROBABILITY</span>
                  <span className="block font-numeric-telemetry text-numeric-telemetry text-on-surface text-lg font-bold">18%</span>
                  <span className="block font-body-sm text-body-sm text-on-surface-variant mt-2 text-xs">Arrival: N/A</span>
                </div>
                <div className="bg-surface-container p-3 rounded-lg">
                  <span className="block font-label-caps text-label-caps text-tertiary mb-1">SEP FLUX RISK</span>
                  <span className="block font-numeric-telemetry text-numeric-telemetry text-on-surface text-lg font-bold">12%</span>
                  <span className="block font-body-sm text-body-sm text-on-surface-variant mt-2 text-xs">Level: Background</span>
                </div>
              </div>
            </BaseCard>
          </div>

          <div className="lg:col-span-8 flex flex-col gap-gutter">
            <BaseCard variant="plain" className="p-1 shadow-card relative overflow-hidden h-[400px]">
              <div className="absolute inset-0 bg-gradient-to-br from-[#0f172a] to-[#1e293b] rounded-[13px] flex items-center justify-center">
                <div className="w-64 h-64 rounded-full border border-primary/30 bg-blue-900/20 shadow-[0_0_50px_rgba(65,64,209,0.3)] flex items-center justify-center relative overflow-hidden">
                  <div className="absolute inset-y-0 right-0 w-1/2 bg-black/60 backdrop-blur-sm"></div>
                  <span className="font-data-mono text-data-mono text-primary relative z-10">GLOBAL_IMPACT_VISUALIZATION.OBJ</span>
                </div>
              </div>
              <div className="absolute top-4 left-4 right-4 flex justify-between z-10">
                <span className="font-label-caps text-label-caps text-white/80 bg-black/40 px-2 py-1 rounded backdrop-blur-md">TERMINATOR: ACTIVE</span>
                <span className="font-label-caps text-label-caps text-white/80 bg-black/40 px-2 py-1 rounded backdrop-blur-md">ISTRAC UPLINK: OK</span>
              </div>
            </BaseCard>

            <BaseCard variant="plain" size="md" className="shadow-card" title="CAUSAL PROPAGATION CHAIN">
              <div className="flex items-center justify-between text-center relative mt-2">
                <div className="absolute top-1/2 left-0 w-full h-[1px] bg-outline-variant -z-10"></div>
                
                {[
                  { name: 'Flare', icon: 'light_mode' },
                  { name: 'CME', icon: 'storm' },
                  { name: 'SEP', icon: 'scatter_plot' },
                  { name: 'Solar Wind', icon: 'air' },
                  { name: 'Impact', icon: 'public', active: true },
                ].map((step) => (
                  <div key={step.name} className="bg-surface-container-lowest px-2 z-10">
                    <div className={cn(
                      'w-8 h-8 rounded-full border flex items-center justify-center mx-auto mb-2',
                      step.active 
                        ? 'bg-primary-container text-on-primary-container border-primary font-bold' 
                        : 'bg-surface-container border-outline text-primary'
                    )}>
                      <Icon name={step.icon} className="text-sm" />
                    </div>
                    <span className={cn('font-body-sm text-body-sm text-on-surface block text-xs', step.active && 'font-medium')}>{step.name}</span>
                  </div>
                ))}
              </div>
            </BaseCard>
          </div>
        </div>

        {/* Bottom tables & consent panels */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter mt-gutter">
          <EnterpriseTable
            title="SATELLITE & GROUND MATRIX"
            data={ASSET_MATRIX_DATA}
            columns={assetCols}
            className="shadow-card"
          />

          <BaseCard variant="plain" size="md" className="shadow-card flex flex-col" title="AI DECISION ENGINE">
            <div className="flex-1 flex flex-col justify-center items-center text-center p-6 bg-primary-fixed/5 rounded-lg border border-primary/20 mt-2">
              <Icon name="memory" className="text-4xl text-primary mb-3" />
              <h4 className="font-headline-md text-headline-md text-on-surface mb-2">Continue Science Mode</h4>
              <p className="font-body-sm text-body-sm text-on-surface-variant max-w-md mx-auto">
                Consensus reached via ensemble modeling. Geomagnetic indices (Kp: 3, Dst: -18 nT) indicate sub-storm thresholds will not be breached in the 72h window.
              </p>
            </div>
          </BaseCard>
        </div>
      </div>

      <footer className="fixed bottom-0 w-full z-40 flex justify-between items-center px-container-margin py-2 bg-surface-container-highest dark:bg-surface-container-high border-t border-outline-variant md:ml-[260px] md:w-[calc(100%-260px)]">
        <div className="font-data-mono text-data-mono text-tertiary dark:text-tertiary-fixed-dim text-xs">
          AEROSPACE MISSION CONTROL ALPHA • SYSTEM HEALTH: 100% • CONNECTIVITY: ENCRYPTED
        </div>
        <div className="hidden sm:flex space-x-6">
          <a className="font-data-mono text-data-mono text-on-tertiary-fixed-variant hover:text-primary underline transition-colors duration-150 text-xs" href="#">Uplink Status</a>
          <a className="font-data-mono text-data-mono text-on-tertiary-fixed-variant hover:text-primary underline transition-colors duration-150 text-xs" href="#">Ground Station Alpha</a>
          <a className="font-data-mono text-data-mono text-on-tertiary-fixed-variant hover:text-primary underline transition-colors duration-150 text-xs" href="#">Latencies</a>
        </div>
      </footer>
    </>
  );
};

export const IntelligencePage: FC = () => (
  <div className="w-full h-full overflow-auto custom-scrollbar" data-layout="precision">
    <IntelligencePageContent />
  </div>
);

export default IntelligencePage;
