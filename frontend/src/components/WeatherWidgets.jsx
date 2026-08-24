import React from 'react';
import {
  Cloud,
  CloudDrizzle,
  CloudFog,
  CloudLightning,
  CloudRain,
  Compass,
  Droplets,
  Sprout,
  Sun,
  Thermometer,
  Wind
} from 'lucide-react';
import { UI_TRANSLATIONS } from '../utils/translations';

export default function WeatherWidgets({ weatherData, agrometData, currentLang }) {
  const t = UI_TRANSLATIONS[currentLang] || UI_TRANSLATIONS.en;

  if (!weatherData) return null;

  const loc = weatherData.location || { name: 'Guwahati', admin1: 'Assam' };
  const curr = weatherData.current || {};
  const daily = weatherData.daily || [];

  const getWeatherIcon = (desc = '') => {
    const d = desc.toLowerCase();
    if (d.includes('thunder') || d.includes('lightning') || d.includes('বজ্ৰপাত') || d.includes('तूफान')) {
      return <CloudLightning className="w-8 h-8 text-amber-400 animate-pulse" />;
    }
    if (d.includes('rain') || d.includes('drizzle') || d.includes('বৰষুণ') || d.includes('बारिश')) {
      return <CloudRain className="w-8 h-8 text-sky-400" />;
    }
    if (d.includes('cloud') || d.includes('ডাৱৰ') || d.includes('बादल')) {
      return <Cloud className="w-8 h-8 text-slate-300" />;
    }
    if (d.includes('fog') || d.includes('কুঁৱলী') || d.includes('कोहरा')) {
      return <CloudFog className="w-8 h-8 text-slate-400" />;
    }
    return <Sun className="w-8 h-8 text-amber-300" />;
  };

  return (
    <div className="space-y-4">
      {/* Current Weather Hero Card */}
      <div className="glass-panel rounded-2xl p-5 border border-sky-500/20 shadow-xl bg-gradient-to-br from-slate-900/90 via-slate-900/60 to-sky-950/40">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded-md border border-sky-500/20">
                {t.weatherCardTitle}
              </span>
              <span className="text-xs text-slate-400">
                {loc.admin1 || loc.country}
              </span>
            </div>
            <h2 className="text-2xl font-bold text-white mt-1">
              {loc.name}
            </h2>
            <p className="text-xs text-slate-300 capitalize font-medium flex items-center gap-1.5 mt-0.5">
              {curr.weather_desc || 'Moderate'}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-sky-500/10 border border-sky-500/20">
              {getWeatherIcon(curr.weather_desc)}
            </div>
            <div>
              <div className="text-3xl font-extrabold text-white tracking-tight">
                {curr.temperature_c !== undefined ? `${curr.temperature_c}°C` : '--'}
              </div>
              <div className="text-[11px] text-slate-400">
                {t.feelsLike}: {curr.apparent_temperature_c !== undefined ? `${curr.apparent_temperature_c}°C` : '--'}
              </div>
            </div>
          </div>
        </div>

        {/* Observation Metrix Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5 pt-4 border-t border-slate-800">
          <div className="bg-slate-800/40 p-2.5 rounded-xl border border-slate-700/40">
            <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
              <Droplets className="w-3.5 h-3.5 text-sky-400" />
              <span>{t.humidity}</span>
            </div>
            <div className="text-sm font-bold text-white mt-1">
              {curr.relative_humidity_pct !== undefined ? `${curr.relative_humidity_pct}%` : '--'}
            </div>
          </div>

          <div className="bg-slate-800/40 p-2.5 rounded-xl border border-slate-700/40">
            <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
              <Wind className="w-3.5 h-3.5 text-teal-400" />
              <span>{t.wind}</span>
            </div>
            <div className="text-sm font-bold text-white mt-1">
              {curr.wind_speed_kmh !== undefined ? `${curr.wind_speed_kmh} km/h` : '--'}
            </div>
          </div>

          <div className="bg-slate-800/40 p-2.5 rounded-xl border border-slate-700/40">
            <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
              <Compass className="w-3.5 h-3.5 text-indigo-400" />
              <span>{t.pressure}</span>
            </div>
            <div className="text-sm font-bold text-white mt-1">
              {curr.surface_pressure_hpa !== undefined ? `${curr.surface_pressure_hpa} hPa` : '1012 hPa'}
            </div>
          </div>

          <div className="bg-slate-800/40 p-2.5 rounded-xl border border-slate-700/40">
            <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
              <CloudDrizzle className="w-3.5 h-3.5 text-cyan-400" />
              <span>Precipitation</span>
            </div>
            <div className="text-sm font-bold text-white mt-1">
              {curr.precipitation_mm !== undefined ? `${curr.precipitation_mm} mm` : '0 mm'}
            </div>
          </div>
        </div>
      </div>

      {/* 7-Day Forecast Row */}
      {daily && daily.length > 0 && (
        <div className="glass-panel rounded-2xl p-4 border border-slate-800">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center justify-between">
            <span>{t.forecastTitle} ({daily.length} Days)</span>
            <span className="text-[10px] text-sky-400 font-medium">Open-Meteo High Res</span>
          </h3>

          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
            {daily.map((item, idx) => (
              <div
                key={idx}
                className="bg-slate-800/50 hover:bg-slate-800/80 p-2.5 rounded-xl border border-slate-700/50 flex flex-col items-center text-center transition-all duration-200"
              >
                <span className="text-[11px] font-semibold text-slate-300">
                  {item.date ? item.date.slice(5) : `Day ${idx+1}`}
                </span>
                <div className="my-1.5">
                  {getWeatherIcon(item.weather_desc)}
                </div>
                <div className="text-xs font-bold text-white">
                  {item.max_temp_c}° / <span className="text-slate-400 font-normal">{item.min_temp_c}°</span>
                </div>
                {item.precipitation_probability_pct > 0 && (
                  <div className="mt-1.5 px-1.5 py-0.5 rounded bg-sky-500/10 text-[10px] font-semibold text-sky-300 flex items-center gap-0.5">
                    <Droplets className="w-2.5 h-2.5" />
                    <span>{item.precipitation_probability_pct}%</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AgroMet Farmer Advisory Card if present */}
      {agrometData && (
        <div className="glass-panel rounded-2xl p-4 border border-emerald-500/30 bg-gradient-to-br from-emerald-950/40 via-slate-900/60 to-slate-900/80 shadow-lg">
          <div className="flex items-center gap-2 mb-2">
            <div className="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400">
              <Sprout className="w-4 h-4" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-emerald-300">
                {t.agroTitle}: {agrometData.crop_name}
              </h4>
              <span className="text-[11px] text-emerald-400/80 font-medium">
                {t.growthStage}: {agrometData.growth_stage}
              </span>
            </div>
          </div>

          <div className="text-xs text-slate-200 leading-relaxed bg-black/30 p-3 rounded-xl border border-emerald-500/20 mb-3">
            {currentLang === 'as'
              ? agrometData.advisory_as
              : (currentLang === 'hi' ? agrometData.advisory_hi : agrometData.advisory_en)}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
            <div className="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
              <span className="font-semibold text-emerald-400 block mb-0.5">💧 {t.irrigation}:</span>
              <span className="text-slate-300">{agrometData.irrigation_advice}</span>
            </div>
            <div className="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
              <span className="font-semibold text-teal-400 block mb-0.5">🧪 {t.pesticide}:</span>
              <span className="text-slate-300">{agrometData.fertilizer_pesticide_advice}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
