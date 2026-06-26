import React from 'react';
import { BaseCard, Icon } from '@design-system/index';

export const ExplainableAiWorkspace: React.FC = () => {
  return (
    <div className="absolute inset-0 overflow-y-auto p-8 bg-surface-container-lowest">
      <div className="max-w-5xl mx-auto space-y-6">
        <div>
          <h1 className="font-display-md text-[24px] font-bold text-on-surface">Explainable AI Engine (XAI)</h1>
          <p className="font-body-lg text-on-surface-variant mt-2">
            Transparent analysis of model predictions, feature importance, and counterfactuals.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <BaseCard variant="plain" title="Global Feature Importance (SHAP)" icon="bar_chart" className="shadow-sm">
            <div className="h-64 flex flex-col justify-center items-center text-on-surface-variant border border-dashed border-outline-variant mt-4 rounded-lg bg-surface-bright">
              <Icon name="insert_chart" className="text-[48px] opacity-20 mb-2" />
              <div className="font-label-caps uppercase text-[12px] opacity-60">SHAP Summary Plot Placeholder</div>
            </div>
          </BaseCard>

          <BaseCard variant="plain" title="Local Prediction Explanation" icon="troubleshoot" className="shadow-sm">
            <div className="space-y-4 mt-4">
              <div className="p-3 bg-surface-bright border border-surface-variant rounded-lg">
                <div className="font-label-caps text-[10px] uppercase text-on-surface-variant mb-1">Target Event</div>
                <div className="font-body-sm font-bold text-on-surface">M-Class Flare Probability: 85%</div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-24 font-data-mono text-[10px] text-on-surface-variant truncate">Magnetic Shear</div>
                  <div className="flex-1 h-2 bg-surface-container rounded overflow-hidden">
                    <div className="h-full bg-error" style={{ width: '65%' }} />
                  </div>
                  <div className="w-8 font-numeric-telemetry text-[10px] text-right">+0.32</div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-24 font-data-mono text-[10px] text-on-surface-variant truncate">Temperature</div>
                  <div className="flex-1 h-2 bg-surface-container rounded overflow-hidden">
                    <div className="h-full bg-error" style={{ width: '45%' }} />
                  </div>
                  <div className="w-8 font-numeric-telemetry text-[10px] text-right">+0.15</div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-24 font-data-mono text-[10px] text-on-surface-variant truncate">Area (MH)</div>
                  <div className="flex-1 h-2 bg-surface-container rounded overflow-hidden">
                    <div className="h-full bg-primary" style={{ width: '20%' }} />
                  </div>
                  <div className="w-8 font-numeric-telemetry text-[10px] text-right">-0.08</div>
                </div>
              </div>
            </div>
          </BaseCard>
          
          <BaseCard variant="plain" title="Counterfactual Analysis" icon="alt_route" className="shadow-sm md:col-span-2">
            <div className="flex items-center justify-between p-4 bg-surface-container-low border border-surface-variant rounded-xl mt-4">
              <div className="flex-1 text-center">
                <div className="font-body-sm text-on-surface-variant">Original Prediction</div>
                <div className="font-display-sm font-bold text-error mt-1">M-Class (85%)</div>
                <div className="font-data-mono text-[11px] text-on-surface-variant mt-2">Shear = 45°</div>
              </div>
              <div className="px-4 text-outline-variant">
                <Icon name="arrow_forward" className="text-[24px]" />
              </div>
              <div className="flex-1 text-center">
                <div className="font-body-sm text-on-surface-variant">Counterfactual Prediction</div>
                <div className="font-display-sm font-bold text-[#10b981] mt-1">C-Class (92%)</div>
                <div className="font-data-mono text-[11px] text-on-surface-variant mt-2 bg-[#10b981]/10 px-2 py-1 rounded inline-block text-[#10b981]">If Shear was &lt; 30°</div>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </div>
  );
};
