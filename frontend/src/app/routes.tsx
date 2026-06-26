import { lazy, Suspense } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { Layout } from '@components/layout';
import { ROUTES } from '@constants/index';
import { ShellPage } from '@features/mission/ShellPage';
import { AiScientistPage } from '@features/ai-scientist/AiScientistPage';

const OverviewPage = lazy(() =>
  import('@features/mission/OverviewPage').then((m) => ({ default: m.OverviewPage })),
);
const PlatformPage = lazy(() =>
  import('@features/mission/PlatformPage').then((m) => ({ default: m.PlatformPage })),
);
const OperationsPage = lazy(() =>
  import('@features/mission/OperationsPage').then((m) => ({ default: m.OperationsPage })),
);
const AlertsPage = lazy(() =>
  import('@features/mission/AlertsPage').then((m) => ({ default: m.AlertsPage })),
);
const TimelinePage = lazy(() =>
  import('@features/mission/TimelinePage').then((m) => ({ default: m.TimelinePage })),
);
const IntelligencePage = lazy(() =>
  import('@features/mission/IntelligencePage').then((m) => ({ default: m.IntelligencePage })),
);
const CollaborationPage = lazy(() =>
  import('@features/mission/CollaborationPage').then((m) => ({ default: m.CollaborationPage })),
);
const PhysicsLabPage = lazy(() =>
  import('@features/physics/PhysicsLabPage').then((m) => ({ default: m.PhysicsLabPage })),
);
const DigitalTwinPage = lazy(() =>
  import('@features/digital-twin/DigitalTwinPage').then((m) => ({ default: m.DigitalTwinPage })),
);

const KnowledgeGraphPage = lazy(() =>
  import('@features/knowledge-graph/KnowledgeGraphPage').then((m) => ({ default: m.KnowledgeGraphPage })),
);
const AssetManagerPage = lazy(() =>
  import('@features/knowledge-graph/AssetManagerPage').then((m) => ({ default: m.AssetManagerPage })),
);
const ResearchPage = lazy(() =>
  import('@features/research/ResearchPage').then((m) => ({ default: m.ResearchPage })),
);
const AdminPage = lazy(() =>
  import('@features/admin/AdminPage').then((m) => ({ default: m.AdminPage })),
);
const DesignSystemPage = lazy(() =>
  import('@features/admin/DesignSystemPage').then((m) => ({ default: m.DesignSystemPage })),
);
const SystemDiagnosticsPage = lazy(() =>
  import('@features/admin/SystemDiagnosticsPage').then((m) => ({ default: m.SystemDiagnosticsPage })),
);
const LogsPage = lazy(() =>
  import('@features/admin/LogsPage').then((m) => ({ default: m.LogsPage })),
);
const ConfigurationPage = lazy(() =>
  import('@features/admin/ConfigurationPage').then((m) => ({ default: m.ConfigurationPage })),
);
const SpectralAnalysisPage = lazy(() =>
  import('@features/investigation/SpectralAnalysisPage').then((m) => ({ default: m.SpectralAnalysisPage })),
);
const SensorInspectorPage = lazy(() =>
  import('@features/investigation/SensorInspectorPage').then((m) => ({ default: m.SensorInspectorPage })),
);
const ActiveRegionsPage = lazy(() =>
  import('@features/digital-twin/ActiveRegionsPage').then((m) => ({ default: m.ActiveRegionsPage })),
);

import { PageSkeleton } from '@design-system/components/skeletons';
import { AppErrorBoundary } from '@design-system/components/error-boundaries';

function ShellRoute({ children }: { children: React.ReactNode }) {
  return (
    <AppErrorBoundary>
      <Layout>
        <Suspense fallback={<PageSkeleton />}>{children}</Suspense>
      </Layout>
    </AppErrorBoundary>
  );
}



export function AppRouter() {
  return (
    <Routes>
      <Route
        path={ROUTES.shell}
        element={
          <ShellRoute>
            <ShellPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.platform}
        element={
          <ShellRoute>
            <PlatformPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.overview}
        element={
          <ShellRoute>
            <OverviewPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.operations}
        element={
          <ShellRoute>
            <OperationsPage />
          </ShellRoute>
        }
      />
      <Route
        path="/operations/alerts"
        element={
          <ShellRoute>
            <AlertsPage />
          </ShellRoute>
        }
      />
      <Route
        path="/operations/timeline"
        element={
          <ShellRoute>
            <TimelinePage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.intelligence}
        element={
          <ShellRoute>
            <IntelligencePage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.ai}
        element={
          <ShellRoute>
            <AiScientistPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.physics}
        element={
          <ShellRoute>
            <PhysicsLabPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.digitalTwin}
        element={
          <ShellRoute>
            <DigitalTwinPage />
          </ShellRoute>
        }
      />

      <Route
        path={ROUTES.knowledgeGraph}
        element={
          <ShellRoute>
            <KnowledgeGraphPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.assetManager}
        element={
          <ShellRoute>
            <AssetManagerPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.research}
        element={
          <ShellRoute>
            <ResearchPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.collaboration}
        element={
          <ShellRoute>
            <CollaborationPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.admin}
        element={
          <ShellRoute>
            <AdminPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.designSystem}
        element={
          <ShellRoute>
            <DesignSystemPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.spectral}
        element={
          <ShellRoute>
            <SpectralAnalysisPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.sensors}
        element={
          <ShellRoute>
            <SensorInspectorPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.regions}
        element={
          <ShellRoute>
            <ActiveRegionsPage />
          </ShellRoute>
        }
      />
      <Route
        path={ROUTES.diagnostics}
        element={
          <ShellRoute>
            <SystemDiagnosticsPage />
          </ShellRoute>
        }
      />
      <Route
        path="/system/logs"
        element={
          <ShellRoute>
            <LogsPage />
          </ShellRoute>
        }
      />
      <Route
        path="/system/config"
        element={
          <ShellRoute>
            <ConfigurationPage />
          </ShellRoute>
        }
      />
      <Route path="*" element={<Navigate to={ROUTES.shell} replace />} />
    </Routes>
  );
}
