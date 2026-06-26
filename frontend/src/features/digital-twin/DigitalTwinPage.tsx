import type { FC } from 'react';
import { cn } from '@utils/cn';
import { 
  PageLayout, 
  BaseCard, 
  BaseBadge, 
  Slider,
  Icon,
  MissionTimeline
} from '@design-system/index';
import { TwinCanvas } from './components/TwinCanvas';
import { Leva, useControls } from 'leva';
import { useWorkspaceStore } from '../../realtime/workspaceStore';

export const DigitalTwinPageContent: FC = () => {
  const setLayer = useWorkspaceStore(state => state.setDigitalTwinLayer);

  // Leva controls linked to our zustand store for layer opacities
  useControls({
    Photosphere: { value: 100, min: 0, max: 100, onChange: (v) => setLayer('photosphereOpacity', v) },
    Corona: { value: 80, min: 0, max: 100, onChange: (v) => setLayer('coronaOpacity', v) },
    MagneticGrid: { value: 30, min: 0, max: 100, onChange: (v) => setLayer('magneticOpacity', v) }
  });

  return (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-gutter h-full relative">
    <div className="absolute top-20 right-4 z-50">
      <Leva theme={{ colors: { highlight1: '#4140d1', highlight2: '#4140d1', elevation1: '#111318', elevation2: '#1b1d22', elevation3: '#26282e' } }} fill={false} flat />
    </div>
    {/* Left Column (Solar Overlays & Active Regions) */}
    <div className="col-span-1 md:col-span-3 flex flex-col gap-gutter h-full overflow-y-auto">
      
      <BaseCard variant="plain" size="sm" className="shadow-sm" title="SOLAR OVERLAYS" icon="layers">
        <div className="flex flex-col gap-3 mt-4">
          <label className="flex items-center justify-between cursor-pointer group">
            <span className="font-body-sm text-on-surface-variant group-hover:text-primary transition-colors">Photosphere (Visible)</span>
            <div className="relative w-10 h-5 bg-surface-container-highest rounded-full border border-outline-variant">
              <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-primary rounded-full transition-transform translate-x-5"></div>
            </div>
          </label>
          <label className="flex items-center justify-between cursor-pointer group">
            <span className="font-body-sm text-on-surface-variant group-hover:text-primary transition-colors">Chromosphere (H-Alpha)</span>
            <div className="relative w-10 h-5 bg-surface-container-highest rounded-full border border-outline-variant">
              <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-outline rounded-full transition-transform"></div>
            </div>
          </label>
          <label className="flex items-center justify-between cursor-pointer group">
            <span className="font-body-sm text-on-surface-variant group-hover:text-primary transition-colors">Corona (EUV 193Å)</span>
            <div className="relative w-10 h-5 bg-surface-container-highest rounded-full border border-outline-variant">
              <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-primary rounded-full transition-transform translate-x-5"></div>
            </div>
          </label>
          <label className="flex items-center justify-between cursor-pointer group">
            <span className="font-body-sm text-on-surface-variant group-hover:text-primary transition-colors">Magnetic Field Lines</span>
            <div className="relative w-10 h-5 bg-surface-container-highest rounded-full border border-outline-variant">
              <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-primary rounded-full transition-transform translate-x-5"></div>
            </div>
          </label>
          <div className="mt-2 pt-3 border-t border-surface-container-high">
            <Slider label="Opacity" min={0} max={100} value={85} onChange={() => {}} />
          </div>
        </div>
      </BaseCard>
      
      <BaseCard variant="plain" size="sm" className="shadow-sm flex-1 flex flex-col" title="ACTIVE REGIONS" badge={
        <span className="flex items-center justify-center w-5 h-5 bg-primary-container text-primary rounded-full text-[10px] font-bold">4</span>
      }>
        <div className="flex flex-col gap-2 overflow-y-auto pr-1 mt-4">
          <div className="p-3 rounded-lg border border-primary bg-primary-fixed-dim/10 cursor-pointer">
            <div className="flex justify-between items-start mb-1">
              <span className="font-numeric-telemetry text-numeric-telemetry text-primary font-bold">AR13872</span>
              <BaseBadge variant="critical">High Risk</BaseBadge>
            </div>
            <div className="flex justify-between font-body-sm text-on-surface-variant text-[12px]">
              <span>Complexity: β-γ-δ</span>
              <span>Flare Prob: 85%</span>
            </div>
          </div>
          
          <div className="p-3 rounded-lg border border-outline-variant hover:border-primary/50 bg-surface transition-colors cursor-pointer">
            <div className="flex justify-between items-start mb-1">
              <span className="font-numeric-telemetry text-numeric-telemetry text-on-surface font-bold">AR13873</span>
              <BaseBadge variant="warning">Mod Risk</BaseBadge>
            </div>
            <div className="flex justify-between font-body-sm text-on-surface-variant text-[12px]">
              <span>Complexity: β-γ</span>
              <span>Flare Prob: 42%</span>
            </div>
          </div>
          
          <div className="p-3 rounded-lg border border-outline-variant hover:border-primary/50 bg-surface transition-colors cursor-pointer">
            <div className="flex justify-between items-start mb-1">
              <span className="font-numeric-telemetry text-numeric-telemetry text-on-surface font-bold">AR13874</span>
              <BaseBadge variant="offline">Low Risk</BaseBadge>
            </div>
            <div className="flex justify-between font-body-sm text-on-surface-variant text-[12px]">
              <span>Complexity: α</span>
              <span>Flare Prob: 5%</span>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>
    
    {/* Center Column (3D Viewer) */}
    <div className="col-span-1 md:col-span-6 flex flex-col h-full bg-surface-container-lowest rounded-2xl border border-outline-variant shadow-sm overflow-hidden relative">
      <div className="absolute top-0 left-0 w-full p-6 z-10 glass-panel border-x-0 border-t-0 rounded-t-2xl flex justify-between items-center">
        <div>
          <h2 className="font-headline-md text-headline-md text-on-surface mb-1">Digital Twin Viewer</h2>
          <p className="font-body-sm text-on-surface-variant">Real-Time Virtual Solar Environment • Synthesis 99.8%</p>
        </div>
        <div className="flex gap-2">
          <button className="w-10 h-10 rounded border border-outline-variant bg-surface flex items-center justify-center text-on-surface-variant hover:text-primary hover:border-primary transition-colors cursor-pointer"><Icon name="zoom_in" /></button>
          <button className="w-10 h-10 rounded border border-outline-variant bg-surface flex items-center justify-center text-on-surface-variant hover:text-primary hover:border-primary transition-colors cursor-pointer"><Icon name="360" /></button>
          <button className="w-10 h-10 rounded border border-outline-variant bg-surface flex items-center justify-center text-on-surface-variant hover:text-primary hover:border-primary transition-colors cursor-pointer"><Icon name="fullscreen" /></button>
        </div>
      </div>
      
      <div className="flex-1 w-full relative bg-surface-container-highest">
        <TwinCanvas />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none opacity-10 z-10">
          <Icon name="add" className="text-[64px] text-primary" />
        </div>
      </div>
      
      <div className="absolute bottom-0 left-0 w-full p-4 z-10 glass-panel border-x-0 border-b-0 rounded-b-2xl">
        <MissionTimeline />
      </div>
    </div>
    
    {/* Right Column (System State, Physics Metrics, Event Matching) */}
    <div className="col-span-1 md:col-span-3 flex flex-col gap-gutter h-full overflow-y-auto">
      
      <BaseCard variant="plain" size="sm" className="shadow-sm" title="SYSTEM STATE" status="nominal">
        <div className="grid grid-cols-2 gap-2 mb-4 mt-2">
          <div className="p-2 border border-outline-variant rounded bg-surface">
            <p className="text-[10px] text-outline uppercase mb-1">Status</p>
            <p className="font-data-mono text-data-mono text-primary font-bold">TRACKING</p>
          </div>
          <div className="p-2 border border-outline-variant rounded bg-surface">
            <p className="text-[10px] text-outline uppercase mb-1">Sync Ratio</p>
            <p className="font-data-mono text-data-mono text-on-surface font-bold">99.8%</p>
          </div>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex justify-between font-body-sm">
            <span className="text-on-surface-variant">Data Latency</span>
            <span className="font-data-mono text-primary">12ms</span>
          </div>
          <div className="flex justify-between font-body-sm">
            <span className="text-on-surface-variant">Mesh Density</span>
            <span className="font-data-mono text-on-surface">Ultra (8M Poly)</span>
          </div>
        </div>
      </BaseCard>
      
      <BaseCard variant="plain" size="sm" className="shadow-sm" title="PHYSICS METRICS" icon="analytics">
        <div className="flex flex-col gap-3 mt-2">
          <div className="relative p-3 border border-outline-variant rounded-lg bg-surface flex flex-col gap-1">
            <div className="flex justify-between items-center">
              <span className="font-body-sm text-on-surface-variant">Coronal Temp</span>
              <span className="font-numeric-telemetry text-secondary font-bold">1.2M K</span>
            </div>
            <div className="w-full h-1 bg-surface-container-high rounded-full overflow-hidden mt-1">
              <div className="h-full bg-secondary w-[75%]"></div>
            </div>
          </div>
          <div className="relative p-3 border border-outline-variant rounded-lg bg-surface flex flex-col gap-1">
            <div className="flex justify-between items-center">
              <span className="font-body-sm text-on-surface-variant">X-Ray Flux</span>
              <span className="font-numeric-telemetry text-primary font-bold">M2.4</span>
            </div>
            <div className="w-full h-1 bg-surface-container-high rounded-full overflow-hidden mt-1">
              <div className="h-full bg-primary w-[45%]"></div>
            </div>
          </div>
          <div className="relative p-3 border border-outline-variant rounded-lg bg-surface flex flex-col gap-1">
            <div className="flex justify-between items-center">
              <span className="font-body-sm text-on-surface-variant">Solar Wind</span>
              <span className="font-numeric-telemetry text-on-surface font-bold">420 km/s</span>
            </div>
            <div className="w-full h-1 bg-surface-container-high rounded-full overflow-hidden mt-1">
              <div className="h-full bg-outline w-[30%]"></div>
            </div>
          </div>
        </div>
      </BaseCard>
      
      <BaseCard variant="plain" size="sm" className="shadow-sm flex-1" title="EVENT MATCHING" icon="compare_arrows">
        <p className="font-body-sm text-on-surface-variant mb-3 leading-relaxed mt-2">Comparing current AR topology against historical flare profiles.</p>
        <div className="flex flex-col gap-2">
          {[
            { tag: 'X2.2 (2017)', val: '89%', color: 'bg-secondary' },
            { tag: 'M9.1 (2021)', val: '76%', color: 'bg-primary' },
            { tag: 'X1.1 (2023)', val: '62%', color: 'bg-outline' },
          ].map((hist, idx) => (
            <div key={idx} className="flex items-center justify-between p-2 rounded hover:bg-surface-container-low transition-colors cursor-pointer border border-transparent hover:border-outline-variant">
              <div className="flex items-center gap-2">
                <div className={cn('w-2 h-2 rounded-full', hist.color)}></div>
                <span className="font-data-mono text-[12px] text-on-surface">{hist.tag}</span>
              </div>
              <span className="font-numeric-telemetry text-[14px] text-primary">{hist.val}</span>
            </div>
          ))}
        </div>
        <button className="mt-4 w-full text-center py-2 text-[12px] text-primary font-bold border border-primary rounded hover:bg-primary-container hover:text-on-primary-container transition-colors bg-transparent cursor-pointer">
          VIEW FULL MATRIX
        </button>
      </BaseCard>
    </div>
  </div>
  );
};

export const DigitalTwinPage: FC = () => (
  <PageLayout className="p-gutter">
    <DigitalTwinPageContent />
  </PageLayout>
);

export default DigitalTwinPage;
