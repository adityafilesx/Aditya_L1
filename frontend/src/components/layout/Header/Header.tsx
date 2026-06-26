import type { ReactNode } from 'react';
import { Icon } from '@components/common/Icon';
import { cn } from '@utils/cn';
import { commanderAvatar } from '@assets/images';

type HeaderNavItem = {
  id: string;
  label: string;
  href?: string;
  active?: boolean;
};

type HeaderProps = {
  title: string;
  navItems?: HeaderNavItem[];
  showIcons?: boolean;
  className?: string;
  children?: ReactNode;
};

export function Header({
  title,
  navItems = [],
  showIcons = true,
  className,
  children,
}: HeaderProps) {
  return (
    <header
      className={cn(
        'bg-surface border-b border-outline-variant flex justify-between items-center w-full px-container-margin py-component-padding-y fixed top-0 z-50',
        className,
      )}
    >
      <div className="flex items-center gap-8">
        <h1 className="font-display-lg text-headline-md font-bold text-primary">{title}</h1>
        {navItems.length > 0 && (
          <nav className="hidden md:flex gap-6">
            {navItems.map((item) => (
              <a
                key={item.id}
                href={item.href ?? '#'}
                className={cn(
                  'font-label-caps text-label-caps transition-colors',
                  item.active
                    ? 'text-primary border-b-2 border-primary pb-1 font-bold'
                    : 'text-on-surface-variant hover:text-primary',
                )}
              >
                {item.label}
              </a>
            ))}
          </nav>
        )}
      </div>
      <div className="flex items-center gap-4">
        {children}
        {showIcons && (
          <>
            <Icon name="schedule" className="text-on-surface-variant cursor-pointer hover:text-primary" />
            <Icon name="timer" className="text-on-surface-variant cursor-pointer hover:text-primary" />
            <Icon name="notifications" className="text-on-surface-variant cursor-pointer hover:text-primary" />
            <img
              className="w-10 h-10 rounded-full border border-outline-variant object-cover"
              src={commanderAvatar}
              alt="Mission commander"
            />
          </>
        )}
      </div>
    </header>
  );
}
