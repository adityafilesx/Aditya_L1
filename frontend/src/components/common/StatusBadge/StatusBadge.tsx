import type { Severity } from '@app-types/index';
import { cn } from '@utils/cn';

type StatusBadgeProps = {
  label: string;
  severity?: Severity;
  pulse?: boolean;
  className?: string;
};

const severityStyles: Record<Severity, string> = {
  success: 'bg-success/10 text-success',
  warning: 'bg-warning/10 text-warning',
  critical: 'bg-critical/10 text-critical',
  info: 'bg-primary-container/10 text-primary',
  neutral: 'bg-surface-container text-on-surface-variant',
};

export function StatusBadge({ label, severity = 'neutral', pulse = false, className }: StatusBadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-label-caps uppercase font-bold',
        severityStyles[severity],
        className,
      )}
    >
      {pulse && <span className={cn('w-2 h-2 rounded-full bg-current', pulse && 'blink')} />}
      {label}
    </span>
  );
}
