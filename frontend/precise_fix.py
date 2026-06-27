import os

def precise_fix(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # DataDisplay, Checkbox, Slider need label
    content = content.replace('<DataDisplay title=', '<DataDisplay label=')
    content = content.replace('<Slider title=', '<Slider label=')
    content = content.replace('<Checkbox title=', '<Checkbox label=')
    content = content.replace('<TimeRangeSelector title=', '<TimeRangeSelector label=') # For DesignSystemPage
    
    # ForecastSummary uses SummaryItem or something?
    content = content.replace('<SummaryItem title=', '<SummaryItem label=')
    
    # MetricCard needs title instead of label
    content = content.replace('<MetricCard label=', '<MetricCard title=')
    content = content.replace('<LargeMetricCard label=', '<LargeMetricCard title=')
    
    # Button and Badge need title instead of label (in case any were missed or reverted)
    # The previous script did this, but just to be sure:
    content = content.replace('<BaseButton label=', '<BaseButton title=')
    content = content.replace('<PrimaryButton label=', '<PrimaryButton title=')
    content = content.replace('<SecondaryButton label=', '<SecondaryButton title=')
    content = content.replace('<GhostButton label=', '<GhostButton title=')
    content = content.replace('<DangerButton label=', '<DangerButton title=')
    content = content.replace('<IconButton label=', '<IconButton title=')
    content = content.replace('<ToolbarButton label=', '<ToolbarButton title=')
    content = content.replace('<CommandButton label=', '<CommandButton title=')
    content = content.replace('<DropdownButton label=', '<DropdownButton title=')
    content = content.replace('<ActionButton label=', '<ActionButton title=')
    
    content = content.replace('<BaseBadge label=', '<BaseBadge title=')
    content = content.replace('<StatusBadge label=', '<StatusBadge title=')
    content = content.replace('<HealthBadge label=', '<HealthBadge title=')
    content = content.replace('<RiskBadge label=', '<RiskBadge title=')
    content = content.replace('<MissionBadge label=', '<MissionBadge title=')
    content = content.replace('<TelemetryBadge label=', '<TelemetryBadge title=')
    content = content.replace('<ConfidenceBadge label=', '<ConfidenceBadge title=')
    content = content.replace('<SeverityBadge label=', '<SeverityBadge title=')
    
    # In AdminPage, fix import FC if reverted
    content = content.replace("import { FC } from 'react'", "import type { FC } from 'react'")
    
    # SpectralAnalysisPage.tsx(59,26): error TS2559: Type 'string' has no properties in common with type 'Partial<DataTitle>'
    # I'll manually fix this later if this regex doesn't catch it
    
    with open(filepath, 'w') as f:
        f.write(content)

src_dir = '/Users/aditya1981/Documents/Unified Data Ingestion Engine/frontend/src'
for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'):
            precise_fix(os.path.join(root, f))
