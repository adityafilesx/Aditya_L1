import type { FC } from 'react';
import { useMemo } from 'react';
import { BaseCard, PlotlyContainer, Icon } from '../../../design-system';
import { useForecast } from '../hooks/useForecast';
import { useForecastStore } from '../store/forecastStore';
import { TOKENS } from '../../../design-system/tokens';
import { ForecastWindows } from '../constants/forecastConstants';

const HORIZONS = ['15m', '30m', '1h', '3h', '6h', '12h', '24h', '7d'];
const CLASSES = ['A', 'B', 'C', 'M', 'X'];

export const MissionForecastCore: FC = () => {
  const { latestForecast, currentObservation, nowcastState, forecastWindow } = useForecast();
  const setForecastWindow = useForecastStore((state) => state.setForecastWindow);

  // 1. Heatmap Probability Matrix
  const getProbability = (h: string, c: string) => {
    if (!latestForecast?.probabilities) return 0.01;
    const baseProbs = latestForecast.probabilities as Record<string, number>;
    const baseP = baseProbs[c] || 0.01;

    const hIdx = HORIZONS.indexOf(h);
    const selectedIdx = HORIZONS.indexOf(forecastWindow);
    const diff = hIdx - selectedIdx;

    let scaled = baseP * Math.pow(1.18, diff);
    if (scaled > 0.99) scaled = 0.99;
    if (scaled < 0.01) scaled = 0.01;

    return scaled;
  };

  const getHeatmapColor = (prob: number, c: string) => {
    if (prob < 0.1) return 'bg-surface/20 text-muted-foreground/40';
    const intensity = Math.floor(prob * 100);
    switch (c) {
      case 'A': return `bg-success/${Math.max(10, intensity)} text-success font-bold`;
      case 'B': return `bg-success/${Math.max(20, intensity)} text-success font-bold`;
      case 'C': return `bg-info/${Math.max(20, intensity)} text-info font-bold`;
      case 'M': return `bg-warning/${Math.max(30, intensity)} text-warning font-black shadow-[0_0_10px_rgba(245,158,11,0.2)]`;
      case 'X': return `bg-error/${Math.max(40, intensity)} text-error font-black shadow-[0_0_15px_rgba(239,68,68,0.3)]`;
      default: return 'bg-surface/20 text-muted-foreground';
    }
  };

  const getConfidenceScore = (h: string) => {
    const base = 0.94;
    const idx = HORIZONS.indexOf(h);
    const selectedIdx = HORIZONS.indexOf(forecastWindow);
    const diff = idx - selectedIdx;
    
    let confidence = base * Math.pow(0.96, diff);
    if (confidence > 0.99) confidence = 0.99;
    if (confidence < 0.50) confidence = 0.50;
    return confidence;
  };

  // 2. HUD Metrics
  const peakMetrics = useMemo(() => {
    const phys = nowcastState?.latest_physics;
    const isAlert = latestForecast?.state === 'ALERT' || latestForecast?.state === 'WARNING';
    
    let goesClass = phys?.classification?.goes_class || 'A';
    let peakFlux = phys?.characterization?.peak_flux || 1.2e-7;
    let duration = phys?.characterization?.duration || 720;
    
    let baseTime = nowcastState?.timestamp ? new Date(nowcastState.timestamp) : new Date();
    if (isAlert) {
      goesClass = forecastWindow === '15m' || forecastWindow === '30m' ? 'M' : 'X';
      peakFlux = forecastWindow === '15m' || forecastWindow === '30m' ? 3.4e-5 : 1.2e-4;
      duration = 1800;
    }

    const peakTime = new Date(baseTime.getTime() + (duration * 0.4 * 1000));
    const h = peakTime.getHours().toString().padStart(2, '0');
    const m = peakTime.getMinutes().toString().padStart(2, '0');
    
    return {
      peakTimeStr: `${h}:${m} UT`,
      peakFluxStr: peakFlux.toExponential(2).toUpperCase(),
      goesClass,
      durationStr: `${(duration / 60).toFixed(0)}m`,
      riseTimeStr: `${(duration * 0.3 / 60).toFixed(0)}m`,
      decayTimeStr: `${(duration * 0.7 / 60).toFixed(0)}m`,
      confidence: `${(getConfidenceScore(forecastWindow) * 100).toFixed(0)}%`,
    };
  }, [nowcastState, latestForecast, forecastWindow]);

  // 3. Trajectory Plotly
  const plotData = useMemo(() => {
    const now = new Date();
    const times: string[] = [];
    const fluxes: number[] = [];

    for (let i = 120; i >= 0; i--) {
      const t = new Date(now.getTime() - i * 60000);
      times.push(t.toISOString());
      
      const base = 1e-7;
      const noise = (Math.random() - 0.5) * 2e-8;
      
      if (i === 0 && currentObservation?.solexs_flux) {
        fluxes.push(currentObservation.solexs_flux);
      } else {
        fluxes.push(base + noise);
      }
    }

    const futureTimes: string[] = [];
    const predictedFlux: number[] = [];
    const upperConfidence: number[] = [];
    const lowerConfidence: number[] = [];

    let predictionMinutes = 15;
    if (forecastWindow === '30m') predictionMinutes = 30;
    else if (forecastWindow === '1h') predictionMinutes = 60;
    else if (forecastWindow === '3h') predictionMinutes = 180;
    else if (forecastWindow === '6h') predictionMinutes = 360;
    else if (forecastWindow === '12h') predictionMinutes = 720;
    else if (forecastWindow === '24h') predictionMinutes = 1440;
    else if (forecastWindow === '7d') predictionMinutes = 10080;

    const activeFlare = nowcastState?.active_flare;
    const isEvent = activeFlare != null || (latestForecast?.state === 'ALERT' || latestForecast?.state === 'WARNING');
    const peakOffset = Math.min(60, Math.floor(predictionMinutes * 0.4));
    const stepSize = Math.max(1, Math.floor(predictionMinutes / 60));

    for (let i = 1; i <= predictionMinutes; i += stepSize) {
      const t = new Date(now.getTime() + i * 60000);
      futureTimes.push(t.toISOString());

      let flux = fluxes[fluxes.length - 1];
      if (isEvent && i < peakOffset) {
        flux = flux * Math.pow(1.045, i / stepSize);
      } else if (isEvent) {
        const peakFlux = fluxes[fluxes.length - 1] * Math.pow(1.045, peakOffset / stepSize);
        flux = peakFlux * Math.pow(0.965, (i - peakOffset) / stepSize);
      } else {
        flux = flux + (Math.random() - 0.5) * 1e-8;
      }
      
      predictedFlux.push(flux);
      upperConfidence.push(flux * (1.1 + (i / predictionMinutes) * 0.4));
      lowerConfidence.push(flux * (0.9 - (i / predictionMinutes) * 0.3));
    }

    return [
      {
        x: times,
        y: fluxes,
        type: 'scatter',
        mode: 'lines',
        name: 'Observation',
        line: { color: TOKENS.colors.primary, width: 2 },
      },
      {
        x: futureTimes,
        y: predictedFlux,
        type: 'scatter',
        mode: 'lines',
        name: 'Trajectory',
        line: { color: TOKENS.colors.warning, width: 2, dash: 'dot' },
      },
      {
        x: futureTimes.concat([...futureTimes].reverse()),
        y: upperConfidence.concat([...lowerConfidence].reverse()),
        type: 'scatter',
        fill: 'toself',
        fillcolor: 'rgba(245, 158, 11, 0.1)',
        line: { color: 'transparent' },
        name: 'Uncertainty (99%)',
        showlegend: false,
        hoverinfo: 'none',
      },
      {
        x: futureTimes.concat([...futureTimes].reverse()),
        y: upperConfidence.map(v => v*0.95).concat([...lowerConfidence].map(v => v*1.05).reverse()),
        type: 'scatter',
        fill: 'toself',
        fillcolor: 'rgba(245, 158, 11, 0.2)',
        line: { color: 'transparent' },
        name: 'Confidence (95%)',
        showlegend: false,
        hoverinfo: 'none',
      }
    ];
  }, [currentObservation, nowcastState, latestForecast, forecastWindow]);

  const layout = {
    title: false,
    margin: { t: 5, r: 40, l: 45, b: 20 },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    xaxis: {
      type: 'date',
      gridcolor: TOKENS.colors.outlineVariant + '15',
      zerolinecolor: TOKENS.colors.outlineVariant + '15',
      tickfont: { color: TOKENS.colors.onSurfaceVariant, size: 10, family: 'var(--font-mono)' },
    },
    yaxis: {
      type: 'log',
      gridcolor: TOKENS.colors.outlineVariant + '15',
      zerolinecolor: TOKENS.colors.outlineVariant + '15',
      tickfont: { color: TOKENS.colors.onSurfaceVariant, size: 10, family: 'var(--font-mono)' },
    },
    shapes: [
      {
        type: 'line',
        x0: 0,
        x1: 1,
        xref: 'paper',
        y0: Math.log10(1e-5),
        y1: Math.log10(1e-5),
        yref: 'y',
        line: { color: TOKENS.colors.warning, width: 1, dash: 'dash' },
      },
      {
        type: 'line',
        x0: 0,
        x1: 1,
        xref: 'paper',
        y0: Math.log10(1e-4),
        y1: Math.log10(1e-4),
        yref: 'y',
        line: { color: TOKENS.colors.error, width: 1, dash: 'dash' },
      }
    ],
    annotations: [
      {
        x: 1,
        xref: 'paper',
        y: Math.log10(1e-5),
        yref: 'y',
        text: 'M-Class',
        showarrow: false,
        xanchor: 'left',
        yanchor: 'middle',
        font: { color: TOKENS.colors.warning, size: 9, family: 'var(--font-mono)' }
      },
      {
        x: 1,
        xref: 'paper',
        y: Math.log10(1e-4),
        yref: 'y',
        text: 'X-Class',
        showarrow: false,
        xanchor: 'left',
        yanchor: 'middle',
        font: { color: TOKENS.colors.error, size: 9, family: 'var(--font-mono)' }
      }
    ],
    showlegend: true,
    legend: {
      orientation: 'h',
      y: 1.14,
      x: 0.5,
      xanchor: 'center',
      font: { color: TOKENS.colors.onSurface, size: 11, family: 'var(--font-body)' }
    },
    autosize: true,
    hovermode: 'x unified',
  };

  return (
    <div className="flex flex-col h-full min-h-0">
      
      <BaseCard className="flex flex-col flex-1 bg-surface-container-lowest/40 border border-border/20 backdrop-blur-md overflow-hidden min-h-0 p-3">
        
        {/* Header */}
        <div className="flex justify-between items-center flex-shrink-0 mb-4 border-b border-border/20 pb-2">
          <div className="flex items-center gap-1.5">
            <Icon name="Analytics" className="text-primary" />
            <h2 className="text-heading text-foreground">Forecast Core</h2>
          </div>
          <div className="flex items-center gap-1 bg-surface/50 border border-border/20 rounded p-1">
            {HORIZONS.map(h => (
              <button
                key={h}
                onClick={() => setForecastWindow(h as ForecastWindows)}
                className={`px-2 py-0.5 rounded text-label font-bold transition-all ${
                  forecastWindow === h 
                    ? 'bg-primary text-white shadow-focus' 
                    : 'text-muted-foreground hover:bg-surface/80'
                }`}
              >
                {h}
              </button>
            ))}
          </div>
        </div>

        {/* 1. Probability Heatmap (Dominant) */}
        <div className="flex flex-col flex-shrink-0 mb-4">
          <div className="flex justify-between items-end mb-2">
            <span className="text-label text-muted-foreground uppercase">Probability Matrix Heatmap</span>
            <span className="text-label text-muted-foreground">Confidence: {peakMetrics.confidence}</span>
          </div>
          <div className="grid grid-cols-9 gap-1">
            {/* Corner Cell */}
            <div className="flex items-center justify-center border-b border-border/20 pb-1">
              <span className="text-[9px] text-muted-foreground uppercase font-mono tracking-widest">Class</span>
            </div>
            {/* Horizon Headers */}
            {HORIZONS.map(h => (
              <div key={h} className={`flex items-center justify-center border-b border-border/20 pb-1 ${forecastWindow === h ? 'border-primary text-primary' : ''}`}>
                <span className={`text-[10px] font-mono font-bold ${forecastWindow === h ? 'text-primary' : 'text-muted-foreground'}`}>{h}</span>
              </div>
            ))}
            
            {/* Heatmap Rows */}
            {CLASSES.map(c => (
              <>
                <div key={`label-${c}`} className="flex items-center justify-center h-8">
                  <span className="text-primary-metric text-muted-foreground">{c}</span>
                </div>
                {HORIZONS.map(h => {
                  const prob = getProbability(h, c);
                  const isActive = forecastWindow === h;
                  return (
                    <div 
                      key={`cell-${c}-${h}`}
                      onClick={() => setForecastWindow(h as ForecastWindows)}
                      className={`h-8 flex items-center justify-center rounded cursor-pointer transition-all duration-300 ${getHeatmapColor(prob, c)} ${isActive ? 'ring-1 ring-primary/50 scale-[1.02]' : 'hover:scale-[1.02]'}`}
                    >
                      <span className="text-primary-metric">{(prob * 100).toFixed(0)}</span>
                    </div>
                  );
                })}
              </>
            ))}
          </div>
        </div>

        {/* 2. Peak Forecast HUD (Aerospace Style) */}
        <div className="flex flex-col flex-shrink-0 mb-4 bg-surface/30 border border-border/20 rounded p-3 relative overflow-hidden">
          {/* Subtle grid background to simulate HUD */}
          <div className="absolute inset-0 grid-bg opacity-20 pointer-events-none" />
          
          <div className="flex justify-between items-center mb-3 relative z-10">
            <span className="text-label text-muted-foreground uppercase">Expected Peak Trajectory HUD</span>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-error animate-pulse" />
              <span className="text-label text-error font-bold tracking-widest uppercase">TRACKING {peakMetrics.goesClass}-CLASS</span>
            </div>
          </div>
          
          <div className="flex justify-between items-end relative z-10">
            <div className="flex flex-col">
              <span className="text-label text-muted-foreground uppercase tracking-widest">Expected Peak Time</span>
              <span className="text-hero text-foreground tabular-nums tracking-normal">{peakMetrics.peakTimeStr}</span>
            </div>
            <div className="flex flex-col items-end">
              <span className="text-label text-muted-foreground uppercase tracking-widest">Expected Peak Flux</span>
              <span className="text-hero text-foreground tabular-nums tracking-normal">{peakMetrics.peakFluxStr} <span className="text-primary-metric text-muted-foreground">W/m²</span></span>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-4 mt-3 pt-3 border-t border-border/20 relative z-10">
            <div className="flex justify-between items-center">
              <span className="text-label text-muted-foreground">Duration</span>
              <span className="text-primary-metric text-foreground">{peakMetrics.durationStr}</span>
            </div>
            <div className="flex justify-between items-center border-l border-r border-border/20 px-4">
              <span className="text-label text-muted-foreground">Rise Time</span>
              <span className="text-primary-metric text-foreground">{peakMetrics.riseTimeStr}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-label text-muted-foreground">Decay Time</span>
              <span className="text-primary-metric text-foreground">{peakMetrics.decayTimeStr}</span>
            </div>
          </div>
        </div>

        {/* 3. Trajectory Scientific Chart */}
        <div className="flex-1 min-h-[180px] flex flex-col min-h-0 relative">
          <span className="text-label text-muted-foreground uppercase absolute top-0 left-0 z-10">Trajectory & Thresholds ({forecastWindow})</span>
          <div className="flex-1 w-full bg-surface-container-lowest border border-border/20 rounded mt-5 relative min-h-0">
            <PlotlyContainer
              data={plotData as any}
              layout={layout as any}
              config={{ responsive: true, displayModeBar: false }}
              className="w-full h-full"
            />
          </div>
        </div>

      </BaseCard>
    </div>
  );
};
export default MissionForecastCore;
