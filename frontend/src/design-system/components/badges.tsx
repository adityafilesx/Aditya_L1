import React from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';

export interface BaseBadgeProps {
  title?: string;
  subtitle?: string;
  children?: React.ReactNode;
  className?: string;
  variant?: 'nominal' | 'success' | 'warning' | 'degraded' | 'critical' | 'error' | 'offline' | 'live' | 'primary' | 'secondary' | 'info';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  status?: string;
  icon?: string;
  badge?: React.ReactNode;
  animation?: boolean;
}

const sizeClasses = {
  sm: 'px-2 py-0.5 text-[10px]',
  md: 'px-3 py-1 text-[11px]',
  lg: 'px-4 py-1.5 text-xs',
};

const variantClasses = {
  success: 'bg-green-500/10 text-green-600 border-green-500/20',
  nominal: 'bg-primary-container/10 text-primary border-primary-container/20',
  primary: 'bg-primary-container/10 text-primary border-primary-container/20',
  secondary: 'bg-secondary-container/10 text-secondary-container border-secondary-container/20',
  warning: 'bg-yellow-500/10 text-yellow-600 border-yellow-500/20',
  degraded: 'bg-yellow-500/10 text-yellow-600 border-yellow-500/20',
  critical: 'bg-red-500/10 text-red-600 border-red-500/20',
  error: 'bg-red-500/10 text-red-600 border-red-500/20',
  offline: 'bg-surface-container-highest text-on-surface-variant border-outline-variant',
  live: 'bg-green-500/10 text-green-600 border-green-500/20',
  info: 'bg-primary-container/10 text-primary border-primary-container/20',
};

export const BaseBadge: React.FC<BaseBadgeProps> = ({
  title,
  children,
  className,
  variant = 'nominal',
  size = 'sm',
  loading,
  disabled,
  icon,
  animation,
}) => {
  const content = children || title;

  return (
    <span
      className={cn(
        'rounded-full font-label-caps inline-flex items-center gap-1.5 border leading-none',
        sizeClasses[size],
        variantClasses[variant],
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
    >
      {loading && (
        <span className="material-symbols-outlined animate-spin text-[10px]">
          progress_activity
        </span>
      )}
      {!loading && variant === 'live' && (
        <span
          className={cn(
            'w-1.5 h-1.5 rounded-full bg-green-500',
            animation !== false && 'telemetry-blink'
          )}
        />
      )}
      {!loading && icon && (
        <Icon name={icon} className="text-[12px] leading-none" />
      )}
      {content}
    </span>
  );
};

export const StatusBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge {...props} />
);

export const HealthBadge: React.FC<BaseBadgeProps> = ({ status, ...props }) => {
  let variant: BaseBadgeProps['variant'] = 'nominal';
  if (status === 'DEGRADED' || status === 'warning') variant = 'warning';
  if (status === 'CRITICAL' || status === 'critical' || status === 'error') variant = 'critical';
  if (status === 'OFFLINE' || status === 'offline') variant = 'offline';
  return <BaseBadge variant={variant} {...props} />;
};

export const RiskBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="warning" {...props} />
);

export const MissionBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="nominal" {...props} />
);

export const TelemetryBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="live" {...props} />
);

export const ConfidenceBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="nominal" {...props} />
);

export const SeverityBadge: React.FC<BaseBadgeProps> = ({ status, ...props }) => {
  let variant: BaseBadgeProps['variant'] = 'info';
  const normStatus = String(status || props.children || '').toUpperCase();
  if (normStatus === 'WARNING' || normStatus === 'MAINTENANCE') variant = 'warning';
  if (normStatus === 'CRITICAL' || normStatus === 'EMERGENCY' || normStatus === 'ERROR') variant = 'critical';
  if (normStatus === 'OK' || normStatus === 'NOMINAL' || normStatus === 'LIVE') variant = 'success';
  if (normStatus === 'OFFLINE') variant = 'offline';
  return <BaseBadge variant={variant} {...props} />;
};

export const ModelBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="nominal" {...props} />
);

export const SensorBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="nominal" {...props} />
);

export const DeploymentBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="nominal" {...props} />
);

export const PhysicsBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="secondary" {...props} />
);

export const PredictionBadge: React.FC<BaseBadgeProps> = (props) => (
  <BaseBadge variant="nominal" {...props} />
);
