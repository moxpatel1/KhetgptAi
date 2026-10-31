import React from 'react';
import { Camera, MessageSquare, ShieldCheck, PhoneCall, ChevronRight, Sparkles } from 'lucide-react';
import { type Language, translations } from '../i18n/translations';

interface HomeProps {
  onNavigate: (tab: 'scan' | 'chat') => void;
  language: Language;
  onReplayIntro?: () => void;
}

export const Home: React.FC<HomeProps> = ({ onNavigate, language, onReplayIntro }) => {
  const t = translations[language];

  return (
    <div className="space-y-10 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-green-800 via-emerald-800 to-teal-900 text-white shadow-xl px-6 py-12 sm:px-12 sm:py-16">
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-green-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-emerald-400/20 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-3xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-green-200 text-xs sm:text-sm font-semibold mb-6">
            <Sparkles className="w-4 h-4 text-green-300" />
            <span>{t.tagline}</span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
            {t.homeHeroTitle}
          </h1>

          <p className="mt-4 text-base sm:text-lg text-green-100/90 leading-relaxed max-w-2xl">
            {t.homeHeroSubtitle}
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <button
              onClick={() => onNavigate('scan')}
              className="flex items-center space-x-2 bg-white text-green-900 font-bold px-6 py-3.5 rounded-xl shadow-lg hover:bg-green-50 transition-all hover:shadow-xl transform active:scale-95 text-sm sm:text-base"
            >
              <Camera className="w-5 h-5 text-green-700" />
              <span>{t.homeScanCardBtn}</span>
            </button>
            <button
              onClick={() => onNavigate('chat')}
              className="flex items-center space-x-2 bg-emerald-600/80 hover:bg-emerald-600 border border-emerald-400/40 text-white font-bold px-6 py-3.5 rounded-xl shadow-lg transition-all hover:shadow-xl transform active:scale-95 text-sm sm:text-base backdrop-blur-sm"
            >
              <MessageSquare className="w-5 h-5" />
              <span>{t.homeChatCardBtn}</span>
            </button>
            {onReplayIntro && (
              <button
                onClick={onReplayIntro}
                className="flex items-center space-x-2 bg-black/20 hover:bg-black/35 border border-white/20 text-emerald-100 hover:text-white font-semibold px-4 py-3.5 rounded-xl transition-all transform active:scale-95 text-sm sm:text-base backdrop-blur-md"
                title={t.replayIntro}
              >
                <Sparkles className="w-4 h-4 text-amber-300" />
                <span className="hidden sm:inline">{t.replayIntro}</span>
              </button>
            )}
          </div>
        </div>
      </section>

      {/* Two Prominent Core Cards */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
        {/* Card 1: Crop Disease Scan */}
        <div 
          onClick={() => onNavigate('scan')}
          className="group relative bg-white rounded-3xl p-7 border border-gray-200 shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer overflow-hidden flex flex-col justify-between hover:border-green-300"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-green-50 rounded-bl-full -z-0 transition-transform group-hover:scale-110" />
          
          <div className="relative z-10">
            <div className="w-14 h-14 rounded-2xl bg-green-100 text-green-700 flex items-center justify-center shadow-inner mb-6 group-hover:bg-green-600 group-hover:text-white transition-colors">
              <Camera className="w-7 h-7" />
            </div>
            <div className="inline-block text-xs font-bold text-green-700 tracking-wider uppercase mb-1">
              Computer Vision
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              {t.homeScanCardTitle}
            </h2>
            <p className="text-gray-600 leading-relaxed text-sm sm:text-base">
              {t.homeScanCardDesc}
            </p>
          </div>

          <div className="relative z-10 mt-6 pt-4 border-t border-gray-100 flex items-center justify-between text-green-700 font-bold group-hover:text-green-800">
            <span>{t.homeScanCardBtn}</span>
            <ChevronRight className="w-5 h-5 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        {/* Card 2: KhetGPT AI */}
        <div 
          onClick={() => onNavigate('chat')}
          className="group relative bg-white rounded-3xl p-7 border border-gray-200 shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer overflow-hidden flex flex-col justify-between hover:border-emerald-300"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-50 rounded-bl-full -z-0 transition-transform group-hover:scale-110" />

          <div className="relative z-10">
            <div className="w-14 h-14 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center shadow-inner mb-6 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
              <MessageSquare className="w-7 h-7" />
            </div>
            <div className="inline-block text-xs font-bold text-emerald-700 tracking-wider uppercase mb-1">
              RAG Knowledge Base
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              {t.homeChatCardTitle}
            </h2>
            <p className="text-gray-600 leading-relaxed text-sm sm:text-base">
              {t.homeChatCardDesc}
            </p>
          </div>

          <div className="relative z-10 mt-6 pt-4 border-t border-gray-100 flex items-center justify-between text-emerald-700 font-bold group-hover:text-emerald-800">
            <span>{t.homeChatCardBtn}</span>
            <ChevronRight className="w-5 h-5 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </div>
      </section>

      {/* 3-Step Farmer Quick Start Guide */}
      <section className="bg-white rounded-3xl p-8 border border-gray-200 shadow-sm">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-900 text-center mb-8">
          {t.homeStepsTitle}
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="flex flex-col items-center text-center p-5 rounded-2xl bg-gray-50/70 border border-gray-100">
            <div className="w-12 h-12 rounded-full bg-green-100 text-green-700 font-extrabold flex items-center justify-center mb-4 text-lg">
              1
            </div>
            <h3 className="font-bold text-gray-900 mb-2">{t.homeStep1Title}</h3>
            <p className="text-sm text-gray-600 leading-relaxed">{t.homeStep1Desc}</p>
          </div>

          <div className="flex flex-col items-center text-center p-5 rounded-2xl bg-gray-50/70 border border-gray-100">
            <div className="w-12 h-12 rounded-full bg-green-100 text-green-700 font-extrabold flex items-center justify-center mb-4 text-lg">
              2
            </div>
            <h3 className="font-bold text-gray-900 mb-2">{t.homeStep2Title}</h3>
            <p className="text-sm text-gray-600 leading-relaxed">{t.homeStep2Desc}</p>
          </div>

          <div className="flex flex-col items-center text-center p-5 rounded-2xl bg-gray-50/70 border border-gray-100">
            <div className="w-12 h-12 rounded-full bg-green-100 text-green-700 font-extrabold flex items-center justify-center mb-4 text-lg">
              3
            </div>
            <h3 className="font-bold text-gray-900 mb-2">{t.homeStep3Title}</h3>
            <p className="text-sm text-gray-600 leading-relaxed">{t.homeStep3Desc}</p>
          </div>
        </div>
      </section>

      {/* Verified Farmer Trust & Helpline Banner */}
      <section className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-2xl p-6 border border-amber-200 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-amber-500 text-white rounded-xl shadow-md">
            <PhoneCall className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-gray-900 text-base sm:text-lg">
              {t.homeHelplineNotice}
            </h3>
            <p className="text-xs sm:text-sm text-gray-600">
              Government of India Kisan Call Centre | 24x7 Free Advisory
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2 text-xs font-semibold text-amber-800 bg-amber-100 px-3 py-1.5 rounded-lg border border-amber-300">
          <ShieldCheck className="w-4 h-4 text-amber-700" />
          <span>Official Guidelines Grounded</span>
        </div>
      </section>
    </div>
  );
};
