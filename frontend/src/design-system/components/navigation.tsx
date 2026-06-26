import React, { useState } from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';
import { NavLink } from 'react-router-dom';

export interface NavigationProps {
  className?: string;
  onChange?: (id: string) => void;
}

// 1. SidebarNavigation
export const SidebarNavigation: React.FC<{
  sections: { id: string; title: string; items: { id: string; label: string; path: string; icon: string }[] }[];
  activePath: string;
}> = ({ sections, activePath }) => {
  return (
    <div className="space-y-6">
      {sections.map((sec) => (
        <div key={sec.id}>
          <h3 className="px-2 text-[10px] font-label-caps text-surface-variant/30 mb-2 uppercase">
            {sec.title}
          </h3>
          <div className="space-y-1">
            {sec.items.map((item) => {
              const active = activePath === item.path || activePath.startsWith(`${item.path}/`);
              return (
                <NavLink
                  key={item.id}
                  to={item.path}
                  className={cn(
                    'flex items-center gap-3 px-3 py-2 transition-all',
                    active
                      ? 'active-sidebar-item font-semibold'
                      : 'text-surface-variant/60 sidebar-item-hover rounded-lg'
                  )}
                >
                  <Icon name={item.icon} filled={active} />
                  <span className="text-body-sm">{item.label}</span>
                </NavLink>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
};

// 2. TopNavigation
export const TopNavigation: React.FC<{
  links: { label: string; path: string; icon?: string }[];
  activePath: string;
}> = ({ links, activePath }) => (
  <div className="flex items-center gap-4 text-xs font-label-caps">
    {links.map((link, idx) => {
      const active = activePath === link.path;
      return (
        <NavLink
          key={idx}
          to={link.path}
          className={cn(
            'hover:text-primary transition-colors',
            active ? 'text-primary font-bold' : 'text-on-surface-variant'
          )}
        >
          {link.icon && <Icon name={link.icon} className="mr-1.5" />}
          {link.label}
        </NavLink>
      );
    })}
  </div>
);

// 3. WorkspaceSwitcher
export const WorkspaceSwitcher: React.FC<{
  workspaces: { id: string; label: string }[];
  activeId: string;
  onSwitch: (id: string) => void;
}> = ({ workspaces, activeId, onSwitch }) => {
  const [open, setOpen] = useState(false);
  const activeLabel = workspaces.find((w) => w.id === activeId)?.label || activeId;

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="px-3 py-1.5 bg-surface-container-low border border-outline-variant rounded font-label-caps text-label-caps flex items-center gap-2"
      >
        <span>{activeLabel}</span>
        <Icon name="keyboard_arrow_down" />
      </button>
      {open && (
        <div className="absolute left-0 mt-1 w-48 bg-white border border-outline-variant rounded-lg shadow-lg py-2 z-50">
          {workspaces.map((w) => (
            <button
              key={w.id}
              onClick={() => {
                onSwitch(w.id);
                setOpen(false);
              }}
              className={cn(
                'w-full text-left px-4 py-2 text-xs font-label-caps hover:bg-surface-container-low',
                w.id === activeId && 'text-primary font-bold'
              )}
            >
              {w.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

// 4. QuickActions
export const QuickActions: React.FC<{
  actions: { id: string; label: string; icon: string; onClick: () => void }[];
}> = ({ actions }) => (
  <div className="grid grid-cols-2 gap-2 p-2 bg-surface-container-low rounded-lg border border-outline-variant">
    {actions.map((act) => (
      <button
        key={act.id}
        onClick={act.onClick}
        className="flex items-center gap-2 px-3 py-2 bg-white hover:bg-primary-container hover:text-white rounded border border-outline-variant/30 text-xs transition-colors font-label-caps"
      >
        <Icon name={act.icon} className="text-[18px]" />
        {act.label}
      </button>
    ))}
  </div>
);

// 5. Tabs
export const Tabs: React.FC<{
  tabs: { id: string; label: string; count?: number }[];
  activeTab: string;
  onTabChange: (id: string) => void;
  className?: string;
}> = ({ tabs, activeTab, onTabChange, className }) => (
  <div className={cn('flex gap-2 border-b border-outline-variant overflow-x-auto whitespace-nowrap', className)}>
    {tabs.map((tab) => (
      <button
        key={tab.id}
        onClick={() => onTabChange(tab.id)}
        className={cn(
          'px-4 py-2 border-b-2 font-label-caps text-label-caps text-xs flex items-center gap-1.5 transition-all',
          activeTab === tab.id
            ? 'border-primary text-primary font-bold'
            : 'border-transparent text-on-surface-variant hover:text-primary'
        )}
      >
        {tab.label}
        {tab.count !== undefined && (
          <span className="px-1.5 py-0.5 rounded-full bg-surface-container text-on-surface-variant text-[10px]">
            {tab.count}
          </span>
        )}
      </button>
    ))}
  </div>
);

// 6. SubTabs
export const SubTabs: React.FC<{
  tabs: { id: string; label: string }[];
  activeTab: string;
  onTabChange: (id: string) => void;
  className?: string;
}> = ({ tabs, activeTab, onTabChange, className }) => (
  <div className={cn('flex gap-1 border-b border-outline-variant/30 py-1 overflow-x-auto', className)}>
    {tabs.map((tab) => (
      <button
        key={tab.id}
        onClick={() => onTabChange(tab.id)}
        className={cn(
          'px-3 py-1 text-[11px] font-label-caps rounded-md transition-all',
          activeTab === tab.id
            ? 'bg-primary-container/15 text-primary font-semibold'
            : 'text-on-surface-variant/80 hover:text-primary hover:bg-surface-container-low'
        )}
      >
        {tab.label}
      </button>
    ))}
  </div>
);

// 7. NavigationRail (Compact layout navigation rail)
export const NavigationRail: React.FC<{
  items: { id: string; icon: string; label: string; onClick: () => void; active?: boolean }[];
  className?: string;
}> = ({ items, className }) => (
  <div className={cn('w-16 bg-sidebar-dark flex flex-col items-center py-4 gap-6 text-white h-full border-r border-white/5', className)}>
    {items.map((item) => (
      <button
        key={item.id}
        onClick={item.onClick}
        className={cn(
          'w-10 h-10 rounded-lg flex items-center justify-center transition-colors relative group',
          item.active ? 'bg-primary-container text-white' : 'text-surface-variant/60 hover:text-white hover:bg-white/5'
        )}
        title={item.label}
      >
        <Icon name={item.icon} filled={item.active} />
        <span className="absolute left-16 bg-sidebar-dark border border-outline-variant/30 text-white text-[10px] font-label-caps px-2 py-1 rounded shadow-lg hidden group-hover:block whitespace-nowrap z-50">
          {item.label}
        </span>
      </button>
    ))}
  </div>
);
