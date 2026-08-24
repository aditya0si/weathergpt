import React, { useState } from 'react';
import { AlertTriangle, ChevronDown, ChevronUp, ShieldAlert, ShieldCheck } from 'lucide-react';
import { UI_TRANSLATIONS } from '../utils/translations';

export default function AlertBanner({ alerts, currentLang }) {
  const [expanded, setExpanded] = useState(false);
  const t = UI_TRANSLATIONS[currentLang] || UI_TRANSLATIONS.en;

  if (!alerts || alerts.length === 0) return null;

  const activeAlerts = alerts.filter(a => ['Yellow', 'Orange', 'Red'].includes(a.severity));
  if (activeAlerts.length === 0) return null;

  const mainAlert = activeAlerts[0];
  const severityColors = {
    Red: 'bg-rose-950/60 border-rose-500/50 text-rose-200',
    Orange: 'bg-amber-950/60 border-amber-500/50 text-amber-200',
    Yellow: 'bg-yellow-950/60 border-yellow-500/50 text-yellow-200',
  };

  const badgeColors = {
    Red: 'bg-rose-500 text-white animate-pulse',
    Orange: 'bg-amber-500 text-slate-950 font-bold',
    Yellow: 'bg-yellow-500 text-slate-950 font-bold',
  };

  const actions = currentLang === 'as'
    ? mainAlert.safety_actions_as
    : (currentLang === 'hi' ? mainAlert.safety_actions_hi : mainAlert.safety_actions_en);

  return (
    <div className={`rounded-xl border p-4 transition-all duration-300 ${severityColors[mainAlert.severity] || severityColors.Yellow} backdrop-blur-md shadow-lg`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-black/30 border border-white/10">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider ${badgeColors[mainAlert.severity]}`}>
                {mainAlert.severity} Alert
              </span>
              <span className="text-xs font-semibold text-white/90">
                {mainAlert.district}, {mainAlert.state}
              </span>
              <span className="text-[11px] text-white/60">
                (IMD Bulletin)
              </span>
            </div>
            <h4 className="text-sm font-semibold text-white">
              {mainAlert.event_type}
            </h4>
            <p className="text-xs text-white/80 mt-0.5 leading-relaxed">
              {mainAlert.description}
            </p>
          </div>
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center gap-1 text-xs font-medium px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
        >
          <span>{expanded ? 'Hide Safety Rules' : 'Safety Precautions'}</span>
          {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>
      </div>

      {expanded && actions && actions.length > 0 && (
        <div className="mt-3 pt-3 border-t border-white/10 animate-fadeIn">
          <div className="text-xs font-semibold text-white/90 mb-1.5 flex items-center gap-1.5">
            <ShieldAlert className="w-4 h-4 text-amber-300" />
            <span>{t.safetyPrecautions}:</span>
          </div>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-white/80">
            {actions.map((act, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-black/20 p-2 rounded-lg border border-white/5">
                <span className="text-amber-400 font-bold">•</span>
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
