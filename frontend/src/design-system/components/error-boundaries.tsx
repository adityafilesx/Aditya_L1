import React from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import type { FallbackProps } from 'react-error-boundary';
import { Icon } from '@components/common/Icon/Icon';

const GlobalErrorFallback = ({ error, resetErrorBoundary }: FallbackProps) => {
  return (
    <div className="min-h-screen bg-surface flex flex-col items-center justify-center p-6 text-center">
      <Icon name="gpp_bad" className="text-critical text-6xl mb-4" />
      <h1 className="font-display-lg text-headline-md text-on-surface mb-2">CRITICAL SYSTEM FAILURE</h1>
      <p className="font-body-sm text-on-surface-variant max-w-md mb-6">
        The Mission Control UI encountered an unrecoverable rendering error. Diagnostic logs have been retained.
      </p>
      <div className="bg-surface-container-low border border-error/20 rounded p-4 mb-6 max-w-2xl overflow-auto text-left font-data-mono text-xs text-error">
        {(error as Error).message || String(error)}
      </div>
      <button
        onClick={resetErrorBoundary}
        className="px-6 py-2 bg-primary text-on-primary rounded font-label-caps text-label-caps hover:bg-primary-container transition-colors"
      >
        REBOOT SYSTEM
      </button>
    </div>
  );
};

const WidgetErrorFallback = ({ error, resetErrorBoundary }: FallbackProps) => {
  return (
    <div className="w-full h-full min-h-[200px] flex flex-col items-center justify-center bg-error/5 border border-error/20 rounded-xl p-4 text-center">
      <Icon name="error" className="text-error text-3xl mb-2" />
      <p className="font-label-caps text-label-caps text-error mb-1">Widget Render Failure</p>
      <p className="font-data-mono text-[10px] text-on-surface-variant mb-4 truncate w-full max-w-xs">
        {(error as Error).message || String(error)}
      </p>
      <button
        onClick={resetErrorBoundary}
        className="px-3 py-1 bg-surface-container border border-outline-variant rounded font-label-caps text-[10px] hover:bg-surface-container-high transition-colors"
      >
        RETRY
      </button>
    </div>
  );
};

export const AppErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ErrorBoundary FallbackComponent={GlobalErrorFallback}>
      {children}
    </ErrorBoundary>
  );
};

export const WidgetErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ErrorBoundary FallbackComponent={WidgetErrorFallback}>
      {children}
    </ErrorBoundary>
  );
};

export const WebGLErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ErrorBoundary
      FallbackComponent={({ error, resetErrorBoundary }) => (
        <div className="w-full h-full min-h-[400px] flex flex-col items-center justify-center bg-terminal-bg border border-outline/30 rounded-xl p-6 text-center">
          <Icon name="3d_rotation" className="text-primary-fixed text-4xl mb-3 opacity-50" />
          <p className="font-data-mono text-xs text-primary-fixed mb-2">WEBGL_CONTEXT_LOST</p>
          <p className="font-data-mono text-[10px] text-surface-variant/60 mb-6 max-w-sm">
            {(error as Error).message || String(error)}
          </p>
          <button
            onClick={resetErrorBoundary}
            className="px-4 py-1.5 border border-primary-fixed text-primary-fixed rounded font-data-mono text-[10px] hover:bg-primary-fixed/10 transition-colors"
          >
            REINITIALIZE CONTEXT
          </button>
        </div>
      )}
    >
      {children}
    </ErrorBoundary>
  );
};
