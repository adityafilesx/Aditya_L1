import os

def explicit_fix():
    # AdminPage
    p = 'src/features/admin/AdminPage.tsx'
    with open(p, 'r') as f: c = f.read()
    c = c.replace("import { FC } from 'react'", "import type { FC } from 'react'")
    with open(p, 'w') as f: f.write(c)

    # DesignSystemPage
    p = 'src/features/admin/DesignSystemPage.tsx'
    with open(p, 'r') as f: c = f.read()
    c = c.replace('title="Last 24 Hours"', 'label="Last 24 Hours"')
    c = c.replace('title="Auto-refresh"', 'label="Auto-refresh"')
    with open(p, 'w') as f: f.write(c)

    # LogsPage
    p = 'src/features/admin/LogsPage.tsx'
    with open(p, 'r') as f: c = f.read()
    c = c.replace('variant="outline"', 'variant="secondary"')
    with open(p, 'w') as f: f.write(c)

    # ForecastSummary
    p = 'src/features/forecast/components/ForecastSummary.tsx'
    with open(p, 'r') as f: c = f.read()
    c = c.replace('title=', 'label=')
    with open(p, 'w') as f: f.write(c)

    # OperationsPage
    p = 'src/features/mission/OperationsPage.tsx'
    with open(p, 'r') as f: c = f.read()
    c = c.replace('<DataDisplay title=', '<DataDisplay label=')
    with open(p, 'w') as f: f.write(c)

    # TimelinePage
    p = 'src/features/mission/TimelinePage.tsx'
    with open(p, 'r') as f: c = f.read()
    c = c.replace('variant="outline"', 'variant="secondary"')
    with open(p, 'w') as f: f.write(c)

    # SpectralAnalysisPage
    p = 'src/features/investigation/SpectralAnalysisPage.tsx'
    with open(p, 'r') as f: c = f.read()
    c = c.replace('title="X-Ray Flux"', "title={{ text: 'X-Ray Flux' }}")
    c = c.replace('title="Power"', "title={{ text: 'Power' }}")
    with open(p, 'w') as f: f.write(c)

explicit_fix()
