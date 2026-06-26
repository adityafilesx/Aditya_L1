import { create } from 'zustand';

interface ActiveRegion {
  id: string;
  lat: number;
  lon: number;
  hale_class?: string;
  mcintosh_class?: string;
}

interface DigitalTwinState {
  photosphereOpacity: number;
  chromosphereOpacity: number;
  coronaOpacity: number;
  magneticOpacity: number;
  showPredictionLayer: boolean;
  showPhysicsLayer: boolean;
}

interface WorkspaceState {
  globalCursorTime: number | null; // UNIX timestamp for synchronized time brushing
  selectedEventId: string | null;
  activeRegion: ActiveRegion | null;
  isPlaying: boolean;
  replaySpeed: number;
  digitalTwin: DigitalTwinState;
  
  // Actions
  setCursorTime: (time: number | null) => void;
  setSelectedEvent: (eventId: string | null) => void;
  setActiveRegion: (region: ActiveRegion | null) => void;
  setReplayState: (isPlaying: boolean, speed?: number) => void;
  setDigitalTwinLayer: (layer: keyof DigitalTwinState, value: number | boolean) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  globalCursorTime: null,
  selectedEventId: null,
  activeRegion: null,
  isPlaying: false,
  replaySpeed: 1.0,
  digitalTwin: {
    photosphereOpacity: 100,
    chromosphereOpacity: 0,
    coronaOpacity: 80,
    magneticOpacity: 30,
    showPredictionLayer: false,
    showPhysicsLayer: false
  },

  setCursorTime: (time) => set({ globalCursorTime: time }),
  setSelectedEvent: (id) => set({ selectedEventId: id }),
  setActiveRegion: (region) => set({ activeRegion: region }),
  setReplayState: (isPlaying, speed) => set((state) => ({ 
    isPlaying, 
    replaySpeed: speed ?? state.replaySpeed 
  })),
  setDigitalTwinLayer: (layer, value) => set((state) => ({
    digitalTwin: { ...state.digitalTwin, [layer]: value }
  })),
}));
