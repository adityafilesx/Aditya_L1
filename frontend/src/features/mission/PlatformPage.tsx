import type { FC } from 'react';
import { MetricCard, ChartContainer, PageLayout, PlotlyContainer } from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';

export const PlatformPageContent: FC = () => {
  const missionState = useStreamStore(state => state.mission);
  const history = useStreamStore(state => state.history);
  const connectionStatus = useStreamStore(state => state.connectionStatus);

  if (!missionState && connectionStatus === 'connecting') {
    return (
      <>
        <div className="grid grid-cols-12 gap-6 mb-6">
          <div className="col-span-3"><MetricCard loading={true} /></div>
          <div className="col-span-3"><MetricCard loading={true} /></div>
          <div className="col-span-3"><MetricCard loading={true} /></div>
          <div className="col-span-3"><MetricCard loading={true} /></div>
        </div>
        <ChartContainer loading={true} className="h-[400px]" />
      </>
    );
  }

  const state = missionState || {} as any;
  const telemetry = state.telemetry || {};
  const physics = state.physics || {};
  const forecast = state.forecast || {};

  return (
    <>
      <div className="grid grid-cols-12 gap-6 mb-6">
        <div className="col-span-3">
          <MetricCard 
            title="Live Telemetry (Soft X-Ray)" 
            value={telemetry.solexs_sdd2_ctr?.toFixed(1) || '0.0'} 
            status="primary" 
          />
        </div>
        <div className="col-span-3">
          <MetricCard 
            title="Physics (Temperature)" 
            value={`${physics.temperature_mk?.toFixed(1) || '0.0'} MK`} 
            status="success" 
          />
        </div>
        <div className="col-span-3">
          <MetricCard 
            title="Nowcast Conf." 
            value={`${((forecast.confidence || 0) * 100).toFixed(0)}%`} 
            status="primary" 
          />
        </div>
        <div className="col-span-3">
          <MetricCard 
            title="Mission Status" 
            value={state.state === 2 ? 'ALERT' : state.state === 1 ? 'WATCH' : 'NOMINAL'} 
            status={state.state > 0 ? 'warning' : 'success'} 
          />
        </div>
      </div>
      
      <ChartContainer 
        title="Nowcasting Telemetry Stream" 
        subtitle="Real-time aggregation of sensor data" 
        className="h-[400px]"
      >
        <PlotlyContainer 
          data={[{
            x: history.telemetry.map(t => new Date(t.timestamp).getTime()),
            y: history.telemetry.map(t => t.solexs_sdd2_ctr),
            type: 'scatter',
            mode: 'lines',
            fill: 'tozeroy',
            line: { color: '#8884d8' },
            name: 'SoLEXS SDD2'
          }]} 
          layout={{ showlegend: false, margin: {t:0,b:0,l:40,r:10} }}
          syncCursor
        />
      </ChartContainer>
    </>
  );
};

export const PlatformPage: FC = () => (
  <PageLayout className="p-0">
    <div className="p-6">
      <PlatformPageContent />
    </div>
  </PageLayout>
);
export default PlatformPage;
