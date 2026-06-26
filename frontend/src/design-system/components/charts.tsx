import React from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';

export interface ChartContainerProps {
  title?: string;
  subtitle?: string;
  children?: React.ReactNode;
  className?: string;
  loading?: boolean;
  error?: string | boolean;
  empty?: string | boolean;
  timeRange?: string;
  timeRangeOptions?: string[];
  onTimeRangeChange?: (val: string) => void;
  onRefresh?: () => void;
  onFullscreen?: () => void;
  onExport?: () => void;
  actions?: React.ReactNode;
  legend?: React.ReactNode;
  footer?: React.ReactNode;
}

export const ChartContainer: React.FC<ChartContainerProps> = ({
  title,
  subtitle,
  children,
  className,
  loading = false,
  error = false,
  empty = false,
  timeRange = 'L-24H',
  timeRangeOptions = ['L-24H', 'L-6H', 'L-1H'],
  onTimeRangeChange,
  onRefresh,
  onFullscreen,
  onExport,
  actions,
  legend,
  footer,
}) => {
  return (
    <div className={cn('bento-card flex flex-col', className)}>
      {(title || subtitle || onRefresh || onFullscreen || onExport || actions) && (
        <div className="p-6 border-b border-outline-variant flex justify-between items-center">
          <div>
            {title && <h3 className="font-headline-md text-headline-md text-on-surface">{title}</h3>}
            {subtitle && <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{subtitle}</p>}
          </div>
          <div className="flex items-center gap-2">
            {actions}
            {onExport && (
              <button
                type="button"
                onClick={onExport}
                className="p-2 hover:bg-surface-container-high rounded transition-colors"
                title="Export Chart"
              >
                <Icon name="export_notes" className="text-on-surface-variant" />
              </button>
            )}
            {onRefresh && (
              <button
                type="button"
                onClick={onRefresh}
                className="p-2 hover:bg-surface-container-high rounded transition-colors"
                title="Refresh Data"
              >
                <Icon name="refresh" className="text-on-surface-variant" />
              </button>
            )}
            {onFullscreen && (
              <button
                type="button"
                onClick={onFullscreen}
                className="p-2 hover:bg-surface-container-high rounded transition-colors"
                title="Fullscreen Mode"
              >
                <Icon name="fullscreen" className="text-on-surface-variant" />
              </button>
            )}
            {onTimeRangeChange && timeRangeOptions && (
              <>
                <div className="h-8 w-px bg-outline-variant mx-1"></div>
                <select
                  value={timeRange}
                  onChange={(e) => onTimeRangeChange?.(e.target.value)}
                  className="bg-surface-container-low border border-outline-variant rounded font-label-caps text-label-caps px-3 py-1 outline-none cursor-pointer"
                >
                  {timeRangeOptions.map((opt) => (
                    <option key={opt} value={opt}>
                      {opt}
                    </option>
                  ))}
                </select>
              </>
            )}
          </div>
        </div>
      )}

      <div className="flex-1 min-h-[300px] relative overflow-hidden flex items-center justify-center bg-slate-50">
        {loading && <ChartLoading />}
        {!loading && error && <ChartError message={typeof error === 'string' ? error : undefined} />}
        {!loading && !error && empty && <ChartEmpty message={typeof empty === 'string' ? empty : undefined} />}
        {!loading && !error && !empty && children}
      </div>

      {legend && <div className="p-4 border-t border-outline-variant/30">{legend}</div>}
      {footer && <div className="px-6 py-4 bg-surface-container-low border-t border-outline-variant/30">{footer}</div>}
    </div>
  );
};

export const ChartToolbar: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <div className={cn('flex items-center gap-2 p-2 bg-surface-container-low rounded-lg border border-outline-variant', className)}>
    {children}
  </div>
);

export const ChartLegend: React.FC<{ items: { label: string; color: string }[]; className?: string }> = ({
  items,
  className,
}) => (
  <div className={cn('flex flex-wrap gap-4 text-xs font-label-caps text-on-surface-variant', className)}>
    {items.map((item, idx) => (
      <div key={idx} className="flex items-center gap-1.5">
        <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ backgroundColor: item.color }} />
        <span>{item.label}</span>
      </div>
    ))}
  </div>
);

export const ChartFooter: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <div className={cn('text-[11px] text-on-surface-variant/60 font-data-mono', className)}>{children}</div>
);

export const ChartLoading: React.FC = () => (
  <div className="animate-pulse flex flex-col items-center justify-center gap-3">
    <div className="w-12 h-12 rounded-full border-4 border-primary border-t-transparent animate-spin"></div>
    <span className="font-label-caps text-[11px] text-primary">Loading telemetry stream...</span>
  </div>
);

export const ChartEmpty: React.FC<{ message?: string }> = ({ message = 'No data points available.' }) => (
  <div className="text-center">
    <Icon name="insert_chart" className="text-on-surface-variant/30 text-5xl mb-2" />
    <p className="font-label-caps text-label-caps text-on-surface-variant">{message}</p>
  </div>
);

export const ChartError: React.FC<{ message?: string }> = ({ message = 'Failed to load telemetry stream.' }) => (
  <div className="text-center p-6 bg-error/5 border border-error/20 rounded-xl">
    <Icon name="error" className="text-error text-5xl mb-2" />
    <p className="font-label-caps text-label-caps text-error">{message}</p>
  </div>
);

export const ChartExport: React.FC<{ onExport: (format: 'csv' | 'json' | 'png') => void }> = ({ onExport }) => (
  <div className="flex gap-2">
    <button onClick={() => onExport('csv')} className="px-2 py-1 bg-surface-container rounded text-[10px] font-bold">CSV</button>
    <button onClick={() => onExport('json')} className="px-2 py-1 bg-surface-container rounded text-[10px] font-bold">JSON</button>
    <button onClick={() => onExport('png')} className="px-2 py-1 bg-surface-container rounded text-[10px] font-bold">PNG</button>
  </div>
);
