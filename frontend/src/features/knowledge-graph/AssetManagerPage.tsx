import React, { useState } from 'react';
import { PageLayout, BaseCard, BaseBadge, Icon } from '@design-system/index';

// Mock list of spectral fitting images for the asset manager
const MOCK_ASSETS = [
  { id: 'SF-001', eventId: 'EV-X2.2', timestamp: '2026-06-25T18:00:00Z', region: 'AR13872', type: 'Hardness Ratio', url: '/api/assets/spectral_fitting_images/Hardness_Ratio_evolution.png' },
  { id: 'SF-002', eventId: 'EV-M9.1', timestamp: '2026-06-25T17:45:00Z', region: 'AR13873', type: 'Emission Measure', url: '/api/assets/spectral_fitting_images/Emission_Measure_norm_evolution.png' },
  { id: 'SF-003', eventId: 'EV-X2.2', timestamp: '2026-06-25T18:10:00Z', region: 'AR13872', type: 'Temperature', url: '/api/assets/spectral_fitting_images/dT_dt_evolution.png' },
  { id: 'SF-004', eventId: 'EV-M9.1', timestamp: '2026-06-25T17:50:00Z', region: 'AR13873', type: 'Spectral Index', url: '/api/assets/spectral_fitting_images/Spectral_Index_Gamma_evolution.png' },
];

export const AssetManagerPageContent: React.FC = () => {
  const [filter, setFilter] = useState('');
  
  const filteredAssets = MOCK_ASSETS.filter(a => a.eventId.includes(filter) || a.region.includes(filter) || a.type.toLowerCase().includes(filter.toLowerCase()));

  return (
    <div className="flex flex-col h-full gap-4">
      <div className="flex justify-between items-center glass-panel p-4 rounded-xl">
        <div>
          <h2 className="font-headline-md text-headline-md text-on-surface">Scientific Asset Manager</h2>
          <p className="font-body-sm text-on-surface-variant">Spectral Fitting & Evolution Imagery</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="relative">
            <Icon name="search" className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]" />
            <input 
              type="text" 
              placeholder="Search assets..." 
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="bg-surface-container-highest border border-outline-variant rounded-lg pl-10 pr-4 py-2 font-body-sm text-on-surface outline-none focus:border-primary transition-colors w-64"
            />
          </div>
          <button className="bg-surface-container-high px-4 py-2 rounded-lg font-label-caps text-[12px] font-bold text-on-surface border border-outline-variant hover:bg-surface-container transition-colors flex items-center gap-2">
            <Icon name="filter_list" className="text-[16px]" /> FILTER
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter flex-1 overflow-y-auto pb-8">
        {filteredAssets.map(asset => (
          <BaseCard key={asset.id} variant="plain" size="sm" className="overflow-hidden flex flex-col hover:border-primary/50 transition-colors group cursor-pointer">
            <div className="h-40 bg-surface-container-lowest w-full relative border-b border-outline-variant/30 flex items-center justify-center p-2">
              <div className="absolute top-2 right-2 flex gap-1">
                <button className="w-6 h-6 rounded bg-surface/80 backdrop-blur flex items-center justify-center border border-outline-variant opacity-0 group-hover:opacity-100 transition-opacity hover:text-primary"><Icon name="bookmark_border" className="text-[14px]" /></button>
                <button className="w-6 h-6 rounded bg-surface/80 backdrop-blur flex items-center justify-center border border-outline-variant opacity-0 group-hover:opacity-100 transition-opacity hover:text-primary"><Icon name="download" className="text-[14px]" /></button>
              </div>
              <div className="w-full h-full flex items-center justify-center text-on-surface-variant/30 border border-dashed border-outline-variant/50 rounded bg-surface-container-highest">
                <span className="font-label-caps text-[10px]">{asset.type} IMG</span>
              </div>
            </div>
            <div className="p-4 flex flex-col gap-2">
              <div className="flex justify-between items-start">
                <span className="font-numeric-telemetry text-primary font-bold">{asset.id}</span>
                <BaseBadge variant="nominal">{asset.region}</BaseBadge>
              </div>
              <div className="font-body-sm text-[12px] text-on-surface-variant">{asset.type}</div>
              <div className="mt-2 pt-2 border-t border-outline-variant/30 flex justify-between font-data-mono text-[10px] text-on-surface-variant/60">
                <span>{asset.eventId}</span>
                <span>{new Date(asset.timestamp).toLocaleTimeString()}</span>
              </div>
            </div>
          </BaseCard>
        ))}
      </div>
    </div>
  );
};

export const AssetManagerPage: React.FC = () => (
  <PageLayout className="p-gutter">
    <AssetManagerPageContent />
  </PageLayout>
);

export default AssetManagerPage;
