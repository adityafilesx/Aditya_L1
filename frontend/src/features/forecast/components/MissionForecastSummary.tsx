import type { FC } from 'react';
import { useMemo, useState, useEffect } from 'react';
import { useForecast } from '../hooks/useForecast';

const ESCALATION_LADDER = ['GREEN', 'YELLOW', 'ORANGE', 'RED', 'CRITICAL'];

export const MissionForecastSummary: FC = () => {
  const { latestForecast, currentObservation, nowcastState, forecastWindow } = useForecast();

  const [obsAge, setObsAge] = useState(0);

  useEffect(() => {
    setObsAge(0);
  }, [currentObservation]);

  useEffect(() => {
    const timer = setInterval(() => {
      setObsAge(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const summary = useMemo(() => {
    const state = latestForecast?.state || 'QUIET';
    let alertLevel = 'GREEN';
    
    if (state === 'ALERT') alertLevel = 'CRITICAL';
    else if (state === 'WARNING') alertLevel = 'ORANGE';
    else if (state === 'WATCH') alertLevel = 'YELLOW';

    const activeRegion = currentObservation?.metadata?.source_instrument || 'AR3664';
    const context = state === 'ALERT' ? 'HIGH FLARING' : 'NOMINAL';
    const dataQuality = currentObservation?.quality?.overall_scientific_confidence != null
      ? (currentObservation.quality.overall_scientific_confidence >= 0.8 ? 'VALID' : 'DEGRADED')
      : 'VALID';

    return {
      state,
      alertLevel,
      activeRegion,
      context,
      dataQuality,
      profile: forecastWindow
    };
  }, [latestForecast, currentObservation, forecastWindow]);

  const getLadderColor = (level: string, activeLevel: string) => {
    const isActive = level === activeLevel;
    if (!isActive) return 'bg-surface-container border-border/40 text-muted-foreground opacity-50';
    switch (level) {
      case 'CRITICAL': return 'bg-error/20 text-error border-error shadow-focus';
      case 'RED': return 'bg-error/20 text-error border-error';
      case 'ORANGE': return 'bg-warning/20 text-warning border-warning shadow-focus';
      case 'YELLOW': return 'bg-secondary/20 text-secondary border-secondary shadow-focus';
      default: return 'bg-success/20 text-success border-success shadow-focus';
    }
  };

  return (
    <div className="w-full h-[64px] px-4 py-2 flex items-center justify-between select-none">
      
      {/* 1. Left: Alert Escalation Ladder */}
      <div className="flex flex-col gap-1.5 flex-shrink-0 border-r border-border/20 pr-6 h-full justify-center">
        <span className="text-label text-muted-foreground uppercase leading-none">Mission State</span>
        <div className="flex items-center gap-1">
          {ESCALATION_LADDER.map((level) => (
            <div 
              key={level}
              className={`px-2 py-0.5 border text-[11px] font-mono font-bold rounded-control transition-all duration-300 ${getLadderColor(level, summary.alertLevel)}`}
            >
              {level}
            </div>
          ))}
        </div>
      </div>

      {/* 2. Center: Forecast Context */}
      <div className="flex-1 flex justify-center gap-8 border-r border-border/20 px-6 h-full items-center">
        <div className="flex flex-col gap-1">
          <span className="text-label text-muted-foreground uppercase leading-none">Active Region</span>
          <span className="text-primary-metric text-foreground">{summary.activeRegion}</span>
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-label text-muted-foreground uppercase leading-none">Solar Context</span>
          <span className="text-primary-metric text-foreground">{summary.context}</span>
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-label text-muted-foreground uppercase leading-none">Observation Quality</span>
          <span className="text-primary-metric text-success">{summary.dataQuality}</span>
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-label text-muted-foreground uppercase leading-none">Forecast Profile</span>
          <span className="text-primary-metric text-foreground uppercase">{summary.profile} HORIZON</span>
        </div>
      </div>

      {/* 3. Right: Data Freshness / Telemetry */}
      <div className="flex flex-col pl-6 flex-shrink-0 h-full justify-center min-w-[120px] gap-1">
        <span className="text-label text-muted-foreground uppercase leading-none">Data Freshness</span>
        <div className="flex items-baseline gap-1">
          <span className={`text-hero tabular-nums ${obsAge > 5 ? 'text-warning' : 'text-success'}`}>{obsAge}</span>
          <span className="text-label text-muted-foreground">sec</span>
        </div>
      </div>

    </div>
  );
};
export default MissionForecastSummary;
