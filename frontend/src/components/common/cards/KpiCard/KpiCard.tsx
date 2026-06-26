import type { ReactNode } from 'react';
import { cn } from '@utils/cn';

type KpiCardProps = {
  label: string;
  value: string;
  unit?: string;
  trend?: string;
  icon?: ReactNode;
  className?: string;
  children?: ReactNode;
};

export function KpiCard({ label, value, unit, trend, icon, className, children }: KpiCardProps) {
  return (
    <div className={cn('bento-card p-4', className)}>
      <div className="flex items-start justify-between mb-2">
        <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">{label}</span>
        {icon}
      </div>
      <div className="flex items-baseline gap-1">
        <span className="data-value">{value}</span>
        {unit && <span className="unit-label">{unit}</span>}
      </div>
      {trend && <p className="text-[11px] text-on-surface-variant mt-1">{trend}</p>}
      {children}
    </div>
  );
}
