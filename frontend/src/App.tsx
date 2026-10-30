import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Home } from './pages/Home';
import { CropScan } from './pages/CropScan';
import { KhetGPTChat } from './pages/KhetGPTChat';
import { type Language, translations } from './i18n/translations';
import { Sprout, PhoneCall, ShieldCheck } from 'lucide-react';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<'home' | 'scan' | 'chat'>('home');
  const [language, setLanguage] = useState<Language>(() => {
    const saved = localStorage.getItem('khetgpt_lang');
    return (saved === 'gu' || saved === 'hi' || saved === 'en') ? saved : 'gu';
  });

  useEffect(() => {
    localStorage.setItem('khetgpt_lang', language);
  }, [language]);

  const t = translations[language];

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans antialiased selection:bg-green-100 selection:text-green-900">
      {/* Sticky Top Navigation */}
      <Navbar
        currentTab={currentTab}
        onSelectTab={setCurrentTab}
        language={language}
        onSelectLanguage={setLanguage}
      />

      {/* Main View Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {currentTab === 'home' && (
          <Home
            onNavigate={(tab) => setCurrentTab(tab)}
            language={language}
          />
        )}
        {currentTab === 'scan' && (
          <CropScan language={language} />
        )}
        {currentTab === 'chat' && (
          <KhetGPTChat language={language} />
        )}
      </main>

      {/* Standard Farmer Platform Footer */}
      <footer className="border-t border-gray-200 bg-white py-8 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-gray-500">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 rounded-lg bg-green-600 text-white flex items-center justify-center">
              <Sprout className="w-3.5 h-3.5" />
            </div>
            <span className="font-bold text-gray-800">{t.appName}</span>
            <span>— AI Agriculture Advisory for India</span>
          </div>

          <div className="flex items-center space-x-4">
            <span className="flex items-center text-green-700 font-medium">
              <PhoneCall className="w-3.5 h-3.5 mr-1" />
              Kisan Helpline: 1800-180-1551
            </span>
            <span>•</span>
            <span className="flex items-center">
              <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-600" />
              ICAR & Ministry Grounded
            </span>
          </div>

          <div className="text-gray-400">
            KhetGPT © {new Date().getFullYear()} • Dedicated to Indian Farmers
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
