import React, { useState } from 'react';
import { PageLayout, BaseCard, Icon, EnterpriseTable, BaseBadge, ActionButton } from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

export const AlertsPage: React.FC = () => {
  const alerts = useStreamStore(state => state.mission?.alerts) || [];
  const [filter, setFilter] = useState('ALL');

  const columns = [
    { header: 'ID', accessorKey: 'id', cell: (row: any) => <span className="font-bold text-on-surface">{row.id}</span> },
    { header: 'Time (UTC)', accessorKey: 'timestamp', cell: (row: any) => new Date(row.timestamp).toLocaleTimeString() },
    { 
      header: 'Severity', 
      accessorKey: 'severity', 
      cell: (row: any) => (
        <BaseBadge 
          label={row.severity} 
          variant={row.severity === 'CRITICAL' ? 'critical' : row.severity === 'WARNING' ? 'warning' : 'primary'} 
        />
      )
    },
    { header: 'Type', accessorKey: 'type', cell: (row: any) => row.type },
    { header: 'Description', accessorKey: 'description', cell: (row: any) => row.description },
    { 
      header: 'Actions', 
      accessorKey: 'actions', 
      cell: () => (
        <div className="flex gap-2">
          <ActionButton icon="check" label="Ack" variant="ghost" onClick={() => {}} />
          <ActionButton icon="info" label="Details" variant="ghost" onClick={() => {}} />
        </div>
      )
    },
  ];

  const filteredAlerts = filter === 'ALL' ? alerts : alerts.filter(a => a.severity === filter);

  return (
    <PageLayout className="p-gutter space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-headline-lg text-on-surface flex items-center gap-3">
            <Icon name="notifications_active" className="text-primary" />
            Alert Management
          </h1>
          <p className="text-on-surface-variant font-body-md mt-1">Real-time mission alert triage and history.</p>
        </div>
        <div className="flex gap-3">
          <ActionButton icon="done_all" label="Acknowledge All" onClick={() => {}} />
        </div>
      </div>

      <div className="flex gap-2">
        {['ALL', 'INFO', 'WARNING', 'CRITICAL'].map(level => (
          <button
            key={level}
            onClick={() => setFilter(level)}
            className={`px-4 py-2 rounded-md font-label-md transition-colors ${filter === level ? 'bg-primary text-on-primary' : 'bg-surface-variant text-on-surface-variant hover:bg-surface-highlight'}`}
          >
            {level}
          </button>
        ))}
      </div>

      <BaseCard className="overflow-hidden">
        <EnterpriseTable columns={columns} data={filteredAlerts} />
      </BaseCard>
    </PageLayout>
  );
};

export default AlertsPage;
