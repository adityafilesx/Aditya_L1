import React from 'react';
import { cn } from '@utils/cn';

export const SkeletonBase: React.FC<{ className?: string; style?: React.CSSProperties }> = ({ className, style }) => (
  <div className={cn('animate-pulse bg-surface-container rounded', className)} style={style} />
);

export const SkeletonCard: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn('bento-card p-6 flex flex-col gap-4', className)}>
    <SkeletonBase className="w-1/3 h-6" />
    <SkeletonBase className="w-1/4 h-4 mt-2" />
    <div className="mt-4 flex-1 flex items-center justify-center">
      <SkeletonBase className="w-full h-full min-h-[100px] opacity-50" />
    </div>
  </div>
);

export const SkeletonTable: React.FC<{ rows?: number; className?: string }> = ({ rows = 5, className }) => (
  <div className={cn('w-full', className)}>
    <div className="flex border-b border-outline-variant/30 pb-3 mb-2 gap-4">
      <SkeletonBase className="flex-1 h-4" />
      <SkeletonBase className="flex-1 h-4" />
      <SkeletonBase className="flex-1 h-4" />
    </div>
    {Array.from({ length: rows }).map((_, i) => (
      <div key={i} className="flex border-b border-outline-variant/20 py-3 gap-4">
        <SkeletonBase className="flex-1 h-4 opacity-70" />
        <SkeletonBase className="flex-1 h-4 opacity-70" />
        <SkeletonBase className="flex-1 h-4 opacity-70" />
      </div>
    ))}
  </div>
);

export const SkeletonChart: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn('bento-card flex flex-col', className)}>
    <div className="p-6 border-b border-outline-variant flex justify-between items-center">
      <div>
        <SkeletonBase className="w-32 h-6" />
        <SkeletonBase className="w-24 h-4 mt-1" />
      </div>
      <div className="flex gap-2">
        <SkeletonBase className="w-8 h-8 rounded" />
        <SkeletonBase className="w-8 h-8 rounded" />
      </div>
    </div>
    <div className="flex-1 min-h-[300px] p-6 flex items-end gap-2 justify-between opacity-30">
      {Array.from({ length: 12 }).map((_, i) => (
        <SkeletonBase key={i} className="w-full rounded-t" style={{ height: `${Math.max(20, Math.random() * 100)}%` }} />
      ))}
    </div>
  </div>
);

export const SkeletonTimeline: React.FC<{ count?: number; className?: string }> = ({ count = 4, className }) => (
  <div className={cn('flex flex-col gap-6', className)}>
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="flex gap-4">
        <div className="w-12 shrink-0 flex flex-col items-center">
          <SkeletonBase className="w-8 h-8 rounded-full mb-2" />
          <SkeletonBase className="w-0.5 flex-1" />
        </div>
        <div className="flex-1">
          <SkeletonBase className="w-24 h-4 mb-2" />
          <SkeletonCard className="p-4 min-h-[80px]" />
        </div>
      </div>
    ))}
  </div>
);

export const PageSkeleton: React.FC = () => (
  <div className="w-full h-full p-6 animate-in fade-in duration-300">
    <div className="flex items-center justify-between mb-8">
      <SkeletonBase className="w-48 h-8" />
      <SkeletonBase className="w-32 h-8" />
    </div>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <SkeletonCard className="h-32" />
      <SkeletonCard className="h-32" />
      <SkeletonCard className="h-32" />
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        <SkeletonChart />
      </div>
      <div>
        <div className="bento-card p-6">
          <SkeletonBase className="w-32 h-6 mb-6" />
          <SkeletonTable rows={4} />
        </div>
      </div>
    </div>
  </div>
);
