import React, { useState } from 'react';
import { Sprout, Camera, MessageSquare, Home, Globe, Menu, X } from 'lucide-react';
import { type Language, translations } from '../i18n/translations';

interface NavbarProps {
  currentTab: 'home' | 'scan' | 'chat';
  onSelectTab: (tab: 'home' | 'scan' | 'chat') => void;
  language: Language;
  onSelectLanguage: (lang: Language) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  onSelectTab,
  language,
  onSelectLanguage
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const t = translations[language];

  const handleTabClick = (tab: 'home' | 'scan' | 'chat') => {
    onSelectTab(tab);
    setMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Brand Logo */}
          <div 
            onClick={() => handleTabClick('home')}
            className="flex items-center space-x-2.5 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-700 flex items-center justify-center text-white shadow-md shadow-green-500/20 group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-gray-900 group-hover:text-green-700 transition-colors">
                {t.appName}
              </span>
              <span className="hidden sm:inline-block ml-2 text-xs font-medium px-2 py-0.5 bg-green-100 text-green-800 rounded-full">
                AI Agriculture
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1 lg:space-x-2">
            <button
              onClick={() => handleTabClick('home')}
              className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${
                currentTab === 'home'
                  ? 'bg-green-50 text-green-700 font-bold border border-green-200'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Home className="w-4 h-4" />
              <span>{t.navHome}</span>
            </button>

            <button
              onClick={() => handleTabClick('scan')}
              className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${
                currentTab === 'scan'
                  ? 'bg-green-50 text-green-700 font-bold border border-green-200'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Camera className="w-4 h-4" />
              <span>{t.navScan}</span>
            </button>

            <button
              onClick={() => handleTabClick('chat')}
              className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${
                currentTab === 'chat'
                  ? 'bg-green-50 text-green-700 font-bold border border-green-200'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              <span>{t.navChat}</span>
            </button>
          </nav>

          {/* Language Selector (Pills) */}
          <div className="flex items-center space-x-2">
            <div className="hidden sm:flex items-center bg-gray-100 p-1 rounded-xl border border-gray-200 text-xs font-semibold">
              <Globe className="w-3.5 h-3.5 text-gray-500 ml-1.5 mr-1" />
              <button
                onClick={() => onSelectLanguage('gu')}
                className={`px-2.5 py-1 rounded-lg transition-all ${
                  language === 'gu'
                    ? 'bg-green-600 text-white font-bold shadow-sm'
                    : 'text-gray-700 hover:text-gray-900'
                }`}
              >
                ગુજરાતી
              </button>
              <button
                onClick={() => onSelectLanguage('hi')}
                className={`px-2.5 py-1 rounded-lg transition-all ${
                  language === 'hi'
                    ? 'bg-green-600 text-white font-bold shadow-sm'
                    : 'text-gray-700 hover:text-gray-900'
                }`}
              >
                हिन्दी
              </button>
              <button
                onClick={() => onSelectLanguage('en')}
                className={`px-2.5 py-1 rounded-lg transition-all ${
                  language === 'en'
                    ? 'bg-green-600 text-white font-bold shadow-sm'
                    : 'text-gray-700 hover:text-gray-900'
                }`}
              >
                English
              </button>
            </div>

            {/* Mobile Language Switcher (Compact Dropdown) */}
            <div className="sm:hidden">
              <select
                value={language}
                onChange={(e) => onSelectLanguage(e.target.value as Language)}
                className="bg-gray-100 border border-gray-300 text-gray-800 text-xs font-bold rounded-lg px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="gu">ગુજરાતી</option>
                <option value="hi">हिन्दी</option>
                <option value="en">English</option>
              </select>
            </div>

            {/* Mobile Menu Toggle Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white px-4 pt-2 pb-4 space-y-1 shadow-lg">
          <button
            onClick={() => handleTabClick('home')}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-semibold ${
              currentTab === 'home' ? 'bg-green-50 text-green-700 font-bold' : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Home className="w-5 h-5 text-green-600" />
            <span>{t.navHome}</span>
          </button>
          <button
            onClick={() => handleTabClick('scan')}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-semibold ${
              currentTab === 'scan' ? 'bg-green-50 text-green-700 font-bold' : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Camera className="w-5 h-5 text-green-600" />
            <span>{t.navScan}</span>
          </button>
          <button
            onClick={() => handleTabClick('chat')}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-semibold ${
              currentTab === 'chat' ? 'bg-green-50 text-green-700 font-bold' : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <MessageSquare className="w-5 h-5 text-green-600" />
            <span>{t.navChat}</span>
          </button>
        </div>
      )}
    </header>
  );
};
