import type { FC } from 'react';
import { 
  PageLayout, 
  Header, 
  BaseCard, 
  SeverityBadge, 
  EnterpriseTable, 
  Icon
} from '@design-system/index';
import type { ColumnDef } from '@design-system/index';

interface LogbookRow {
  id: string;
  time: string;
  subsystem: string;
  category: string;
  severity: string;
}

const LOGBOOK_DATA: LogbookRow[] = [
  { id: '1', time: '14:21:05.112', subsystem: 'VELC', category: 'CALIBRATION', severity: 'INFO' },
  { id: '2', time: '14:19:44.801', subsystem: 'SUIT', category: 'DATA_LINK', severity: 'WARN' },
  { id: '3', time: '14:15:00.000', subsystem: 'PAPA', category: 'STATE_CHANGE', severity: 'INFO' }
];

export const CollaborationPageContent: FC = () => {
  const columns: ColumnDef<LogbookRow>[] = [
    { 
      header: 'UTC TIME', 
      accessorKey: 'time', 
      cell: (row) => <span className="text-on-surface-variant group-hover:text-primary transition-colors">{row.time}</span> 
    },
    { 
      header: 'SUBSYSTEM', 
      accessorKey: 'subsystem' 
    },
    { 
      header: 'CATEGORY', 
      accessorKey: 'category' 
    },
    { 
      header: 'SEVERITY', 
      accessorKey: 'severity', 
      cell: (row) => <SeverityBadge status={row.severity}>{row.severity}</SeverityBadge>,
      className: 'pr-4'
    }
  ];

  return (
    <>
      <Header
        title="Mission Collaboration"
        subtitle="Mission Replay • Reporting • Scientific Review • Collaboration"
        actions={
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-surface-container-lowest px-3 py-1.5 border border-outline-variant rounded shadow-sm">
              <div className="w-2 h-2 rounded-full bg-[#10b981] animate-pulse"></div>
              <span className="font-data-mono text-[11px] text-on-surface">SESSION ACTIVE</span>
            </div>
            <button className="flex items-center gap-2 bg-surface-container-lowest px-3 py-1.5 border border-outline-variant rounded shadow-sm hover:border-primary transition-colors font-label-caps text-label-caps">
              <Icon name="ios_share" className="text-[16px]" /> EXPORT
            </button>
          </div>
        }
      />
      
      <section className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-gutter mb-section-gap">
        <BaseCard variant="plain" className="!p-3 hover:border-primary transition-colors group shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <div className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase tracking-widest">Status</div>
          <div className="flex items-center gap-2">
            <Icon name="check_circle" className="text-[#10b981] text-[16px] fill" />
            <span className="font-numeric-telemetry text-numeric-telemetry text-on-surface group-hover:text-primary transition-colors">Approved</span>
          </div>
        </BaseCard>
        
        <BaseCard variant="plain" className="!p-3 hover:border-primary transition-colors shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <div className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase tracking-widest">Event</div>
          <div className="font-data-mono text-[16px] text-on-surface">AR13872</div>
        </BaseCard>
        
        <BaseCard variant="plain" className="!p-3 hover:border-primary transition-colors shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <div className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase tracking-widest">Confidence</div>
          <div className="font-numeric-telemetry text-numeric-telemetry text-on-surface">96%</div>
        </BaseCard>
        
        <BaseCard variant="plain" className="!p-3 hover:border-primary transition-colors shadow-[0_10px_30px_rgba(15,23,42,0.04)] relative overflow-hidden">
          <div className="absolute bottom-0 left-0 w-full h-1 bg-[#f59e0b]"></div>
          <div className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase tracking-widest">Risk</div>
          <div className="font-numeric-telemetry text-numeric-telemetry text-[#d97706]">21%</div>
        </BaseCard>
        
        <BaseCard variant="plain" className="!p-3 hover:border-primary transition-colors shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <div className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase tracking-widest">Operator</div>
          <div className="font-body-sm text-on-surface truncate">V. Sharma</div>
        </BaseCard>
        
        <BaseCard variant="plain" className="!p-3 hover:border-primary transition-colors shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <div className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase tracking-widest">Reviewer</div>
          <div className="font-body-sm text-on-surface truncate">Dr. K. Rao</div>
        </BaseCard>
        
        <BaseCard variant="plain" className="!p-3 hover:border-primary transition-colors shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <div className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase tracking-widest">Modified</div>
          <div className="font-data-mono text-[12px] text-on-surface">14:22 UTC</div>
        </BaseCard>
      </section>
      
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        <div className="lg:col-span-8 flex flex-col gap-gutter">
          <BaseCard 
            variant="plain" 
            className="flex flex-col overflow-hidden !p-0 shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
            title={
              <span className="font-label-caps text-label-caps text-on-surface flex items-center gap-2">
                <Icon name="movie" className="text-[16px]" /> REPLAY ENGINE
              </span>
            }
            badge={
              <div className="font-data-mono text-[12px] bg-surface-container-high px-2 py-0.5 rounded text-on-surface-variant">SYNC: ACTIVE</div>
            }
          >
            <div className="h-64 bg-inverse-surface grid-bg relative p-4 flex flex-col justify-end">
              <div className="absolute inset-0 flex items-center justify-center opacity-20">
                <Icon name="satellite_alt" size="xl" className="text-white" />
              </div>
              
              <div className="absolute top-4 left-4 flex flex-col gap-1 z-10">
                <div className="font-data-mono text-[10px] text-[#10b981]">VEL: 4.2 km/s</div>
                <div className="font-data-mono text-[10px] text-[#f59e0b]">ALT: 1.5M km</div>
                <div className="font-data-mono text-[10px] text-white">ATT: NOMINAL</div>
              </div>
              
              <div className="bg-surface-container-lowest/10 backdrop-blur-md border border-white/10 rounded p-2 flex items-center justify-between z-10 gap-4 mt-auto">
                <div className="flex items-center gap-1">
                  <button className="text-white hover:text-primary-fixed transition-colors"><Icon name="skip_previous" /></button>
                  <button className="text-white hover:text-primary-fixed transition-colors"><Icon name="play_arrow" /></button>
                  <button className="text-white hover:text-primary-fixed transition-colors"><Icon name="skip_next" /></button>
                </div>
                <div className="flex-1 h-1 bg-white/20 rounded-full relative cursor-pointer">
                  <div className="absolute top-0 left-0 h-full w-[45%] bg-primary-fixed rounded-full"></div>
                  <div className="absolute top-1/2 left-[45%] -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow border-2 border-primary-fixed"></div>
                </div>
                <div className="font-data-mono text-[12px] text-white flex items-center gap-2">
                  <span>T+ 04:12:33</span>
                  <span className="text-white/50">/</span>
                  <span className="text-white/50">T+ 09:00:00</span>
                </div>
                <div className="font-data-mono text-[10px] text-white/70 bg-white/10 px-2 rounded">1.0x</div>
              </div>
            </div>
          </BaseCard>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
            <BaseCard 
              variant="plain" 
              className="overflow-hidden !p-0 shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
              title={
                <span className="font-label-caps text-label-caps text-on-surface-variant flex justify-between w-full">
                  <span>SOLAR FLUX (X-RAY)</span>
                  <Icon name="show_chart" className="text-[14px]" />
                </span>
              }
            >
              <div className="h-40 p-2 relative">
                <div className="bg-cover bg-center w-full h-full rounded border border-outline-variant/50"></div>
              </div>
            </BaseCard>
            
            <BaseCard 
              variant="plain" 
              className="overflow-hidden !p-0 shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
              title={
                <span className="font-label-caps text-label-caps text-on-surface-variant flex justify-between w-full">
                  <span>PHYSICS DIAGNOSTICS</span>
                  <Icon name="biotech" className="text-[14px]" />
                </span>
              }
            >
              <div className="h-40 p-4 relative flex flex-col gap-1 justify-center">
                <div className="flex justify-between items-center text-[11px] font-data-mono border-b border-outline-variant/30 pb-1">
                  <span className="text-on-surface-variant">TEMP_CORE</span>
                  <span className="text-on-surface">5.4M K</span>
                </div>
                <div className="flex justify-between items-center text-[11px] font-data-mono border-b border-outline-variant/30 pb-1">
                  <span className="text-on-surface-variant">MAG_FIELD</span>
                  <span className="text-on-surface">120 G</span>
                </div>
                <div className="flex justify-between items-center text-[11px] font-data-mono border-b border-outline-variant/30 pb-1">
                  <span className="text-on-surface-variant">DENSITY</span>
                  <span className="text-on-surface">1e9 cm⁻³</span>
                </div>
              </div>
            </BaseCard>
            
            <BaseCard 
              variant="plain" 
              className="overflow-hidden !p-0 shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
              title={
                <span className="font-label-caps text-label-caps text-on-surface-variant flex justify-between w-full">
                  <span>DIGITAL TWIN (SUIT)</span>
                  <Icon name="view_in_ar" className="text-[14px]" />
                </span>
              }
            >
              <div className="h-40 p-2 bg-[#191c1e] relative">
                <div className="w-full h-full border border-[#4140d1]/30 rounded flex items-center justify-center relative overflow-hidden">
                  <div className="absolute w-20 h-20 border border-[#4140d1] rounded-full animate-[spin_10s_linear_infinite]"></div>
                  <div className="absolute w-16 h-16 border-t border-b border-white/50 rounded-full animate-[spin_5s_linear_infinite_reverse]"></div>
                </div>
              </div>
            </BaseCard>
            
            <BaseCard 
              variant="plain" 
              className="overflow-hidden !p-0 shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
              title={
                <span className="font-label-caps text-label-caps text-on-surface-variant flex justify-between w-full">
                  <span>KNOWLEDGE GRAPH</span>
                  <Icon name="hub" className="text-[14px]" />
                </span>
              }
            >
              <div className="h-40 p-2 relative flex items-center justify-center">
                <div className="bg-cover bg-center w-full h-full rounded opacity-70"></div>
              </div>
            </BaseCard>
          </div>
          
          <EnterpriseTable
            title="MISSION LOGBOOK"
            data={LOGBOOK_DATA}
            columns={columns}
            actions={<button className="text-primary text-[11px] font-data-mono hover:underline">VIEW ALL</button>}
            className="shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
          />
        </div>
        
        <div className="lg:col-span-4 flex flex-col gap-gutter">
          <BaseCard 
            variant="plain" 
            className="flex flex-col h-[400px] !p-0 shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
            title={
              <span className="font-label-caps text-label-caps text-on-surface flex items-center gap-2">
                <Icon name="forum" className="text-[16px]" /> THREADS
              </span>
            }
            badge={
              <span className="bg-primary-container text-on-primary-container px-1.5 rounded-full text-[10px] font-bold">3</span>
            }
          >
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded bg-surface-container-high border border-outline-variant flex items-center justify-center shrink-0 font-label-caps text-[10px]">OP</div>
                <div>
                  <div className="flex items-baseline gap-2">
                    <span className="font-label-caps text-[11px] text-on-surface">operator07</span>
                    <span className="font-data-mono text-[9px] text-on-surface-variant">14:05 UTC</span>
                  </div>
                  <p className="font-body-sm text-[13px] mt-1 text-on-surface">Noticing a slight deviation in the SUIT thermal profile at T+ 03:45. <span className="text-primary">@review_team</span> can we validate this against the twin?</p>
                </div>
              </div>
              
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded bg-primary-fixed border border-primary/20 flex items-center justify-center shrink-0 font-label-caps text-[10px] text-on-primary-fixed">KR</div>
                <div>
                  <div className="flex items-baseline gap-2">
                    <span className="font-label-caps text-[11px] text-on-surface">dr_krao</span>
                    <span className="font-data-mono text-[9px] text-on-surface-variant">14:10 UTC</span>
                  </div>
                  <p className="font-body-sm text-[13px] mt-1 text-on-surface">Reviewing now. Attaching spectral fit from the last polling cycle.</p>
                  <div className="mt-2 border border-outline-variant rounded p-2 flex items-center gap-2 bg-surface-container-low hover:border-primary transition-colors cursor-pointer w-max">
                    <Icon name="image" className="text-[16px] text-outline" />
                    <span className="font-data-mono text-[10px]">fit_AR13872_v2.png</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="p-3 border-t border-outline-variant bg-surface shrink-0">
              <div className="flex items-center gap-2 bg-surface-container-lowest border border-outline-variant rounded p-1 focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/10 transition-all">
                <input className="w-full bg-transparent border-none text-[13px] focus:ring-0 px-2 placeholder-outline-variant font-body-sm outline-none" placeholder="Add a note or @mention..." type="text"/>
                <button className="p-1 text-on-surface-variant hover:text-primary transition-colors"><Icon name="attach_file" className="text-[18px]" /></button>
                <button className="p-1 bg-primary text-on-primary rounded hover:bg-primary-container transition-colors"><Icon name="send" className="text-[18px]" /></button>
              </div>
            </div>
          </BaseCard>
          
          <BaseCard 
            variant="plain" 
            className="flex flex-col flex-1 !p-0 shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
            title={
              <span className="font-label-caps text-label-caps text-on-surface flex items-center gap-2">
                <Icon name="checklist" className="text-[16px]" /> REVIEW TASKS
              </span>
            }
          >
            <div className="p-3 space-y-2 overflow-y-auto">
              <div className="border border-outline-variant rounded p-2.5 flex items-start gap-3 hover:border-primary transition-colors cursor-pointer group">
                <div className="w-4 h-4 rounded border border-outline-variant mt-0.5 group-hover:border-primary"></div>
                <div>
                  <div className="font-body-sm text-[13px] font-medium text-on-surface">Validate CME Velocity Model</div>
                  <div className="font-label-caps text-[9px] text-on-surface-variant mt-1">PENDING VALIDATION</div>
                </div>
              </div>
              
              <div className="border border-outline-variant rounded p-2.5 flex items-start gap-3 bg-surface-container-low cursor-pointer">
                <div className="w-4 h-4 rounded border-none bg-[#10b981] mt-0.5 flex items-center justify-center">
                  <Icon name="check" className="text-white text-[12px] font-bold" />
                </div>
                <div>
                  <div className="font-body-sm text-[13px] font-medium text-on-surface line-through opacity-70">Cross-check magnetometer raw data</div>
                  <div className="font-label-caps text-[9px] text-on-surface-variant mt-1">MODEL REVIEW</div>
                </div>
              </div>
              
              <div className="border border-outline-variant rounded p-2.5 flex items-start gap-3 hover:border-primary transition-colors cursor-pointer group">
                <div className="w-4 h-4 rounded border border-outline-variant mt-0.5 group-hover:border-primary"></div>
                <div>
                  <div className="font-body-sm text-[13px] font-medium text-on-surface">Draft Executive Summary paragraph 2</div>
                  <div className="font-label-caps text-[9px] text-on-surface-variant mt-1 text-[#d97706]">PUBLICATION CHECKLIST</div>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter mt-gutter mb-section-gap">
        <BaseCard 
          variant="plain" 
          className="flex flex-col h-[300px] overflow-hidden !p-0 shadow-[0_10px_30px_rgba(15,23,42,0.04)] lg:col-span-8"
          title={
            <span className="font-label-caps text-label-caps text-on-surface">REPORT BUILDER</span>
          }
          actions={
            <div className="hidden sm:flex gap-2">
              <button className="p-1 text-on-surface-variant hover:bg-surface-container-high rounded"><Icon name="format_bold" className="text-[16px]" /></button>
              <button className="p-1 text-on-surface-variant hover:bg-surface-container-high rounded"><Icon name="format_italic" className="text-[16px]" /></button>
              <button className="p-1 text-on-surface-variant hover:bg-surface-container-high rounded"><Icon name="code" className="text-[16px]" /></button>
            </div>
          }
          footer={
            <div className="font-data-mono text-[10px] text-on-surface-variant w-full text-right">Last saved: 2m ago</div>
          }
        >
          <div className="p-6 overflow-y-auto flex-1 font-body-sm text-on-surface leading-relaxed border-t border-outline-variant/30">
            <h2 className="text-lg font-semibold mb-4">1.0 Preliminary Observations of AR13872</h2>
            <p className="mb-3">During the observation window 14:00 - 15:00 UTC, the VELC instrument recorded anomalous scattering corresponding to a minor coronal mass ejection (CME) precursor.</p>
            <p className="font-data-mono text-[12px] bg-surface-container p-3 rounded border border-outline-variant/50 text-tertiary mb-3">
              {'\\begin{equation}'}<br/>
              F<sub>λ</sub> = ∫<sub>0</sub><sup>∞</sup> S<sub>λ</sub>(τ) e<sup>-τ</sup> dτ<br/>
              {'\\end{equation}'}
            </p>
            <p className="mb-0">The spectral lines indicate a localized temperature spike exceeding standard operational bounds by 4%, warranting further review against the digital twin baseline models.</p>
          </div>
        </BaseCard>
        
        <div className="lg:col-span-4 flex flex-col gap-gutter">
          <BaseCard 
            variant="plain" 
            className="p-4 flex-1 shadow-[0_10px_30px_rgba(15,23,42,0.04)]"
            title={
              <span className="font-label-caps text-label-caps text-on-surface">MEDIA ASSETS</span>
            }
            actions={
              <span className="text-[10px] font-data-mono text-primary cursor-pointer hover:underline">VIEW GRID</span>
            }
          >
            <div className="grid grid-cols-3 gap-2 mt-4">
              <div className="aspect-square bg-cover bg-center rounded border border-outline-variant hover:border-primary transition-colors cursor-pointer"></div>
              <div className="aspect-square bg-cover bg-center rounded border border-outline-variant hover:border-primary transition-colors cursor-pointer"></div>
              <div className="aspect-square rounded border border-dashed border-outline-variant flex items-center justify-center text-outline hover:text-primary hover:border-primary transition-colors cursor-pointer bg-surface-container-low">
                <Icon name="add" className="text-[20px]" />
              </div>
            </div>
          </BaseCard>
          
          <div className="bg-primary border border-primary-fixed rounded-xl p-4 text-on-primary flex items-center justify-between shadow-[0_10px_30px_rgba(65,64,209,0.15)] cursor-pointer hover:bg-primary-container transition-colors">
            <div>
              <div className="font-label-caps text-[12px] font-bold tracking-wider">GENERATE PUBLICATION</div>
              <div className="font-data-mono text-[10px] text-on-primary/70 mt-1">PDF / IEEE FORMAT / ZIP</div>
            </div>
            <Icon name="cloud_download" className="text-[24px]" />
          </div>
        </div>
      </div>
    </>
  );
};

export const CollaborationPage: FC = () => (
  <PageLayout className="p-0" data-layout="precision">
    <div className="p-6">
      <CollaborationPageContent />
    </div>
  </PageLayout>
);

export default CollaborationPage;
