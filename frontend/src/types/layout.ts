export type LayoutVariant = 'shell' | 'dashboard' | 'precision' | 'standalone';

export type NavItem = {
  id: string;
  label: string;
  icon: string;
  path: string;
  filled?: boolean;
};

export type NavSection = {
  id: string;
  title: string;
  items: NavItem[];
};

export type ToolbarTab = {
  id: string;
  label: string;
};

export type Severity = 'success' | 'warning' | 'critical' | 'info' | 'neutral';

export type KpiMetric = {
  label: string;
  value: string;
  unit?: string;
  trend?: string;
  severity?: Severity;
};
