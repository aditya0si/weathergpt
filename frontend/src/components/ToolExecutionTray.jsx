import React, { useState } from 'react';
import { CheckCircle2, ChevronRight, Clock, Code2, Terminal, Wrench, XCircle } from 'lucide-react';

export default function ToolExecutionTray({ toolCalls }) {
  const [openIndex, setOpenIndex] = useState(null);

  if (!toolCalls || toolCalls.length === 0) {
    return (
      <div className="text-xs text-slate-500 italic flex items-center gap-1.5 p-2 bg-slate-900/40 rounded-lg border border-slate-800">
        <Terminal className="w-3.5 h-3.5" />
        <span>Direct Agent Synthesis (Zero Tool Calls)</span>
      </div>
    );
  }

  return (
    <div className="space-y-2 mt-2 pt-2 border-t border-slate-800/80">
      <div className="flex items-center justify-between text-[11px] font-semibold uppercase tracking-wider text-slate-400">
        <div className="flex items-center gap-1.5">
          <Wrench className="w-3.5 h-3.5 text-sky-400" />
          <span>Agent Tool Execution Trace ({toolCalls.length})</span>
        </div>
      </div>

      <div className="space-y-1.5">
        {toolCalls.map((call, idx) => {
          const isOpen = openIndex === idx;
          return (
            <div key={idx} className="rounded-lg bg-slate-900/80 border border-slate-800 overflow-hidden transition-all text-xs">
              <button
                onClick={() => setOpenIndex(isOpen ? null : idx)}
                className="w-full px-3 py-2 flex items-center justify-between hover:bg-slate-800/60 transition-colors text-left"
              >
                <div className="flex items-center gap-2">
                  {call.success ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  ) : (
                    <XCircle className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                  )}
                  <span className="font-mono font-medium text-sky-300">
                    {call.tool_name}()
                  </span>
                  <span className="text-[10px] text-slate-400 font-mono">
                    {JSON.stringify(call.arguments).slice(0, 35)}...
                  </span>
                </div>

                <div className="flex items-center gap-2 text-[10px] text-slate-400 shrink-0">
                  <span className="flex items-center gap-1 bg-slate-800 px-2 py-0.5 rounded text-slate-300">
                    <Clock className="w-3 h-3 text-amber-400" />
                    {call.latency_ms} ms
                  </span>
                  <ChevronRight className={`w-3.5 h-3.5 transition-transform ${isOpen ? 'rotate-90' : ''}`} />
                </div>
              </button>

              {isOpen && (
                <div className="p-3 bg-black/40 border-t border-slate-800/80 space-y-2 font-mono text-[11px]">
                  <div>
                    <span className="text-slate-400 font-semibold block mb-0.5">Parameters:</span>
                    <pre className="p-2 rounded bg-slate-950/80 text-sky-300 overflow-x-auto text-[10px]">
                      {JSON.stringify(call.arguments, null, 2)}
                    </pre>
                  </div>
                  <div>
                    <span className="text-slate-400 font-semibold block mb-0.5">Returned Output Payload:</span>
                    <pre className="p-2 rounded bg-slate-950/80 text-emerald-300 overflow-x-auto max-h-48 text-[10px]">
                      {JSON.stringify(call.result, null, 2)}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
