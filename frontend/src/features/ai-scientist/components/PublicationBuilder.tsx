import React from 'react';
import { BaseCard, Icon } from '@design-system/index';

export const PublicationBuilder: React.FC = () => {
  return (
    <div className="absolute inset-0 overflow-y-auto p-8 bg-surface-container-lowest">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-display-md text-[24px] font-bold text-on-surface">Scientific Publication Builder</h1>
            <p className="font-body-lg text-on-surface-variant mt-2">
              Generate markdown reports, PDF manuscripts, and LaTeX exports from active research sessions.
            </p>
          </div>
          <button className="px-4 py-2 bg-[#10b981] text-white rounded-lg font-label-caps uppercase text-[12px] font-bold shadow-sm hover:shadow transition-all border-none cursor-pointer flex items-center gap-2">
            <Icon name="download" /> Export LaTeX
          </button>
        </div>

        <div className="flex gap-6">
          <div className="w-64 flex flex-col gap-2">
            <div className="font-label-caps uppercase text-[11px] text-on-surface-variant font-bold mb-2">Sections</div>
            {['Abstract', 'Introduction', 'Mission Context', 'Physics Methodology', 'Results (Spectra)', 'Discussion', 'References'].map((section, idx) => (
              <div key={idx} className={`px-3 py-2 rounded-lg cursor-pointer font-body-sm flex items-center justify-between ${
                idx === 4 ? 'bg-primary/10 text-primary font-bold' : 'hover:bg-surface-container text-on-surface'
              }`}>
                {section}
                {idx === 4 && <Icon name="edit" className="text-[14px]" />}
              </div>
            ))}
          </div>

          <BaseCard variant="plain" className="flex-1 shadow-sm min-h-[500px] p-6">
            <div className="font-data-mono text-[12px] text-on-surface-variant/50 float-right">Results (Spectra)</div>
            <div className="prose prose-sm max-w-none mt-4">
              <h2 className="text-on-surface font-display-sm text-[20px] font-bold border-b border-surface-variant pb-2 mb-4">Results: Spectral Fitting for AR13872</h2>
              <p className="text-on-surface-variant leading-relaxed mb-4">
                The SoLEXS spectral data indicates a pronounced hardening of the spectrum during the impulsive phase. The fitted thermal component yields a peak temperature of <span className="font-data-mono bg-surface-container px-1 py-0.5 rounded">14.2 MK</span>, consistent with the expected emission measure derived from GOES cross-calibration.
              </p>
              
              <div className="my-6 p-4 border border-dashed border-outline-variant rounded-lg bg-surface flex flex-col items-center justify-center text-on-surface-variant/60">
                <Icon name="image" className="text-[32px] mb-2" />
                <div className="font-label-caps text-[10px] uppercase">Figure 3: Thermal vs Non-thermal Fit</div>
              </div>

              <p className="text-on-surface-variant leading-relaxed">
                As seen in Figure 3, the non-thermal bremsstrahlung component dominates energies &gt;15 keV, modeled utilizing a thick-target approach ($F \propto E^&#123;-\delta&#125;$). The spectral index $\delta$ was calculated at 3.8.
              </p>
            </div>
          </BaseCard>
        </div>
      </div>
    </div>
  );
};
