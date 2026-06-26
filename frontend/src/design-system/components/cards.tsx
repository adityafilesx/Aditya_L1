import React from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';

export interface BaseCardProps {
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  icon?: string;
  status?: 'nominal' | 'success' | 'warning' | 'degraded' | 'critical' | 'error' | 'offline' | string;
  value?: React.ReactNode;
  trend?: React.ReactNode;
  badge?: React.ReactNode;
  actions?: React.ReactNode;
  footer?: React.ReactNode;
  loading?: boolean;
  error?: boolean | string;
  empty?: boolean | string;
  children?: React.ReactNode;
  className?: string;
  variant?: 'bento' | 'glass' | 'panel' | 'lab' | 'plain';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  animation?: boolean;
}

export const BaseCard: React.FC<BaseCardProps> = ({
  title,
  subtitle,
  icon,
  status,
  value,
  trend,
  badge,
  actions,
  footer,
  loading = false,
  error = false,
  empty = false,
  children,
  className,
  variant = 'bento',
  size = 'md',
  disabled = false,
}) => {
  const cardClasses = {
    bento: 'bento-card',
    glass: 'glass-card',
    panel: 'glass-panel',
    lab: 'lab-card',
    plain: 'bg-white rounded-card border border-card-border',
  };

  const getStatusColor = (s?: string) => {
    if (!s) return '';
    const norm = s.toLowerCase();
    if (norm === 'nominal' || norm === 'success' || norm === 'ok' || norm === 'active') return 'bg-success';
    if (norm === 'warning' || norm === 'degraded' || norm === 'lag') return 'bg-warning';
    if (norm === 'critical' || norm === 'error' || norm === 'danger') return 'bg-critical';
    if (norm === 'offline') return 'bg-surface-dim';
    return '';
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-surface-container-highest rounded w-1/3"></div>
          <div className="h-8 bg-surface-container-highest rounded w-2/3"></div>
          <div className="h-3 bg-surface-container-highest rounded w-1/2"></div>
        </div>
      );
    }

    if (error) {
      return (
        <div className="flex flex-col items-center justify-center text-center py-6">
          <Icon name="warning" className="text-critical text-3xl mb-2" />
          <p className="text-body-sm font-semibold text-on-surface">Error Loading Data</p>
          <p className="text-[11px] text-on-surface-variant/60">{typeof error === 'string' ? error : 'Unable to load telemetry.'}</p>
        </div>
      );
    }

    if (empty) {
      return (
        <div className="flex flex-col items-center justify-center text-center py-6">
          <Icon name="inbox" className="text-on-surface-variant/40 text-3xl mb-2" />
          <p className="text-body-sm font-semibold text-on-surface-variant/60">No Data Available</p>
          <p className="text-[11px] text-on-surface-variant/40">{typeof empty === 'string' ? empty : 'No telemetry points available.'}</p>
        </div>
      );
    }

    return (
      <>
        {/* Metric Header / Standard layout */}
        {value !== undefined ? (
          <div>
            <div className="flex justify-between items-start mb-2">
              <span className="font-label-caps text-label-caps text-on-surface-variant block">
                {title}
              </span>
              {icon && <Icon name={icon} className="text-secondary opacity-50" />}
              {status && <span className={cn('w-2 h-2 rounded-full', getStatusColor(status))} />}
            </div>
            <div className="font-numeric-telemetry text-numeric-telemetry text-primary font-bold">
              {value}
            </div>
            {trend && <div className="text-[11px] text-on-surface-variant/60 mt-1">{trend}</div>}
          </div>
        ) : (
          children
        )}
      </>
    );
  };

  const hasStandardHeader = value === undefined && (title || subtitle || icon || actions || status);

  return (
    <div
      className={cn(
        cardClasses[variant],
        size === 'sm' && 'p-4',
        size === 'md' && 'p-6',
        size === 'lg' && 'p-8',
        disabled && 'opacity-60 cursor-not-allowed',
        className
      )}
    >
      {hasStandardHeader && !loading && !error && !empty && (
        <div className="flex justify-between items-start mb-4">
          <div>
            {title && (
              <h3 className={cn(
                typeof title === 'string' ? 'font-headline-md text-headline-md text-on-surface' : ''
              )}>
                {title}
              </h3>
            )}
            {subtitle && (
              <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
                {subtitle}
              </p>
            )}
          </div>
          <div className="flex items-center gap-2">
            {badge}
            {status && <span className={cn('w-2 h-2 rounded-full inline-block', getStatusColor(status))} />}
            {icon && <Icon name={icon} className="text-on-surface-variant opacity-75" />}
            {actions}
          </div>
        </div>
      )}

      {renderContent()}

      {footer && !loading && !error && !empty && (
        <div className="mt-4 pt-4 border-t border-outline-variant/30 flex justify-between items-center text-body-sm text-on-surface-variant">
          {footer}
        </div>
      )}
    </div>
  );
};

export const MetricCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="bento" size="sm" {...props} />
);

export const LargeMetricCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="bento" size="md" {...props} />
);

export const StatusCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="glass" {...props} />
);

export const MissionCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="bento" {...props} />
);

export const PhysicsCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="lab" {...props} />
);

export const SensorCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="glass" {...props} />
);

export const ResearchCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="bento" {...props} />
);

export const AlertCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="glass" {...props} />
);

export const PredictionCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="glass" {...props} />
);

export const TimelineCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="bento" {...props} />
);

export const ModelCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="bento" {...props} />
);

export const RecommendationCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="glass" {...props} />
);

export const ComparisonCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="bento" {...props} />
);

export const InformationCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="glass" {...props} />
);

export const SummaryCard: React.FC<BaseCardProps> = (props) => (
  <BaseCard variant="panel" {...props} />
);
