import React from 'react';
import { BaseCard, Icon, EnterpriseTable } from '@design-system/index';

export const ExperimentManager: React.FC = () => {
  return (
    <div className="absolute inset-0 overflow-y-auto p-8 bg-surface-container-lowest">
      <div className="max-w-5xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-display-md text-[24px] font-bold text-on-surface">Experiment Manager</h1>
            <p className="font-body-lg text-on-surface-variant mt-2">
              Track model comparisons, hyperparameter sweeps, and dataset versions.
            </p>
          </div>
          <button className="px-4 py-2 bg-primary text-white rounded-lg font-label-caps uppercase text-[12px] font-bold shadow-sm hover:shadow transition-all border-none cursor-pointer flex items-center gap-2">
            <Icon name="add" /> New Experiment
          </button>
        </div>

        <BaseCard variant="plain" className="shadow-sm p-0 overflow-hidden">
          <EnterpriseTable
            title="Recent Model Experiments"
            data={[
              { id: 'exp-1', name: 'XGBoost Baseline', dataset: 'v1.4.2', metric: '0.88 AUC', status: 'Completed' },
              { id: 'exp-2', name: 'TCN Spectral Fusion', dataset: 'v2.0.0-rc', metric: '0.91 AUC', status: 'Completed' },
              { id: 'exp-3', name: 'Transformer (Temporal)', dataset: 'v2.0.0', metric: 'Running (Epoch 12)', status: 'Active' },
            ]}
            columns={[
              { header: 'Experiment', accessorKey: 'name' },
              { header: 'Dataset', accessorKey: 'dataset' },
              { header: 'Key Metric', accessorKey: 'metric' },
              { 
                header: 'Status', 
                accessorKey: 'status',
                cell: (row) => (
                  <span className={`px-2 py-0.5 rounded text-[10px] font-label-caps uppercase ${
                    row.status === 'Completed' ? 'bg-[#10b981]/10 text-[#10b981]' : 'bg-primary/10 text-primary animate-pulse'
                  }`}>
                    {row.status}
                  </span>
                )
              }
            ]}
          />
        </BaseCard>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <BaseCard variant="plain" title="Hyperparameter Sweep (TCN)" icon="tune" className="shadow-sm">
            <div className="h-48 flex flex-col justify-center items-center text-on-surface-variant border border-dashed border-outline-variant mt-4 rounded-lg bg-surface-bright">
              <Icon name="scatter_plot" className="text-[48px] opacity-20 mb-2" />
              <div className="font-label-caps uppercase text-[12px] opacity-60">Parallel Coordinates Plot Placeholder</div>
            </div>
          </BaseCard>

          <BaseCard variant="plain" title="Dataset Version Lineage" icon="account_tree" className="shadow-sm">
            <div className="h-48 flex flex-col justify-center items-center text-on-surface-variant border border-dashed border-outline-variant mt-4 rounded-lg bg-surface-bright">
              <Icon name="schema" className="text-[48px] opacity-20 mb-2" />
              <div className="font-label-caps uppercase text-[12px] opacity-60">Dataset DAG Placeholder</div>
            </div>
          </BaseCard>
        </div>
      </div>
    </div>
  );
};
