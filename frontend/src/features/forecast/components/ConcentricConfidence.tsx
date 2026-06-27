import type { FC } from 'react';
import { useMemo } from 'react';

interface ConcentricConfidenceProps {
  overall: number;
  observation: number;
  physics: number;
  model: number;
  calibration: number;
}

export const ConcentricConfidence: FC<ConcentricConfidenceProps> = ({
  overall,
  observation,
  physics,
  model,
  calibration
}) => {
  const components = useMemo(() => [
    { name: 'Observation', val: observation, bg: 'bg-success' },
    { name: 'Physics', val: physics, bg: 'bg-info' },
    { name: 'Model', val: model, bg: 'bg-danger' },
    { name: 'Calibration', val: calibration, bg: 'bg-warning' },
  ], [observation, physics, model, calibration]);

  const R = 26;
  const circumference = 2 * Math.PI * R;
  const overallPct = Math.round(overall * 100);

  return (
    <div className="flex flex-col gap-3 h-full bg-surface/10 border border-border/30 rounded p-3">

      {/* Hero: Overall confidence */}
      <div className="flex items-center gap-3 flex-shrink-0">
        <div className="relative w-16 h-16 flex-shrink-0">
          <svg viewBox="0 0 64 64" className="w-full h-full -rotate-90">
            <circle cx="32" cy="32" r={R} fill="transparent" stroke="rgba(255,255,255,0.06)" strokeWidth="6" />
            <circle
              cx="32"
              cy="32"
              r={R}
              fill="transparent"
              className="stroke-primary transition-all duration-1000"
              strokeWidth="6"
              strokeLinecap="round"
              strokeDasharray={`${overall * circumference} ${circumference}`}
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-heading text-foreground font-bold tabular-nums leading-none">
              {overallPct}<span className="text-label text-muted-foreground">%</span>
            </span>
          </div>
        </div>
        <div className="flex flex-col">
          <span className="text-label text-muted-foreground uppercase tracking-widest">Overall</span>
          <span className="text-primary-metric text-foreground font-bold leading-tight">Forecast Confidence</span>
        </div>
      </div>

      {/* Component breakdown — labeled bars */}
      <div className="flex-1 flex flex-col justify-around gap-2 min-h-0 font-mono">
        {components.map(c => {
          const pct = Math.round(c.val * 100);
          return (
            <div key={c.name} className="flex items-center gap-2">
              <span className="w-20 flex-shrink-0 text-label text-muted-foreground truncate">{c.name}</span>
              <div className="flex-1 h-1.5 bg-surface-container rounded-full overflow-hidden">
                <div className={`h-full ${c.bg} transition-all duration-700`} style={{ width: `${pct}%` }} />
              </div>
              <span className="w-9 flex-shrink-0 text-right text-label text-foreground font-bold tabular-nums">{pct}%</span>
            </div>
          );
        })}
      </div>

    </div>
  );
};
export default ConcentricConfidence;
