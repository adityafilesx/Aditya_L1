import React, { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { PageLayout, Header, Icon, BaseCard, DangerButton } from '@design-system/index';
import { useStreamStore } from '../../realtime/streamStore';
import { api } from '../../api/endpoints';
import { PageSkeleton } from '@design-system/components/skeletons';
import { OfflineState } from '@design-system/components/feedback';
import {
  HeaderStatusBar,
  DetectorWidget,
  PipelineStatusCard,
  InstrumentMetadataCard,
  ServingStatusCard,
  ModelRegistryCard,
  InferenceReadinessCard,
  ConformalCalibrationCard,
  ThermalProfileCard,
  SpectralProfileCard,
  PlasmaStateCard,
  NeupertConsistencyCard,
  FeatureStoreCard,
  PredictionTargetCard,
  TimelineWidget,
  TraceabilityMatrixCard
} from './components';

export const OperationsPageContent: React.FC = () => {
  const missionState = useStreamStore(state => state.mission);
  const connectionStatus = useStreamStore(state => state.connectionStatus);

  // REST API Queries
  const { data: systemConfig } = useQuery({
    queryKey: ['systemConfig'],
    queryFn: api.system.getConfig,
    staleTime: 60000,
  });

  const { data: systemDiagnostics } = useQuery({
    queryKey: ['systemDiagnostics'],
    queryFn: api.system.getDiagnostics,
    refetchInterval: 10000,
  });

  const { data: featureRegistry } = useQuery({
    queryKey: ['featureRegistry'],
    queryFn: api.features.getRegistry,
    refetchInterval: 30000,
  });

  const { data: mlRegistry } = useQuery({
    queryKey: ['mlRegistry'],
    queryFn: api.ml.getRegistry,
    refetchInterval: 30000,
  });

  const { data: mlCalibration } = useQuery({
    queryKey: ['mlCalibration'],
    queryFn: api.ml.getCalibration,
    refetchInterval: 30000,
  });

  const { data: mlMetrics } = useQuery({
    queryKey: ['mlMetrics'],
    queryFn: api.ml.getMetrics,
    refetchInterval: 30000,
  });

  const { data: mlTargets } = useQuery({
    queryKey: ['mlTargets'],
    queryFn: api.ml.getTargets,
    refetchInterval: 30000,
  });

  // Calculate global last updated
  const lastUpdated = useMemo(() => {
    let latest = 0;
    if (missionState?.telemetry?.timestamp) {
      latest = Math.max(latest, new Date(missionState.telemetry.timestamp).getTime());
    }
    if (systemDiagnostics?.timestamp) {
      // Handle python time.time() float which is in seconds
      const diagTime = typeof systemDiagnostics.timestamp === 'number' && systemDiagnostics.timestamp < 2000000000 ? systemDiagnostics.timestamp * 1000 : new Date(systemDiagnostics.timestamp).getTime();
      if (!isNaN(diagTime)) latest = Math.max(latest, diagTime);
    }
    return latest > 0 ? new Date(latest).toISOString() : null;
  }, [missionState, systemDiagnostics]);

  if (!missionState && connectionStatus === 'connecting') {
    return <PageSkeleton />;
  }

  if (!missionState && connectionStatus === 'disconnected') {
    return <OfflineState />;
  }

  const state = missionState || {} as any;
  const telemetry = state.telemetry || {};
  const physics = state.physics || {};
  const alerts = state.alerts || [];

  return (
    <>
      <Header
        title="Operations Center"
        subtitle="Real-Time Mission Operations & Scientific Investigation"
        actions={
          <HeaderStatusBar
            connectionStatus={connectionStatus}
            operator={state.operator || 'Cmdr. Aditi'}
            clockUtc="Live"
            systemConfig={systemConfig}
            lastUpdated={lastUpdated}
            missionStateNum={state.state || 0}
          />
        }
      />

      <div className="grid grid-cols-12 gap-gutter">
        {/* Detectors & Physics */}
        <div className="col-span-12 xl:col-span-3 flex flex-col gap-gutter">
          <DetectorWidget
            title="SoLEXS SDD2"
            iconColor="bg-primary"
            flux={telemetry?.solexs_sdd2_ctr}
            unit="cps"
            status={state.sensors?.solexs_sdd2 || 'UNKNOWN'}
            triggerThreshold={systemConfig?.target_threshold_cps}
            eventCount={telemetry?.event_count}
          />
          <DetectorWidget
            title="HEL1OS Broad"
            iconColor="bg-secondary"
            flux={telemetry?.helios_czt_broad_ctr}
            unit="cps"
            status={state.sensors?.helios_czt_broad || 'UNKNOWN'}
            triggerThreshold={systemConfig?.target_threshold_cps}
            eventCount={telemetry?.event_count}
          />
          <ThermalProfileCard physics={physics} />
          <SpectralProfileCard physics={physics} />
        </div>

        {/* Center: Pipelines, Physics States, Inference */}
        <div className="col-span-12 xl:col-span-6 flex flex-col gap-gutter">
          <div className="grid grid-cols-2 gap-gutter h-48">
            <PipelineStatusCard
              latencyMs={systemDiagnostics?.hardware?.network_latency_ms}
              cpu={systemDiagnostics?.hardware?.cpu_percent}
              memory={systemDiagnostics?.hardware?.memory_percent}
              disk={systemDiagnostics?.hardware?.disk_percent}
              status={systemDiagnostics?.engines?.api_gateway?.status}
            />
            <InstrumentMetadataCard
              sensors={state.sensors}
              uptimeSec={systemDiagnostics?.hardware?.process_uptime_sec}
            />
          </div>

          <div className="grid grid-cols-2 gap-gutter h-32">
            <PlasmaStateCard physics={physics} />
            <NeupertConsistencyCard physics={physics} />
          </div>

          <div className="grid grid-cols-2 gap-gutter h-64">
            <ModelRegistryCard models={mlRegistry?.models || []} />
            <InferenceReadinessCard metrics={mlMetrics || []} />
          </div>
        </div>

        {/* Right: Feature Store, Calibration, Operations */}
        <div className="col-span-12 xl:col-span-3 flex flex-col gap-gutter">
          <div className="grid grid-cols-2 gap-gutter">
            <ServingStatusCard modelsStatus={state.models} />
            <FeatureStoreCard features={featureRegistry?.features || []} />
          </div>
          <PredictionTargetCard targets={mlTargets?.targets || []} />
          <ConformalCalibrationCard calibration={mlCalibration?.results} />
          <TraceabilityMatrixCard diagnostics={systemDiagnostics} config={systemConfig} />
        </div>
      </div>

      {/* Lower section */}
      <div className="grid grid-cols-12 gap-gutter mt-gutter mb-20">
        <div className="col-span-12 xl:col-span-9 h-[400px]">
          <TimelineWidget alerts={alerts} />
        </div>

        <div className="col-span-12 xl:col-span-3 flex flex-col gap-4">
          <BaseCard variant="plain" size="md" className="card-shadow h-full" title={
            <span className="font-label-caps text-label-caps text-on-surface mb-6 flex items-center gap-2">
              <Icon name="terminal" className="text-on-surface-variant" /> OPERATOR COMMANDS
            </span>
          }>
            <div className="flex flex-col gap-3">
              <button className="w-full flex items-center justify-between p-4 bg-surface-container border border-outline-variant rounded-lg hover:bg-surface-container-high transition-colors">
                <span className="font-label-caps text-label-caps font-bold">GENERATE REPORT</span>
                <Icon name="description" />
              </button>
              <button className="w-full flex items-center justify-between p-4 bg-surface-container border border-outline-variant rounded-lg hover:bg-surface-container-high transition-colors">
                <span className="font-label-caps text-label-caps font-bold">EXPORT SESSION</span>
                <Icon name="cloud_upload" />
              </button>
              <DangerButton className="w-full flex items-center justify-between p-4 bg-error/10 border border-error/20 rounded-lg text-error hover:bg-error/20 transition-colors">
                <span className="font-label-caps text-label-caps font-bold text-left">EMERGENCY PROCEDURES</span>
                <Icon name="report_problem" />
              </DangerButton>
            </div>
            <div className="mt-8 p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Icon name="info" className="text-primary text-[18px]" />
                <span className="text-[11px] font-bold text-primary uppercase">Manual Override</span>
              </div>
              <p className="text-[12px] text-on-surface-variant">Press <kbd className="px-1 bg-surface-variant rounded">Ctrl+Shift+L</kbd> to unlock full instrument command console.</p>
            </div>
          </BaseCard>
        </div>
      </div>
    </>
  );
};

export const OperationsPage: React.FC = () => (
  <PageLayout className="p-gutter">
    <OperationsPageContent />
  </PageLayout>
);

export default OperationsPage;
