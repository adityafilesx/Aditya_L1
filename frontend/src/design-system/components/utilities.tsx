import React, { useState } from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';

export interface UtilityProps {
  children?: React.ReactNode;
  className?: string;
  title?: string;
  icon?: string;
}

// 1. Tooltip
export const Tooltip: React.FC<{ text: string; children: React.ReactNode; className?: string }> = ({
  text,
  children,
  className,
}) => (
  <div className={cn('relative group inline-block', className)}>
    {children}
    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-inverse-surface border border-outline-variant/30 text-white text-[10px] font-label-caps rounded shadow-md hidden group-hover:block whitespace-nowrap z-50">
      {text}
    </div>
  </div>
);

// 2. Popover
export const Popover: React.FC<{ content: React.ReactNode; children: React.ReactNode; className?: string }> = ({
  content,
  children,
  className,
}) => {
  const [open, setOpen] = useState(false);
  return (
    <div className={cn('relative inline-block', className)}>
      <div onClick={() => setOpen(!open)} className="cursor-pointer">{children}</div>
      {open && (
        <>
          <div onClick={() => setOpen(false)} className="fixed inset-0 z-40" />
          <div className="absolute mt-2 bg-white border border-outline-variant rounded-lg shadow-lg p-4 z-50 min-w-[200px]">
            {content}
          </div>
        </>
      )}
    </div>
  );
};

// 3. Divider
export const Divider: React.FC<{ vertical?: boolean; className?: string }> = ({ vertical = false, className }) => (
  <div
    className={cn(
      vertical ? 'h-8 w-px bg-outline-variant/30 mx-1' : 'w-full h-px bg-outline-variant/30 my-4',
      className
    )}
  />
);

// 4. Avatar
export const Avatar: React.FC<{ src?: string; alt?: string; fallback?: string; size?: 'sm' | 'md' | 'lg'; className?: string }> = ({
  src,
  alt = 'avatar',
  fallback = 'U',
  size = 'md',
  className,
}) => {
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
  };

  return (
    <div className={cn('rounded-full border-2 border-primary-container p-[2px] overflow-hidden bg-surface-container', sizes[size], className)}>
      {src ? (
        <img src={src} alt={alt} className="w-full h-full rounded-full object-cover" />
      ) : (
        <div className="w-full h-full rounded-full flex items-center justify-center font-bold text-xs text-primary bg-primary-container/10">
          {fallback}
        </div>
      )}
    </div>
  );
};

// 5. Chip / Tag
export const Chip: React.FC<UtilityProps & { variant?: 'primary' | 'secondary' | 'neutral'; active?: boolean; onClick?: () => void }> = ({
  title,
  children,
  className,
  variant = 'neutral',
  active,
  onClick,
}) => (
  <button
    type="button"
    onClick={onClick}
    className={cn(
      'px-3 py-1 rounded-full text-xs font-label-caps border transition-all flex items-center gap-1.5',
      variant === 'primary' && 'bg-primary-container/10 text-primary border-primary-container/20 hover:bg-primary-container/20',
      variant === 'secondary' && 'bg-secondary-container/10 text-secondary border-secondary-container/20 hover:bg-secondary-container/20',
      variant === 'neutral' && 'bg-surface-container-highest text-on-surface-variant border-outline-variant hover:bg-surface-variant',
      active && 'bg-primary-container text-white border-primary-container hover:bg-primary-container',
      className
    )}
  >
    {children || title}
  </button>
);

export const Tag: React.FC<UtilityProps & { color?: string }> = ({ title, children, className, color }) => (
  <span
    className={cn(
      'px-2 py-0.5 rounded text-[10px] font-label-caps border bg-surface-container font-bold',
      className
    )}
    style={color ? { color, borderColor: `${color}33`, backgroundColor: `${color}11` } : undefined}
  >
    {children || title}
  </span>
);

// 6. Accordion / Collapse
export const Accordion: React.FC<UtilityProps & { subtitle?: string; defaultOpen?: boolean }> = ({
  title,
  subtitle,
  children,
  className,
  defaultOpen = false,
}) => {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className={cn('border border-outline-variant rounded-lg overflow-hidden bg-white mb-2', className)}>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between items-center p-4 bg-surface-container-low hover:bg-surface-container transition-colors text-left"
      >
        <div>
          <span className="font-bold text-sm text-on-surface">{title}</span>
          {subtitle && <p className="text-xs text-on-surface-variant mt-0.5">{subtitle}</p>}
        </div>
        <Icon name={open ? 'expand_less' : 'expand_more'} />
      </button>
      {open && <div className="p-4 border-t border-outline-variant/30">{children}</div>}
    </div>
  );
};

export const Collapse: React.FC<{ isOpen: boolean; children: React.ReactNode; className?: string }> = ({
  isOpen,
  children,
  className,
}) => {
  if (!isOpen) return null;
  return <div className={cn('animate-fade-in', className)}>{children}</div>;
};

// 7. Tree (File tree or hierarchy view)
export interface TreeNode {
  id: string;
  label: string;
  icon?: string;
  children?: TreeNode[];
}

export const Tree: React.FC<{ nodes: TreeNode[]; onNodeSelect?: (node: TreeNode) => void; className?: string }> = ({
  nodes,
  onNodeSelect,
  className,
}) => {
  const renderNode = (node: TreeNode, depth = 0) => {
    const hasChildren = node.children && node.children.length > 0;
    const [expanded, setExpanded] = useState(false);

    return (
      <div key={node.id} className="text-xs font-data-mono">
        <div
          onClick={() => {
            if (hasChildren) setExpanded(!expanded);
            onNodeSelect?.(node);
          }}
          className="flex items-center gap-1.5 py-1.5 px-2 hover:bg-surface-container-low rounded cursor-pointer text-on-surface-variant"
          style={{ paddingLeft: `${depth * 16 + 8}px` }}
        >
          {hasChildren ? (
            <Icon name={expanded ? 'expand_less' : 'expand_more'} className="text-[16px]" />
          ) : (
            <span className="w-4" />
          )}
          {node.icon && <Icon name={node.icon} className="text-[16px]" />}
          <span>{node.label}</span>
        </div>
        {hasChildren && expanded && (
          <div>
            {node.children!.map((child) => renderNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return <div className={cn('space-y-0.5', className)}>{nodes.map((node) => renderNode(node))}</div>;
};

// 8. Timeline (Operational log timeline)
export interface TimelineItemProps {
  time: string;
  title: string;
  description?: string;
  status?: 'active' | 'completed' | 'neutral';
  icon?: string;
}

export const Timeline: React.FC<{ items: TimelineItemProps[]; className?: string }> = ({ items, className }) => {
  return (
    <div className={cn('flex flex-col gap-4 overflow-y-auto pr-2', className)}>
      {items.map((item, idx) => {
        const isActive = item.status === 'active';
        return (
          <div
            key={idx}
            className={cn(
              'relative pl-6 border-l-2',
              isActive ? 'border-primary-container' : 'border-outline-variant/50'
            )}
          >
            <div
              className={cn(
                'absolute -left-[7px] top-0 w-3 h-3 rounded-full ring-4 ring-white',
                isActive ? 'bg-primary' : 'bg-outline-variant'
              )}
            />
            <div className="font-data-mono text-[10px] text-outline leading-none mb-1">{item.time}</div>
            <p className={cn('text-[12px] leading-tight font-semibold', isActive ? 'text-primary font-bold' : 'text-on-surface')}>
              {item.title}
            </p>
            {item.description && <p className="text-[11px] text-on-surface-variant/75 mt-0.5 leading-snug">{item.description}</p>}
          </div>
        );
      })}
    </div>
  );
};

// 9. CommandPalette (Quick launcher overlay)
export const CommandPalette: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  commands: { id: string; label: string; shortcut?: string; action: () => void }[];
}> = ({ isOpen, onClose, commands }) => {
  const [filter, setFilter] = useState('');
  if (!isOpen) return null;

  const filtered = commands.filter((cmd) =>
    cmd.label.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-start justify-center p-4 pt-[15vh] z-[3000]">
      <div onClick={onClose} className="absolute inset-0 cursor-pointer" />
      <div className="relative w-full max-w-lg bg-white border border-outline-variant rounded-xl shadow-2xl overflow-hidden flex flex-col z-[3010] animate-fade-in">
        <div className="flex items-center px-4 border-b border-outline-variant bg-surface-container-low">
          <Icon name="search" className="text-on-surface-variant/40 mr-2" />
          <input
            type="text"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Type a command or search action..."
            className="w-full py-3 bg-transparent text-sm font-data-mono text-on-surface focus:outline-none"
            autoFocus
          />
          <button onClick={onClose} className="text-xs font-label-caps text-on-surface-variant opacity-60">ESC</button>
        </div>
        <div className="max-h-[300px] overflow-y-auto p-2 divide-y divide-outline-variant/10">
          {filtered.length === 0 ? (
            <div className="text-center py-6 text-xs text-on-surface-variant/40 font-data-mono">No actions found.</div>
          ) : (
            filtered.map((cmd) => (
              <button
                key={cmd.id}
                onClick={() => {
                  cmd.action();
                  onClose();
                }}
                className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-primary-container hover:text-white rounded text-xs font-data-mono transition-colors group"
              >
                <span>{cmd.label}</span>
                {cmd.shortcut && (
                  <span className="text-[10px] text-on-surface-variant group-hover:text-white/60">{cmd.shortcut}</span>
                )}
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
