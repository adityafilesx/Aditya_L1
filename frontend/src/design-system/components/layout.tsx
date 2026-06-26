import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';
import { useUtcClock } from '@hooks/index';
import { 
  APP_NAME, 
  APP_SUBTITLE, 
  APP_OS, 
  APP_VERSION, 
  SHELL_NAV_SECTIONS, 
  MISSION_ELAPSED_TIME 
} from '@constants/index';
import { TOOLBAR_TABS } from '@constants/navigation';
import { commanderAvatar } from '@assets/images';

export interface LayoutProps {
  children?: React.ReactNode;
  className?: string;
  variant?: 'shell' | 'content-only' | 'split' | 'grid';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  status?: string;
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  icon?: string;
  actions?: React.ReactNode;
  footer?: React.ReactNode;
}

// 1. AppLayout (Wraps everything)
export const AppLayout: React.FC<LayoutProps> = ({
  children,
  className,
  variant = 'shell',
}) => {
  if (variant === 'content-only') {
    return <div className={cn('min-h-screen bg-surface', className)}>{children}</div>;
  }

  return (
    <div className={cn('shell-body min-h-screen bg-surface', className)}>
      <Sidebar />
      <Toolbar />
      <main
        className={cn(
          'fixed top-[104px] left-[284px] right-8 bottom-14 bg-white rounded-[18px] border border-outline-variant custom-shadow overflow-hidden'
        )}
      >
        {children}
      </main>
      <Footer />
    </div>
  );
};

// 2. Sidebar Component
export const Sidebar: React.FC<{ className?: string }> = ({ className }) => {
  const location = useLocation();

  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-full w-[260px] bg-sidebar-dark text-white flex flex-col z-50',
        className
      )}
    >
      <div className="p-6 mb-2">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-primary-container rounded flex items-center justify-center">
            <Icon name="wb_sunny" filled className="text-white" />
          </div>
          <div>
            <h1 className="font-display-lg text-[18px] leading-tight tracking-tight uppercase">
              {APP_NAME}
            </h1>
            <p className="text-[10px] text-surface-variant/40 tracking-[0.2em] font-label-caps uppercase">
              {APP_SUBTITLE}
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 space-y-6 pb-20 custom-scrollbar">
        {SHELL_NAV_SECTIONS.map((section) => (
          <SidebarGroup key={section.id} title={section.title}>
            {section.items.map((item) => {
              const active = isActive(item.path);
              return (
                <SidebarItem
                  key={item.id}
                  to={item.path}
                  label={item.label}
                  icon={item.icon}
                  active={active}
                  filled={active || item.filled}
                />
              );
            })}
          </SidebarGroup>
        ))}
      </div>

      <SidebarFooter version={APP_VERSION} os={APP_OS} />
    </aside>
  );
};

// 3. Sidebar Group
export const SidebarGroup: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <section>
    <h2 className="px-2 text-[10px] font-label-caps text-surface-variant/30 mb-2 uppercase">
      {title}
    </h2>
    <nav className="space-y-1">{children}</nav>
  </section>
);

// 4. Sidebar Item
export const SidebarItem: React.FC<{
  to: string;
  label: string;
  icon: string;
  active?: boolean;
  filled?: boolean;
}> = ({ to, label, icon, active, filled }) => (
  <NavLink
    to={to}
    className={cn(
      'flex items-center gap-3 px-3 py-2 transition-all',
      active
        ? 'active-sidebar-item font-semibold'
        : 'text-surface-variant/60 sidebar-item-hover rounded-lg'
    )}
  >
    <Icon name={icon} filled={filled} />
    <span className="text-body-sm">{label}</span>
  </NavLink>
);

// 5. Sidebar Footer
export const SidebarFooter: React.FC<{ version: string; os: string }> = ({ version, os }) => (
  <div className="p-4 border-t border-white/5 bg-sidebar-footer">
    <div className="flex items-center justify-between text-[11px] text-surface-variant/40 font-data-mono">
      <span>VER: {version}</span>
      <span className="text-primary-container">OS: {os}</span>
    </div>
  </div>
);

// 6. Toolbar Component
export const Toolbar: React.FC<{ activeTab?: string; onTabChange?: (tabId: string) => void }> = ({
  activeTab = 'operations',
  onTabChange,
}) => {
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
                : 'text-on-surface-variant hover:text-primary'
            )}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="flex items-center gap-8">
        <div className="flex flex-col items-center">
          <span className="text-[10px] font-label-caps text-on-surface-variant/50 uppercase tracking-widest leading-none">
            UTC Time
          </span>
          <span className="font-data-mono text-primary text-[14px] tabular-nums leading-none mt-1">{utcTime}</span>
        </div>
        <div className="h-8 w-px bg-outline-variant/30" />
        <div className="flex flex-col items-center">
          <span className="text-[10px] font-label-caps text-on-surface-variant/50 uppercase tracking-widest leading-none">
            Mission Elapsed Time
          </span>
          <span className="font-numeric-telemetry text-on-surface text-[16px] font-bold tabular-nums leading-none mt-1">
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
};

// 7. Footer Component
export const Footer: React.FC = () => (
  <footer className="fixed bottom-0 left-[260px] right-0 h-10 bg-white border-t border-outline-variant px-8 flex items-center justify-between text-[11px] text-on-surface-variant/60 font-data-mono z-40">
    <div className="flex items-center gap-4">
      <span className="flex items-center gap-1.5">
        <span className="w-2 h-2 bg-success rounded-full" />
        SYSTEM STATE: NOMINAL
      </span>
      <span>|</span>
      <span>UPLINK: 4.8 Gbps</span>
      <span>|</span>
      <span>STATION ID: IN-ISRO-ISTRAC-02</span>
    </div>
    <div>
      <span>© 2026 ADITYA-L1 MISSION OPERATIONS SHIELD</span>
    </div>
  </footer>
);

// 8. Header Component (Dashboard header)
export const Header: React.FC<LayoutProps> = ({ title, subtitle, actions }) => (
  <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-gutter gap-4">
    <div>
      <h2 className="font-display-lg text-headline-md text-on-surface">{title}</h2>
      {subtitle && <p className="font-body-lg text-body-lg text-on-surface-variant">{subtitle}</p>}
    </div>
    {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
  </div>
);

// 9. PageLayout
export const PageLayout: React.FC<LayoutProps> = ({ children, className }) => (
  <div className={cn('w-full h-full overflow-auto custom-scrollbar p-6', className)}>
    {children}
  </div>
);

// 10. WorkspaceLayout
export const WorkspaceLayout: React.FC<LayoutProps> = ({ children, className }) => (
  <div className={cn('grid grid-cols-12 gap-6 h-full p-6 overflow-hidden', className)}>
    {children}
  </div>
);

// 11. ContentContainer
export const ContentContainer: React.FC<LayoutProps> = ({ children, className }) => (
  <div className={cn('flex-1 w-full overflow-auto custom-scrollbar', className)}>
    {children}
  </div>
);

// 12. SplitView (Horizontal side-by-side or vertical split)
export const SplitView: React.FC<LayoutProps> = ({ children, className, variant = 'split' }) => (
  <div className={cn('flex gap-6', variant === 'split' ? 'flex-row' : 'flex-col', className)}>
    {children}
  </div>
);

// 13. GridLayout
export const GridLayout: React.FC<LayoutProps> = ({ children, className }) => (
  <div className={cn('grid gap-gutter', className)}>
    {children}
  </div>
);

// 14. ResizablePanel
export const ResizablePanel: React.FC<LayoutProps> = ({ children, className }) => (
  <div className={cn('flex-1 min-w-[200px]', className)}>
    {children}
  </div>
);

// 15. DockPanel
export const DockPanel: React.FC<LayoutProps> = ({ children, className }) => (
  <div className={cn('bg-white border border-outline-variant rounded-xl shadow-sm overflow-hidden flex flex-col', className)}>
    {children}
  </div>
);

// 16. WorkspaceTabs
export const WorkspaceTabs: React.FC<{
  tabs: { id: string; label: string; active?: boolean }[];
  onTabSelect?: (id: string) => void;
  className?: string;
}> = ({ tabs, onTabSelect, className }) => (
  <div className={cn('flex border-b border-outline-variant mb-4', className)}>
    {tabs.map((tab) => (
      <button
        key={tab.id}
        onClick={() => onTabSelect?.(tab.id)}
        className={cn(
          'px-4 py-2 border-b-2 font-label-caps text-label-caps text-xs',
          tab.active
            ? 'border-primary text-primary font-bold'
            : 'border-transparent text-on-surface-variant hover:text-primary'
        )}
      >
        {tab.label}
      </button>
    ))}
  </div>
);

// 17. SectionHeader
export const SectionHeader: React.FC<LayoutProps> = ({ title, subtitle, actions, className }) => (
  <div className={cn('flex justify-between items-center mb-4', className)}>
    <div>
      <h3 className="font-headline-md text-headline-md text-on-surface">{title}</h3>
      {subtitle && <p className="text-body-sm text-on-surface-variant mt-0.5">{subtitle}</p>}
    </div>
    {actions && <div className="flex items-center gap-2">{actions}</div>}
  </div>
);

// 18. PageTitle
export const PageTitle: React.FC<{ title: string; subtitle?: string; className?: string }> = ({
  title,
  subtitle,
  className,
}) => (
  <div className={cn('mb-6', className)}>
    <h1 className="font-display-lg text-on-surface">{title}</h1>
    {subtitle && <p className="text-on-surface-variant mt-1">{subtitle}</p>}
  </div>
);

// 19. Breadcrumb
export const Breadcrumb: React.FC<{ items: { label: string; link?: string }[]; className?: string }> = ({
  items,
  className,
}) => (
  <div className={cn('flex items-center gap-1 text-[11px] font-label-caps text-on-surface-variant/60', className)}>
    {items.map((item, index) => (
      <React.Fragment key={index}>
        {index > 0 && <Icon name="chevron_right" className="text-[14px]" />}
        {item.link ? (
          <a href={item.link} className="hover:text-primary">{item.label}</a>
        ) : (
          <span className={cn(index === items.length - 1 && 'text-primary font-bold')}>{item.label}</span>
        )}
      </React.Fragment>
    ))}
  </div>
);
