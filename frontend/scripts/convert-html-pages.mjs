#!/usr/bin/env node
/**
 * Converts Stitch HTML exports to React TSX page content components.
 * Strips duplicated head/styles/scripts and layout chrome where configured.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const LEGACY = path.join(ROOT, 'stitch-export');

const PAGE_MAP = [
  {
    source: 'aditya_l1_mission_control_shell/code.html',
    feature: 'mission/ShellPage',
    layout: 'shell-placeholder',
  },
  {
    source: 'aditya_l1_integrated_mission_control_platform/code.html',
    feature: 'mission/PlatformPage',
    extract: 'main',
    layout: 'shell',
  },
  {
    source: 'aditya_l1_mission_overview_dashboard/code.html',
    feature: 'mission/OverviewPage',
    extract: 'main',
    layout: 'dashboard',
  },
  {
    source: 'aditya_l1_operations_center/code.html',
    feature: 'mission/OperationsPage',
    extract: 'main',
    layout: 'dashboard',
  },
  {
    source: 'mission_intelligence_space_weather_operations_center/code.html',
    feature: 'mission/IntelligencePage',
    extract: 'main',
    layout: 'precision',
  },
  {
    source: 'ai_intelligence_workspace/code.html',
    feature: 'ai/AiWorkspacePage',
    extract: 'main',
    layout: 'sidebar-main',
  },
  {
    source: 'aditya_l1_physics_laboratory/code.html',
    feature: 'physics/PhysicsLabPage',
    extract: 'main',
    layout: 'shell',
  },
  {
    source: 'aditya_l1_digital_twin_center/code.html',
    feature: 'digital-twin/DigitalTwinPage',
    extract: 'main',
    layout: 'dashboard',
  },
  {
    source: 'aditya_l1_knowledge_graph_intelligence_center/code.html',
    feature: 'knowledge-graph/KnowledgeGraphPage',
    extract: 'main',
    layout: 'dashboard',
  },
  {
    source: 'aditya_l1_mission_collaboration_replay_reporting_center/code.html',
    feature: 'mission/CollaborationPage',
    extract: 'main',
    layout: 'precision',
  },
  {
    source: 'aditya_l1_research_benchmarking_publication_workspace/code.html',
    feature: 'research/ResearchPage',
    extract: 'main',
    layout: 'dashboard',
  },
  {
    source: 'platform_administration_infrastructure_console/code.html',
    feature: 'admin/AdminPage',
    extract: 'main',
    layout: 'precision',
  },
  {
    source: 'mission_control_design_system/code.html',
    feature: 'admin/DesignSystemPage',
    extract: 'main',
    layout: 'shell',
  },
  {
    source: 'three.js/code.html',
    feature: 'digital-twin/ThreeJsViewerPage',
    extract: 'body-full',
    layout: 'standalone',
    skip: true,
  },
];

function htmlToJsx(html) {
  let jsx = html;

  jsx = jsx.replace(/<!--[\s\S]*?-->/g, '');
  jsx = jsx.replace(/<script[\s\S]*?<\/script>/gi, '');
  jsx = jsx.replace(/\sstyle="[^"]*"/gi, '');
  jsx = jsx.replace(/\sdata-alt="[^"]*"/gi, '');
  jsx = jsx.replace(/\sclass=/g, ' className=');
  jsx = jsx.replace(/\sfor=/g, ' htmlFor=');
  jsx = jsx.replace(/\stabindex=/g, ' tabIndex=');
  jsx = jsx.replace(/\sreadonly/g, ' readOnly');
  jsx = jsx.replace(/\smaxlength=/g, ' maxLength=');
  jsx = jsx.replace(/\sminlength=/g, ' minLength=');
  jsx = jsx.replace(/\sautocomplete=/g, ' autoComplete=');
  jsx = jsx.replace(/\scrossorigin=/g, ' crossOrigin=');
  jsx = jsx.replace(/\sfill-rule=/g, ' fillRule=');
  jsx = jsx.replace(/\sclip-rule=/g, ' clipRule=');
  jsx = jsx.replace(/\sstroke-width=/g, ' strokeWidth=');
  jsx = jsx.replace(/\sstroke-linecap=/g, ' strokeLinecap=');
  jsx = jsx.replace(/\sstroke-linejoin=/g, ' strokeLinejoin=');
  jsx = jsx.replace(/\spreserveaspectratio=/g, ' preserveAspectRatio=');
  jsx = jsx.replace(/\sviewbox=/g, ' viewBox=');
  jsx = jsx.replace(/\sclip-path=/g, ' clipPath=');
  jsx = jsx.replace(/\sfill-opacity=/g, ' fillOpacity=');
  jsx = jsx.replace(/\sstop-color=/g, ' stopColor=');
  jsx = jsx.replace(/\sstop-opacity=/g, ' stopOpacity=');
  jsx = jsx.replace(/\sstroke-dasharray=/g, ' strokeDasharray=');

  // Merge duplicate className attributes
  jsx = jsx.replace(/className="([^"]*)"([^>]*?)className="([^"]*)"/g, 'className="$1 $3"$2');

  // Remove duplicate attributes (e.g. duplicate data-icon from re-processing)
  jsx = jsx.replace(/(\s[\w-]+="[^"]*")(\s\1)+/g, '$1');

  jsx = jsx.replace(/<img([^>]*?)(?<!\/)>/gi, '<img$1 />');
  jsx = jsx.replace(/<br(?!\/)>/gi, '<br />');
  jsx = jsx.replace(/<hr(?!\/)>/gi, '<hr />');
  jsx = jsx.replace(/<input([^>]*?)(?<!\/)>/gi, '<input$1 />');
  jsx = jsx.replace(/<meta([^>]*?)(?<!\/)>/gi, '');
  jsx = jsx.replace(/<link([^>]*?)(?<!\/)>/gi, '');

  // Escape LaTeX braces for JSX
  jsx = jsx.replace(/\\begin\{equation\}/g, "{'\\\\begin{equation}'}");
  jsx = jsx.replace(/\\end\{equation\}/g, "{'\\\\end{equation}'}");
  jsx = jsx.replace(/F_\{\\lambda\}/g, 'F<sub>λ</sub>');
  jsx = jsx.replace(/\\int_\{0\}\^\{\\infty\}/g, '∫<sub>0</sub><sup>∞</sup>');
  jsx = jsx.replace(/S_\{\\lambda\}\(\\tau\) e\^\{-\\tau\} d\\tau/g, 'S<sub>λ</sub>(τ) e<sup>-τ</sup> dτ');

  return jsx.trim();
}

function extractContent(html, mode) {
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  if (!bodyMatch) return html;
  let body = bodyMatch[1];

  if (mode === 'body-full') return body;

  if (mode === 'main') {
    const mainMatch = body.match(/<main[^>]*>([\s\S]*)<\/main>/i);
    if (mainMatch) return mainMatch[1];
  }

  return body;
}

function splitIntoSections(html, maxLines = 280) {
  const lines = html.split('\n');
  if (lines.length <= maxLines) return [html];

  const sections = [];
  let current = [];
  let depth = 0;

  for (const line of lines) {
    current.push(line);
    if (line.match(/<section|<div className="[^"]*grid|<article|<header className="flex flex-col/)) {
      if (current.length > 50 && depth === 0) {
        sections.push(current.join('\n'));
        current = [];
      }
      depth++;
    }
    if (line.match(/<\/section>|<\/article>/) && depth > 0) {
      depth--;
      if (depth === 0 && current.length > 20) {
        sections.push(current.join('\n'));
        current = [];
      }
    }
  }
  if (current.length) sections.push(current.join('\n'));
  return sections.length ? sections : [html];
}

function generateComponent(name, content, layout) {
  const componentName = name.split('/').pop();
  const sections = splitIntoSections(content);

  if (sections.length === 1) {
    return `/* eslint-disable */
// Auto-converted from Stitch HTML export. Visual fidelity preserved.
import type { FC } from 'react';

export const ${componentName}Content: FC = () => (
  <>
${sections[0]
  .split('\n')
  .map((l) => '    ' + l)
  .join('\n')}
  </>
);

export const ${componentName}: FC = () => (
  <div className="w-full h-full overflow-auto custom-scrollbar" data-layout="${layout}">
    <${componentName}Content />
  </div>
);
`;
  }

  const sectionComponents = sections
    .map((section, i) => {
      const sectionName = `${componentName}Section${i + 1}`;
      return {
        name: sectionName,
        code: `const ${sectionName}: FC = () => (
  <>
${section
  .split('\n')
  .map((l) => '    ' + l)
  .join('\n')}
  </>
);`,
      };
    });

  return `/* eslint-disable */
// Auto-converted from Stitch HTML export. Visual fidelity preserved.
import type { FC } from 'react';

${sectionComponents.map((s) => s.code).join('\n\n')}

export const ${componentName}Content: FC = () => (
  <>
${sectionComponents.map((s) => `    <${s.name} />`).join('\n')}
  </>
);

export const ${componentName}: FC = () => (
  <div className="w-full h-full overflow-auto custom-scrollbar" data-layout="${layout}">
    <${componentName}Content />
  </div>
);
`;
}

for (const page of PAGE_MAP) {
  const sourcePath = path.join(LEGACY, page.source);
  if (!fs.existsSync(sourcePath)) {
    console.warn(`Skip missing: ${page.source}`);
    continue;
  }

  if (page.layout === 'shell-placeholder') {
    const outDir = path.join(ROOT, 'src/features/mission');
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(
      path.join(outDir, 'ShellPage.tsx'),
      `import { Icon } from '@components/common/Icon';

export function ShellPage() {
  return (
    <div className="w-full h-full p-10 flex flex-col items-center justify-center text-center opacity-20">
      <Icon name="space_dashboard" size="xl" className="mb-4" />
      <h3 className="font-display-lg text-[24px]">Mission Workspace Ready</h3>
      <p className="font-body-lg">Select an operational module from the sidebar to begin analysis.</p>
    </div>
  );
}
`,
    );
    console.log('Generated ShellPage.tsx');
    continue;
  }

  if (page.skip) {
    console.log(`Skipped manual page: ${page.feature}`);
    continue;
  }

  const html = fs.readFileSync(sourcePath, 'utf8');
  const extracted = extractContent(html, page.extract);
  const jsx = htmlToJsx(extracted);
  const componentCode = generateComponent(page.feature, jsx, page.layout);
  const [featureDir, fileName] = [
    path.join(ROOT, 'src/features', page.feature.split('/')[0]),
    `${page.feature.split('/')[1]}.tsx`,
  ];
  fs.mkdirSync(featureDir, { recursive: true });
  fs.writeFileSync(path.join(featureDir, fileName), componentCode);
  console.log(`Generated ${page.feature}.tsx (${jsx.split('\n').length} lines)`);
}

console.log('Conversion complete.');
