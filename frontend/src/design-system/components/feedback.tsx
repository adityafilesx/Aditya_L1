import React from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';

export interface FeedbackProps {
  title?: string;
  subtitle?: string;
  children?: React.ReactNode;
  variant?: 'info' | 'success' | 'warning' | 'critical' | 'error';
  className?: string;
  onClose?: () => void;
  actions?: React.ReactNode;
}

// 1. Alert (Inline banner card style)
export const Alert: React.FC<FeedbackProps> = ({
  title,
  subtitle,
  children,
  variant = 'info',
  className,
  onClose,
}) => {
  const variantStyles = {
    info: 'bg-primary-container/10 border-primary-container text-primary',
    success: 'bg-green-500/10 border-green-500 text-green-600',
    warning: 'bg-yellow-500/10 border-yellow-500 text-yellow-600',
    critical: 'bg-red-500/10 border-red-500 text-red-600',
    error: 'bg-red-500/10 border-red-500 text-red-600',
  };

  const icons = {
    info: 'info',
    success: 'check_circle',
    warning: 'construction',
    critical: 'emergency_home',
    error: 'warning',
  };

  return (
    <div className={cn('p-3 border-l-4 rounded flex gap-3 shadow-sm', variantStyles[variant], className)}>
      <Icon name={icons[variant]} className="text-[20px] shrink-0" />
      <div className="flex-1">
        {title && <p className="font-label-caps text-[10px] font-bold tracking-wider">{title.toUpperCase()}</p>}
        <p className="text-xs text-on-surface-variant mt-0.5">{children || subtitle}</p>
      </div>
      {onClose && (
        <button onClick={onClose} className="p-1 hover:bg-black/5 rounded">
          <Icon name="close" className="text-xs" />
        </button>
      )}
    </div>
  );
};

// 2. Toast
export const Toast: React.FC<FeedbackProps & { duration?: number }> = ({
  title,
  subtitle,
  variant = 'info',
  onClose,
  className,
}) => {
  return (
    <div className={cn('fixed bottom-6 right-6 bg-white border border-outline-variant rounded-lg shadow-lg p-4 max-w-sm flex items-start gap-3 z-[2000] animate-slide-in-right', className)}>
      <Alert title={title} subtitle={subtitle} variant={variant} onClose={onClose} className="border-none bg-transparent shadow-none p-0 flex-1" />
    </div>
  );
};

// 3. Notification
export const Notification: React.FC<FeedbackProps> = ({ title, subtitle, className }) => (
  <div className={cn('p-3 bg-surface-container-low border border-outline-variant/30 rounded-lg hover:bg-surface-container transition-colors', className)}>
    {title && <p className="text-xs font-bold text-on-surface">{title}</p>}
    {subtitle && <p className="text-[11px] text-on-surface-variant/80 mt-0.5">{subtitle}</p>}
  </div>
);

// 4. Snackbar
export const Snackbar: React.FC<FeedbackProps> = (props) => (
  <div className="fixed bottom-4 left-1/2 -translate-x-1/2 bg-inverse-surface text-inverse-on-surface px-4 py-2 rounded shadow-lg text-xs z-[2000] flex items-center gap-3">
    <span>{props.title || props.children}</span>
    {props.actions}
  </div>
);

// 5. LoadingOverlay
export const LoadingOverlay: React.FC<{ active: boolean }> = ({ active }) => {
  if (!active) return null;
  return (
    <div className="fixed inset-0 bg-black/30 backdrop-blur-xs flex items-center justify-center z-[3000]">
      <div className="bg-white p-6 rounded-xl border border-outline-variant shadow-xl flex flex-col items-center gap-3">
        <div className="w-10 h-10 border-4 border-primary border-t-transparent animate-spin rounded-full"></div>
        <span className="font-label-caps text-xs text-primary">System Synchronizing...</span>
      </div>
    </div>
  );
};

// 6. ProgressBar
export const ProgressBar: React.FC<{ value: number; max?: number; className?: string }> = ({
  value,
  max = 100,
  className,
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  return (
    <div className={cn('w-full bg-surface-container rounded-full h-2 overflow-hidden', className)}>
      <div className="bg-primary-container h-full transition-all duration-300" style={{ width: `${percentage}%` }} />
    </div>
  );
};

// 7. ProgressRing
export const ProgressRing: React.FC<{ value: number; size?: number; className?: string }> = ({
  value,
  size = 36,
  className,
}) => {
  const radius = size * 0.4;
  const stroke = size * 0.1;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (Math.min(value, 100) / 100) * circumference;

  return (
    <svg height={size} width={size} className={cn('transform -rotate-90', className)}>
      <circle
        stroke="var(--outline-variant)"
        fill="transparent"
        strokeWidth={stroke}
        r={normalizedRadius}
        cx={size / 2}
        cy={size / 2}
        className="opacity-20"
      />
      <circle
        stroke="var(--primary)"
        fill="transparent"
        strokeWidth={stroke}
        strokeDasharray={circumference + ' ' + circumference}
        style={{ strokeDashoffset }}
        r={normalizedRadius}
        cx={size / 2}
        cy={size / 2}
        className="transition-all duration-300 stroke-primary-container"
      />
    </svg>
  );
};

// 8. SkeletonLoader
export const SkeletonLoader: React.FC<{ variant?: 'text' | 'card' | 'circle'; className?: string }> = ({
  variant = 'text',
  className,
}) => {
  const classes = {
    text: 'h-4 bg-surface-container-highest rounded skeleton',
    card: 'h-24 bg-surface-container-low rounded-xl border border-outline-variant/30 skeleton',
    circle: 'w-12 h-12 bg-surface-container-highest rounded-full skeleton',
  };
  return <div className={cn(classes[variant], className)} />;
};

// 9. EmptyState
export const EmptyState: React.FC<FeedbackProps & { icon?: string }> = ({
  title = 'No Data Points',
  subtitle = 'Telemetry stream is waiting for a Ground Station uplink connection.',
  icon = 'inbox',
  className,
  actions,
}) => (
  <div className={cn('flex flex-col items-center justify-center text-center p-8', className)}>
    <div className="w-16 h-16 bg-surface-container rounded-full flex items-center justify-center mb-4">
      <Icon name={icon} className="text-on-surface-variant/30 text-[32px]" />
    </div>
    <h5 className="font-headline-md text-on-surface-variant/40">{title}</h5>
    <p className="text-sm text-on-surface-variant/40 max-w-xs mt-2">{subtitle}</p>
    {actions && <div className="mt-6">{actions}</div>}
  </div>
);

// 10. ErrorState
export const ErrorState: React.FC<FeedbackProps & { onRetry?: () => void }> = ({
  title = 'Telemetry Stream Outage',
  subtitle = 'Ground station reported connection timeout. Retrying link handshake...',
  onRetry,
  className,
}) => (
  <EmptyState
    title={title}
    subtitle={subtitle}
    icon="wifi_off"
    className={className}
    actions={
      onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 border border-outline-variant rounded-lg font-label-caps text-xs opacity-70 hover:opacity-100 transition-opacity"
        >
          RETRY CONNECTION
        </button>
      )
    }
  />
);

// 11. OfflineState
export const OfflineState: React.FC = () => (
  <ErrorState
    title="Station Offline"
    subtitle="Ground Link disconnected. Please verify transponder tracking locks."
  />
);
