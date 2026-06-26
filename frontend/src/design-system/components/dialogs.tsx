import React from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';
import { PrimaryButton, SecondaryButton } from './buttons';

export interface BaseDialogProps {
  isOpen: boolean;
  onClose: () => void;
  title?: React.ReactNode;
  children?: React.ReactNode;
  actions?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'fullscreen';
  className?: string;
}

// 1. Modal
export const Modal: React.FC<BaseDialogProps> = ({
  isOpen,
  onClose,
  title,
  children,
  actions,
  size = 'md',
  className,
}) => {
  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-xl',
    lg: 'max-w-3xl',
    xl: 'max-w-5xl',
    fullscreen: 'max-w-none w-screen h-screen rounded-none',
  };

  return (
    <div className="fixed inset-0 bg-black/55 backdrop-blur-sm flex items-center justify-center p-4 z-[1000] animate-fade-in">
      <div
        className={cn(
          'w-full bg-white rounded-xl shadow-xl flex flex-col border border-outline-variant max-h-[90vh] overflow-hidden',
          sizeClasses[size],
          className
        )}
      >
        <div className="flex justify-between items-center px-6 py-4 border-b border-outline-variant">
          {title && <h3 className="font-headline-md text-headline-md text-on-surface">{title}</h3>}
          <button
            onClick={onClose}
            className="p-1 hover:bg-surface-container rounded-full transition-colors text-on-surface-variant"
            aria-label="Close dialog"
          >
            <Icon name="close" />
          </button>
        </div>
        <div className="flex-1 p-6 overflow-y-auto custom-scrollbar">{children}</div>
        {actions && (
          <div className="px-6 py-4 border-t border-outline-variant bg-surface-container-low flex justify-end gap-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
};

// 2. Drawer (Sliding side panel)
export const Drawer: React.FC<BaseDialogProps & { position?: 'left' | 'right' }> = ({
  isOpen,
  onClose,
  title,
  children,
  actions,
  position = 'right',
  className,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-[1000] flex justify-end">
      <div onClick={onClose} className="absolute inset-0 cursor-pointer" />
      <div
        className={cn(
          'relative w-full max-w-lg bg-white h-full shadow-2xl flex flex-col z-[1010]',
          position === 'right' ? 'animate-slide-in-right' : 'animate-slide-in-left',
          className
        )}
      >
        <div className="flex justify-between items-center px-6 py-4 border-b border-outline-variant">
          {title && <h3 className="font-headline-md text-headline-md text-on-surface">{title}</h3>}
          <button
            onClick={onClose}
            className="p-1 hover:bg-surface-container rounded-full transition-colors"
            aria-label="Close panel"
          >
            <Icon name="close" />
          </button>
        </div>
        <div className="flex-1 p-6 overflow-y-auto custom-scrollbar">{children}</div>
        {actions && (
          <div className="px-6 py-4 border-t border-outline-variant bg-surface-container-low flex justify-end gap-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
};

// 3. ConfirmationDialog
export interface ConfirmationDialogProps extends BaseDialogProps {
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  loading?: boolean;
}

export const ConfirmationDialog: React.FC<ConfirmationDialogProps> = ({
  isOpen,
  onClose,
  title = 'Confirmation Required',
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  onConfirm,
  loading = false,
}) => (
  <Modal
    isOpen={isOpen}
    onClose={onClose}
    title={title}
    size="sm"
    actions={
      <>
        <SecondaryButton onClick={onClose} disabled={loading}>
          {cancelLabel}
        </SecondaryButton>
        <PrimaryButton onClick={onConfirm} loading={loading}>
          {confirmLabel}
        </PrimaryButton>
      </>
    }
  >
    <p className="text-body-sm text-on-surface-variant">{message}</p>
  </Modal>
);

// 4. FullscreenDialog
export const FullscreenDialog: React.FC<BaseDialogProps> = (props) => (
  <Modal size="fullscreen" {...props} />
);

// 5. InspectorPanel
export const InspectorPanel: React.FC<BaseDialogProps> = (props) => (
  <Drawer position="right" {...props} />
);

// 6. SettingsDialog
export const SettingsDialog: React.FC<BaseDialogProps> = (props) => (
  <Drawer position="right" title={props.title || 'System Settings'} {...props} />
);

// 7. QuickActionDialog
export const QuickActionDialog: React.FC<BaseDialogProps> = (props) => (
  <Modal size="sm" title={props.title || 'Quick Actions'} {...props} />
);
