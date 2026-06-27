import type { FC } from 'react';
import { useMemo } from 'react';
import { BaseCard, Icon } from '../../../design-system';
import { useForecast } from '../hooks/useForecast';

export const TrustAndRepository: FC = () => {
  const { latestForecast, forecastWindow } = useForecast();

  const trust = useMemo(() => {
    let score = 94;
    let delta = '+2';
    
    if (forecastWindow === '24h') {
      score = 86;
      delta = '-1';
    } else if (forecastWindow === '7d') {
      score = 72;
      delta = '-5';
    }

    return {
      score,
      delta,
      isPositive: !delta.startsWith('-')
    };
  }, [forecastWindow]);

  const repo = useMemo(() => {
    return {
      forecastId: latestForecast?.forecast_id || 'F-3910A',
      version: 'v4.1.2',
      verification: 'PENDING',
      replay: 'AVAILABLE',
      stored: 'S3-ARCHIVE'
    };
  }, [latestForecast]);

  return (
    <BaseCard className="flex flex-col h-full bg-surface-container-lowest/40 border border-border/20 backdrop-blur-md overflow-hidden p-3">
      
      {/* Component Contract Header */}
      <div className="flex justify-between items-center flex-shrink-0 mb-3 border-b border-border/20 pb-2">
        <div className="flex items-center gap-1.5 min-w-0">
          <Icon name="Verified" className="text-primary flex-shrink-0" />
          <h2 className="text-heading text-foreground truncate">Trust & Repository</h2>
        </div>
      </div>

      <div className="flex-1 flex gap-3 min-h-0">
        
        {/* Left: Trust History */}
        <div className="flex-1 flex flex-col justify-center border-r border-border/20 pr-3">
          <div className="flex justify-between items-center mb-1">
            <span className="text-label font-bold text-muted-foreground uppercase tracking-widest">Trust Score</span>
            <span className="text-label text-muted-foreground">24h</span>
          </div>
          
          <div className="flex items-end gap-2 mb-3">
            <span className="text-hero text-foreground leading-none">{trust.score}%</span>
            <span className={`text-label font-bold pb-0.5 ${trust.isPositive ? 'text-success' : 'text-error'}`}>
              {trust.isPositive ? '▲' : '▼'} {trust.delta}%
            </span>
          </div>

          {/* Simple CSS Sparkline representation */}
          <div className="h-6 w-full flex items-end gap-[2px] opacity-70 mt-auto">
            {[40, 50, 45, 60, 55, 70, 75, 80, 78, 85, 90, 88, 92, 94].map((h, i) => (
              <div key={i} className="flex-1 bg-primary rounded-t-sm transition-all" style={{ height: `${(h / 100) * 100}%` }} />
            ))}
          </div>
        </div>

        {/* Right: Forecast Repository */}
        <div className="flex-1 flex flex-col justify-center pl-1">
          <span className="text-label font-bold text-muted-foreground uppercase tracking-widest mb-2 block">Repository</span>
          
          <div className="flex flex-col gap-1.5">
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">ID:</span><span className="text-primary-metric text-foreground truncate max-w-[80px]">{repo.forecastId}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Ver:</span><span className="text-primary-metric text-foreground">{repo.version}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Verif:</span><span className="text-primary-metric text-warning">{repo.verification}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Replay:</span><span className="text-primary-metric text-success">{repo.replay}</span></div>
            <div className="flex justify-between items-center"><span className="text-label text-muted-foreground">Stored:</span><span className="text-primary-metric text-foreground truncate max-w-[80px]">{repo.stored}</span></div>
          </div>
        </div>

      </div>
    </BaseCard>
  );
};
export default TrustAndRepository;
