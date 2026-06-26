import type { FC } from 'react';
import { cn } from '@utils/cn';
import { 
  PageLayout, 
  BaseCard, 
  BaseBadge,
  PrimaryButton,
  SecondaryButton,
  GhostButton,
  IconButton,
  EnterpriseTable,
  TextInput,
  TimeRange,
  NumberInput,
  Toggle,
  Alert,
  SkeletonLoader,
  EmptyState,
  ProgressBar,
  Icon
} from '@design-system/index';
import type { ColumnDef } from '@design-system/index';

interface TelemetryStreamRow {
  id: string;
  hexId: string;
  instrument: string;
  status: string;
  valA: number;
  valB: string;
  timestamp: string;
}

const TELEMETRY_STREAM_DATA: TelemetryStreamRow[] = [
  { id: '1', hexId: '0xAF11', instrument: 'VELC Coronal', status: 'OK', valA: 1.2404, valB: '9.21k', timestamp: '2024-05-24 12:44:59.001' },
  { id: '2', hexId: '0xAF12', instrument: 'SUIT Telescope', status: 'LAG', valA: 0.9921, valB: '4.12k', timestamp: '2024-05-24 12:44:59.004' }
];

export const DesignSystemPageContent: FC = () => {
  const streamCols: ColumnDef<TelemetryStreamRow>[] = [
    { header: 'ID (HEX)', accessorKey: 'hexId', cell: (row) => <span className="text-primary">{row.hexId}</span> },
    { header: 'INSTRUMENT', accessorKey: 'instrument', cell: (row) => <span className="text-on-surface font-body-sm">{row.instrument}</span> },
    { 
      header: 'STATUS', 
      accessorKey: 'status', 
      cell: (row) => (
        <span className={cn(
          'px-2 py-0.5 rounded text-xs font-bold',
          row.status === 'OK' ? 'bg-green-500/10 text-green-600' : 'bg-yellow-500/10 text-yellow-600'
        )}>
          {row.status}
        </span>
      )
    },
    { header: 'VAL_A', accessorKey: 'valA' },
    { header: 'VAL_B', accessorKey: 'valB' },
    { header: 'UTC TIMESTAMP', accessorKey: 'timestamp', cell: (row) => <span className="opacity-50">{row.timestamp}</span> }
  ];

  return (
    <>
      <section className="mb-12">
        <h3 className="font-display-lg text-on-surface mb-2">Design System</h3>
        <p className="text-on-surface-variant max-w-2xl">Standardized visual language for Aditya-L1's mission-critical data environments. Built for clarity, precision, and rapid decision-making.</p>
      </section>
      
      <div className="grid grid-cols-12 gap-gutter">
        <BaseCard variant="glass" className="col-span-12 p-8" title={
          <span className="flex items-center gap-4">
            <Icon name="text_fields" className="text-primary" /> Typography &amp; Scientific Notation
          </span>
        }>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mt-4">
            <div className="space-y-6">
              <div>
                <p className="font-label-caps text-on-surface-variant mb-2">Display Large (Space Grotesk)</p>
                <h1 className="font-display-lg text-on-surface">Precision Control</h1>
              </div>
              <div>
                <p className="font-label-caps text-on-surface-variant mb-2">Headline Medium (Inter)</p>
                <h2 className="font-headline-md text-on-surface">Telemetry Overview</h2>
              </div>
              <div>
                <p className="font-label-caps text-on-surface-variant mb-2">Body Large (Inter)</p>
                <p className="font-body-lg text-on-surface">High-precision enterprise engineering tool.</p>
              </div>
            </div>
            <div className="space-y-6">
              <div className="bg-surface-container p-6 rounded-xl border border-outline-variant">
                <p className="font-label-caps text-on-surface-variant mb-4">Scientific &amp; Telemetry (JetBrains Mono / Space Grotesk)</p>
                <div className="space-y-4">
                  <div className="flex justify-between items-end border-b border-outline-variant/30 pb-2">
                    <span className="font-body-sm">Solar Flux Intensity</span>
                    <span className="font-numeric-telemetry text-primary">1.25×10⁻⁵ W/m²</span>
                  </div>
                  <div className="flex justify-between items-end border-b border-outline-variant/30 pb-2">
                    <span className="font-body-sm">Angular Position</span>
                    <span className="font-numeric-telemetry text-primary">45.0001° α</span>
                  </div>
                  <div className="flex justify-between items-end border-b border-outline-variant/30 pb-2">
                    <span className="font-body-sm">UTC Sync Timestamp</span>
                    <span className="font-data-mono text-secondary">2024-05-24 T 12:45:00.003Z</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </BaseCard>
        
        <BaseCard variant="glass" className="col-span-12 p-8" title={
          <span className="flex items-center gap-4">
            <Icon name="palette" className="text-primary" /> Color Palette Tokens
          </span>
        }>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mt-4">
            <div className="space-y-2">
              <div className="h-20 bg-primary-container rounded-xl"></div>
              <p className="font-label-caps text-[10px]">Primary Accent</p>
              <p className="font-data-mono text-xs">#5B5CEB</p>
            </div>
            <div className="space-y-2">
              <div className="h-20 bg-secondary-container rounded-xl border border-outline-variant"></div>
              <p className="font-label-caps text-[10px]">Secondary Flare</p>
              <p className="font-data-mono text-xs">#FF6A3D</p>
            </div>
            <div className="space-y-2">
              <div className="h-20 bg-inverse-surface rounded-xl"></div>
              <p className="font-label-caps text-[10px]">Inverse Surface</p>
              <p className="font-data-mono text-xs">#2D3133</p>
            </div>
            <div className="space-y-2">
              <div className="h-20 bg-[#22c55e] rounded-xl opacity-20 border border-[#22c55e]"></div>
              <p className="font-label-caps text-[10px]">Nominal (Success)</p>
              <p className="font-data-mono text-xs">#22C55E</p>
            </div>
            <div className="space-y-2">
              <div className="h-20 bg-[#eab308] rounded-xl opacity-20 border border-[#eab308]"></div>
              <p className="font-label-caps text-[10px]">Degraded (Warning)</p>
              <p className="font-data-mono text-xs">#EAB308</p>
            </div>
            <div className="space-y-2">
              <div className="h-20 bg-error rounded-xl opacity-20 border border-error"></div>
              <p className="font-label-caps text-[10px]">Critical (Error)</p>
              <p className="font-data-mono text-xs">#BA1A1A</p>
            </div>
          </div>
        </BaseCard>
        
        <BaseCard variant="glass" className="col-span-12 lg:col-span-6 p-8" title={
          <span className="flex items-center gap-4">
            <Icon name="smart_button" className="text-primary" /> Buttons &amp; States
          </span>
        }>
          <div className="space-y-8 mt-4">
            <div className="flex flex-wrap gap-4">
              <PrimaryButton>Primary Action</PrimaryButton>
              <SecondaryButton>Secondary</SecondaryButton>
              <GhostButton>Ghost Button</GhostButton>
            </div>
            <div className="flex flex-wrap gap-4">
              <PrimaryButton disabled>Disabled State</PrimaryButton>
              <PrimaryButton loading>Loading</PrimaryButton>
              <IconButton icon="add" />
            </div>
          </div>
        </BaseCard>
        
        <BaseCard variant="glass" className="col-span-12 lg:col-span-6 p-8" title={
          <span className="flex items-center gap-4">
            <Icon name="verified_user" className="text-primary" /> Status Badges
          </span>
        }>
          <div className="flex flex-wrap gap-4 mt-4">
            <BaseBadge variant="live" size="sm">LIVE</BaseBadge>
            <BaseBadge variant="nominal" size="sm">NOMINAL</BaseBadge>
            <BaseBadge variant="warning" size="sm">DEGRADED</BaseBadge>
            <BaseBadge variant="critical" size="sm">CRITICAL</BaseBadge>
            <BaseBadge variant="offline" size="sm">OFFLINE</BaseBadge>
          </div>
        </BaseCard>
        
        <div className="col-span-12 grid grid-cols-1 md:grid-cols-3 gap-gutter">
          <BaseCard variant="glass" className="p-6" title={
            <span className="flex justify-between items-start w-full">
              <span className="font-label-caps text-on-surface-variant">SOLAR FLUX (SoLEXS)</span>
              <Icon name="wb_sunny" className="text-secondary opacity-50" />
            </span>
          }>
            <p className="font-numeric-telemetry text-primary text-3xl mb-1 mt-4">0.428 <span className="text-sm font-normal text-on-surface-variant">SFU</span></p>
            <div className="h-12 w-full bg-surface-container rounded flex items-end gap-0.5 overflow-hidden p-1">
              <div className="flex-1 bg-primary-container opacity-20 h-1/2"></div>
              <div className="flex-1 bg-primary-container opacity-30 h-3/4"></div>
              <div className="flex-1 bg-primary-container opacity-40 h-2/3"></div>
              <div className="flex-1 bg-primary-container opacity-60 h-full"></div>
              <div className="flex-1 bg-primary-container opacity-40 h-5/6"></div>
            </div>
          </BaseCard>

          <BaseCard variant="glass" className="p-6" title={
            <span className="flex justify-between items-start w-full">
              <span className="font-label-caps text-on-surface-variant">FLARE PROBABILITY</span>
              <Icon name="bolt" className="text-secondary opacity-50" />
            </span>
          }>
            <p className="font-numeric-telemetry text-primary text-3xl mb-1 mt-4">12.5 <span className="text-sm font-normal text-on-surface-variant">%</span></p>
            <div className="mt-4">
              <ProgressBar value={12.5} />
            </div>
          </BaseCard>

          <BaseCard variant="glass" className="p-6" title={
            <span className="flex justify-between items-start w-full">
              <span className="font-label-caps text-on-surface-variant">HEL1OS SENSOR</span>
              <Icon name="sensors" className="text-secondary opacity-50" />
            </span>
          }>
            <div className="flex items-center gap-2 text-green-600 mb-2 mt-4">
              <Icon name="check_circle" className="text-[18px]" />
              <span className="font-label-caps text-[11px]">ACTIVE - STREAMING</span>
            </div>
            <p className="font-data-mono text-xs opacity-60">Packet ID: 0x4F2A_991</p>
          </BaseCard>
        </div>
        
        <div className="col-span-12">
          <EnterpriseTable
            title="Telemetry Stream Analysis"
            data={TELEMETRY_STREAM_DATA}
            columns={streamCols}
            actions={
              <div className="flex gap-2">
                <button className="px-3 py-1.5 border border-outline-variant rounded text-body-sm font-label-caps flex items-center gap-2">
                  <Icon name="filter_list" className="text-[18px]" /> Filter
                </button>
                <button className="px-3 py-1.5 bg-primary-container text-white rounded text-body-sm font-label-caps">Export CSV</button>
              </div>
            }
          />
        </div>
        
        <BaseCard variant="glass" className="col-span-12 lg:col-span-8 p-8" title={
          <span className="flex items-center gap-4">
            <Icon name="edit_note" className="text-primary" /> High-Density Inputs
          </span>
        }>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
            <div className="space-y-4">
              <TextInput label="PARAMETER OVERRIDE" defaultValue="SUIT_EXPOSURE_SYNC" />
              <TimeRange label="TIME WINDOW (UTC)" startTime="" endTime="" onStartChange={() => {}} onEndChange={() => {}} />
            </div>
            <div className="space-y-4">
              <NumberInput label="SENSOR SENSITIVITY (eV)" placeholder="0.0000" step="0.0001" />
              <Toggle label="Auto-Correct Protocol" />
            </div>
          </div>
        </BaseCard>
        
        <BaseCard variant="glass" className="col-span-12 lg:col-span-4 p-8" title={
          <span className="flex items-center gap-4">
            <Icon name="warning" className="text-primary" /> Alert Severities
          </span>
        }>
          <div className="space-y-4 mt-4">
            <Alert variant="info" title="MISSION DIRECTIVE">Ajust VELC sampling to 50Hz.</Alert>
            <Alert variant="warning" title="MAINTENANCE">Database re-indexing in 05m.</Alert>
            <Alert variant="error" title="EMERGENCY">Sensor SUIT thermal overload detected!</Alert>
          </div>
        </BaseCard>
        
        <BaseCard variant="glass" className="col-span-12 md:col-span-6 p-8">
          <p className="font-label-caps text-on-surface-variant mb-6 text-[11px]">SKELETON LOADERS</p>
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <SkeletonLoader variant="circle" />
              <div className="space-y-2 flex-1">
                <SkeletonLoader variant="text" className="w-1/4" />
                <SkeletonLoader variant="text" className="w-3/4" />
              </div>
            </div>
            <SkeletonLoader variant="card" />
          </div>
        </BaseCard>

        <BaseCard variant="glass" className="col-span-12 md:col-span-6 p-8 flex flex-col items-center justify-center text-center">
          <EmptyState
            title="No Telemetry Feed"
            subtitle="Check L-Band uplink or verify ground station connectivity."
            icon="wifi_off"
            className="p-0 shadow-none bg-transparent"
            actions={
              <button className="px-4 py-2 border border-outline-variant rounded-lg font-label-caps text-xs opacity-50 hover:opacity-100 transition-opacity">RETRY CONNECTION</button>
            }
          />
        </BaseCard>
        
        <BaseCard variant="glass" className="col-span-12 p-8 bg-inverse-surface text-on-primary-container border-none shadow-none" title={
          <span className="flex items-center gap-4">
            <Icon name="token" /> System Tokens
          </span>
        }>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mt-4">
            <div>
              <p className="font-label-caps text-surface-variant mb-6">SPACING SCALE (px)</p>
              <div className="flex items-end gap-3 h-16">
                <div className="w-1 bg-primary-container h-1" title="4px"></div>
                <div className="w-2 bg-primary-container h-2" title="8px"></div>
                <div className="w-4 bg-primary-container h-4" title="16px"></div>
                <div className="w-6 bg-primary-container h-6" title="24px"></div>
                <div className="w-8 bg-primary-container h-8" title="32px"></div>
                <div className="w-12 bg-primary-container h-12" title="48px"></div>
                <div className="w-16 bg-primary-container h-16" title="64px"></div>
              </div>
            </div>
            <div>
              <p className="font-label-caps text-surface-variant mb-6">RADIUS SCALE</p>
              <div className="flex gap-4">
                <div className="w-12 h-12 border-2 border-primary-container rounded-[6px]" title="6px"></div>
                <div className="w-12 h-12 border-2 border-primary-container rounded-lg" title="8px"></div>
                <div className="w-12 h-12 border-2 border-primary-container rounded-xl" title="12px"></div>
                <div className="w-12 h-12 border-2 border-primary-container rounded-[18px]" title="18px"></div>
                <div className="w-12 h-12 border-2 border-primary-container rounded-full" title="full"></div>
              </div>
            </div>
            <div>
              <p className="font-label-caps text-surface-variant mb-6">ELEVATION (Depth)</p>
              <div className="space-y-4">
                <div className="p-4 bg-surface rounded-xl text-on-surface text-center font-label-caps text-[10px] shadow-sm">Level 1 - Border Only</div>
                <div className="p-4 bg-surface rounded-xl text-on-surface text-center font-label-caps text-[10px]">Level 2 - Floating Overlay</div>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>
    </>
  );
};

export const DesignSystemPage: FC = () => (
  <PageLayout className="p-6" data-layout="shell">
    <DesignSystemPageContent />
  </PageLayout>
);

export default DesignSystemPage;
