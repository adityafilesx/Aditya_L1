import React, { useState, useEffect } from 'react';
import { PageLayout, BaseCard, Icon, PlotlyContainer, MetricCard } from '@design-system/index';

export const SpectralAnalysisPage: React.FC = () => {
  const [data, setData] = useState<any>({ energy: [], flux: [], model: [], residuals: [] });

  useEffect(() => {
    // Generate mock spectral data
    const energy = Array.from({ length: 100 }, (_, i) => 1 + i * 0.5);
    const flux = energy.map(e => 100 * Math.exp(-e / 10) + Math.random() * 5);
    const model = energy.map(e => 100 * Math.exp(-e / 10));
    const residuals = flux.map((f, i) => f - model[i]);
    
    setData({ energy, flux, model, residuals });
  }, []);

  return (
    <PageLayout className="p-gutter space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-headline-lg text-on-surface flex items-center gap-3">
            <Icon name="science" className="text-primary" />
            Spectral Analysis
          </h1>
          <p className="text-on-surface-variant font-body-md mt-1">Interactive spectral fitting workstation for thermal and non-thermal emission characterization.</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6 mb-6">
        <div className="col-span-3"><MetricCard title="Thermal Temp (MK)" value="15.2" status="success" /></div>
        <div className="col-span-3"><MetricCard title="Emission Measure" value="2.4e48" status="success" /></div>
        <div className="col-span-3"><MetricCard title="Power Law Index" value="3.1" status="primary" /></div>
        <div className="col-span-3"><MetricCard title="Chi-Square" value="1.05" status="success" /></div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-8 space-y-6">
          <BaseCard title="Spectral Fit" variant="elevated" className="h-[400px]">
            <PlotlyContainer 
              data={[
                {
                  x: data.energy,
                  y: data.flux,
                  type: 'scatter',
                  mode: 'markers',
                  name: 'Observed Data',
                  marker: { color: '#8884d8' }
                },
                {
                  x: data.energy,
                  y: data.model,
                  type: 'scatter',
                  mode: 'lines',
                  name: 'Fitted Model',
                  line: { color: '#82ca9d' }
                }
              ]}
              layout={{
                xaxis: { title: 'Energy (keV)', type: 'log' },
                yaxis: { title: 'Flux (counts/s/keV)', type: 'log' },
                margin: { t: 20, b: 40, l: 60, r: 20 },
                showlegend: true
              }}
            />
          </BaseCard>

          <BaseCard title="Residuals" variant="glass" className="h-[250px]">
             <PlotlyContainer 
              data={[
                {
                  x: data.energy,
                  y: data.residuals,
                  type: 'bar',
                  name: 'Residuals',
                  marker: { color: '#ffc658' }
                }
              ]}
              layout={{
                xaxis: { title: 'Energy (keV)' },
                yaxis: { title: 'sigma' },
                margin: { t: 20, b: 40, l: 60, r: 20 },
                showlegend: false
              }}
            />
          </BaseCard>
        </div>

        <div className="col-span-4 space-y-6">
          <BaseCard title="Fit Parameters" variant="elevated">
             <div className="space-y-4">
               <div>
                 <label className="text-sm font-label-md text-on-surface-variant">Model Type</label>
                 <select className="w-full bg-surface border border-outline rounded-md p-2 mt-1">
                   <option>vth + pow</option>
                   <option>vth</option>
                   <option>1_vth + pow</option>
                 </select>
               </div>
               <div>
                 <label className="text-sm font-label-md text-on-surface-variant">Energy Range (keV)</label>
                 <div className="flex gap-2 mt-1">
                   <input type="number" defaultValue="3" className="w-1/2 bg-surface border border-outline rounded-md p-2" />
                   <input type="number" defaultValue="50" className="w-1/2 bg-surface border border-outline rounded-md p-2" />
                 </div>
               </div>
               <div>
                 <label className="text-sm font-label-md text-on-surface-variant">Background Subtraction</label>
                 <select className="w-full bg-surface border border-outline rounded-md p-2 mt-1">
                   <option>Pre-flare average</option>
                   <option>User defined</option>
                   <option>None</option>
                 </select>
               </div>
               <button className="w-full bg-primary text-on-primary py-2 rounded-md hover:bg-primary-hover font-label-md transition-colors mt-4">
                 Run Fit Optimization
               </button>
             </div>
          </BaseCard>
        </div>
      </div>
    </PageLayout>
  );
};

export default SpectralAnalysisPage;
