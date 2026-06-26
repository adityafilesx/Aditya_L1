import type { ReactNode } from 'react';
import { Sidebar } from '@components/layout/Sidebar';
import { Toolbar } from '@components/layout/Toolbar';
import { Footer } from '@components/layout/Footer';
import { cn } from '@utils/cn';

type LayoutProps = {
  children: ReactNode;
  variant?: 'shell' | 'content-only';
  className?: string;
  mainClassName?: string;
};

export function Layout({
  children,
  variant = 'shell',
  className,
  mainClassName,
}: LayoutProps) {
  if (variant === 'content-only') {
    return <div className={cn('min-h-screen', className)}>{children}</div>;
  }

  return (
    <div className={cn('shell-body', className)}>
      <Sidebar />
      <Toolbar />
      <main
        className={cn(
          'fixed top-[104px] left-[284px] right-8 bottom-14 bg-white rounded-[18px] border border-outline-variant custom-shadow overflow-hidden',
          mainClassName,
        )}
      >
        {children}
      </main>
      <Footer />
    </div>
  );
}
