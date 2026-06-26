import type { FC } from 'react';
import { 
  PageLayout, 
  Header, 
  BaseCard, 
  Icon,
  PlotlyContainer
} from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

export const ResearchPageContent: FC = () => {
  const history = useStreamStore(state => state.history);
  const timeAxis = history.telemetry.map(t => new Date(t.timestamp).getTime());
  const solexs = history.telemetry.map(t => t.solexs_sdd2_ctr);
  
  // Create a mock scalogram by using the solexs data and adding random frequency bands
  const freqs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
  const zData = freqs.map((f) => 
    solexs.map(s => (s * (Math.sin(f) + 1.5)) + (Math.random() * 10))
  );

  return (
    <>
      <Header
        title="Spectral & Wavelet Workstation"
        subtitle="Energy Spectra Analysis • Continuous Wavelet Transform • High-Resolution Dynamics"
        className="mb-section-gap border-b border-outline-variant pb-6"
        actions={
          <div className="flex gap-2">
            <button className="bg-surface-container-highest px-3 py-1 rounded text-[10px] font-bold text-on-surface-variant flex items-center gap-2 border border-outline-variant hover:bg-surface-container transition-colors cursor-pointer" onClick={() => console.log('Exporting CSV/PNG...')}>
               <Icon name="download" className="text-primary text-[14px]" /> EXPORT DATA
            </button>
            <button className="bg-surface-container-highest px-3 py-1 rounded text-[10px] font-bold text-on-surface-variant flex items-center gap-2 border border-outline-variant hover:bg-surface-container transition-colors cursor-pointer" onClick={() => console.log('Generating Jupyter Notebook...')}>
               <Icon name="book" className="text-secondary text-[14px]" /> TO JUPYTER
            </button>
            <span className="bg-surface-container-highest px-3 py-1 rounded text-[10px] font-bold text-on-surface-variant flex items-center gap-2">
               <Icon name="waves" className="text-primary text-[14px]" /> REAL-TIME CWT
            </span>
            <span className="bg-surface-container-highest px-3 py-1 rounded text-[10px] font-bold text-on-surface-variant flex items-center gap-2">
               <Icon name="blur_on" className="text-secondary text-[14px]" /> 1024 BINS
            </span>
          </div>
        }
      />
      
      <section className="mb-section-gap flex flex-col gap-6 h-[800px]">
        <div className="grid grid-cols-12 gap-gutter h-1/2">
          <BaseCard variant="lab" className="col-span-12 lg:col-span-8 p-0 flex flex-col h-full" title={
            <span className="font-label-caps text-[12px] flex items-center gap-2">
              <Icon name="waterfall_chart" className="text-secondary" /> Wavelet Scalogram (CWT)
            </span>
          }>
             <div className="flex-1 w-full relative">
               <PlotlyContainer 
                 data={[{
                   z: zData,
                   x: timeAxis,
                   y: freqs,
                   type: 'heatmap',
                   colorscale: 'Jet',
                   showscale: true
                 }]}
                 layout={{
                   xaxis: { title: { text: 'Time (UTC)' } },
                   yaxis: { title: { text: 'Frequency (Hz)' } },
                   margin: { t: 10, b: 40, l: 50, r: 20 },
                 }}
                 syncCursor
               />
             </div>
          </BaseCard>

          <BaseCard variant="lab" className="col-span-12 lg:col-span-4 p-0 flex flex-col h-full" title={
            <span className="font-label-caps text-[12px] flex items-center gap-2">
              <Icon name="stacked_line_chart" className="text-primary" /> Spectral Cross-Section
            </span>
          }>
             <div className="flex-1 w-full relative p-4 flex flex-col">
                <div className="text-[10px] font-data-mono text-on-surface-variant mb-2">Live Cross-Section at Cursor Time</div>
                <div className="flex-1">
                  <PlotlyContainer 
                    data={[{
                      x: freqs,
                      y: zData.map(row => row[row.length - 1] || 0),
                      type: 'scatter',
                      mode: 'lines',
                      line: { color: '#8884d8', shape: 'spline' },
                      fill: 'tozeroy'
                    }]}
                    layout={{
                      xaxis: { title: { text: 'Frequency (Hz)' } },
                      yaxis: { title: { text: 'Power' } },
                      margin: { t: 10, b: 40, l: 40, r: 10 },
                    }}
                  />
                </div>
             </div>
          </BaseCard>
        </div>

        <div className="grid grid-cols-1 gap-gutter h-1/2">
          <BaseCard variant="lab" className="p-0 flex flex-col h-full" title={
            <span className="font-label-caps text-[12px] flex items-center gap-2">
              <Icon name="image" className="text-tertiary" /> Dynamic Spectra Image Viewer
            </span>
          }>
             <div className="flex-1 w-full relative bg-black flex items-center justify-center overflow-hidden group">
                <div className="absolute top-4 left-4 z-10 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button className="bg-surface-container/80 text-on-surface hover:bg-surface-container p-2 rounded backdrop-blur">
                    <Icon name="zoom_in" />
                  </button>
                  <button className="bg-surface-container/80 text-on-surface hover:bg-surface-container p-2 rounded backdrop-blur">
                    <Icon name="zoom_out" />
                  </button>
                  <button className="bg-surface-container/80 text-on-surface hover:bg-surface-container p-2 rounded backdrop-blur">
                    <Icon name="contrast" />
                  </button>
                </div>
                
                <PlotlyContainer 
                  data={[{
                    z: zData.map(row => row.map(v => Math.log10(v + 1))),
                    x: timeAxis,
                    y: freqs,
                    type: 'heatmap',
                    colorscale: 'Magma',
                    showscale: false
                  }]}
                  layout={{
                    xaxis: { visible: false },
                    yaxis: { visible: false },
                    margin: { t: 0, b: 0, l: 0, r: 0 },
                    paper_bgcolor: 'black',
                    plot_bgcolor: 'black'
                  }}
                  syncCursor
                />
             </div>
          </BaseCard>
        </div>
      </section>
    </>
  );
};

export const ResearchPage: FC = () => (
  <PageLayout className="p-6" data-layout="dashboard">
    <ResearchPageContent />
  </PageLayout>
);

export default ResearchPage;
