import React from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';

export interface BaseButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  title?: string;
  subtitle?: string;
  icon?: string;
  iconPosition?: 'left' | 'right';
  loading?: boolean;
  disabled?: boolean;
  tooltip?: string;
  shortcut?: string; // Keyboard shortcut string (e.g. '⌘K')
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'icon' | 'toolbar' | 'command' | 'dropdown' | 'action';
  badge?: React.ReactNode;
}

export const BaseButton: React.FC<BaseButtonProps> = ({
  title,
  subtitle,
  children,
  className,
  icon,
  iconPosition = 'left',
  loading = false,
  disabled = false,
  tooltip,
  shortcut,
  size = 'md',
  variant = 'primary',
  badge,
  type = 'button',
  ...rest
}) => {
  const content = children || title;

  const sizeClasses = {
    sm: 'px-3 py-1 text-[11px] rounded-md h-8',
    md: 'px-6 py-2 text-body-sm rounded-lg h-10',
    lg: 'px-8 py-3 text-body-lg rounded-xl h-12',
  };

  const variantClasses = {
    primary: 'bg-primary-container text-on-primary-container font-label-caps hover:brightness-110 active:scale-[0.98] transition-all',
    secondary: 'bg-surface-container border border-outline-variant text-on-surface font-label-caps hover:bg-surface-variant transition-all active:scale-[0.98]',
    ghost: 'text-primary font-label-caps hover:underline active:opacity-80 transition-all',
    danger: 'bg-error text-on-error font-label-caps hover:bg-error/90 active:scale-[0.98] transition-all',
    icon: 'w-10 h-10 border border-outline-variant rounded-lg flex items-center justify-center text-on-surface hover:text-primary active:scale-[0.98] transition-all p-0',
    toolbar: 'p-2 hover:bg-surface-container-high rounded text-on-surface-variant transition-colors flex items-center justify-center',
    command: 'flex items-center justify-between w-full px-4 py-2 text-left hover:bg-surface-container-high rounded transition-colors text-body-sm font-data-mono text-on-surface-variant',
    dropdown: 'px-4 py-2 bg-surface-container-low border border-outline-variant rounded font-label-caps text-label-caps flex items-center gap-2 hover:bg-surface-container-high transition-colors',
    action: 'text-primary font-bold text-[11px] hover:underline uppercase active:opacity-80 transition-all',
  };

  const buttonElement = (
    <button
      type={type}
      disabled={disabled || loading}
      className={cn(
        'inline-flex items-center justify-center gap-2 transition-all select-none',
        variant !== 'icon' && variant !== 'toolbar' && variant !== 'command' && variant !== 'action' && sizeClasses[size],
        variantClasses[variant],
        (disabled || loading) && 'opacity-50 cursor-not-allowed pointer-events-none',
        className
      )}
      title={tooltip}
      {...rest}
    >
      {loading && (
        <span className="material-symbols-outlined animate-spin text-[18px]">
          progress_activity
        </span>
      )}
      {!loading && icon && iconPosition === 'left' && (
        <Icon name={icon} className="leading-none text-[18px]" />
      )}
      {variant !== 'icon' && (
        <span className="flex flex-col text-left">
          <span>{content}</span>
          {subtitle && <span className="text-[10px] opacity-60 leading-none mt-0.5">{subtitle}</span>}
        </span>
      )}
      {!loading && icon && iconPosition === 'right' && (
        <Icon name={icon} className="leading-none text-[18px]" />
      )}
      {variant === 'icon' && icon && !loading && (
        <Icon name={icon} className="leading-none text-[20px]" />
      )}
      {variant === 'dropdown' && !icon && (
        <Icon name="keyboard_arrow_down" className="leading-none text-[18px] ml-1" />
      )}
      {badge && <span className="ml-1">{badge}</span>}
      {shortcut && (
        <span className="ml-auto pl-4 text-[10px] opacity-40 font-data-mono font-normal">
          {shortcut}
        </span>
      )}
    </button>
  );

  return buttonElement;
};

export const PrimaryButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="primary" {...props} />
);

export const SecondaryButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="secondary" {...props} />
);

export const GhostButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="ghost" {...props} />
);

export const DangerButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="danger" {...props} />
);

export const IconButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="icon" {...props} />
);

export const ToolbarButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="toolbar" {...props} />
);

export const CommandButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="command" {...props} />
);

export const DropdownButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="dropdown" {...props} />
);

export const ActionButton: React.FC<BaseButtonProps> = (props) => (
  <BaseButton variant="action" {...props} />
);
