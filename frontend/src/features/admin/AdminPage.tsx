import { useEffect, useState } from 'react';
import type { FC } from 'react';
import { cn } from '@utils/cn';
import { 
  PageLayout, 
  Header, 
  BaseCard, 
  EnterpriseTable 
} from '@design-system/index';
import type { ColumnDef } from '@design-system/index';

interface Diagnostics {
  timestamp: number;
  hardware: {
    cpu_percent: number;
    memory_percent: number;
    gpu_percent: number;
    disk_percent: number;
    process_uptime_sec: number;
    thread_count: number;
    network_latency_ms: number;
  };
  engines: Record<string, { status: string; version?: string; type?: string; connections?: number }>;
  overall_status: string;
}

interface ServiceRow {
  id: string;
  service: string;
  version: string;
  status: string;
}

export const AdminPageContent: FC = () => {
  const [diagnostics, setDiagnostics] = useState<Diagnostics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDiagnostics = async () => {
      try {
        const res = await fetch('/api/system/diagnostics');
        if (res.ok) {
          const data = await res.json();
          setDiagnostics(data);
        }
      } catch (err) {
        console.error('Failed to fetch diagnostics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDiagnostics();
    const interval = setInterval(fetchDiagnostics, 5000);
    return () => clearInterval(interval);
  }, []);

  const serviceCols: ColumnDef<ServiceRow>[] = [
    { header: 'SUBSYSTEM', accessorKey: 'service' },
    { header: 'VERSION', accessorKey: 'version', cell: (row) => <span className="font-data-mono">{row.version}</span> },
    { 
      header: 'STATUS', 
      accessorKey: 'status', 
      cell: (row) => (
        <span className={cn(
          'px-2 py-0.5 rounded-sm text-xs font-bold',
          row.status === 'ONLINE' ? 'bg-[#10b981]/10 text-[#10b981]' : 
          row.status === 'OFFLINE' ? 'bg-error/10 text-error' :
          'bg-[#f59e0b]/10 text-[#f59e0b]'
        )}>
          {row.status}
        </span>
      )
    }
  ];

  const serviceData: ServiceRow[] = diagnostics ? Object.entries(diagnostics.engines).map(([key, val]) => ({
    id: key,
    service: key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
    version: val.version || val.type || '-',
    status: val.status
  })) : [];

  const formatUptime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return `${h}h ${m}m ${s}s`;
  };

  return (
    <>
      <Header
        title="System Diagnostics (SIT)"
        subtitle="Phase 11.5 • System Integration Test • Verification"
        actions={
          <div className="flex gap-4">
            <div className="bg-surface-container-lowest border border-outline-variant px-3 py-1.5 rounded-DEFAULT text-xs font-data-mono text-on-surface">ENV: INTEGRATION</div>
            <div className={cn("border px-3 py-1.5 rounded-DEFAULT text-xs font-data-mono", diagnostics?.overall_status === 'HEALTHY' ? 'bg-[#10b981]/10 border-[#10b981] text-[#10b981]' : 'bg-error/10 border-error text-error')}>
              {diagnostics?.overall_status || 'UNKNOWN'}
            </div>
          </div>
        }
        className="mb-section-gap border-b border-outline-variant pb-6"
      />
      
      <div className="grid grid-cols-12 gap-gutter">
        <div className="col-span-12 grid grid-cols-2 md:grid-cols-6 gap-gutter mb-6">
          <BaseCard variant="plain" className="p-5 shadow-sm hover:border-primary-container transition-colors">
            <div className="text-on-surface-variant font-label-caps text-label-caps mb-2">CPU</div>
            <div className="font-numeric-telemetry text-3xl text-on-surface">{diagnostics?.hardware.cpu_percent || 0}<span className="text-base text-on-surface-variant ml-1">%</span></div>
          </BaseCard>

          <BaseCard variant="plain" className="p-5 shadow-sm hover:border-primary-container transition-colors">
            <div className="text-on-surface-variant font-label-caps text-label-caps mb-2">MEMORY</div>
            <div className="font-numeric-telemetry text-3xl text-on-surface">{diagnostics?.hardware.memory_percent || 0}<span className="text-base text-on-surface-variant ml-1">%</span></div>
          </BaseCard>

          <BaseCard variant="plain" className="p-5 shadow-sm hover:border-primary-container transition-colors">
            <div className="text-on-surface-variant font-label-caps text-label-caps mb-2">GPU</div>
            <div className="font-numeric-telemetry text-3xl text-on-surface">{diagnostics?.hardware.gpu_percent || 0}<span className="text-base text-on-surface-variant ml-1">%</span></div>
          </BaseCard>

          <BaseCard variant="plain" className="p-5 shadow-sm hover:border-primary-container transition-colors">
            <div className="text-on-surface-variant font-label-caps text-label-caps mb-2">API LATENCY</div>
            <div className="font-numeric-telemetry text-3xl text-on-surface">{diagnostics?.hardware.network_latency_ms || 0}<span className="text-base text-on-surface-variant ml-1">ms</span></div>
          </BaseCard>

          <BaseCard variant="plain" className="p-5 shadow-sm hover:border-primary-container transition-colors">
            <div className="text-on-surface-variant font-label-caps text-label-caps mb-2">UPTIME</div>
            <div className="font-numeric-telemetry text-xl text-on-surface mt-2">{diagnostics ? formatUptime(diagnostics.hardware.process_uptime_sec) : '0h 0m 0s'}</div>
          </BaseCard>

          <BaseCard variant="plain" className="p-5 shadow-sm hover:border-primary-container transition-colors">
            <div className="text-on-surface-variant font-label-caps text-label-caps mb-2">WS CLIENTS</div>
            <div className="font-numeric-telemetry text-3xl text-on-surface">{diagnostics?.engines.streaming_engine?.connections || 0}</div>
          </BaseCard>
        </div>
        
        <section className="col-span-12 xl:col-span-8">
          <EnterpriseTable
            title="SUBSYSTEM HEALTH MATRIX"
            data={serviceData}
            columns={serviceCols}
            actions={<span className="font-data-mono text-xs text-on-surface-variant">POLLING: 5s</span>}
            className="shadow-sm border border-outline-variant"
          />
        </section>
        
        <section className="col-span-12 xl:col-span-4">
          <BaseCard variant="plain" className="bg-inverse-surface rounded-[18px] card-shadow overflow-hidden h-[300px] flex flex-col border border-inverse-surface !p-0">
            <div className="px-4 py-3 border-b border-tertiary flex justify-between items-center bg-[#1e2326]">
              <h2 className="font-label-caps text-label-caps text-on-secondary">DIAGNOSTIC LOGS</h2>
              <div className="flex gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-error"></span>
                <span className="w-2.5 h-2.5 rounded-full bg-[#f59e0b]"></span>
                <span className="w-2.5 h-2.5 rounded-full bg-[#10b981]"></span>
              </div>
            </div>
            <div className="p-4 overflow-y-auto font-data-mono text-xs text-on-tertiary-fixed-variant leading-relaxed flex-1 space-y-1">
              {loading ? <div>Loading...</div> : (
                <>
                  <div><span className="text-[#10b981]">[INFO]</span> Phase 11.5 SIT Active.</div>
                  <div><span className="text-[#10b981]">[INFO]</span> Polling /api/system/diagnostics.</div>
                  {diagnostics && Object.values(diagnostics.engines).some(e => e.status === 'OFFLINE') && (
                    <div><span className="text-error">[ERROR]</span> One or more subsystems offline.</div>
                  )}
                  {diagnostics && Object.entries(diagnostics.engines).map(([key, val]) => (
                    val.status === 'ONLINE' && <div key={key}><span className="text-[#10b981]">[OK]</span> {key} loaded successfully.</div>
                  ))}
                  <div><span className="text-on-primary-fixed-variant blink">_</span></div>
                </>
              )}
            </div>
          </BaseCard>
        </section>
      </div>
    </>
  );
};

export const AdminPage: FC = () => (
  <PageLayout className="p-0" data-layout="precision">
    <div className="p-6">
      <AdminPageContent />
    </div>
  </PageLayout>
);

export default AdminPage;
