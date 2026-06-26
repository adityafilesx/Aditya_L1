import React, { useState } from 'react';
import { useAiScientistStore } from '../store/aiScientistStore';
import { Icon } from '@design-system/index';

export const CommandConsole: React.FC = () => {
  const [input, setInput] = useState('');
  const { addMessage, updateMessage, setTyping } = useAiScientistStore();

  const handleSend = async () => {
    if (!input.trim()) return;

    const query = input;

    // Add user message
    addMessage({
      id: `user-${Date.now()}`,
      role: 'user',
      content: query,
      timestamp: new Date().toISOString(),
    });

    setInput('');
    setTyping(true);

    const aiMessageId = `ai-${Date.now()}`;
    let fullContent = '';
    let finalConfidence = 0;
    const allSources: Array<{ id: string; title: string; url: string }> = [];

    try {
      const response = await fetch('/api/reasoning/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      if (!response.ok || !response.body) throw new Error('Backend unreachable');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      // Add initial empty AI message
      addMessage({
        id: aiMessageId,
        role: 'ai',
        content: '',
        timestamp: new Date().toISOString(),
      });

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          try {
            const parsed = JSON.parse(line.slice(6));
            if (parsed.type === 'agent_result' && parsed.content) {
              fullContent += (fullContent ? '\n\n' : '') + parsed.content;
              if (parsed.sources) {
                for (const s of parsed.sources) {
                  allSources.push({ id: s.id || '', title: s.title, url: '#' });
                }
              }
              updateMessage(aiMessageId, { content: fullContent });
            } else if (parsed.type === 'complete') {
              finalConfidence = parsed.confidence || 0;
            }
          } catch { /* skip malformed chunks */ }
        }
      }

      // Final update with metadata
      updateMessage(aiMessageId, {
        content: fullContent || 'No response from the reasoning engine.',
        metadata: {
          confidence: finalConfidence,
          sources: allSources,
        },
      });
    } catch {
      // Fallback: use a simple non-streaming analyze call or show error
      try {
        const fallback = await fetch('/api/reasoning/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query }),
        });
        if (fallback.ok) {
          const data = await fallback.json();
          addMessage({
            id: aiMessageId,
            role: 'ai',
            content: data.content || 'Analysis complete.',
            timestamp: new Date().toISOString(),
            metadata: {
              confidence: data.confidence,
              sources: (data.sources || []).map((s: any) => ({ id: s.id || '', title: s.title, url: '#' })),
            },
          });
        } else {
          throw new Error('Fallback failed');
        }
      } catch {
        addMessage({
          id: aiMessageId,
          role: 'ai',
          content: '⚠️ The Scientific Reasoning Engine is not reachable. Please ensure the backend is running on port 8000.',
          timestamp: new Date().toISOString(),
        });
      }
    } finally {
      setTyping(false);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2 overflow-x-auto hide-scrollbar pb-1">
        <button className="px-2 py-1 bg-surface-container hover:bg-surface-container-high rounded border border-surface-variant text-[10px] font-label-caps uppercase text-on-surface-variant flex items-center gap-1 transition-colors">
          <Icon name="compare_arrows" className="text-[12px]" /> /compare
        </button>
        <button className="px-2 py-1 bg-surface-container hover:bg-surface-container-high rounded border border-surface-variant text-[10px] font-label-caps uppercase text-on-surface-variant flex items-center gap-1 transition-colors">
          <Icon name="summarize" className="text-[12px]" /> /explain
        </button>
        <button className="px-2 py-1 bg-surface-container hover:bg-surface-container-high rounded border border-surface-variant text-[10px] font-label-caps uppercase text-on-surface-variant flex items-center gap-1 transition-colors">
          <Icon name="picture_as_pdf" className="text-[12px]" /> /report
        </button>
        <button className="px-2 py-1 bg-surface-container hover:bg-surface-container-high rounded border border-surface-variant text-[10px] font-label-caps uppercase text-on-surface-variant flex items-center gap-1 transition-colors">
          <Icon name="search" className="text-[12px]" /> /literature
        </button>
      </div>
      
      <div className="relative flex items-end bg-surface-container-low border border-surface-variant rounded-xl overflow-hidden shadow-sm focus-within:border-primary focus-within:ring-1 focus-within:ring-primary transition-all">
        <button className="p-3 text-on-surface-variant hover:text-primary transition-colors border-none bg-transparent cursor-pointer">
          <Icon name="attach_file" />
        </button>
        
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="Ask the AI Scientist... (e.g. 'Explain the Neupert Effect for the current flare')"
          className="flex-1 max-h-32 min-h-[48px] py-3 bg-transparent border-none outline-none font-body-lg text-on-surface resize-none"
          rows={1}
        />
        
        <button 
          onClick={handleSend}
          disabled={!input.trim()}
          className="m-2 w-10 h-10 rounded-lg bg-primary text-white flex items-center justify-center shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed border-none cursor-pointer"
        >
          <Icon name="send" />
        </button>
      </div>
    </div>
  );
};
