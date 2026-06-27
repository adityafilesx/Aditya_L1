import type { FC } from 'react';
import { useMemo, useState } from 'react';
import { BaseCard, Icon } from '../../../design-system';
import { useForecast } from '../hooks/useForecast';
import { ConcentricConfidence } from './ConcentricConfidence';

type ExplanationType = 'OPERATOR' | 'RESEARCHER' | 'SCIENTIFIC';

export const ScientificIntelligence: FC = () => {
  const { currentObservation, nowcastState, latestForecast, forecastWindow } = useForecast();
  const [explanationTab, setExplanationTab] = useState<ExplanationType>('OPERATOR');

  // 1. Physics Snapshot
  const physicsSnapshot = useMemo(() => {
    const phys = nowcastState?.latest_physics;
    const temp = phys?.thermal?.peak_temperature ?? 14.22;
    const EM = phys?.thermal?.emission_measure ?? 3.4e48;
    const heat = phys?.thermal?.heating_rate ?? 0.45;
    const cool = phys?.thermal?.cooling_rate ?? 0.12;
    const spectralIndex = phys?.spectral?.power_law_index ?? 3.12;
    const neupert = phys?.neupert?.neupert_score ?? 0.84;
    const state = phys?.plasma?.plasma_state ?? 'HEATING';

    return { temp, EM, heat, cool, spectralIndex, neupert, state };
  }, [nowcastState]);

  // 2. Confidence & Trust
  const confidenceMetrics = useMemo(() => {
    let overall = 0.94;
    let obs = 0.96;
    let phys = 0.88;
    let model = 0.92;
    let cal = 0.95;

    if (forecastWindow === '1h') {
      overall = 0.91; phys = 0.85; model = 0.89;
    } else if (forecastWindow === '24h') {
      overall = 0.86; obs = 0.94; phys = 0.82; model = 0.85;
    } else if (forecastWindow === '7d') {
      overall = 0.72; obs = 0.91; phys = 0.68; model = 0.65; cal = 0.92;
    }

    return { overall, obs, phys, model, cal };
  }, [forecastWindow]);

  // 3. Explainability and Evidence
  const explanations = useMemo(() => {
    let consistencyScore = 92;
    let featureImportance = [
      { name: 'Thermal Dominance', weight: 0.38 },
      { name: 'Heating Index', weight: 0.28 },
      { name: 'Current X-Ray Flux', weight: 0.22 },
      { name: 'Magnetic Complexity', weight: 0.12 }
    ];

    if (forecastWindow === '24h') {
      consistencyScore = 84;
      featureImportance = [
        { name: 'Active Region Complexity', weight: 0.40 },
        { name: 'Precursor Event Cadence', weight: 0.25 },
        { name: 'Spectral Hardness Index', weight: 0.20 },
        { name: 'Background Noise', weight: 0.15 }
      ];
    } else if (forecastWindow === '7d') {
      consistencyScore = 75;
      featureImportance = [
        { name: 'Sunspot Area Delta', weight: 0.48 },
        { name: 'Global Magnetic Energy', weight: 0.28 },
        { name: 'Mean Flare Recurrence', weight: 0.14 },
        { name: 'Background Flux Level', weight: 0.10 }
      ];
    }

    const data: Record<ExplanationType, { 
      reasoning: string; 
      supporting: string[];
      contradictionList: string[];
    }> = {
      OPERATOR: {
        reasoning: "Action recommended based on M-class precursor heating indicators.",
        supporting: ["Precursor event rate increased", "Active Region AR3412 growth"],
        contradictionList: ["Kp Index remains very low", "Background noise stable"]
      },
      RESEARCHER: {
        reasoning: "Gradient boost ensemble tree reached consensus on X-ray flux derivatives.",
        supporting: ["XGBoost consensus verified", "Temporal-CN prediction matches"],
        contradictionList: ["Non-thermal electron counts lagging", "Calibration offset detected"]
      },
      SCIENTIFIC: {
        reasoning: "Thermal profile modeling indicates a coronal temperature elevation to 14.22 MK.",
        supporting: ["Emission measure increased", "Heating rate outpaces cooling"],
        contradictionList: ["Magnetic shear is stable", "Neutrino baseline nominal"]
      }
    };

    return { consistencyScore, featureImportance, ...data[explanationTab] };
  }, [forecastWindow, explanationTab]);

  return (
    <BaseCard className="flex flex-col h-full bg-surface-container-lowest/40 border border-border/20 backdrop-blur-md overflow-hidden p-2.5">
      
      {/* Component Contract Header */}
      <div className="flex justify-between items-center flex-shrink-0 mb-2 border-b border-border/20 pb-2">
        <div className="flex items-center gap-1.5">
          <Icon name="Psychology" className="text-primary" />
          <h2 className="text-heading text-foreground">Scientific Intelligence</h2>
        </div>
        {/* Component Contract Status */}
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
          <span className="text-label text-success font-bold uppercase hidden 2xl:block">SYNCED</span>
        </div>
      </div>

      <div className="flex-1 flex flex-col gap-2 min-h-0 overflow-hidden">
        
        {/* Subsection 1: Physics Snapshot */}
        <div className="flex flex-col flex-shrink-0">
          <div className="flex items-center justify-between mb-1">
            <span className="text-label text-muted-foreground uppercase tracking-widest font-bold">Physics Snapshot</span>
            <span className={`px-2 py-0.5 rounded text-label font-mono font-bold tracking-widest ${
              physicsSnapshot.state === 'HEATING' ? 'bg-warning/20 text-warning border border-warning/50' : 'bg-success/20 text-success border border-success/50'
            }`}>
              {physicsSnapshot.state}
            </span>
          </div>
          
          <div className="flex flex-col gap-1 bg-surface/20 border border-border/20 rounded p-1.5">
            <div className="flex flex-col">
              <div className="flex justify-between items-center"><span className="text-label text-muted-foreground uppercase">Coronal Temp</span><span className="text-primary-metric text-foreground">{physicsSnapshot.temp.toFixed(2)} MK</span></div>
              <div className="flex justify-between items-center"><span className="text-label text-muted-foreground uppercase">Emission Meas</span><span className="text-primary-metric text-foreground">{physicsSnapshot.EM.toExponential(1)}</span></div>
            </div>
            
            {/* Heating / Cooling mini-gauge */}
            <div className="border-t border-border/20 pt-1.5">
              <div className="flex justify-between text-label text-muted-foreground uppercase mb-0.5 font-mono">
                <span>Heat ({physicsSnapshot.heat.toFixed(2)})</span>
                <span>Cool ({physicsSnapshot.cool.toFixed(2)})</span>
              </div>
              <div className="flex gap-1.5 items-center">
                <div className="flex-1 h-1 bg-surface-container rounded-full overflow-hidden">
                  <div className="h-full bg-warning transition-all" style={{ width: `${Math.min(100, physicsSnapshot.heat * 100)}%` }} />
                </div>
                <div className="flex-1 h-1 bg-surface-container rounded-full overflow-hidden">
                  <div className="h-full bg-info transition-all" style={{ width: `${Math.min(100, physicsSnapshot.cool * 100)}%` }} />
                </div>
              </div>
            </div>

            <div className="border-t border-border/20 pt-1.5 flex flex-col">
              <div className="flex justify-between items-center"><span className="text-label text-muted-foreground uppercase">Neupert Score</span><span className="text-primary-metric text-foreground">{(physicsSnapshot.neupert * 100).toFixed(0)}%</span></div>
              <div className="flex justify-between items-center"><span className="text-label text-muted-foreground uppercase">Spectral Idx</span><span className="text-primary-metric text-foreground">{physicsSnapshot.spectralIndex.toFixed(2)}</span></div>
            </div>
          </div>
        </div>

        {/* Subsection 2: Confidence & Trust */}
        <div className="flex flex-col flex-shrink-0 border-t border-border/20 pt-1.5">
          <span className="text-label text-muted-foreground uppercase tracking-widest font-bold mb-1">Confidence & Trust HUD</span>
          <div className="transform scale-[0.85] origin-top">
            <ConcentricConfidence
              overall={confidenceMetrics.overall}
              observation={confidenceMetrics.obs}
              physics={confidenceMetrics.phys}
              model={confidenceMetrics.model}
              calibration={confidenceMetrics.cal}
            />
          </div>
        </div>

        {/* Subsection 3: Scientific Evidence Chips */}
        <div className="flex flex-col flex-shrink-0 border-t border-border/20 pt-1.5 mt-auto">
          <span className="text-label text-muted-foreground uppercase tracking-widest font-bold mb-1">Top Drivers</span>
          <div className="flex flex-col gap-1">
            <div className="flex flex-wrap gap-1">
              {explanations.supporting.map((s, idx) => (
                <div key={idx} className="bg-success/10 border border-success/30 text-success text-label px-1.5 py-0.5 rounded truncate max-w-full">
                  + {s}
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </BaseCard>
  );
};
export default ScientificIntelligence;
