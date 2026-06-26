import React from 'react';
import { PageLayout, BaseCard, Icon, EnterpriseTable, BaseBadge, ActionButton } from '@design-system/index';

const MOCK_REGIONS = [
  { id: 'AR3451', coords: 'N15W42', class: 'Beta-Gamma-Delta', prob: 0.85, history: 'Growing' },
  { id: 'AR3452', coords: 'S22E10', class: 'Alpha', prob: 0.05, history: 'Stable' },
  { id: 'AR3453', coords: 'N05E88', class: 'Beta', prob: 0.22, history: 'Rotating in' },
  { id: 'AR3454', coords: 'S10W80', class: 'Beta-Gamma', prob: 0.45, history: 'Decaying' },
];

export const ActiveRegionsPage: React.FC = () => {
  const columns = [
    { header: 'Region ID', accessorKey: 'id', cell: (row: any) => <span className="font-bold text-primary">{row.id}</span> },
    { header: 'Coordinates', accessorKey: 'coords', cell: (row: any) => row.coords },
    { header: 'Hale Class', accessorKey: 'class', cell: (row: any) => row.class },
    { 
      header: 'Flare Prob.', 
      accessorKey: 'prob', 
      cell: (row: any) => (
        <span className={row.prob > 0.5 ? 'text-critical font-bold' : ''}>
          {(row.prob * 100).toFixed(0)}%
        </span>
      ) 
    },
    { header: 'History', accessorKey: 'history', cell: (row: any) => row.history },
    { 
      header: 'Actions', 
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
            <Icon name="emergency_recording" className="text-primary" />
            Active Regions Tracker
          </h1>
          <p className="text-on-surface-variant font-body-md mt-1">Digital twin simulation and tracking for solar active regions (ARs).</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-8">
           <BaseCard className="overflow-hidden">
             <EnterpriseTable columns={columns} data={MOCK_REGIONS} />
           </BaseCard>
        </div>
        <div className="col-span-4 space-y-6">
           <BaseCard title="AR3451 Detail" variant="elevated">
             <div className="space-y-4">
               <div className="flex justify-between items-center">
                 <span className="text-on-surface-variant font-label-md">Area (MH)</span>
                 <span className="text-on-surface font-body-md">1250</span>
               </div>
               <div className="flex justify-between items-center">
                 <span className="text-on-surface-variant font-label-md">Magnetic Flux</span>
                 <span className="text-on-surface font-body-md">4.2e22 Mx</span>
               </div>
               <div className="flex justify-between items-center">
                 <span className="text-on-surface-variant font-label-md">Zürich Class</span>
                 <span className="text-on-surface font-body-md">Fkc</span>
               </div>
               
               <div className="h-[150px] bg-surface border border-outline rounded-md flex items-center justify-center mt-4">
                 <Icon name="image" className="text-4xl text-on-surface-variant opacity-50" />
                 <span className="ml-2 text-on-surface-variant">HMI Magnetogram</span>
               </div>
               
               <button className="w-full bg-primary text-on-primary py-2 rounded-md hover:bg-primary-hover transition-colors font-label-md mt-4">
                 Run AI Forecast on Region
               </button>
             </div>
           </BaseCard>
        </div>
      </div>
    </PageLayout>
  );
};

export default ActiveRegionsPage;
