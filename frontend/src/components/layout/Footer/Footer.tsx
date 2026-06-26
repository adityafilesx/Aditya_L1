import { APP_VERSION, CONNECTIVITY_LATENCY, COPYRIGHT, STATION_ID } from '@constants/index';
import { Icon } from '@components/common/Icon';

export function Footer() {
  return (
    <footer className="fixed bottom-0 left-[260px] right-0 h-10 bg-surface-container border-t border-outline-variant flex items-center justify-between px-8 z-40">
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-label-caps text-on-surface-variant/40">Status:</span>
          <span className="text-[10px] font-label-caps text-primary uppercase font-bold tracking-wider">
            {APP_VERSION} Stable Build
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-label-caps text-on-surface-variant/40">Connectivity:</span>
          <div className="flex items-center gap-1 text-[10px] font-label-caps text-secondary uppercase font-bold">
            <Icon name="network_check" className="text-[14px]" />
            <span>Optimal ({CONNECTIVITY_LATENCY})</span>
          </div>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-[10px] font-data-mono text-on-surface-variant/60">
          <Icon name="satellite_alt" className="text-[14px]" />
          <span>{STATION_ID}</span>
        </div>
        <div className="h-4 w-px bg-outline-variant" />
        <span className="text-[10px] font-data-mono text-on-surface-variant/60">{COPYRIGHT}</span>
      </div>
    </footer>
  );
}
