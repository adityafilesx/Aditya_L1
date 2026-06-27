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
  const gauges = useMemo(() => {
    return [
      { name: 'Overall', val: overall, r: 44, color: 'stroke-primary' },
      { name: 'Observation', val: observation, r: 36, color: 'stroke-success' },
      { name: 'Physics', val: physics, r: 28, color: 'stroke-info' },
      { name: 'Model', val: model, r: 20, color: 'stroke-danger' },
      { name: 'Calibration', val: calibration, r: 12, color: 'stroke-warning' }
    ];
  }, [overall, observation, physics, model, calibration]);

  const getStrokeDash = (radius: number, percentage: number) => {
    const circumference = 2 * Math.PI * radius;
    const strokeVal = (percentage / 100) * circumference;
    return `${strokeVal} ${circumference}`;
  };

  return (
    <div className="flex items-center gap-4 bg-surface/10 border border-border/30 rounded p-2 text-[10px]">
      
      {/* 1. SVG concentric rings */}
      <div className="w-24 h-24 relative flex-shrink-0">
        <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
          {gauges.map(g => (
            <g key={g.name}>
              {/* Background Ring */}
              <circle
                cx="50"
                cy="50"
                r={g.r}
                fill="transparent"
                stroke="rgba(255,255,255,0.05)"
                strokeWidth="3.5"
              />
              {/* Active Ring */}
              <circle
                cx="50"
                cy="50"
                r={g.r}
                fill="transparent"
                className={`transition-all duration-1000 ${g.color}`}
                strokeWidth="3.5"
                strokeDasharray={getStrokeDash(g.r, g.val * 100)}
                strokeLinecap="round"
              />
            </g>
          ))}
        </svg>
      </div>

      {/* 2. Legends and indicators */}
      <div className="flex-1 flex flex-col gap-1.5 font-mono">
        {gauges.map(g => (
          <div key={g.name} className="flex justify-between items-center text-[9px] leading-none">
            <div className="flex items-center gap-1.5">
              <span className={`w-1.5 h-1.5 rounded-full ${
                g.color.replace('stroke-', 'bg-')
              }`} />
              <span className="text-muted-foreground">{g.name}:</span>
            </div>
            <span className="font-bold text-foreground">{(g.val * 100).toFixed(0)}%</span>
          </div>
        ))}
      </div>

    </div>
  );
};
export default ConcentricConfidence;
