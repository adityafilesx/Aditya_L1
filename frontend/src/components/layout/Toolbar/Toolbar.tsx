import { useState } from 'react';
import { MISSION_ELAPSED_TIME } from '@constants/index';
import { TOOLBAR_TABS } from '@constants/navigation';
import { useUtcClock } from '@hooks/index';
import { Icon } from '@components/common/Icon';
import { cn } from '@utils/cn';
import { commanderAvatar } from '@assets/images';

type ToolbarProps = {
  activeTab?: string;
  onTabChange?: (tabId: string) => void;
};

export function Toolbar({ activeTab = 'operations', onTabChange }: ToolbarProps) {
  const utcTime = useUtcClock();
  const [selectedTab, setSelectedTab] = useState(activeTab);

  const handleTabClick = (tabId: string) => {
    setSelectedTab(tabId);
    onTabChange?.(tabId);
  };

  return (
    <nav className="fixed top-4 left-[284px] right-8 h-[72px] bg-white/80 backdrop-blur-md rounded-xl border border-outline-variant custom-shadow flex items-center justify-between px-6 z-40">
      <div className="flex items-center gap-2 bg-surface-container-low p-1 rounded-lg">
        {TOOLBAR_TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => handleTabClick(tab.id)}
            className={cn(
              'px-4 py-2 rounded-md transition-all text-label-caps',
              selectedTab === tab.id
                ? 'bg-white text-primary font-semibold shadow-sm'
                : 'text-on-surface-variant hover:text-primary',
            )}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="flex items-center gap-8">
        <div className="flex flex-col items-center">
          <span className="text-[10px] font-label-caps text-on-surface-variant/50 uppercase tracking-widest">
            UTC Time
          </span>
          <span className="font-data-mono text-primary text-[14px] tabular-nums">{utcTime}</span>
        </div>
        <div className="h-8 w-px bg-outline-variant/30" />
        <div className="flex flex-col items-center">
          <span className="text-[10px] font-label-caps text-on-surface-variant/50 uppercase tracking-widest">
            Mission Elapsed Time
          </span>
          <span className="font-numeric-telemetry text-on-surface text-[16px] font-bold tabular-nums">
            {MISSION_ELAPSED_TIME}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1 bg-secondary-container/10 rounded-full">
          <span className="w-2 h-2 bg-secondary-container rounded-full blink" />
          <span className="text-[10px] font-bold text-on-secondary-container uppercase">Live</span>
        </div>
        <button
          type="button"
          className="relative p-2 text-on-surface-variant hover:bg-surface-variant rounded-full transition-colors"
          aria-label="Notifications"
        >
          <Icon name="notifications" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-error rounded-full border-2 border-white" />
        </button>
        <div className="h-8 w-px bg-outline-variant/30" />
        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-body-sm font-bold leading-none">Commander</p>
            <p className="text-[11px] text-on-surface-variant/60 leading-tight">Aditya-L1 Ops</p>
          </div>
          <div className="w-10 h-10 rounded-full border-2 border-primary-container p-[2px]">
            <img
              className="w-full h-full rounded-full object-cover"
              src={commanderAvatar}
              alt="Mission commander"
            />
          </div>
        </div>
      </div>
    </nav>
  );
}
