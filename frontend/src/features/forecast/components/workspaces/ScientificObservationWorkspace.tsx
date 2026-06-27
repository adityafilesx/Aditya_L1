import type { FC } from 'react';
import { BaseCard, Icon } from '@design-system/index';
import { useForecast } from '../../hooks/useForecast';

export const ScientificObservationWorkspace: FC = () => {
  const { currentObservation } = useForecast();

  return (
    <BaseCard
      variant="glass"
      className="p-4 h-full min-h-[400px] flex flex-col"
      title={
        <span className="font-label-caps text-label-caps text-on-surface-variant flex items-center gap-2">
          <Icon name="insights" className="text-primary" /> Live Scientific Observation Stream
        </span>
      }
    >
      {currentObservation ? (
        <div className="flex-1 flex flex-col gap-4">
          <div className="flex justify-between items-center bg-surface-container rounded p-3">
            <div className="flex flex-col">
              <span className="text-xs text-secondary uppercase">SoLEXS Validated Flux</span>
              <span className="text-2xl font-mono text-primary">{currentObservation.solexs_flux.toExponential(2)}</span>
            </div>
            <div className="flex flex-col text-right">
              <span className="text-xs text-secondary uppercase">HEL1OS Validated Flux</span>
              <span className="text-2xl font-mono text-primary">{currentObservation.helios_flux.toExponential(2)}</span>
            </div>
          </div>
          
          <div className="flex-1 bg-surface-container-low rounded border border-outline-variant border-dashed flex flex-col items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/5 to-transparent animate-pulse opacity-50"></div>
            <div className="text-center space-y-2 z-10 p-6">
              <Icon name="multiline_chart" className="text-4xl text-on-surface-variant/50 block mx-auto" />
              <p className="text-on-surface-variant font-label-caps">Live Telemetry Rendering</p>
              <div className="text-xs text-on-surface-variant/70 flex gap-4 justify-center mt-2">
                <span className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-blue-400"></div> SoLEXS Background: {currentObservation.noise_background.soft_xray_background.toExponential(2)}</span>
                <span className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-purple-400"></div> HEL1OS Background: {currentObservation.noise_background.hard_xray_background.toExponential(2)}</span>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex-1 bg-surface-container-low rounded border border-outline-variant border-dashed flex items-center justify-center relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/5 to-transparent animate-pulse opacity-50"></div>
          <div className="text-center space-y-2 z-10">
            <Icon name="sensors_off" className="text-4xl text-on-surface-variant/50 block mx-auto" />
            <p className="text-on-surface-variant font-label-caps">Awaiting Scientific Data Stream</p>
          </div>
        </div>
      )}
    </BaseCard>
  );
};
