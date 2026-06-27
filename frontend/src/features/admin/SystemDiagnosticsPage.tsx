import React, { useEffect, useState } from 'react';
import { PageLayout, Header, BaseCard, EnterpriseTable } from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

export const SystemDiagnosticsPage: React.FC = () => {
  const connectionStatus = useStreamStore(state => state.connectionStatus);
  const missionState = useStreamStore(state => state.mission);
  
  const [metrics, setMetrics] = useState({
    packetRate: 0,
    droppedMessages: 0,
    reconnectCount: 0,
    latency: Math.floor(Math.random() * 20) + 10,
  });

  useEffect(() => {
    // Simulate real-time metrics for diagnostics that aren't provided directly by the backend yet
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        packetRate: connectionStatus === 'connected' ? Math.floor(Math.random() * 50) + 200 : 0,
        latency: connectionStatus === 'connected' ? Math.floor(Math.random() * 20) + 10 : 0,
      }));
    }, 1000);
    return () => clearInterval(interval);
  }, [connectionStatus]);

  const subsystems = [
    { id: '1', name: 'WebSocket Link', status: connectionStatus === 'connected' ? 'ONLINE' : 'OFFLINE' },
    { id: '2', name: 'API Server', status: connectionStatus === 'connected' ? 'ONLINE' : 'DEGRADED' },
    { id: '3', name: 'Telemetry Engine', status: missionState?.telemetry ? 'ONLINE' : 'WAITING' },
    { id: '4', name: 'Physics Engine', status: missionState?.physics ? 'ONLINE' : 'WAITING' },
    { id: '5', name: 'Digital Twin', status: missionState?.digital_twin ? 'ONLINE' : 'WAITING' },
    { id: '6', name: 'Forecast Engine', status: missionState?.forecast ? 'ONLINE' : 'WAITING' },
    { id: '7', name: 'Knowledge Graph', status: 'ONLINE' }, // Placeholder for graph DB connection
    { id: '8', name: 'AI Reasoning', status: missionState?.recommendations ? 'ONLINE' : 'WAITING' },
  ];

  return (
    <PageLayout className="p-gutter">
      <Header
        title="System Diagnostics"
        subtitle="Developer Integration Monitor & Subsystem Health"
        actions={
          <div className="flex items-center gap-2 px-3 py-1 bg-surface-container-low rounded border border-outline-variant">
             <span className={`w-2 h-2 rounded-full ${connectionStatus === 'connected' ? 'bg-success' : 'bg-critical'}`}></span>
             <span className="font-label-caps text-label-caps text-on-surface uppercase">
               STREAM: {connectionStatus}
             </span>
          </div>
        }
      />

      <div className="grid grid-cols-1 md:grid-cols-4 gap-gutter mb-gutter">
         <BaseCard variant="plain" size="md">
           <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">Latency</span>
           <div className="font-numeric-telemetry text-2xl font-bold text-success">{metrics.latency}ms</div>
         </BaseCard>
         <BaseCard variant="plain" size="md">
           <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">Packet Rate</span>
           <div className="font-numeric-telemetry text-2xl font-bold text-primary">{metrics.packetRate} /s</div>
         </BaseCard>
         <BaseCard variant="plain" size="md">
           <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">Reconnects</span>
           <div className="font-numeric-telemetry text-2xl font-bold text-warning">{metrics.reconnectCount}</div>
         </BaseCard>
         <BaseCard variant="plain" size="md">
           <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">Dropped Pkgs</span>
           <div className="font-numeric-telemetry text-2xl font-bold text-success">{metrics.droppedMessages}</div>
         </BaseCard>
      </div>

      <div className="grid grid-cols-1 gap-gutter">
        <EnterpriseTable 
          title="SUBSYSTEM HEALTH MATRIX"
          data={subsystems}
          columns={[
            { header: 'Subsystem', accessorKey: 'name' },
            { 
              header: 'Status', 
              accessorKey: 'status',
              cell: (row) => (
                <span className={`px-2 py-1 rounded text-[10px] font-bold ${
                  row.status === 'ONLINE' ? 'bg-success/10 text-success' : 
                  row.status === 'WAITING' ? 'bg-warning/10 text-warning' : 
                  'bg-critical/10 text-critical'
                }`}>
                  {row.status}
                </span>
              )
            }
          ]}
        />
      </div>
    </PageLayout>
  );
};

export default SystemDiagnosticsPage;
