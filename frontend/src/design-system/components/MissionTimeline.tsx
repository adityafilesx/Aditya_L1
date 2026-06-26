import React from 'react';
import { useWorkspaceStore } from '../../realtime/workspaceStore';
import { useStreamStore } from '../../realtime/streamStore';
import { Icon } from '@components/common/Icon/Icon';
import { cn } from '../../utils/cn';

export const MissionTimeline: React.FC<{ className?: string }> = ({ className }) => {
  const { globalCursorTime, isPlaying, setReplayState, setCursorTime } = useWorkspaceStore();
  const history = useStreamStore(state => state.history);
  
  const minTime = history.telemetry.length > 0 ? new Date(history.telemetry[0].timestamp).getTime() : Date.now() - 24 * 3600 * 1000;
  const maxTime = history.telemetry.length > 0 ? new Date(history.telemetry[history.telemetry.length - 1].timestamp).getTime() : Date.now();
  
  const handleScrub = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    const newTime = minTime + percent * (maxTime - minTime);
    setCursorTime(newTime);
  };
  
  const percent = globalCursorTime ? Math.max(0, Math.min(100, ((globalCursorTime - minTime) / (maxTime - minTime)) * 100)) : 100;
  
  return (
    <div className={cn("flex flex-col gap-2 p-4 bg-surface-container-highest border border-outline-variant rounded-lg", className)}>
      <div className="flex justify-between items-center px-1">
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setReplayState(!isPlaying)}
            className="w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center hover:bg-primary/90 transition-colors border-none cursor-pointer"
          >
            <Icon name={isPlaying ? "pause" : "play_arrow"} filled className="text-[18px]" />
          </button>
          <span className="font-data-mono text-data-mono text-primary font-bold">
            {globalCursorTime ? new Date(globalCursorTime).toISOString().substring(11, 19) : "LIVE"}
          </span>
        </div>
        <div className="flex gap-4">
          <span className="font-label-caps text-[10px] text-on-surface-variant cursor-pointer hover:text-primary">MINUTES</span>
          <span className="font-label-caps text-[10px] text-primary border-b border-primary">HOURS</span>
          <span className="font-label-caps text-[10px] text-on-surface-variant cursor-pointer hover:text-primary">DAYS</span>
        </div>
      </div>
      
      <div 
        className="relative w-full h-3 bg-surface-container-high rounded-full cursor-pointer overflow-hidden"
        onMouseDown={handleScrub}
      >
        <div 
          className="absolute left-0 top-0 h-full bg-primary/30"
          style={{ width: `${percent}%` }}
        />
        <div 
          className="absolute top-0 h-full w-1 bg-primary transform -translate-x-1/2"
          style={{ left: `${percent}%` }}
        />
      </div>
      
      <div className="flex justify-between px-1 mt-1 text-[10px] text-outline font-data-mono">
        <span>{new Date(minTime).toLocaleTimeString()}</span>
        <span>{new Date(minTime + (maxTime - minTime) / 2).toLocaleTimeString()}</span>
        <span>{new Date(maxTime).toLocaleTimeString()}</span>
      </div>
    </div>
  );
};
