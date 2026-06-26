import React, { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';
import 'katex/dist/katex.min.css';

import { useAiScientistStore } from '../store/aiScientistStore';
import { BaseBadge, Icon } from '@design-system/index';

export const ResearchConversation: React.FC = () => {
  const { messages, isTyping } = useAiScientistStore();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="absolute inset-0 overflow-y-auto p-4 space-y-6">
      {messages.map((msg) => (
        <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
          <div className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
            
            {/* Avatar */}
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shadow-sm flex-shrink-0 ${
              msg.role === 'user' ? 'bg-primary text-white' : 'bg-surface-container-high border border-surface-variant text-primary'
            }`}>
              <Icon name={msg.role === 'user' ? 'person' : 'science'} className="text-[18px]" />
            </div>

            {/* Content */}
            <div className={`flex flex-col gap-1 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`px-4 py-3 rounded-2xl shadow-sm ${
                msg.role === 'user' 
                  ? 'bg-primary text-white rounded-tr-sm' 
                  : 'bg-surface border border-surface-variant text-on-surface rounded-tl-sm'
              }`}>
                <div className={`markdown-body text-[14px] leading-relaxed ${msg.role === 'user' ? 'text-white' : ''}`}>
                  <ReactMarkdown
                    remarkPlugins={[remarkMath, remarkGfm]}
                    rehypePlugins={[rehypeKatex]}
                  >
                    {msg.content}
                  </ReactMarkdown>
                </div>
              </div>

              {/* Metadata (Sources, Confidence) */}
              {msg.metadata && (
                <div className="flex flex-wrap gap-2 mt-1">
                  {msg.metadata.confidence && (
                    <BaseBadge variant="primary" className="!bg-primary/10 !text-primary !border-primary/20">
                      {(msg.metadata.confidence * 100).toFixed(1)}% Confidence
                    </BaseBadge>
                  )}
                  {msg.metadata.sources?.map((src) => (
                    <a key={src.id} href={src.url} className="flex items-center gap-1 px-2 py-0.5 rounded bg-surface-container border border-surface-variant hover:border-primary transition-colors text-[10px] text-on-surface-variant decoration-transparent">
                      <Icon name="article" className="text-[12px]" />
                      <span className="truncate max-w-[150px]">{src.title}</span>
                    </a>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}

      {isTyping && (
        <div className="flex justify-start">
          <div className="flex gap-3 max-w-[80%]">
            <div className="w-8 h-8 rounded-full bg-surface-container-high border border-surface-variant text-primary flex items-center justify-center shadow-sm flex-shrink-0">
              <Icon name="science" className="text-[18px]" />
            </div>
            <div className="px-4 py-4 rounded-2xl shadow-sm bg-surface border border-surface-variant rounded-tl-sm flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} className="h-4" />
    </div>
  );
};
