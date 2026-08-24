import React, { useEffect, useRef, useState } from 'react';
import {
  Bot,
  CornerDownLeft,
  Loader2,
  RefreshCw,
  Send,
  Sparkles,
  User,
  Zap
} from 'lucide-react';
import { UI_TRANSLATIONS } from '../utils/translations';
import ToolExecutionTray from './ToolExecutionTray';

export default function ChatWindow({
  messages,
  isLoading,
  onSendMessage,
  onClearChat,
  currentLang
}) {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const t = UI_TRANSLATIONS[currentLang] || UI_TRANSLATIONS.en;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!inputMessage.trim() || isLoading) return;
    onSendMessage(inputMessage.trim());
    setInputMessage('');
  };

  const handleQuickPrompt = (promptText) => {
    // Strip leading emojis if any
    const cleaned = promptText.replace(/^[^\w\u0900-\u097F\u0980-\u09FF]+/, '').trim();
    onSendMessage(cleaned);
  };

  const quickPrompts = [
    t.quickPrompt1,
    t.quickPrompt2,
    t.quickPrompt3,
    t.quickPrompt4,
    t.quickPrompt5,
  ];

  return (
    <div className="flex flex-col h-[700px] glass-panel rounded-2xl border border-slate-800 shadow-2xl overflow-hidden">
      {/* Chat Header Bar */}
      <div className="px-5 py-3 border-b border-slate-800 flex items-center justify-between bg-slate-900/60 backdrop-blur-md">
        <div className="flex items-center gap-2.5">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Indic Multilingual Reasoning Agent
          </span>
        </div>

        <button
          onClick={onClearChat}
          className="text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1.5 px-2.5 py-1 rounded-lg hover:bg-slate-800 transition-colors"
          title={t.clearHistory}
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>{t.clearHistory}</span>
        </button>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => {
          const isUser = msg.role === 'user';
          return (
            <div
              key={idx}
              className={`flex items-start gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
            >
              {!isUser && (
                <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shrink-0 shadow-md ring-1 ring-white/20">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-[85%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed shadow-lg ${
                  isUser
                    ? 'bg-sky-600 text-white rounded-tr-none font-medium'
                    : 'bg-slate-900/90 border border-slate-800 text-slate-100 rounded-tl-none'
                }`}
              >
                {/* Text Content */}
                <div className="whitespace-pre-wrap font-sans">
                  {msg.content}
                </div>

                {/* Tool Execution Inspector for Assistant */}
                {!isUser && msg.tool_calls && (
                  <ToolExecutionTray toolCalls={msg.tool_calls} />
                )}

                {/* Latency and provider footprint */}
                {!isUser && msg.latency_ms && (
                  <div className="mt-2 text-[10px] text-slate-400 flex items-center justify-between border-t border-slate-800/60 pt-1.5">
                    <span>⚡ Latency: {msg.latency_ms} ms</span>
                    <span className="font-mono text-sky-400">{msg.provider_used || 'WeatherGPT-Hybrid'}</span>
                  </div>
                )}
              </div>

              {isUser && (
                <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 shrink-0">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          );
        })}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-xl bg-sky-600/30 border border-sky-500/40 flex items-center justify-center text-sky-300 shrink-0 animate-spin">
              <Loader2 className="w-4 h-4" />
            </div>
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl rounded-tl-none p-3.5 text-xs text-sky-300 flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 animate-pulse text-amber-400" />
              <span>{t.thinking}</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Questions Shelf */}
      <div className="px-4 py-2 border-t border-slate-800/80 bg-slate-950/40 overflow-x-auto flex items-center gap-2 no-scrollbar">
        <div className="flex items-center gap-1 text-[11px] font-semibold text-slate-400 shrink-0 mr-1">
          <Zap className="w-3.5 h-3.5 text-amber-400" />
          <span>Quick:</span>
        </div>
        {quickPrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleQuickPrompt(p)}
            className="px-2.5 py-1 rounded-lg bg-slate-800/60 hover:bg-sky-500/20 hover:border-sky-500/40 border border-slate-700/60 text-[11px] font-medium text-slate-300 hover:text-white transition-all whitespace-nowrap"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Input Bar Form */}
      <form onSubmit={handleSubmit} className="p-3 border-t border-slate-800 bg-slate-900/80 flex items-center gap-2">
        <input
          ref={inputRef}
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder={t.inputPlaceholder}
          disabled={isLoading}
          className="flex-1 bg-slate-950/80 border border-slate-700/80 focus:border-sky-500 focus:ring-1 focus:ring-sky-500 rounded-xl px-4 py-3 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none transition-all"
        />

        <button
          type="submit"
          disabled={!inputMessage.trim() || isLoading}
          className="px-4 py-3 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold rounded-xl shadow-lg shadow-sky-500/20 flex items-center gap-1.5 transition-all text-xs sm:text-sm"
        >
          <span>{t.sendButton}</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}
