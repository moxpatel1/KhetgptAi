export type Language = 'gu' | 'hi' | 'en';

export interface TranslationStrings {
  appName: string;
  tagline: string;
  navHome: string;
  navScan: string;
  navChat: string;
  langSelect: string;

  // Home Page
  homeHeroTitle: string;
  homeHeroSubtitle: string;
  homeScanCardTitle: string;
  homeScanCardDesc: string;
  homeScanCardBtn: string;
  homeChatCardTitle: string;
  homeChatCardDesc: string;
  homeChatCardBtn: string;
  homeStepsTitle: string;
  homeStep1Title: string;
  homeStep1Desc: string;
  homeStep2Title: string;
  homeStep2Desc: string;
  homeStep3Title: string;
  homeStep3Desc: string;
  homeHelplineNotice: string;

  // Crop Disease Scan
  scanTitle: string;
  scanSubtitle: string;
  scanUploadPrompt: string;
  scanUploadHint: string;
  scanCameraBtn: string;
  scanUploadBtn: string;
  scanAnalyzing: string;
  scanResultTitle: string;
  scanCropLabel: string;
  scanDiseaseLabel: string;
  scanConfidenceLabel: string;
  scanUncertaintyAlert: string;
  scanSymptomsTitle: string;
  scanOrganicTitle: string;
  scanChemicalTitle: string;
  scanPrecautionsTitle: string;
  scanPreventiveTitle: string;
  scanHealthyBanner: string;
  scanResetBtn: string;

  // KhetGPT AI Chat
  chatTitle: string;
  chatSubtitle: string;
  chatNewBtn: string;
  chatHistoryTitle: string;
  chatPlaceholder: string;
  chatSendBtn: string;
  chatEmptyTitle: string;
  chatEmptyDesc: string;
  chatPrompt1: string;
  chatPrompt2: string;
  chatPrompt3: string;
  chatSourcesLabel: string;
  chatThinking: string;
  chatDisclaimer: string;

  // General & Alerts
  loading: string;
  errorGeneric: string;
  retry: string;
}

export const translations: Record<Language, TranslationStrings> = {
  gu: {
    appName: "ખેતGPT",
    tagline: "ભારતીય ખેડૂત માટે આધુનિક AI કૃષિ સહાયક",
    navHome: "હોમ (મુખ્ય પેજ)",
    navScan: "પાક રોગ નિદાન",
    navChat: "ખેતGPT AI ચેટ",
    langSelect: "ભાષા પસંદ કરો",

    homeHeroTitle: "ખેતીમાં AI સાથી — સાચો પાક, સચોટ માર્ગદર્શન",
    homeHeroSubtitle: "પાકના રોગોની ત્વરિત ઓળખ, સત્તાવાર સરકારી યોજનાઓની સચોટ માહિતી અને કૃષિ તજજ્ઞોનું સલાહકાર માર્ગદર્શન હવે તમારી પોતાની ભાષામાં.",
    homeScanCardTitle: "પાક રોગ સ્કેનર (AI કેમેરા)",
    homeScanCardDesc: "પાંદડાનો ફોટો અપલોડ કરો અને સેકન્ડોમાં રોગની ઓળખ, લીંબોળી અર્ક / જૈવિક દવાઓ અને સલામત રાસાયણિક ઉપચાર મેળવો.",
    homeScanCardBtn: "રોગ તપાસો →",
    homeChatCardTitle: "ખેતGPT AI સહાયક",
    homeChatCardDesc: "PM-કિસાન, પાક વીમો (PMFBY), બાગાયતી સહાય, ખાતર અને પશુપાલન સંબંધિત કોઈપણ પ્રશ્ન પૂછો.",
    homeChatCardBtn: "પ્રશ્ન પૂછો →",
    homeStepsTitle: "ખેતGPT નો ઉપયોગ કેવી રીતે કરવો?",
    homeStep1Title: "૧. ભાષા પસંદ કરો",
    homeStep1Desc: "ગુજરાતી, હિન્દી અથવા અંગ્રેજીમાંથી તમારી અનુકૂળ ભાષા પસંદ કરો.",
    homeStep2Title: "૨. ફોટો લો અથવા પ્રશ્ન પૂછો",
    homeStep2Desc: "રોગિષ્ટ પાંદડાનો ફોટો અપલોડ કરો અથવા યોજના અંગે સવાલ લખો.",
    homeStep3Title: "૩. સચોટ સલાહ મેળવો",
    homeStep3Desc: "સત્તાવાર ICAR અને કૃષિ વિભાગના સંદર્ભ સાથે ઉપાયો મેળવો.",
    homeHelplineNotice: "કિસાન કૉલ સેન્ટર ટોલ-ફ્રી નંબર: ૧૮૦૦-૧૮૦-૧૫૫૧",

    scanTitle: "પાક રોગ સ્કેન અને નિદાન",
    scanSubtitle: "ટામેટા, બટાટા, મરચી, મકાઈ, કપાસ, દ્રાક્ષ વગેરે પાકોના રોગનું સચોટ વિશ્લેષણ",
    scanUploadPrompt: "પાંદડાનો સ્પષ્ટ ફોટો અહીં મૂકો અથવા પસંદ કરો",
    scanUploadHint: "JPG અથવા PNG ફોર્મેટ (વધુમાં વધુ ૧૫ MB)",
    scanCameraBtn: "કેમેરાથી ફોટો લો",
    scanUploadBtn: "ફાઇલ પસંદ કરો",
    scanAnalyzing: "AI મૉડલ પાંદડાનું વિશ્લેષણ કરી રહ્યું છે...",
    scanResultTitle: "નિદાન પરિણામ",
    scanCropLabel: "પાકનું નામ:",
    scanDiseaseLabel: "ઓળખાયેલ રોગ:",
    scanConfidenceLabel: "ચોકસાઈ દર (Confidence):",
    scanUncertaintyAlert: "ધ્યાન આપો: આ ફોટામાં રોગના લક્ષણો અસ્પષ્ટ જણાય છે. પાંદડાનો વધુ નજીકથી અને સ્પષ્ટ ફોટો લેવા વિનંતી.",
    scanSymptomsTitle: "મુખ્ય લક્ષણો",
    scanOrganicTitle: "જૈવિક અને દેશી ઉપાયો",
    scanChemicalTitle: "ભલામણ કરેલ રાસાયણિક દવાઓ (CIBRC પ્રમાણિત)",
    scanPrecautionsTitle: "છંટકાવ વખતે સાવચેતીઓ",
    scanPreventiveTitle: "ભવિષ્યમાં રોગ અટકાવવાના પગલાં",
    scanHealthyBanner: "આ પાંદડું તંદુરસ્ત જણાય છે! કોઈ રાસાયણિક દવાની જરૂર નથી.",
    scanResetBtn: "બીજો ફોટો તપાસો",

    chatTitle: "ખેતGPT AI કૃષિ સલાહકાર",
    chatSubtitle: "સરકારી યોજનાઓ, PM-કિસાન, બાગાયત અને પશુપાલન વિશે અધિકૃત માહિતી મેળવો",
    chatNewBtn: "+ નવી ચર્ચા",
    chatHistoryTitle: "પાછલી ચર્ચાઓ",
    chatPlaceholder: "તમારો પ્રશ્ન અહીં લખો (દા.ત. પીએમ કિસાન યોજનાના હપ્તા ક્યારે મળે છે?)...",
    chatSendBtn: "મોકલો",
    chatEmptyTitle: "નમસ્તે ખેડૂત મિત્ર! હું તમારી શું મદદ કરી શકું?",
    chatEmptyDesc: "નીચેનામાંથી કોઈપણ પ્રશ્ન પસંદ કરો અથવા તમારો પોતાનો સવાલ લખો:",
    chatPrompt1: "પીએમ કિસાન યોજનાના નિયમો અને હપ્તાની વિગત આપો.",
    chatPrompt2: "ટામેટામાં પાછોતરા સુકારા (Late Blight) નો રાસાયણિક ઉપાય જણાવો.",
    chatPrompt3: "બાગાયત ખાતાની સહાયલક્ષી યોજનાઓ કઈ કઈ છે?",
    chatSourcesLabel: "સત્તાવાર સરકારી સંદર્ભ:",
    chatThinking: "સરકારી દસ્તાવેજો ચકાસી રહ્યા છીએ...",
    chatDisclaimer: "નોંધ: દવાનો છંટકાવ કરતાં પહેલાં સ્થાનિક કૃષિ વિજ્ઞાન કેન્દ્ર (KVK) ની સલાહ લેવી.",

    loading: "લોડ થઈ રહ્યું છે...",
    errorGeneric: "કંઈક ભૂલ થઈ છે. કૃપા કરીને થોડી વાર પછી પ્રયત્ન કરો.",
    retry: "ફરી પ્રયત્ન કરો"
  },
  hi: {
    appName: "खेतGPT",
    tagline: "भारतीय किसानों के लिए आधुनिक AI कृषि सलाहकार",
    navHome: "होम",
    navScan: "फसल रोग पहचान",
    navChat: "खेतGPT AI चैट",
    langSelect: "भाषा चुनें",

    homeHeroTitle: "खेती में AI का साथ — सही फसल, सटीक समाधान",
    homeHeroSubtitle: "फसल रोगों की तुरंत पहचान, प्रामाणिक सरकारी योजनाओं की जानकारी और कृषि विशेषज्ञों की वैज्ञानिक सलाह अब आपकी अपनी भाषा में।",
    homeScanCardTitle: "फसल रोग स्कैनर (AI कैमरा)",
    homeScanCardDesc: "पत्ती की तस्वीर अपलोड करें और सेकंडों में रोग की पहचान, जैविक उपचार और सुरक्षित रासायनिक समाधान पाएं।",
    homeScanCardBtn: "रोग जांचें →",
    homeChatCardTitle: "खेतGPT AI सहायक",
    homeChatCardDesc: "पीएम-किसान, फसल बीमा (PMFBY), बागवानी अनुदान, उर्वरक और पशुपालन से जुड़ा कोई भी सवाल पूछें।",
    homeChatCardBtn: "सवाल पूछें →",
    homeStepsTitle: "खेतGPT का उपयोग कैसे करें?",
    homeStep1Title: "1. भाषा चुनें",
    homeStep1Desc: "हिंदी, गुजराती या अंग्रेजी में से अपनी पसंदीदा भाषा चुनें।",
    homeStep2Title: "2. फोटो लें या सवाल पूछें",
    homeStep2Desc: "रोगग्रस्त पत्ती की फोटो अपलोड करें या सरकारी योजना पर सवाल लिखें।",
    homeStep3Title: "3. सटीक सलाह पाएं",
    homeStep3Desc: "ICAR और कृषि मंत्रालय के आधिकारिक दस्तावेजों पर आधारित समाधान पाएं।",
    homeHelplineNotice: "किसान कॉल सेंटर टोल-फ्री नंबर: 1800-180-1551",

    scanTitle: "फसल रोग पहचान और प्रबंधन",
    scanSubtitle: "टमाटर, आलू, मिर्च, मक्का, कपास, अंगूर आदि फसलों के रोगों का सटीक विश्लेषण",
    scanUploadPrompt: "पत्ती की स्पष्ट फोटो यहाँ डालें या चुनें",
    scanUploadHint: "JPG या PNG प्रारूप (अधिकतम 15 MB)",
    scanCameraBtn: "कैमरे से फोटो लें",
    scanUploadBtn: "फ़ाइल चुनें",
    scanAnalyzing: "AI मॉडल पत्ती का विश्लेषण कर रहा है...",
    scanResultTitle: "रोग निदान परिणाम",
    scanCropLabel: "फसल का नाम:",
    scanDiseaseLabel: "पहचाना गया रोग:",
    scanConfidenceLabel: "सटीकता दर (Confidence):",
    scanUncertaintyAlert: "सावधानी: इस तस्वीर में रोग के लक्षण स्पष्ट नहीं हैं। कृपया दिन के उजाले में पत्ती की नजदीकी तस्वीर लें।",
    scanSymptomsTitle: "प्रमुख लक्षण",
    scanOrganicTitle: "जैविक एवं प्राकृतिक उपचार",
    scanChemicalTitle: "अनुशंसित रासायनिक उपचार (CIBRC प्रमाणित)",
    scanPrecautionsTitle: "छिड़काव सावधानियां",
    scanPreventiveTitle: "रोकथाम के उपाय",
    scanHealthyBanner: "यह पत्ती पूरी तरह स्वस्थ है! किसी कीटनाशक की आवश्यकता नहीं है।",
    scanResetBtn: "दूसरी फोटो जांचें",

    chatTitle: "खेतGPT AI कृषि सलाहकार",
    chatSubtitle: "सरकारी योजनाओं, PM-किसान, फसल बीमा और पशुपालन पर आधिकारिक जानकारी पाएं",
    chatNewBtn: "+ नई बातचीत",
    chatHistoryTitle: "पिछली बातचीत",
    chatPlaceholder: "अपना सवाल यहाँ पूछें (उदा. पीएम किसान सम्मान निधि की किस्त कैसे चेक करें?)...",
    chatSendBtn: "भेजें",
    chatEmptyTitle: "नमस्ते किसान भाई! मैं आपकी क्या सहायता कर सकता हूँ?",
    chatEmptyDesc: "नीचे दिए गए सुझावों में से चुनें या अपना प्रश्न टाइप करें:",
    chatPrompt1: "पीएम किसान योजना की पात्रता और किस्तों का विवरण दीजिए।",
    chatPrompt2: "टमाटर में अगेती और पछेती झुलसा का क्या रासायनिक उपचार है?",
    chatPrompt3: "जैविक खाद एवं वर्मीकम्पोस्ट बनाने की सही विधि क्या है?",
    chatSourcesLabel: "आधिकारिक सरकारी संदर्भ:",
    chatThinking: "आधिकारिक कृषि दस्तावेजों से जानकारी जुटाई जा रही है...",
    chatDisclaimer: "नोट: किसी भी दवा के छिड़काव से पूर्व नजदीकी कृषि विज्ञान केंद्र (KVK) से सलाह अवश्य लें।",

    loading: "लोड हो रहा है...",
    errorGeneric: "कोई त्रुटि हुई। कृपया थोड़ी देर बाद पुनः प्रयास करें।",
    retry: "पुनः प्रयास करें"
  },
  en: {
    appName: "KhetGPT",
    tagline: "AI-Powered Agriculture Assistance for Indian Farmers",
    navHome: "Home",
    navScan: "Crop Disease Scan",
    navChat: "KhetGPT AI Chat",
    langSelect: "Select Language",

    homeHeroTitle: "AI Powered Farming Assistant — Real Crops, Grounded Advice",
    homeHeroSubtitle: "Instant crop disease identification, official government scheme insights, and evidence-based agricultural guidance in your preferred language.",
    homeScanCardTitle: "Crop Disease Scan (AI Vision)",
    homeScanCardDesc: "Upload a crop leaf photograph to receive instant disease identification, organic remedies, and verified chemical treatment with safety waiting periods.",
    homeScanCardBtn: "Diagnose Crop →",
    homeChatCardTitle: "KhetGPT AI Assistant",
    homeChatCardDesc: "Ask any question regarding PM-KISAN, crop insurance (PMFBY), horticulture subsidies, fertilizers, soil health, or animal husbandry.",
    homeChatCardBtn: "Ask KhetGPT →",
    homeStepsTitle: "How to Use KhetGPT",
    homeStep1Title: "1. Select Language",
    homeStep1Desc: "Choose Gujarati, Hindi, or English. All UI and AI answers strictly respect your choice.",
    homeStep2Title: "2. Upload or Ask",
    homeStep2Desc: "Snap a photo of an affected leaf or type an agricultural question.",
    homeStep3Title: "3. Get Grounded Advice",
    homeStep3Desc: "Receive verified recommendations backed by ICAR and Ministry publications with page citations.",
    homeHelplineNotice: "Kisan Call Centre Toll-Free: 1800-180-1551",

    scanTitle: "Crop Disease Scan & Treatment",
    scanSubtitle: "Accurate computer vision diagnostics for Tomato, Potato, Pepper, Corn, Grape, and more Indian staple crops",
    scanUploadPrompt: "Drop or select a clear leaf photograph",
    scanUploadHint: "JPG or PNG formats supported (up to 15 MB)",
    scanCameraBtn: "Capture Photo",
    scanUploadBtn: "Select File",
    scanAnalyzing: "Evaluating leaf features with trained neural network...",
    scanResultTitle: "Diagnostic Assessment",
    scanCropLabel: "Crop Name:",
    scanDiseaseLabel: "Identified Condition:",
    scanConfidenceLabel: "Model Confidence:",
    scanUncertaintyAlert: "Caution: The model has low certainty on this image. It may be blurry, poorly illuminated, or outside supported classes. Please upload a clear daylight close-up.",
    scanSymptomsTitle: "Visual Symptoms",
    scanOrganicTitle: "Biological & Organic Controls",
    scanChemicalTitle: "Recommended Chemical Fungicides / Pesticides",
    scanPrecautionsTitle: "Application Precautions & Waiting Period",
    scanPreventiveTitle: "Preventive Cultural Practices",
    scanHealthyBanner: "This leaf appears healthy! No chemical intervention is needed.",
    scanResetBtn: "Scan Another Leaf",

    chatTitle: "KhetGPT AI Agricultural Assistant",
    chatSubtitle: "Grounded RAG answers from official government guidelines and ICAR research documents",
    chatNewBtn: "+ New Chat",
    chatHistoryTitle: "Recent Conversations",
    chatPlaceholder: "Ask an agricultural question (e.g. What are the eligibility rules for PM-KISAN?)...",
    chatSendBtn: "Send",
    chatEmptyTitle: "Welcome, Farmer Friend! How can I assist you today?",
    chatEmptyDesc: "Select one of the common farmer questions below or type your own:",
    chatPrompt1: "What are the key benefits and enrollment steps for PM-KISAN?",
    chatPrompt2: "How to manage early and late blight in tomato and potato crops?",
    chatPrompt3: "What subsidies are provided under the Horticulture Development Schemes?",
    chatSourcesLabel: "Verified Official Citations:",
    chatThinking: "Searching official agricultural documentation...",
    chatDisclaimer: "Disclaimer: Always confirm pesticide dosages with your local Krishi Vigyan Kendra (KVK).",

    loading: "Loading...",
    errorGeneric: "An unexpected error occurred. Please try again shortly.",
    retry: "Try Again"
  }
};

