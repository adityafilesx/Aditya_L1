import React, { useState } from 'react';
import { PageLayout, BaseCard, Icon, ActionButton } from '@design-system/index';

export const ConfigurationPage: React.FC = () => {
  const [config, setConfig] = useState({
    environment: 'production',
    streamRate: '1000',
    modelConfidenceThreshold: '0.85',
    enableAI: true,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setConfig(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  return (
    <PageLayout className="p-gutter space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-headline-lg text-on-surface flex items-center gap-3">
            <Icon name="settings" className="text-primary" />
            System Configuration
          </h1>
          <p className="text-on-surface-variant font-body-md mt-1">Manage global platform settings and thresholds.</p>
        </div>
        <div className="flex gap-3">
          <ActionButton icon="save" title="Save Changes" onClick={() => {}} />
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-6 space-y-6">
          <BaseCard title="Environment Settings" variant="panel">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-label-md text-on-surface-variant mb-1">Environment</label>
                <select 
                  name="environment" 
                  value={config.environment} 
                  onChange={handleChange}
                  className="w-full bg-surface border border-outline rounded-md p-2 text-on-surface"
                >
                  <option value="development">Development</option>
                  <option value="staging">Staging</option>
                  <option value="production">Production</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-label-md text-on-surface-variant mb-1">Stream Rate (ms)</label>
                <input 
                  type="number" 
                  name="streamRate" 
                  value={config.streamRate} 
                  onChange={handleChange}
                  className="w-full bg-surface border border-outline rounded-md p-2 text-on-surface"
                />
              </div>
            </div>
          </BaseCard>
        </div>

        <div className="col-span-6 space-y-6">
          <BaseCard title="AI & Models" variant="panel">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-label-md text-on-surface-variant mb-1">Confidence Threshold</label>
                <input 
                  type="number" 
                  step="0.01"
                  name="modelConfidenceThreshold" 
                  value={config.modelConfidenceThreshold} 
                  onChange={handleChange}
                  className="w-full bg-surface border border-outline rounded-md p-2 text-on-surface"
                />
              </div>
              <div className="flex items-center gap-2">
                <input 
                  type="checkbox" 
                  name="enableAI" 
                  checked={config.enableAI} 
                  onChange={handleChange}
                  className="w-4 h-4"
                />
                <label className="text-sm font-label-md text-on-surface">Enable AI Scientist Autonomy</label>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </PageLayout>
  );
};

export default ConfigurationPage;
