import React, { useState } from 'react';
import { PageLayout, BaseCard, EnterpriseTable, Icon, ActionButton, BaseBadge } from '@design-system/index';

const MOCK_LOGS = [
  { id: '1', timestamp: new Date(Date.now() - 1000).toISOString(), level: 'INFO', source: 'MissionGenerator', message: 'Published telemetry to stream.' },
  { id: '2', timestamp: new Date(Date.now() - 5000).toISOString(), level: 'WARNING', source: 'WebSocket', message: 'Client reconnect threshold reached.' },
  { id: '3', timestamp: new Date(Date.now() - 15000).toISOString(), level: 'ERROR', source: 'AI_Engine', message: 'Failed to load ensemble weights. Retrying...' },
  { id: '4', timestamp: new Date(Date.now() - 25000).toISOString(), level: 'INFO', source: 'AuthService', message: 'User session verified.' },
  { id: '5', timestamp: new Date(Date.now() - 60000).toISOString(), level: 'INFO', source: 'API_Gateway', message: 'System boot sequence initiated.' },
];

export const LogsPage: React.FC = () => {
  const [filter, setFilter] = useState('ALL');

  const columns = [
    { header: 'Timestamp', accessorKey: 'timestamp', cell: (row: any) => new Date(row.timestamp).toLocaleTimeString() },
    { 
      header: 'Level', 
      accessorKey: 'level', 
      cell: (row: any) => (
        <BaseBadge 
          label={row.level} 
          variant={row.level === 'ERROR' ? 'critical' : row.level === 'WARNING' ? 'warning' : 'primary'} 
        />
      )
    },
    { header: 'Source', accessorKey: 'source', cell: (row: any) => row.source },
    { header: 'Message', accessorKey: 'message', cell: (row: any) => <span className="font-mono text-sm">{row.message}</span> },
  ];

  const filteredLogs = filter === 'ALL' ? MOCK_LOGS : MOCK_LOGS.filter(log => log.level === filter);

  return (
    <PageLayout className="p-gutter space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-headline-lg text-on-surface flex items-center gap-3">
            <Icon name="terminal" className="text-primary" />
            System Logs
          </h1>
          <p className="text-on-surface-variant font-body-md mt-1">Live streaming logs from backend services and frontend clients.</p>
        </div>
        <div className="flex gap-3">
          <ActionButton icon="download" label="Export Logs" onClick={() => {}} />
          <ActionButton icon="delete" label="Clear Console" variant="outline" onClick={() => {}} />
        </div>
      </div>

      <BaseCard className="flex gap-2 p-2">
        {['ALL', 'INFO', 'WARNING', 'ERROR'].map(level => (
          <button
            key={level}
            onClick={() => setFilter(level)}
            className={`px-4 py-2 rounded-md font-label-md transition-colors ${filter === level ? 'bg-primary text-on-primary' : 'bg-surface-variant text-on-surface-variant hover:bg-surface-highlight'}`}
          >
            {level}
          </button>
        ))}
      </BaseCard>

      <BaseCard className="overflow-hidden">
        <EnterpriseTable 
          columns={columns} 
          data={filteredLogs} 
        />
      </BaseCard>
    </PageLayout>
  );
};

export default LogsPage;
