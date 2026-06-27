import { NavLink, useLocation } from 'react-router-dom';
import { APP_NAME, APP_SUBTITLE, APP_OS, APP_VERSION, SHELL_NAV_SECTIONS } from '@constants/index';
import { Icon } from '@components/common/Icon';
import { cn } from '@utils/cn';

type SidebarProps = {
  className?: string;
};

export function Sidebar({ className }: SidebarProps) {
  const location = useLocation();

  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-full w-[260px] bg-surface-container-low text-on-surface flex flex-col z-50 border-r border-outline-variant/30',
        className,
      )}
    >
      <div className="p-6 mb-2">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-primary-container rounded flex items-center justify-center">
            <Icon name="wb_sunny" filled className="text-on-primary-container" />
          </div>
          <div>
            <h1 className="font-display-lg text-[18px] leading-tight tracking-tight uppercase text-on-surface">
              {APP_NAME}
            </h1>
            <p className="text-[10px] text-on-surface-variant tracking-[0.2em] font-label-caps uppercase">
              {APP_SUBTITLE}
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 space-y-6 pb-20 custom-scrollbar">
        {SHELL_NAV_SECTIONS.map((section) => (
          <section key={section.id}>
            <h2 className="px-2 text-[10px] font-label-caps text-on-surface-variant uppercase tracking-wider mb-2">
              {section.title}
            </h2>
            <nav className="space-y-1">
              {section.items.map((item) => {
                const active = isActive(item.path);
                return (
                  <NavLink
                    key={item.id}
                    to={item.path}
                    className={cn(
                      'flex items-center gap-3 px-3 py-2 transition-all rounded-lg',
                      active
                        ? 'active-sidebar-item font-semibold'
                        : 'text-on-surface-variant sidebar-item-hover',
                    )}
                  >
                    <Icon name={item.icon} filled={active || item.filled} />
                    <span className="text-body-sm">{item.label}</span>
                  </NavLink>
                );
              })}
            </nav>
          </section>
        ))}
      </div>

      <div className="p-4 border-t border-outline-variant/20 bg-surface-container">
        <div className="flex items-center justify-between text-[11px] text-on-surface-variant font-data-mono">
          <span>VER: {APP_VERSION}</span>
          <span className="text-primary">OS: {APP_OS}</span>
        </div>
      </div>
    </aside>
  );
}
