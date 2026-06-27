import type { FC } from 'react';
import { useMemo, useState, useEffect } from 'react';
import { BaseCard, Icon } from '../../../design-system';
import { useForecast } from '../hooks/useForecast';
import { useForecastStore } from '../store/forecastStore';

const FORECAST_STATES = ['QUIET', 'WATCH', 'WARNING', 'ALERT', 'RECOVERY'];

export const OperatorCommand: FC = () => {
  const { latestForecast, forecastWindow } = useForecast();
  const setLatestForecast = useForecastStore((state) => state.setLatestForecast);

  const [countdown, setCountdown] = useState(10);
  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => (prev <= 1 ? 10 : prev - 1));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const state = latestForecast?.state || 'QUIET';

  const decision = useMemo(() => {
    let action = 'Maintain standard operations.';
    let justification = 'Coronal temperatures remain nominal. No magnetic reconnection regions have breached active thresholds.';
    let priority = { label: 'LOW', color: 'text-success bg-success/10 border-success/30' };
    let impact = 'None';
    let responseTime = 'N/A';
    let consequence = 'Standard operations sequence continues. Observation cadence maintained at 1Hz.';
    let emergencyProcedure = 'SOP-01: Baseline Solar Observation monitoring.';

    if (state === 'ALERT') {
      action = 'INITIATE SUIT HIGH-CADENCE SEQUENCE';
      justification = 'X-class flare probability has breached the 85% critical trigger limit inside the current forecast window.';
      priority = { label: 'CRITICAL', color: 'text-error bg-error/20 border-error/50 font-black' };
      impact = 'High (Payload Safeguard active)';
      responseTime = '< 5 Mins';
      consequence = 'SUIT payload rotated to backup filters; high cadence recording active. Science links prioritized.';
      emergencyProcedure = 'EOP-09: Trigger instrument safe-mode filters; lock memory buffers.';
    } else if (state === 'WARNING') {
      action = 'Increase telemetry cadence to 5Hz.';
      justification = 'M-class precursor heating indicators have spiked. Increased observation density is required for active tracking.';
      priority = { label: 'HIGH', color: 'text-warning bg-warning/20 border-warning/50 font-bold' };
      impact = 'Moderate telemetry overhead';
      responseTime = '< 15 Mins';
      consequence = 'Observation logs frequency accelerated. Event buffer queues flushed to prevent latency overflow.';
      emergencyProcedure = 'SOP-05: Enable event buffer cache acceleration.';
    } else if (state === 'WATCH') {
      action = 'Review operational timeline for next 24 hours.';
      justification = 'Sub-storm warning signs detected. Review backup ground station options for redundant link coverage.';
      priority = { label: 'MEDIUM', color: 'text-info bg-info/20 border-info/50' };
      impact = 'Low';
      responseTime = '< 1 Hour';
      consequence = 'Secondary ground links set to hot-standby. Backup telemetry sync loops active.';
      emergencyProcedure = 'SOP-03: Establish redundant ground station sync link.';
    } else if (state === 'RECOVERY') {
      action = 'Begin post-event sensor recalibration.';
      justification = 'Flux levels dropping below C-class thresholds. Perform routine damage assessment.';
      priority = { label: 'LOW', color: 'text-success bg-success/10 border-success/30' };
      impact = 'Low';
      responseTime = '< 24 Hours';
      consequence = 'Telemetry returned to nominal 1Hz baseline.';
      emergencyProcedure = 'SOP-12: Post-event instrument calibration.';
    }

    if (forecastWindow === '7d' && state === 'QUIET') {
      action = 'Prepare weekly solar rotation assets schedule.';
      justification = 'Active region AR3412 is rotating into earth-facing quadrant in next 4 days. Schedule redundant tracking slots.';
      priority = { label: 'LOW', color: 'text-success bg-success/10 border-success/30' };
      responseTime = '72 Hours';
    }

    return { action, justification, priority, impact, responseTime, consequence, emergencyProcedure };
  }, [state, forecastWindow]);

  const handleSimulateStatus = (nextState: typeof state) => {
    setIsAcknowledged(false);
    if (latestForecast) {
      setLatestForecast({ ...latestForecast, state: nextState });
    } else {
      setLatestForecast({
        forecast_id: 'SIM-001',
        timestamp: new Date().toISOString(),
        horizon: forecastWindow,
        probabilities: { A: 0.1, B: 0.2, C: 0.3, M: 0.35, X: 0.05 },
        context: { timestamp: new Date().toISOString(), active_regions: 2, current_flux: 1e-6, data_quality: 'VALID' },
        state: nextState
      });
    }
  };

  const [replayState, setReplayState] = useState<'LIVE' | 'PLAYING' | 'PAUSED'>('LIVE');
  const [replaySpeed, setReplaySpeed] = useState<number>(1);
  const [selectedScenario, setSelectedScenario] = useState<string>('2024-02-12');

  const triggerReplayAction = (action: 'play' | 'pause' | 'stop') => {
    if (action === 'play') {
      setReplayState('PLAYING');
    } else if (action === 'pause') {
      setReplayState('PAUSED');
    } else {
      setReplayState('LIVE');
      setLatestForecast(null);
    }
  };

  const [isAcknowledged, setIsAcknowledged] = useState<boolean>(true);

  const getActiveStateStyle = (s: string) => {
    if (s === 'ALERT') return 'bg-error text-white border-error shadow-[0_0_10px_rgba(239,68,68,0.6)]';
    if (s === 'WARNING') return 'bg-warning text-white border-warning shadow-[0_0_10px_rgba(245,158,11,0.6)]';
    if (s === 'WATCH') return 'bg-info text-white border-info shadow-[0_0_10px_rgba(59,130,246,0.6)]';
    if (s === 'RECOVERY') return 'bg-success text-white border-success shadow-[0_0_10px_rgba(34,197,94,0.6)]';
    return 'bg-success text-white border-success shadow-[0_0_10px_rgba(34,197,94,0.6)]';
  };

  return (
    <BaseCard className="flex flex-col h-full bg-surface-container-lowest/40 border border-border/20 backdrop-blur-md overflow-hidden p-3">
      
      {/* Component Contract Header */}
      <div className="flex justify-between items-center flex-shrink-0 mb-3 border-b border-border/20 pb-2">
        <div className="flex items-center gap-1.5">
          <Icon name="shield" className="text-primary" />
          <h2 className="text-heading text-foreground">Decision Intelligence</h2>
        </div>
        
        <div className="flex items-center gap-1 text-label font-mono text-muted-foreground bg-surface/60 px-2 py-0.5 rounded border border-border/30">
          <Icon name="schedule" size="sm" className="animate-spin text-primary [animation-duration:4s]" />
          <span>PASS: {countdown}s</span>
        </div>
      </div>

      <div className="flex-1 flex flex-col gap-3 min-h-0">
        
        {/* Row 1: Forecast State Ladder */}
        <div className="flex flex-col flex-shrink-0 mb-1">
          <div className="flex items-center justify-between mb-2">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest">Forecast State</span>
            {/* Quick override controls hidden in a tiny row */}
            <div className="flex items-center gap-2">
              <button onClick={() => handleSimulateStatus('QUIET')} className="text-label text-muted-foreground hover:text-foreground transition-colors">Q</button>
              <button onClick={() => handleSimulateStatus('WATCH')} className="text-label text-muted-foreground hover:text-foreground transition-colors">T</button>
              <button onClick={() => handleSimulateStatus('WARNING')} className="text-label text-muted-foreground hover:text-foreground transition-colors">W</button>
              <button onClick={() => handleSimulateStatus('ALERT')} className="text-label text-muted-foreground hover:text-foreground transition-colors">A</button>
              <button onClick={() => handleSimulateStatus('RECOVERY')} className="text-label text-muted-foreground hover:text-foreground transition-colors">R</button>
            </div>
          </div>
          
          <div className="flex flex-wrap items-center bg-surface/20 border border-border/20 p-1 rounded gap-1">
            {FORECAST_STATES.map((s) => {
              const isActive = s === state;
              return (
                <div 
                  key={s}
                  className={`flex-[1_1_30%] text-center py-1 rounded text-label font-bold transition-all duration-300 border ${
                    isActive 
                      ? getActiveStateStyle(s)
                      : 'bg-surface/40 text-muted-foreground border-transparent opacity-50'
                  }`}
                >
                  {s}
                </div>
              );
            })}
          </div>
        </div>

        {/* Row 2: Recommended Action + Priority */}
        <div className="bg-surface/20 border border-border/20 rounded p-3 flex flex-col gap-2.5 flex-shrink-0">
          <div className="flex items-start justify-between gap-3">
            <div className="flex flex-col min-w-0">
              <span className="text-label font-bold text-muted-foreground uppercase tracking-widest">Recommended Action</span>
              <span className="text-heading text-foreground leading-tight mt-1">{decision.action}</span>
            </div>
            <div className="flex flex-col items-end flex-shrink-0">
              <span className="text-label font-bold text-muted-foreground uppercase tracking-widest">Priority</span>
              <span className={`px-2.5 py-1 rounded border text-label font-bold mt-1 ${decision.priority.color}`}>
                {decision.priority.label}
              </span>
            </div>
          </div>

          <p className="text-label text-muted-foreground leading-relaxed line-clamp-2">{decision.justification}</p>

          <div className="flex items-center justify-between gap-3 border-t border-border/20 pt-2">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest">Required Response</span>
            <span className="text-primary-metric text-foreground font-bold tabular-nums">{decision.responseTime}</span>
          </div>

          <p className="text-label text-muted-foreground/80 leading-snug line-clamp-2">
            <span className="font-bold text-muted-foreground uppercase tracking-wider">Outcome: </span>
            {decision.consequence}
          </p>
        </div>

        {/* Row 3: Emergency Procedure */}
        <div className="flex items-start gap-2 bg-warning/10 border border-warning/30 rounded p-3 flex-shrink-0">
          <Icon name="warning" size="sm" className="text-warning flex-shrink-0 mt-0.5" />
          <div className="flex flex-col min-w-0">
            <span className="text-label font-bold text-warning/80 uppercase tracking-widest">Emergency Procedure</span>
            <span className="text-label text-warning font-mono leading-snug mt-0.5">{decision.emergencyProcedure}</span>
          </div>
        </div>

        {/* Row 4: Historical Replay */}
        <div className="flex flex-col gap-2 border-t border-border/20 pt-3 flex-shrink-0 mt-auto">
          <div className="flex justify-between items-center">
            <span className="font-bold text-muted-foreground uppercase tracking-widest text-label">Historical Replay</span>
            <button 
              onClick={() => setIsAcknowledged(prev => !prev)}
              className={`px-2 py-0.5 rounded border text-label font-bold font-mono transition-all ${
                isAcknowledged ? 'bg-success/20 border-success text-success' : 'bg-error/20 border-error text-error animate-pulse'
              }`}
            >
              {isAcknowledged ? 'ACKNOWLEDGED' : 'ACK REQUIRED'}
            </button>
          </div>

          <div className="flex gap-2 items-center">
            <select
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="flex-grow bg-surface/50 border border-border/20 rounded px-2 py-1 text-label font-mono text-foreground outline-none cursor-pointer hover:bg-surface/80"
            >
              <option value="2024-02-12">AR3412 - M3.4</option>
              <option value="2024-05-10">AR3664 - X5.8</option>
            </select>

            <select
              value={replaySpeed}
              onChange={(e) => setReplaySpeed(Number(e.target.value))}
              className="bg-surface/50 border border-border/20 rounded px-2 py-1 text-label font-mono text-foreground outline-none cursor-pointer hover:bg-surface/80"
            >
              <option value={1}>1x</option>
              <option value={5}>5x</option>
            </select>
          </div>

          <div className="flex gap-1.5 justify-center text-label font-bold font-mono mt-1">
            <button 
              onClick={() => triggerReplayAction('play')} 
              className={`flex-1 flex items-center justify-center py-1 rounded border transition-colors ${
                replayState === 'PLAYING' ? 'bg-success text-white border-success' : 'bg-surface/50 border-border/20 text-foreground hover:bg-surface'
              }`}
            >
              Play
            </button>
            <button 
              onClick={() => triggerReplayAction('pause')} 
              className={`flex-1 flex items-center justify-center py-1 rounded border transition-colors ${
                replayState === 'PAUSED' ? 'bg-warning text-white border-warning' : 'bg-surface/50 border-border/20 text-foreground hover:bg-surface'
              }`}
            >
              Pause
            </button>
            <button 
              onClick={() => triggerReplayAction('stop')} 
              className="flex-1 flex items-center justify-center py-1 rounded border border-border/20 bg-surface/50 text-foreground hover:bg-surface"
            >
              Live
            </button>
          </div>
        </div>

      </div>
    </BaseCard>
  );
};
export default OperatorCommand;
