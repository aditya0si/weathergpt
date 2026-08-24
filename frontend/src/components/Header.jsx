import React from 'react';
import { CloudLightning, Cpu, Globe, ShieldCheck, Sparkles } from 'lucide-react';
import { UI_TRANSLATIONS } from '../utils/translations';

export default function Header({ currentLang, onSelectLanguage, healthData }) {
  const t = UI_TRANSLATIONS[currentLang] || UI_TRANSLATIONS.en;

  return (
    <header className="glass-panel sticky top-0 z-50 border-b border-slate-800/80 px-4 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
      {/* Brand Identity */}
      <div className="flex items-center gap-3.5">
        <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 via-sky-500 to-indigo-600 shadow-lg shadow-sky-500/20 ring-1 ring-white/20">
          <CloudLightning className="w-5 h-5 text-white animate-pulse" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-100 to-sky-300 bg-clip-text text-transparent">
              {t.appTitle}
            </h1>
            <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wide uppercase bg-sky-500/20 text-sky-300 border border-sky-500/30 rounded-full">
              SIH26068
            </span>
          </div>
          <p className="text-xs text-slate-400 font-medium">
            {t.appSubtitle}
          </p>
        </div>
      </div>

      {/* Center Engine Indicators */}
      <div className="hidden md:flex items-center gap-4 text-xs">
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          <span className="font-semibold">{t.statusLive}</span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/50 text-slate-300">
          <Cpu className="w-3.5 h-3.5 text-sky-400" />
          <span>IMD & Open-Meteo Harmonized</span>
        </div>
      </div>

      {/* Language Switcher */}
      <div className="flex items-center gap-2">
        <div className="flex items-center bg-slate-900/80 p-1 rounded-xl border border-slate-700/60 shadow-inner">
          <button
            onClick={() => onSelectLanguage('en')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              currentLang === 'en'
                ? 'bg-sky-500 text-white shadow-md shadow-sky-500/30 font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            English
          </button>
          <button
            onClick={() => onSelectLanguage('hi')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              currentLang === 'hi'
                ? 'bg-sky-500 text-white shadow-md shadow-sky-500/30 font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            हिन्दी
          </button>
          <button
            onClick={() => onSelectLanguage('as')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              currentLang === 'as'
                ? 'bg-sky-500 text-white shadow-md shadow-sky-500/30 font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            অসমীয়া
          </button>
        </div>
      </div>
    </header>
  );
}
