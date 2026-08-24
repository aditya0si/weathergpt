import React, { useEffect, useState } from 'react';
import { CloudSun, Info, ShieldCheck, Sparkles, Terminal } from 'lucide-react';
import Header from './components/Header';
import AlertBanner from './components/AlertBanner';
import WeatherWidgets from './components/WeatherWidgets';
import ChatWindow from './components/ChatWindow';
import { checkHealth, fetchAlerts, fetchCurrentWeather, sendChatMessage } from './api/client';
import { UI_TRANSLATIONS } from './utils/translations';

export default function App() {
  const [currentLang, setCurrentLang] = useState('en');
  const [healthData, setHealthData] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [agrometData, setAgrometData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  const t = UI_TRANSLATIONS[currentLang] || UI_TRANSLATIONS.en;

  // Initialize App on mount
  useEffect(() => {
    async function initDashboard() {
      try {
        const health = await checkHealth().catch(() => null);
        if (health) setHealthData(health);

        const weather = await fetchCurrentWeather('Guwahati').catch(() => null);
        if (weather) setWeatherData(weather);

        const alertList = await fetchAlerts('Guwahati').catch(() => []);
        if (alertList) setAlerts(alertList);

        // Initial welcome message
        const welcomeText = {
          en: "Welcome to WeatherGPT! 🌦️\nI am your Indic meteorological & agricultural assistant. Ask me about live weather observations, 7-day forecasts, severe IMD weather alerts, crop advisories (Paddy, Tea, Mustard, Wheat), or climate science.",
          hi: "WeatherGPT में आपका स्वागत है! 🌦️\nमैं आपका भारतीय मौसम एवं कृषि परामर्श सहायक हूँ। वर्तमान मौसम, 7-दिवसीय पूर्वानुमान, मौसम विभाग (IMD) की चेतावनियों, फसलों (धान, गेहूं, सरसों, चाय) की सलाह या जलवायु विज्ञान के बारे में पूछें।",
          as: "WeatherGPT লৈ স্বাগতম! 🌦️\nমই আপোনাৰ বতৰ আৰু কৃষি পৰামৰ্শদাতা AI। বৰ্তমান বতৰ, ৭ দিনৰ পূৰ্বানুমান, বতৰ বিজ্ঞান কেন্দ্ৰৰ সতৰ্কবাৰ্তা, শস্যৰ পৰামৰ্শ (শালি ধান, চাহ, সৰিয়হ, মৰাপাট) বা জলবায়ু বিজ্ঞান সম্পৰ্কে সোধক।"
        }[currentLang] || "Welcome to WeatherGPT!";

        setMessages([
          {
            role: 'assistant',
            content: welcomeText,
            timestamp: new Date().toISOString(),
          }
        ]);
      } catch (err) {
        console.error("Dashboard initialization error:", err);
      }
    }
    initDashboard();
  }, []);

  // Language Change Handler
  const handleLanguageChange = (lang) => {
    setCurrentLang(lang);
  };

  // Chat message submission
  const handleSendMessage = async (text) => {
    const userMsg = {
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage(text, currentLang);
      
      const assistantMsg = {
        role: 'assistant',
        content: response.reply,
        tool_calls: response.tool_calls,
        latency_ms: response.latency_ms,
        provider_used: response.provider_used,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMsg]);

      // Update Dashboard Context if response contains rich weather data
      if (response.weather_summary) {
        setWeatherData(response.weather_summary);
      }
      if (response.alerts && response.alerts.length > 0) {
        setAlerts(response.alerts);
      }
      if (response.agromet) {
        setAgrometData(response.agromet);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `⚠️ Error processing query: ${err.message}. Please check connection to WeatherGPT backend.`,
          timestamp: new Date().toISOString(),
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#090d16] text-slate-100">
      {/* Top Glassmorphic Navigation Bar */}
      <Header
        currentLang={currentLang}
        onSelectLanguage={handleLanguageChange}
        healthData={healthData}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">
        {/* Active Severe Alert Banner */}
        <AlertBanner alerts={alerts} currentLang={currentLang} />

        {/* 2-Column Responsive Dashboard Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column: Live Weather & AgroMet Cards (5 Cols) */}
          <div className="lg:col-span-5 space-y-6">
            <WeatherWidgets
              weatherData={weatherData}
              agrometData={agrometData}
              currentLang={currentLang}
            />

            {/* Architecture / Source Tag Card */}
            <div className="glass-panel rounded-2xl p-4 border border-slate-800 text-xs text-slate-400 space-y-2">
              <div className="flex items-center gap-2 font-semibold text-slate-300">
                <ShieldCheck className="w-4 h-4 text-sky-400" />
                <span>Verified Meteorological Sources</span>
              </div>
              <p className="text-[11px] leading-relaxed">
                Weather observations and numerical forecasts are synthesized from the <strong>India Meteorological Department (IMD)</strong>, <strong>Open-Meteo High-Resolution NWP</strong>, and <strong>NOAA GFS</strong> atmospheric soundings.
              </p>
            </div>
          </div>

          {/* Right Column: Conversational AI Agent (7 Cols) */}
          <div className="lg:col-span-7">
            <ChatWindow
              messages={messages}
              isLoading={isLoading}
              onSendMessage={handleSendMessage}
              onClearChat={handleClearChat}
              currentLang={currentLang}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-4 px-6 text-center text-xs text-slate-500 bg-slate-950/60">
        <p>
          WeatherGPT (SIH26068) — Built with FastAPI, React, and Indic Multilingual Function-Calling LLM Agents. MIT Licensed.
        </p>
      </footer>
    </div>
  );
}
