import { create } from 'zustand';

export interface ChatMessage {
  id: string;
  role: 'user' | 'ai' | 'system';
  content: string;
  timestamp: string;
  metadata?: {
    confidence?: number;
    sources?: Array<{ title: string; url: string; id: string }>;
    relatedAssets?: string[];
    isStreaming?: boolean;
    reasoningSummary?: string;
  };
}

export type ScientistMode = 'chat' | 'experiment' | 'xai' | 'literature' | 'report';

interface AiScientistState {
  messages: ChatMessage[];
  isTyping: boolean;
  activeMode: ScientistMode;
  
  addMessage: (msg: ChatMessage) => void;
  updateMessage: (id: string, partial: Partial<ChatMessage>) => void;
  setTyping: (typing: boolean) => void;
  setMode: (mode: ScientistMode) => void;
  clearConversation: () => void;
}

export const useAiScientistStore = create<AiScientistState>((set) => ({
  messages: [
    {
      id: 'system-1',
      role: 'ai',
      content: 'Hello, I am the Aditya-L1 Scientific Assistant. I am synchronized with your Digital Twin, Knowledge Graph, and Mission Timeline. How can we advance our research today?',
      timestamp: new Date().toISOString(),
    }
  ],
  isTyping: false,
  activeMode: 'chat',

  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  updateMessage: (id, partial) => set((state) => ({
    messages: state.messages.map(m => m.id === id ? { ...m, ...partial } : m)
  })),
  setTyping: (isTyping) => set({ isTyping }),
  setMode: (activeMode) => set({ activeMode }),
  clearConversation: () => set({ 
    messages: [{
      id: `sys-${Date.now()}`,
      role: 'ai',
      content: 'Conversation reset. Ready for a new scientific query.',
      timestamp: new Date().toISOString(),
    }] 
  })
}));
