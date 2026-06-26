import React, { useState, useEffect } from 'react';
import { PageLayout, BaseCard, Icon, EnterpriseTable, MetricCard, BaseBadge } from '@design-system/index';

const MOCK_SENSORS = [
  { id: '1', name: 'SoLEXS SDD1', status: 'ONLINE', latency: 45, packetLoss: 0.01, noise: 0.002, lastUpdate: Date.now() },
  { id: '2', name: 'SoLEXS SDD2', status: 'ONLINE', latency: 42, packetLoss: 0.00, noise: 0.001, lastUpdate: Date.now() },
  { id: '3', name: 'HEL1OS CZT', status: 'DEGRADED', latency: 120, packetLoss: 0.5, noise: 0.015, lastUpdate: Date.now() - 5000 },
  { id: '4', name: 'HEL1OS CdTe', status: 'ONLINE', latency: 60, packetLoss: 0.05, noise: 0.005, lastUpdate: Date.now() },
  { id: '5', name: 'SUIT', status: 'OFFLINE', latency: -1, packetLoss: 100, noise: 0, lastUpdate: Date.now() - 3600000 },
];

export const SensorInspectorPage: React.FC = () => {
  const [sensors, setSensors] = useState(MOCK_SENSORS);

  useEffect(() => {
    const interval = setInterval(() => {
      setSensors(prev => prev.map(s => {
        if (s.status === 'OFFLINE') return s;
        return {
          ...s,
          latency: s.latency + (Math.random() * 10 - 5),
          lastUpdate: Date.now()
        };
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const columns = [
    { header: 'Sensor ID', accessorKey: 'name', cell: (row: any) => row.name },
    { 
      header: 'Status', 
      accessorKey: 'status', 
      cell: (row: any) => (
        <BaseBadge 
          label={row.status} 
          variant={row.status === 'ONLINE' ? 'success' : row.status === 'DEGRADED' ? 'warning' : 'critical'} 
        />
      )
    },
    { header: 'Latency (ms)', accessorKey: 'latency', cell: (row: any) => row.latency > 0 ? row.latency.toFixed(1) : 'N/A' },
    { header: 'Packet Loss (%)', accessorKey: 'packetLoss', cell: (row: any) => row.packetLoss.toFixed(2) },
    { header: 'Noise Level', accessorKey: 'noise', cell: (row: any) => row.noise.toFixed(4) },
    { header: 'Last Update', accessorKey: 'lastUpdate', cell: (row: any) => new Date(row.lastUpdate).toLocaleTimeString() },
  ];

  return (
    <PageLayout className="p-gutter space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-headline-lg text-on-surface flex items-center gap-3">
            <Icon name="troubleshoot" className="text-primary" />
            Sensor Inspector
          </h1>
          <p className="text-on-surface-variant font-body-md mt-1">Granular diagnostic views of all payloads and sub-instruments.</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6 mb-6">
        <div className="col-span-3"><MetricCard title="Total Sensors" value="5" status="primary" /></div>
        <div className="col-span-3"><MetricCard title="Online Sensors" value="3" status="success" /></div>
        <div className="col-span-3"><MetricCard title="Avg Latency" value="67 ms" status="warning" /></div>
        <div className="col-span-3"><MetricCard title="Packet Loss" value="0.11%" status="success" /></div>
      </div>

      <BaseCard className="overflow-hidden">
        <EnterpriseTable columns={columns} data={sensors} />
      </BaseCard>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-12">
           <BaseCard title="Detailed Telemetry Diagnostics" variant="elevated">
              <p className="text-on-surface-variant mb-4">Select a sensor above to view high-resolution raw data streams and health diagnostics.</p>
              <div className="h-[200px] bg-surface-highlight border border-outline rounded-md flex items-center justify-center">
                 <span className="text-on-surface-variant font-body-sm">Awaiting sensor selection...</span>
              </div>
           </BaseCard>
        </div>
      </div>
    </PageLayout>
  );
};

export default SensorInspectorPage;
