import React from 'react';
import { PageLayout, BaseCard, Icon, EnterpriseTable, SeverityBadge, ActionButton } from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

export const TimelinePage: React.FC = () => {
  const alerts = useStreamStore(state => state.mission?.alerts) || [];

  const columns = [
    { header: 'Time (UTC)', accessorKey: 'timestamp', cell: (row: any) => new Date(row.timestamp).toLocaleTimeString() },
    { header: 'Event Type', accessorKey: 'type', cell: (row: any) => row.type },
    { 
      header: 'Severity', 
      accessorKey: 'severity', 
      cell: (row: any) => <SeverityBadge status={row.severity}>{row.severity}</SeverityBadge>
    },
    { header: 'Description', accessorKey: 'description', cell: (row: any) => row.description },
    { 
      header: 'Sync', 
      accessorKey: 'actions', 
      cell: () => (
        <div className="flex gap-2">
          <ActionButton icon="view_in_ar" label="Twin" variant="ghost" onClick={() => {}} />
          <ActionButton icon="hub" label="Graph" variant="ghost" onClick={() => {}} />
          <ActionButton icon="science" label="AI" variant="ghost" onClick={() => {}} />
        </div>
      )
    },
  ];

  return (
    <PageLayout className="p-gutter space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-headline-lg text-on-surface flex items-center gap-3">
            <Icon name="view_timeline" className="text-primary" />
            Mission Event Timeline
          </h1>
          <p className="text-on-surface-variant font-body-md mt-1">Chronological event log with cross-engine synchronization.</p>
        </div>
        <div className="flex gap-3">
          <ActionButton icon="replay" label="Replay Events" variant="outline" onClick={() => {}} />
          <ActionButton icon="download" label="Export Timeline" onClick={() => {}} />
        </div>
      </div>

      <div className="flex gap-2 p-2 bg-surface-container rounded-md border border-outline-variant">
        <button className="px-4 py-2 bg-surface-variant text-on-surface-variant hover:bg-surface-highlight rounded font-label-md">Zoom In</button>
        <button className="px-4 py-2 bg-surface-variant text-on-surface-variant hover:bg-surface-highlight rounded font-label-md">Zoom Out</button>
        <button className="px-4 py-2 bg-surface-variant text-on-surface-variant hover:bg-surface-highlight rounded font-label-md">Pan Left</button>
        <button className="px-4 py-2 bg-surface-variant text-on-surface-variant hover:bg-surface-highlight rounded font-label-md">Pan Right</button>
        <div className="flex-1"></div>
        <button className="px-4 py-2 bg-primary text-on-primary rounded font-label-md">Jump to Latest</button>
      </div>

      <BaseCard className="overflow-hidden">
        <EnterpriseTable columns={columns} data={alerts} />
      </BaseCard>
    </PageLayout>
  );
};

export default TimelinePage;
