import type { NavSection, ToolbarTab } from '@app-types/index';

export const SHELL_NAV_SECTIONS: NavSection[] = [
  {
    id: 'overview',
    title: 'Overview',
    items: [
      { id: 'mission-overview', label: 'Mission Overview', icon: 'dashboard', path: '/overview' },
    ],
  },
  {
    id: 'operations',
    title: 'Operations',
    items: [
      { id: 'nowcasting', label: 'Nowcasting', icon: 'settings_remote', path: '/operations/nowcasting', filled: true },
      { id: 'forecasting', label: 'Forecasting', icon: 'analytics', path: '/forecast' },
      { id: 'alerts', label: 'Alerts', icon: 'notifications_active', path: '/operations/alerts' },
      { id: 'timeline', label: 'Timeline', icon: 'view_timeline', path: '/operations/timeline' },
    ],
  },
  {
    id: 'investigation',
    title: 'Investigation',
    items: [
      { id: 'ai-intelligence', label: 'AI Intelligence', icon: 'psychology', path: '/investigation/ai' },
      { id: 'physics', label: 'Physics', icon: 'lyrics', path: '/investigation/physics' },
      { id: 'spectral', label: 'Spectral Analysis', icon: 'open_run', path: '/investigation/spectral' },
      { id: 'sensor-inspector', label: 'Sensor Inspector', icon: 'troubleshoot', path: '/investigation/sensors' },
    ],
  },
  {
    id: 'digital-twin',
    title: 'Digital Twin',
    items: [
      { id: 'solar-twin', label: 'Solar Twin', icon: 'view_in_ar', path: '/digital-twin' },
      { id: 'active-regions', label: 'Active Regions', icon: 'emergency_recording', path: '/digital-twin/regions' },
    ],
  },
  {
    id: 'knowledge',
    title: 'Knowledge',
    items: [
      { id: 'knowledge-graph', label: 'Knowledge Graph', icon: 'hub', path: '/knowledge/graph' },
      { id: 'asset-manager', label: 'Asset Manager', icon: 'image_search', path: '/knowledge/assets' },
      { id: 'event-library', label: 'Event Library', icon: 'menu_book', path: '/knowledge/events' },
      { id: 'research', label: 'AI Scientist', icon: 'science', path: '/research' },
      { id: 'collaboration', label: 'Collaboration', icon: 'groups', path: '/reports/collaboration' },
    ],
  },
  {
    id: 'system',
    title: 'System',
    items: [
      { id: 'intelligence', label: 'Space Weather', icon: 'public', path: '/intelligence' },
      { id: 'system-health', label: 'System Health', icon: 'health_metrics', path: '/system/diagnostics' },
      { id: 'logs', label: 'Logs', icon: 'terminal', path: '/system/logs' },
      { id: 'configuration', label: 'Configuration', icon: 'settings', path: '/system/config' },
      { id: 'design-system', label: 'Design System', icon: 'palette', path: '/docs/design' },
    ],
  },
];

export const TOOLBAR_TABS: ToolbarTab[] = [
  { id: 'operations', label: 'Operations' },
  { id: 'analysis', label: 'Analysis' },
  { id: 'digital-twin', label: 'Digital Twin' },
  { id: 'reports', label: 'Reports' },
  { id: 'system', label: 'System' },
];

export const ROUTES = {
  shell: '/',
  platform: '/operations/nowcasting',
  overview: '/overview',
  operations: '/operations',
  intelligence: '/intelligence',
  ai: '/investigation/ai',
  physics: '/investigation/physics',
  digitalTwin: '/digital-twin',
  knowledgeGraph: '/knowledge/graph',
  assetManager: '/knowledge/assets',
  research: '/research',
  collaboration: '/reports/collaboration',
  admin: '/system/admin',
  designSystem: '/docs/design',
  spectral: '/investigation/spectral',
  sensors: '/investigation/sensors',
  regions: '/digital-twin/regions',
  diagnostics: '/system/diagnostics',
} as const;
