"""
KhetGPT Crop Disease Treatment & Advisory Knowledge Base
Provides evidence-based treatment protocols, chemical precautions, biological remedies,
and preventive practices in English, Hindi, and Gujarati.
Sourced from ICAR, State Agricultural Universities (AAU/JAU/PAU/IARI), and CIBRC guidelines.
"""

from typing import Dict, Any, Optional

CROP_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "Tomato": {"en": "Tomato", "hi": "टमाटर", "gu": "ટામેટા"},
    "Potato": {"en": "Potato", "hi": "आलू", "gu": "બટાટા"},
    "Corn": {"en": "Corn (Maize)", "hi": "मक्का", "gu": "મકાઈ"},
    "Corn (maize)": {"en": "Corn (Maize)", "hi": "मक्का", "gu": "મકાઈ"},
    "Bell Pepper": {"en": "Bell Pepper / Chilli", "hi": "शिमला मिर्च / मिर्च", "gu": "શિમલા મરચાં / મરચી"},
    "Pepper, bell": {"en": "Bell Pepper / Chilli", "hi": "शिमला मिर्च / मिर्च", "gu": "શિમલા મરચાં / મરચી"},
    "Rice": {"en": "Rice (Paddy)", "hi": "धान / चावल", "gu": "ડાંગર / ચોખા"},
    "Cassava": {"en": "Cassava", "hi": "कसावा", "gu": "કસાવા"},
    "Grape": {"en": "Grape", "hi": "अंगूर", "gu": "દ્રાક્ષ"},
    "Apple": {"en": "Apple", "hi": "सेब", "gu": "સફરજન"},
    "Orange": {"en": "Orange (Citrus)", "hi": "संतरा (नींबू वर्गीय)", "gu": "સંતરા (સાઇટ્રસ)"},
    "Peach": {"en": "Peach", "hi": "आड़ू", "gu": "પીચ"},
    "Cherry (including sour)": {"en": "Cherry", "hi": "चेरी", "gu": "ચેરી"},
    "Blueberry": {"en": "Blueberry", "hi": "ब्लूबेरी", "gu": "બ્લુબેરી"},
    "Raspberry": {"en": "Raspberry", "hi": "रसभरी", "gu": "રાસ્પબેરી"},
    "Soybean": {"en": "Soybean", "hi": "सोयाबीन", "gu": "સોયાબીન"},
    "Squash": {"en": "Squash / Gourd", "hi": "कद्दू / घिया", "gu": "કોળું / દૂધી"},
    "Strawberry": {"en": "Strawberry", "hi": "स्ट्रॉबेरी", "gu": "સ્ટ્રોબેરી"}
}

TREATMENT_DATABASE: Dict[str, Dict[str, Any]] = {
    # ------------------ TOMATO (10 CLASSES) ------------------
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "disease_en": "Early Blight (Alternaria solani)",
        "disease_hi": "अगेती झुलसा (अल्टरनेरिया सोलानी)",
        "disease_gu": "અગેતી સુકારો (અલ્ટરનેરીયા સોલાની)",
        "symptoms": {
            "en": "Brown to black spots with concentric rings (target-board pattern) on older leaves. Leaves turn yellow and drop prematurely.",
            "hi": "पुरानी पत्तियों पर गोल भूरे-काले छल्लेदार धब्बे (टारगेट बोर्ड जैसे)। पत्तियां पीली होकर गिर जाती हैं।",
            "gu": "નીચેના જૂના પાન પર ગોળાકાર કથ્થઈ-કાળા વલયાકાર ડાઘા (ટાર્ગેટ બોર્ડ જેવા). પાન પીળા પડી ખરી પડે છે."
        },
        "biological_control": {
            "en": "Spray Trichoderma viride or Pseudomonas fluorescens @ 5-10 g/L water. Apply neem seed kernel extract (NSKE 5%) preventatively.",
            "hi": "ट्राइकोडर्मा विरिडी या स्यूडोमोनास फ्लोरेसेंस 5-10 ग्राम प्रति लीटर पानी में मिलाकर छिड़कें। नीम अर्क (NSKE 5%) का छिड़काव करें।",
            "gu": "ટ્રાઈકોડર્મા વિરીડી અથવા સ્યુડોમોનાસ ફ્લોરેસન્સ ૫-૧૦ ગ્રામ પ્રતિ લીટર પાણીમાં ભેળવી છંટકાવ કરવો. ૫% લીંબોળીના અર્કનો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "Spray Mancozeb 75% WP (2.5 g/L) or Chlorothalonil 75% WP (2 g/L). In severe spread, apply Azoxystrobin 18.2% + Difenoconazole 11.4% SC (1 ml/L).",
            "hi": "मैनकोजेब 75% WP (2.5 ग्राम/ली) या क्लोरोथालोनिल (2 ग्राम/ली) का छिड़काव करें। गंभीर प्रकोप में एज़ोक्सीस्ट्रोबिन + डिफेनोकोनाज़ोल (1 मिली/ली) दें।",
            "gu": "મેન્કોઝેબ ૭૫% WP (૨.૫ ગ્રામ/લી.) અથવા ક્લોરોથેલોનીલ (૨ ગ્રામ/લી.) નો છંટકાવ કરવો. વધુ ઉપદ્રવમાં એઝોક્સીસ્ટ્રોબિન + ડાયફેનોકોનાઝોલ (૧ મિ.લી./લી.) છાંટવું."
        },
        "precautions": {
            "en": "Observe a 7-day waiting period before harvest. Spray in calm weather early morning. Wear mask and gloves.",
            "hi": "तुड़ाई से कम से कम 7 दिन पहले छिड़काव बंद करें। सुबह के समय छिड़काव करें। मास्क और दस्ताने का प्रयोग करें।",
            "gu": "વીણીના ૭ દિવસ પહેલા દવાનો છંટકાવ બંધ કરવો. સવારના શાંત વાતાવરણમાં છંટકાવ કરવો. માસ્ક અને હાથમોજા પહેરવા."
        },
        "preventive_measures": {
            "en": "Use drip irrigation instead of sprinkler to keep foliage dry. Practice crop rotation with non-solanaceous crops for 2-3 years.",
            "hi": "टपक सिंचाई (ड्रिप) का उपयोग करें ताकि पत्तियां गीली न रहें। 2-3 साल तक टमाटर-आलू परिवार की फसलें न लगाएं।",
            "gu": "ટપક પિયત પદ્ધતિ અપનાવવી જેથી પાન ભીના ન રહે. ટામેટા-બટાટા સિવાયના પાકોની ૨-૩ વર્ષ પાક ફેરબદલી કરવી."
        }
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "disease_en": "Late Blight (Phytophthora infestans)",
        "disease_hi": "पछेती झुलसा (फाइटोफ्थोरा इन्फेस्टन्स)",
        "disease_gu": "પાછોતરો સુકારો (ફાઈટોપ્થોરા ઈન્ફેસ્ટન્સ)",
        "symptoms": {
            "en": "Water-soaked irregular pale-green lesions that rapidly turn dark brown to purplish-black. White cottony fungal growth on leaf undersides in humid cool weather.",
            "hi": "पत्तियों पर जल-सिक्त अनियमित गहरे भूरे-काले धब्बे। नम मौसम में पत्ती की निचली सतह पर सफेद फफूंद दिखाई देती है।",
            "gu": "પાન પર પાણીપોચા અનિયમિત કાળા-કથ્થઈ ડાઘા. ભેજવાળા ઠંડા વાતાવરણમાં પાનની નીચે સફેદ ફૂગની રૂ જેવી જાળી દેખાય છે."
        },
        "biological_control": {
            "en": "Apply Trichoderma harzianum soil treatment and foliar spray @ 5 g/L. Spray bio-formulations of Bacillus amyloliquefaciens.",
            "hi": "ट्राइकोडर्मा हरज़ियानम का भूमि उपचार एवं 5 ग्राम/ली की दर से छिड़काव करें। बैसिलस आधारित जैव कवकनाशी उपयोगी है।",
            "gu": "ટ્રાઈકોડર્મા હાર્ઝિયાનમ ૫ ગ્રામ/લીટર મુજબ છંટકાવ કરવો અને જમીનમાં આપવું. બેસિલસ આધારિત જૈવિક ફૂગનાશક વાપરવું."
        },
        "chemical_control": {
            "en": "Spray Metalaxyl 8% + Mancozeb 64% WP (2.5 g/L) or Cymoxanil 8% + Mancozeb 64% WP (2 g/L). In emergency: Dimethomorph 50% WP (1 g/L).",
            "hi": "मेटालेक्सिल + मैनकोजेब (2.5 ग्राम/ली) या साइमोक्सानिल + मैनकोजेब (2 ग्राम/ली) का तुरंत छिड़काव करें। गंभीर स्थिति में डाईमेथोमोर्फ (1 ग्राम/ली) दें।",
            "gu": "મેટાલક્ષિલ ૮% + મેન્કોઝેબ ૬૪% WP (૨.૫ ગ્રામ/લી.) અથવા સાયમોક્સેનીલ + મેન્કોઝેબ (૨ ગ્રામ/લી.) છાંટવું. વધુ ઉપદ્રવમાં ડાઈમેથોમોર્ફ (૧ ગ્રામ/લી.) આપવું."
        },
        "precautions": {
            "en": "Highly destructive in cloudy, cool, foggy conditions. Take preventive action immediately when temperature drops below 20°C with high humidity.",
            "hi": "बादल छाए रहने और कोहरे में यह रोग बहुत तेजी से फैलता है। तापमान गिरते ही तुरंत सुरक्षात्मक छिड़काव करें।",
            "gu": "વાદળછાયા અને ઝાકળવાળા વાતાવરણમાં રોગ ખૂબ ઝડપથી ફેલાય છે. તાપમાન ઘટે ત્યારે તાત્કાલિક સાવચેતીરૂપ છંટકાવ કરવો."
        },
        "preventive_measures": {
            "en": "Ensure proper field drainage. Remove and destroy infected vines immediately. Avoid dense planting for proper air circulation.",
            "hi": "खेत में जल निकासी की उचित व्यवस्था रखें। रोगग्रस्त पौधों को उखाड़कर नष्ट करें। हवा के आवागमन के लिए उचित दूरी रखें।",
            "gu": "ખેતરમાં પાણી ભરાઈ ન રહે તેની કાળજી રાખવી. રોગિષ્ટ છોડ ઉપાડી બાળી નાખવા. છોડ વચ્ચે પૂરતું અંતર રાખવું."
        }
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "disease_en": "Bacterial Spot (Xanthomonas campestris)",
        "disease_hi": "जीवाणु धब्बा रोग (जैंथोमोनास)",
        "disease_gu": "જીવાણુથી થતો ડાઘાનો રોગ (બેક્ટેરિયલ સ્પોટ)",
        "symptoms": {
            "en": "Small, water-soaked, circular spots on leaves that turn dark brown with yellow halos. Small raised scabby lesions on fruits.",
            "hi": "पत्तियों पर छोटे, जल-सिक्त गहरे भूरे धब्बे जिनके चारों ओर पीला घेरा होता है। फलों पर उभरे हुए खुरदरे धब्बे।",
            "gu": "પાન પર નાના, પાણીપોચા ગોળ કાળા-કથ્થઈ ડાઘા અને ફરતે પીળી કિનારી. ફળ પર ઊપસેલા ખરબચડા ડાઘા જોવા મળે છે."
        },
        "biological_control": {
            "en": "Seed treatment with Pseudomonas fluorescens @ 10 g/kg seed. Foliar spray of bio-control agents at 15-day intervals.",
            "hi": "स्यूडोमोनास फ्लोरेसेंस 10 ग्राम/किग्रा बीज दर से बीजोपचार करें। 15 दिन के अंतराल पर जैव नियंत्रक का छिड़काव करें।",
            "gu": "સ્યુડોમોનાસ ફ્લોરેસન્સ ૧૦ ગ્રામ/કિલો બીજ મુજબ બીજ માવજત આપવી. ૧૫ દિવસના અંતરે જૈવિક છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "Spray Copper Oxychloride 50% WP (3 g/L) mixed with Streptocycline or Plantomycin (1 g in 10 L water). Repeat after 10-12 days.",
            "hi": "कॉपर ऑक्सीक्लोराइड 50% WP (3 ग्राम/ली) के साथ स्ट्रेप्टोसाइक्लिन (1 ग्राम प्रति 10 लीटर पानी) मिलाकर छिड़कें।",
            "gu": "કોપર ઓક્સીક્લોરાઇડ ૫૦% WP (૩ ગ્રામ/લી.) સાથે સ્ટ્રેપ્ટોસાઇક્લીન (૧ ગ્રામ પ્રતિ ૧૦ લીટર પાણી) ભેળવી છંટકાવ કરવો."
        },
        "precautions": {
            "en": "Do not enter fields or prune when plants are wet. Copper sprays should be applied during cooler hours to prevent leaf scorching.",
            "hi": "पत्तियां गीली होने पर निराई-गुड़ाई या कटाई न करें। कॉपर का छिड़काव अधिक धूप में न करें।",
            "gu": "છોડ ભીના હોય ત્યારે ખેતરમાં મજૂરીકામ કે કાપણી ન કરવી. તીવ્ર તાપમાં કોપર દવાનો છંટકાવ ટાળવો."
        },
        "preventive_measures": {
            "en": "Use certified disease-free seeds. Treat seeds in hot water (50°C for 25 mins) before nursery sowing.",
            "hi": "प्रमाणित रोगमुक्त बीजों का ही उपयोग करें। बुवाई से पूर्व बीजों को 50°C गर्म पानी में 25 मिनट उपचारित करें।",
            "gu": "પ્રમાણિત રોગમુક્ત બિયારણ વાપરવું. વાવણી પહેલાં ૫૦°C ગરમ પાણીમાં ૨૫ મિનિટ બીજ માવજત આપવી."
        }
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "disease_en": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "disease_hi": "पर्ण कुंचन रोग (येलो लीफ कर्ल वायरस)",
        "disease_gu": "પાનના કોકડવાટનો વાયરસ (પીળો કોકડવા)",
        "symptoms": {
            "en": "Severe upward leaf cupping, curling, yellowing of leaf margins, reduced leaf size, and severe plant stunting. Flowers abort and fruit set is drastically reduced.",
            "hi": "पत्तियां ऊपर की ओर मुड़कर कटोरीनुमा हो जाती हैं, किनारे पीले पड़ते हैं। पौधा बौना रह जाता है और फल नहीं लगते।",
            "gu": "પાન ઉપર તરફ વળીને વાટકા જેવા થઈ જાય છે, કિનારી પીળી પડે છે અને છોડ ઠિંગણો રહી જાય છે. ફળ બેસતા નથી."
        },
        "biological_control": {
            "en": "Install yellow sticky traps (15-20 per acre) to monitor and capture whiteflies. Spray Neem oil (10,000 ppm) @ 2 ml/L or Verticillium lecanii @ 5 g/L.",
            "hi": "सफेद मक्खी नियंत्रण के लिए प्रति एकड़ 15-20 पीले चिपचिपे ट्रैप लगाएं। नीम तेल (10,000 ppm) 2 मिली/ली का छिड़काव करें।",
            "gu": "સફેદ માખી પકડવા માટે એકરે ૧૫-૨૦ પીળા ચીકણા ટ્રેપ (સ્ટીકી ટ્રેપ) ગોઠવવા. ૧૦,૦૦૦ ppm લીમડાનું તેલ ૨ મિ.લી./લી. મુજબ છાંટવું."
        },
        "chemical_control": {
            "en": "Control whitefly vectors: Spray Diafenthiuron 50% WP (1 g/L) or Spiromesifen 22.9% SC (1 ml/L) or Acetamiprid 20% SP (0.5 g/L).",
            "hi": "सफेद मक्खी की रोकथाम हेतु: डायफेन्थियूरॉन 50% WP (1 ग्राम/ली) या स्पाइरोमेसिफेन (1 मिली/ली) या एसिटामिप्रिड (0.5 ग्राम/ली) का छिड़काव करें।",
            "gu": "સફેદ માખીના નિયંત્રણ માટે: ડાયાફેન્થિયુરોન ૫૦% WP (૧ ગ્રામ/લી.) અથવા સ્પાયરોમેસીફેન (૧ મિ.લી./લી.) અથવા એસીટામિપ્રીડ (૦.૫ ગ્રામ/લી.) છાંટવું."
        },
        "precautions": {
            "en": "Virus cannot be cured once inside the plant; management relies entirely on vector (whitefly) control and rogueing infected plants.",
            "hi": "वायरस से ग्रसित पौधे ठीक नहीं होते, इसलिए सफेद मक्खी का नियंत्रण ही इसका एकमात्र प्रभावी उपाय है।",
            "gu": "વાયરસ લાગ્યા પછી છોડ સારો થતો નથી, તેથી રોગિષ્ટ છોડ તાત્કાલિક ઉપાડી લેવા અને સફેદ માખીનું નિયંત્રણ કરવું."
        },
        "preventive_measures": {
            "en": "Raise nursery under 40-mesh insect-proof nylon net. Plant 2-3 border rows of maize or sorghum as a live barrier against whitefly entry.",
            "hi": "नर्सरी को 40-मेश नायलॉन नेट में तैयार करें। खेत की मेड़ों पर मक्का या ज्वार की 2-3 कतारें सुरक्षा दीवार के रूप में लगाएं।",
            "gu": "ધરૂવાડિયું ૪૦ મેશની જંતુરોધક નેટમાં બનાવવું. ખેતરની ફરતે મકાઈ કે જુવારની ૨-૩ હાર રક્ષણાત્મક વાડ તરીકે વાવવી."
        }
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "disease_en": "Leaf Mold (Passalora fulva)",
        "disease_hi": "टमाटर का पत्ती फफूंद (लीफ मोल्ड)",
        "disease_gu": "ટામેટાનો પાનનો ફૂગ રોગ (લીફ મોલ્ડ)",
        "symptoms": {
            "en": "Pale green or yellowish spots on upper leaf surfaces, with olive-green to grayish velvety fungal mold on lower surfaces.",
            "hi": "पत्तियों की ऊपरी सतह पर हल्के हरे-पीले धब्बे, और निचली सतह पर जैतून जैसे हरे-धूसर मखमली फफूंद के गुच्छे।",
            "gu": "પાનની ઉપરની બાજુ આછા પીળા ડાઘા અને પાનની નીચેની બાજુ કથ્થઈ-લીલા મખમલ જેવા ફૂગના થર દેખાય છે."
        },
        "biological_control": {
            "en": "Spray Trichoderma viride @ 5 g/L or bio-fungicide Bacillus subtilis @ 4 g/L.",
            "hi": "ट्राइकोडर्मा विरिडी 5 ग्राम/ली या बैसिलस सबटिलिस 4 ग्राम/ली का छिड़काव करें।",
            "gu": "ટ્રાઈકોડર્મા વિરીડી ૫ ગ્રામ/લી. અથવા બેસિલસ સબટીલીસ ૪ ગ્રામ/લી. મુજબ છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Difenoconazole 25% EC (1 ml/L) or Copper Oxychloride 50% WP (2.5 g/L).",
            "hi": "डिफेनोकोनाज़ोल 25% EC (1 मिली/ली) या कॉपर ऑक्सीक्लोराइड 50% WP (2.5 ग्राम/ली) का छिड़काव करें।",
            "gu": "ડાયફેનોકોનાઝોલ ૨૫% EC (૧ મિ.લી./લી.) અથવા કોપર ઓક્સીક્લોરાઇડ (૨.૫ ગ્રામ/લી.) છાંટવું."
        },
        "precautions": {
            "en": "Ensure proper ventilation and pruning to lower relative humidity below 85%.",
            "hi": "हवा का संचार बढ़ाएं और निचली पत्तियों की छंटाई करें ताकि नमी कम हो सके।",
            "gu": "હવા ઉજાસ વધારવો અને નીચેના પાનની છાંટણી કરવી જેથી ભેજ ઘટે."
        },
        "preventive_measures": {
            "en": "Avoid wetting foliage during irrigation; use drip system and wider spacing.",
            "hi": "सिंचाई के समय पत्तियों को भीगने न दें; ड्रिप का प्रयोग करें।",
            "gu": "પિયત વખતે પાન ભીના ન થાય તેનું ધ્યાન રાખવું; ટપક પદ્ધતિ વાપરવી."
        }
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "disease_en": "Septoria Leaf Spot (Septoria lycopersici)",
        "disease_hi": "सेप्टोरिया पत्ती धब्बा रोग",
        "disease_gu": "સેપ્ટોરીયા પાનના ટપકાંનો રોગ",
        "symptoms": {
            "en": "Numerous small circular spots (2-3 mm) with dark brown margins and sunken grayish-white centers with tiny black specks.",
            "hi": "पत्तियों पर छोटे गोल धब्बे (2-3 मिमी) जिनके किनारे गहरे भूरे और केंद्र हल्के धूसर रंग के होते हैं।",
            "gu": "પાન પર અસંખ્ય નાના ગોળ ટપકાં (૨-૩ મિ.મી.) જેની કિનારી કાળી-કથ્થઈ અને વચ્ચેનો ભાગ રાખોડી સફેદ હોય છે."
        },
        "biological_control": {
            "en": "Apply Pseudomonas fluorescens foliar spray @ 5 g/L combined with neem cake in soil.",
            "hi": "स्यूडोमोनास फ्लोरेसेंस 5 ग्राम/ली का पर्णीय छिड़काव करें और मिट्टी में नीम की खली डालें।",
            "gu": "સ્યુડોમોનાસ ૫ ગ્રામ/લી. પાણીમાં ભેળવી છાંટવું અને જમીનમાં લીંબોળીનો ખોળ આપવો."
        },
        "chemical_control": {
            "en": "Spray Chlorothalonil 75% WP (2 g/L) or Mancozeb 75% WP (2.5 g/L) at first symptom appearance.",
            "hi": "क्लोरोथालोनिल 75% WP (2 ग्राम/ली) या मैनकोजेब 75% WP (2.5 ग्राम/ली) का छिड़काव करें।",
            "gu": "ક્લોરોથેલોનીલ ૭૫% WP (૨ ગ્રામ/લી.) અથવા મેન્કોઝેબ (૨.૫ ગ્રામ/લી.) નો છંટકાવ કરવો."
        },
        "precautions": {
            "en": "Clean farm implements and stakes between seasons to remove overwintering spores.",
            "hi": "उपकरणों और खूंटियों को अच्छी तरह साफ करें ताकि फफूंद के जीवाणु नष्ट हो सकें।",
            "gu": "સાધનો અને ટેકાના લાકડા સાફ કરવા જેથી ફૂગના અવશેષો નાશ પામે."
        },
        "preventive_measures": {
            "en": "Mulch the soil surface around plants to prevent splash dispersal of soil spores.",
            "hi": "पौधों के चारों ओर मल्चिंग करें ताकि मिट्टी के छींटे पत्तियों पर न पड़ें।",
            "gu": "છોડની ફરતે પ્લાસ્ટિક કે સૂકા ઘાસનું મલ્ચિંગ કરવું જેથી માટીના ઉછાળા ન લાગે."
        }
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato",
        "disease_en": "Two-Spotted Spider Mite (Tetranychus urticae)",
        "disease_hi": "लाल मकड़ी / माइट कीट (दो-धब्बेदार मकड़ी)",
        "disease_gu": "લાલ કથીરી / સ્પાઇડર માઇટ (બે ટપકાંવાળી કથીરી)",
        "symptoms": {
            "en": "Fine yellow stippling or bronzing on upper leaf surface. Silky fine webbing visible on leaf undersides with tiny moving mites.",
            "hi": "पत्तियों की ऊपरी सतह पर बारीक पीले धब्बे और निचली सतह पर महीन रेशमी जाला व चलती हुई सूक्ष्म लाल-पीली मकड़ियां।",
            "gu": "પાનની ઉપરની સપાટી પર પીળા ઝીણા ટપકાં અને નીચેની બાજુ બારીક જાળું તથા હલનચલન કરતી સૂક્ષ્મ કથીરીઓ."
        },
        "biological_control": {
            "en": "Spray Neem oil (10,000 ppm) @ 3 ml/L or release predatory mites (Phytoseiulus persimilis).",
            "hi": "नीम तेल (10,000 ppm) 3 मिली/ली का छिड़काव करें। मित्र कीट (शिकारी माइट) छोड़ें।",
            "gu": "૧૦,૦૦૦ ppm લીંબોળીનું તેલ ૩ મિ.લી./લી. મુજબ છાંટવું અથવા પરભક્ષી કથીરી છોડવી."
        },
        "chemical_control": {
            "en": "Spray Spiromesifen 22.9% SC @ 1 ml/L or Propargite 57% EC @ 2 ml/L or Abamectin 1.9% EC @ 0.75 ml/L.",
            "hi": "स्पाइरोमेसिफेन 22.9% SC (1 मिली/ली) या प्रोपारगाइट 57% EC (2 मिली/ली) का छिड़काव करें।",
            "gu": "સ્પાયરોમેસીફેન ૨૨.૯% SC (૧ મિ.લી./લી.) અથવા પ્રોપારગાઈટ ૫૭% EC (૨ મિ.લી./લી.) છાંટવું."
        },
        "precautions": {
            "en": "Avoid using broad-spectrum synthetic pyrethroids as they kill natural mite predators and cause mite flare-ups.",
            "hi": "पाइरेथ्रॉइड कीटनाशकों का प्रयोग न करें क्योंकि वे मित्र कीटों को मारकर मकड़ी को और बढ़ाते हैं।",
            "gu": "પાયરેથ્રોઇડ દવાઓ ન વાપરવી કારણ કે તે મિત્ર કીટકોને મારી નાખી કથીરીનો ઉપદ્રવ વધારે છે."
        },
        "preventive_measures": {
            "en": "Keep field borders weed-free. Avoid plant water stress during hot dry weather.",
            "hi": "मेड़ों को खरपतवार मुक्त रखें। तेज गर्मी में फसल को पानी की कमी न होने दें।",
            "gu": "શેઢા-પાળાઓ નીંદણમુક્ત રાખવા. ગરમ સૂકા વાતાવરણમાં પાકને પાણીની ખેંચ ન પડવા દેવી."
        }
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato",
        "disease_en": "Target Spot (Corynespora cassiicola)",
        "disease_hi": "टारगेट स्पॉट रोग (कोरीनेस्पोरा)",
        "disease_gu": "ટાર્ગેટ સ્પોટ રોગ (કોરીનેસ્પોરા)",
        "symptoms": {
            "en": "Brown circular lesions with faint concentric rings and light brown centers. Causes rapid defoliation in warm humid conditions.",
            "hi": "हल्के भूरे केंद्र वाले गोल छल्लेदार धब्बे। गर्म और नम मौसम में तेजी से पत्तियां झड़ती हैं।",
            "gu": "આછા કથ્થઈ કેન્દ્રવાળા વલયાકાર ગોળ ડાઘા. ગરમ અને ભેજવાળા વાતાવરણમાં પાન ઝડપથી ખરી પડે છે."
        },
        "biological_control": {
            "en": "Spray Trichoderma harzianum @ 5 g/L with cow urine solution (5%).",
            "hi": "ट्राइकोडर्मा हरज़ियानम 5 ग्राम/ली और गोमूत्र (5%) के घोल का छिड़काव करें।",
            "gu": "ટ્રાઈકોડર્મા ૫ ગ્રામ/લી. અને ૫% ગૌમૂત્રના દ્રાવણનો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "Spray Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L or Fluxapyroxad + Pyraclostrobin @ 0.6 ml/L.",
            "hi": "एज़ोक्सीस्ट्रोबिन + डिफेनोकोनाज़ोल (1 मिली/ली) या फ्लक्सापाइરોક્સેડ + पायराक्लोस्ट्रोबिन का छिड़काव करें।",
            "gu": "એઝોક્સીસ્ટ્રોબિન + ડાયફેનોકોનાઝોલ (૧ મિ.લી./લી.) નો સમયસર છંટકાવ કરવો."
        },
        "precautions": {
            "en": "Avoid working in fields when canopy is damp to prevent spreading fungus to adjacent healthy rows.",
            "hi": "पत्तियां गीली होने पर खेत में काम न करें।",
            "gu": "પાન ભીના હોય ત્યારે ખેતરમાં અવરજવર ટાળવી."
        },
        "preventive_measures": {
            "en": "Stake and tie plants properly; prune bottom suckers to enhance lower air flow.",
            "hi": "पौधों को सहारा (स्टेकिंग) दें और नीचे की अनावश्यक शाखाएं काटें।",
            "gu": "છોડને સ્ટેકિંગ (ટેકા) આપવા અને નીચેની ફૂટોની છાંટણી કરવી જેથી હવા ફરે."
        }
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato",
        "disease_en": "Tomato Mosaic Virus (ToMV)",
        "disease_hi": "टमाटर मोज़ेक वायरस",
        "disease_gu": "ટામેટાનો મોઝેક વાયરસ",
        "symptoms": {
            "en": "Mottling with alternating light green and dark green patches, leaf distortion, blister-like leaf surfaces, and 'shoestring' leaves.",
            "hi": "पत्तियों पर हल्के और गहरे हरे रंग के चितकबरे धब्बे, पत्तियों का मुड़ना और संकरा हो जाना।",
            "gu": "પાન પર આછા અને ઘાટા લીલા રંગના ચિત્ર-વિચિત્ર ડાઘા, પાન સાંકડા થઈ જવા અને સપાટી ખરબચડી થવી."
        },
        "biological_control": {
            "en": "Spray skimmed milk solution (100 ml per liter water) on seedlings before transplanting to reduce mechanical transmission.",
            "hi": "रोपाई से पहले पौध पर मलाई रहित दूध के घोल (100 मिली/ली) का छिड़काव करें।",
            "gu": "ફેરરોપણી પહેલાં ધરૂ પર ૧૦% દૂધના દ્રાવણનો છંટકાવ કરવો જેથી સ્પર્શથી ફેલાતો અટકે."
        },
        "chemical_control": {
            "en": "No chemical viricide exists. Wash hands and tools thoroughly with 10% trisodium phosphate (TSP) or soap solution.",
            "hi": "वायरस के लिए कोई रासायनिक दवा नहीं है। हाथ व औजार साबुन या TSP घोल से धोएं।",
            "gu": "વાયરસ માટે કોઈ રાસાયણિક દવા નથી. હાથ અને સાધનો સાબુના પાણીથી ધોવા."
        },
        "precautions": {
            "en": "Smokers/tobacco users must wash hands with soap before touching tomato seedlings, as tobacco transmits the virus.",
            "hi": "तंबाकू का सेवन करने वाले श्रमिक हाथ धोए बिना पौध को न छुएं।",
            "gu": "તમાકુ ખાનાર કે બીડી પીનાર વ્યક્તિએ હાથ સાબુથી ધોયા વિના છોડને અડવું નહીં."
        },
        "preventive_measures": {
            "en": "Use certified virus-resistant cultivars. Rogue out and bury infected seedlings immediately.",
            "hi": "रोग प्रतिरोधी किस्में लगाएं। ग्रसित पौधों को उखाड़कर गहरे गड्ढे में दबाएं।",
            "gu": "રોગ પ્રતિકારક જાતો વાવવી. રોગિષ્ટ છોડ મૂળમાંથી ઉપાડી ખાડામાં દાટી દેવા."
        }
    },
    "Tomato___healthy": {
        "crop": "Tomato",
        "disease_en": "Healthy Tomato Foliage",
        "disease_hi": "स्वस्थ टमाटर की पत्तियां",
        "disease_gu": "તંદુરસ્ત ટામેટાના પાન",
        "symptoms": {
            "en": "Vigorous, rich green leaves with crisp margins and normal growth. No spots, necrosis, or virus mottling.",
            "hi": "पत्तियां पूरी तरह हरी-भरी, चमकदार और स्वस्थ हैं। कोई धब्बा, पीलापन या कीट क्षति नहीं है।",
            "gu": "ટામેટાના પાન એકદમ લીલાંછમ, તાજાં અને રોગમુક્ત છે. કોઈ ડાઘા કે વાયરસના લક્ષણો નથી."
        },
        "biological_control": {
            "en": "Apply preventive Jivamrit or Panchagavya (3% spray) every 15 days to bolster plant immunity.",
            "hi": "पौधे की रोग प्रतिरोधक क्षमता बढ़ाने हेतु हर 15 दिन में जीवामृत या पंचगव्य (3%) का छिड़काव करें।",
            "gu": "છોડની રોગપ્રતિકારક શક્તિ જાળવવા દર ૧૫ દિવસે જીવામૃત અથવા પંચગવ્ય (૩%) નો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "No chemical pesticide or fungicide is required. Save money and protect beneficial insects.",
            "hi": "किसी भी रासायनिक कीटनाशक की आवश्यकता नहीं है। लागत बचाएं और मित्र कीटों की रक्षा करें।",
            "gu": "કોઈપણ રાસાયણિક જંતુનાશકની જરૂર નથી. દવાઓનો ખર્ચ બચાવો અને જમીનની ફળદ્રુપતા જાળવો."
        },
        "precautions": {
            "en": "Inspect crop weekly, particularly leaf undersides, for early warning signs of pests or mildew.",
            "hi": "साप्ताहिक रूप से खेत का निरीक्षण करें और पत्तियों की निचली सतह की जांच करें।",
            "gu": "અઠવાડિયે એકવાર પાનની નીચેની બાજુ ચૂસિયા જીવાત કે ફૂગ માટે ખાસ તપાસ કરવી."
        },
        "preventive_measures": {
            "en": "Maintain balanced NPK fertilizer and calcium nutrition to prevent blossom-end rot. Keep optimal soil moisture.",
            "hi": "संतुलित खाद और कैल्शियम की पर्याप्त मात्रा दें। खेत में समान नमी बनाए रखें।",
            "gu": "સંતુલિત ખાતર અને કેલ્શિયમ આપવું જેથી ફળ સડવાનો રોગ ન થાય. જમીનમાં પૂરતો ભેજ જાળવવો."
        }
    },

    # ------------------ POTATO (3 CLASSES) ------------------
    "Potato___Early_blight": {
        "crop": "Potato",
        "disease_en": "Potato Early Blight (Alternaria solani)",
        "disease_hi": "आलू अगेती झुलसा",
        "disease_gu": "બટાટાનો અગેતી સુકારો",
        "symptoms": {
            "en": "Target-like circular brown necrotic lesions with yellow chlorotic rings on lower leaves.",
            "hi": "निचली पत्तियों पर कत्थई रंग के गोल छल्लेदार धब्बे, पत्तियां सूखने लगती हैं।",
            "gu": "નીચેના પાન પર ગોળ કથ્થઈ વલયાકાર ટપકાં, સમય જતાં પાન સુકાઈ જાય છે."
        },
        "biological_control": {
            "en": "Spray Pseudomonas fluorescens @ 10 g/L or Trichoderma viride @ 5 g/L.",
            "hi": "स्यूडोमोनास फ्लोरेसेंस 10 ग्राम/ली या ट्राइकोडर्मा 5 ग्राम/ली का छिड़काव करें।",
            "gu": "સ્યુડોમોનાસ ૧૦ ગ્રામ/લી. અથવા ટ્રાઈકોડર્મા ૫ ગ્રામ/લી. પાણીમાં ભેળવી છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Mancozeb 75% WP @ 2.5 g/L or Propineb 70% WP @ 2 g/L.",
            "hi": "मैनकोजेब 75% WP 2.5 ग्राम/ली या प्रोपिनेब 70% WP 2 ग्राम/ली का छिड़काव करें।",
            "gu": "મેન્કોઝેબ ૭૫% WP ૨.૫ ગ્રામ/લી. અથવા પ્રોપીનેબ ૭૦% WP ૨ ગ્રામ/લી. છાંટવું."
        },
        "precautions": {
            "en": "Ensure proper irrigation to avoid plant stress. Spray before flowering and tuber initiation.",
            "hi": "पौधे पर तनाव न आने दें, समय पर हल्की सिंचाई करें। कंद बनने से पहले छिड़काव करें।",
            "gu": "છોડને તણાવ ન આવે તે માટે નિયમિત પિયત આપવું. ગાંઠ બનવા સમયે ખાસ કાળજી રાખવી."
        },
        "preventive_measures": {
            "en": "Use certified seed tubers. Practice 2-year rotation with cereals (wheat, maize).",
            "hi": "प्रमाणित बीज कंदों का ही प्रयोग करें। गेहूं या मक्का के साथ फसल चक्र अपनाएं।",
            "gu": "પ્રમાણિત બિયારણ વાપરવું. ઘઉં કે મકાઈ સાથે પાક ફેરબદલી કરવી."
        }
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "disease_en": "Potato Late Blight (Phytophthora infestans)",
        "disease_hi": "आलू पछेती झुलसा",
        "disease_gu": "બટાટાનો પાછોતરો સુકારો",
        "symptoms": {
            "en": "Dark brown water-soaked lesions that spread very fast across foliage. Decaying smell in field.",
            "hi": "पत्तियों और तनों पर तेजी से फैलने वाले काले-भूरे धब्बे। खेत में सड़ांध जैसी गंध।",
            "gu": "પાન અને ડાળીઓ પર ઝડપથી ફેલાતા કાળા-કથ્થઈ ડાઘા. ખેતરમાં સડો લાગવાની વાસ આવે છે."
        },
        "biological_control": {
            "en": "Spray Trichoderma harzianum @ 5 g/L preventatively before fog season.",
            "hi": "कोहरा शुरू होने से पहले ट्राइकोडर्मा हरज़ियानम 5 ग्राम/ली का छिड़काव करें।",
            "gu": "ઝાકળની ઋતુ શરૂ થતાં પહેલાં ટ્રાઈકોડર્મા હાર્ઝિયાનમ ૫ ગ્રામ/લી. છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Metalaxyl 8% + Mancozeb 64% WP @ 2.5 g/L or Fenamidone 10% + Mancozeb 50% WG @ 2 g/L.",
            "hi": "मेटालेक्सिल + मैनकोजेब (2.5 ग्राम/ली) या फेनामिडोन + मैनकोजेब (2 ग्राम/ली) का छिड़काव करें।",
            "gu": "મેટાલક્ષિલ + મેન્કોઝેબ (૨.૫ ગ્રામ/લી.) અથવા ફેનામિડોન + મેન્કોઝેબ (૨ ગ્રામ/લી.) તાત્કાલિક છાંટવું."
        },
        "precautions": {
            "en": "Cut and destroy potato haulms (stems) 10 days before harvest if late blight occurs on foliage to protect tubers.",
            "hi": "यदि पत्तियों पर रोग दिखे तो कंदों को बचाने के लिए खुदाई से 10 दिन पूर्व तनों को काट दें।",
            "gu": "જો પાન પર રોગ દેખાય તો બટાટા બચાવવા ખોદકામના ૧૦ દિવસ પહેલાં વેલા કાપી નાખવા."
        },
        "preventive_measures": {
            "en": "Treat seed tubers with Mancozeb (2 g/L) before planting. Earth up properly to cover developing tubers.",
            "hi": "बुवाई से पहले बीज कंदों को मैनकोजेब (2 ग्राम/ली) से उपचारित करें। कंदों पर अच्छी तरह मिट्टी चढ़ाएं।",
            "gu": "વાવણી પહેલાં બિયારણને મેન્કોઝેબ (૨ ગ્રામ/લી.) નો પટ આપવો. છોડ ફરતે પૂરતી માટી ચઢાવવી."
        }
    },
    "Potato___healthy": {
        "crop": "Potato",
        "disease_en": "Healthy Potato Crop",
        "disease_hi": "स्वस्थ आलू की फसल",
        "disease_gu": "તંદુરસ્ત બટાટાનો પાક",
        "symptoms": {
            "en": "Lush green foliage without blights or leaf roll symptoms. Sturdy stems and uniform vigor.",
            "hi": "पत्तियां पूरी तरह हरी और स्वस्थ हैं। झुलसा या मरोड़ के कोई लक्षण नहीं हैं।",
            "gu": "બટાટાના પાન એકદમ સ્વસ્થ અને લીલાંછમ છે. કોઈ સુકારો કે કોકડવાટ નથી."
        },
        "biological_control": {
            "en": "Continue routine Trichoderma application with farmyard manure during earthing up.",
            "hi": "मिट्टी चढ़ाते समय गोबर की खाद के साथ ट्राइकोडर्मा का प्रयोग करें।",
            "gu": "માટી ચઢાવતી વખતે છાણિયા ખાતર સાથે ટ્રાઈકોડર્મા જમીનમાં આપવું."
        },
        "chemical_control": {
            "en": "No chemical application needed. Monitor weather conditions for temperature drops below 18°C.",
            "hi": "रासायनिक दवा की आवश्यकता नहीं है। मौसम के तापमान पर नजर रखें।",
            "gu": "રાસાયણિક દવાની જરૂર નથી. વાતાવરણમાં ઠંડી અને ઝાકળ પર ધ્યાન રાખવું."
        },
        "precautions": {
            "en": "Avoid excess irrigation which may create waterlogging favorable for soil rot.",
            "hi": "अत्यधिक सिंचाई न करें जिससे जलभराव न हो।",
            "gu": "વધારે પડતું પાણી ન આપવું જેથી ગાંઠ સડવાનો ભય ન રહે."
        },
        "preventive_measures": {
            "en": "Ensure proper ridging to prevent tuber greening by sun exposure.",
            "hi": "कंदों पर अच्छी तरह मिट्टी चढ़ाकर रखें ताकि वे धूप से हरे न हों।",
            "gu": "બટાટા બહાર ન દેખાય તે રીતે પૂરતી માટી ચઢાવવી જેથી તડકાથી લીલા ન પડે."
        }
    },

    # ------------------ BELL PEPPER / CHILLI (2 CLASSES) ------------------
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Pepper, bell",
        "disease_en": "Bacterial Spot (Xanthomonas)",
        "disease_hi": "जीवाणु धब्बा रोग",
        "disease_gu": "મરચીનો જીવાણુ ડાઘા રોગ",
        "symptoms": {
            "en": "Small circular brown spots with translucent margins on chilli/bell pepper leaves.",
            "hi": "मिर्च की पत्तियों पर छोटे भूरे धब्बे, पत्तियां पीली होकर गिरने लगती हैं।",
            "gu": "મરચીના પાન પર નાના કથ્થઈ ડાઘા અને પાન પીળા પડી ખરી પડે છે."
        },
        "biological_control": {
            "en": "Foliar spray with Pseudomonas fluorescens @ 5 g/L.",
            "hi": "स्यूडोमोनास फ्लोरेसेंस 5 ग्राम प्रति लीटर का छिड़काव करें।",
            "gu": "સ્યુડોમોનાસ ૫ ગ્રામ/લીટર મુજબ છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Copper Hydroxide 77% WP @ 2 g/L + Streptocycline 1 g per 10 L water.",
            "hi": "कॉपर हाइड्रॉक्साइड 77% WP (2 ग्राम/ली) + स्ट्रेप्टोसाइक्लिन (1 ग्राम/10 ली) छिड़कें।",
            "gu": "કોપર હાઈડ્રોક્સાઈડ (૨ ગ્રામ/લી.) + સ્ટ્રેપ્ટોસાઈક્લીન (૧ ગ્રામ પ્રતિ ૧૦ લીટર) છાંટવું."
        },
        "precautions": {
            "en": "Avoid sprinkler irrigation. Prune infected lower leaves in dry weather.",
            "hi": "फव्वारा सिंचाई से बचें। सूखे मौसम में रोगग्रस्त पत्तियां काट दें।",
            "gu": "ફુવારા પિયત ન આપવું. સૂકા વાતાવરણમાં નીચેના રોગિષ્ટ પાન દૂર કરવા."
        },
        "preventive_measures": {
            "en": "Treat seed with hot water or Thiram 75% WP @ 3 g/kg before sowing.",
            "hi": "बुवाई पूर्व बीजों को थायरम (3 ग्राम/किग्रा) से उपचारित करें।",
            "gu": "વાવણી પહેલાં થાયરમ (૩ ગ્રામ/કિલો) નો પટ આપવો."
        }
    },
    "Pepper,_bell___healthy": {
        "crop": "Pepper, bell",
        "disease_en": "Healthy Bell Pepper Foliage",
        "disease_hi": "स्वस्थ शिमला मिर्च की पत्ती",
        "disease_gu": "તંદુરસ્ત શિમલા મરચાં / મરચી",
        "symptoms": {
            "en": "Deep dark green glossy leaves, healthy shoot growth without mosaic or leaf spots.",
            "hi": "गहरी हरी चमकदार पत्तियां, कोई धब्बा या मरोड़िया नहीं।",
            "gu": "ચમકદાર ઘાટા લીલા પાન, કોઈ કોકડવાટ કે ડાઘા નથી."
        },
        "biological_control": {
            "en": "Apply Neem oil (1500 ppm) @ 3 ml/L preventatively to repel thrips and mites.",
            "hi": "थ्रिप्स व माइट से बचाव के लिए नीम तेल (1500 ppm) 3 मिली/ली का नियमित छिड़काव करें।",
            "gu": "થ્રીપ્સ અને કથીરીથી રક્ષણ માટે લીંબોળીના તેલનો નિયમિત છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "No chemical pesticide required.",
            "hi": "रासायनिक दवा की आवश्यकता नहीं है।",
            "gu": "રાસાયણિક દવાની જરૂર નથી."
        },
        "precautions": {
            "en": "Monitor blue/yellow sticky traps for thrips and whiteflies.",
            "hi": "नीले और पीले चिपचिपे कार्ड लगाकर कीटों पर नजर रखें।",
            "gu": "વાદળી અને પીળા સ્ટીકી ટ્રેપ લગાવી જીવાત પર નજર રાખવી."
        },
        "preventive_measures": {
            "en": "Maintain regular watering to avoid flower drop.",
            "hi": "नियमित हल्की सिंचाई करें ताकि फूल न गिरें।",
            "gu": "નિયમિત હળવું પિયત આપવું જેથી ફૂલ ખરી ન પડે."
        }
    },

    # ------------------ CORN / MAIZE (4 CLASSES) ------------------
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (maize)",
        "disease_en": "Common Rust (Puccinia sorghi)",
        "disease_hi": "मक्का का सामान्य रतुआ / गेरुआ",
        "disease_gu": "મકાઈનો ગેરુ રોગ",
        "symptoms": {
            "en": "Golden-brown to cinnamon-brown powdery pustules on both upper and lower leaf surfaces.",
            "hi": "पत्तियों की दोनों सतहों पर सुनहरे-भूरे रंग के दानेदार उभरे हुए फफोले।",
            "gu": "પાનની બંને બાજુ કથ્થઈ રંગના ગેરુ જેવા પાવડરવાળા ફોલ્લા."
        },
        "biological_control": {
            "en": "Spray Bacillus subtilis @ 5 g/L or plant extracts of neem.",
            "hi": "बैसिलस सबटिलिस 5 ग्राम/ली या नीम अर्क का छिड़काव करें।",
            "gu": "બેસિલસ સબટીલીસ ૫ ગ્રામ/લીટર અથવા લીંબોળી અર્કનો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "Spray Azoxystrobin 23% SC @ 1 ml/L or Mancozeb 75% WP @ 2.5 g/L.",
            "hi": "एज़ोक्सीस्ट्रोबिन 23% SC (1 मिली/ली) या मैनकोजेब 75% WP (2.5 ग्राम/ली) का छिड़काव करें।",
            "gu": "એઝોક્સીસ્ટ્રોબિન (૧ મિ.લી./લી.) અથવા મેન્કોઝેબ ૭૫% WP (૨.૫ ગ્રામ/લી.) છાંટવું."
        },
        "precautions": {
            "en": "Spray when pustules first appear, especially in cool, moist weather.",
            "hi": "फफोले दिखते ही छिड़काव करें, विशेष रूप से ठंडे और नम मौसम में।",
            "gu": "ગેરુના ટપકાં દેખાય કે તરત જ છંટકાવ કરવો."
        },
        "preventive_measures": {
            "en": "Plant resistant hybrid maize varieties. Destroy crop residue after harvest.",
            "hi": "रोग प्रतिरोधी संकर मक्का किस्में लगाएं। कटाई बाद अवशेष नष्ट करें।",
            "gu": "રોગ પ્રતિકારક હાઇબ્રિડ જાતો વાવવી. કાપણી બાદ જડિયા બાળી કે દાટી દેવા."
        }
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (maize)",
        "disease_en": "Northern Corn Leaf Blight (Exserohilum turcicum)",
        "disease_hi": "उत्तरी मक्का पत्ती झुलसा",
        "disease_gu": "મકાઈનો મોટો સુકારો (નોર્ધન લીફ બ્લાઇટ)",
        "symptoms": {
            "en": "Long elliptical grayish-green or tan lesions (cigar-shaped) up to 15 cm long on leaves.",
            "hi": "पत्तियों पर सिगार के आकार के लंबे (15 सेमी तक) धूसर-हरे या कत्थई धब्बे।",
            "gu": "પાન પર સિગાર જેવા લાંબા (૧૫ સે.મી. સુધીના) રાખોડી-કથ્થઈ પટ્ટા."
        },
        "biological_control": {
            "en": "Foliar spray with Trichoderma viride @ 5 g/L with cow urine.",
            "hi": "ट्राइकोडर्मा विरिडी 5 ग्राम/ली का गोमूत्र के साथ छिड़काव करें।",
            "gu": "ટ્રાઈકોડર્મા ૫ ગ્રામ/લી. અને ગૌમૂત્ર મિશ્રિત છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "Spray Mancozeb 75% WP @ 2.5 g/L or Pyraclostrobin 20% WG @ 1 g/L.",
            "hi": "मैनकोजेब 75% WP (2.5 ग्राम/ली) या पायराक्लोस्ट्रोबिन (1 ग्राम/ली) छिड़कें।",
            "gu": "મેન્કોઝેબ (૨.૫ ગ્રામ/લી.) અથવા પાયરાક્લોસ્ટ્રોબિન (૧ ગ્રામ/લી.) છાંટવું."
        },
        "precautions": {
            "en": "Apply treatment before silking stage to protect upper canopy leaves.",
            "hi": "भुट्टे के बाल (सिल्क) निकलने से पहले छिड़काव करें ताकि ऊपरी पत्तियां सुरक्षित रहें।",
            "gu": "મકાઈના ડોડામાં મૂછો બેસતા પહેલાં છંટકાવ કરવો જેથી ઉપલા પાન બચે."
        },
        "preventive_measures": {
            "en": "Rotate crops with legumes (gram/soybean) for 1-2 years.",
            "hi": "दलहनी फसलों (चना/सोयाबीन) के साथ फसल चक्र अपनाएं।",
            "gu": "કઠોળ વર્ગના પાકો (ચણા/સોયાબીન) સાથે પાક ફેરબદલી કરવી."
        }
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn (maize)",
        "disease_en": "Gray Leaf Spot (Cercospora zeae-maydis)",
        "disease_hi": "ग्रे लीफ स्पॉट (सर्कोस्पोरा)",
        "disease_gu": "ગ્રે લીફ સ્પોટ (રાખોડી ટપકાં)",
        "symptoms": {
            "en": "Rectangular, brown to gray spots restricted by parallel leaf veins.",
            "hi": "पत्तियों की नसों के बीच आयताकार कत्थई से धूसर धब्बे।",
            "gu": "પાનની નસો વચ્ચે લંબચોરસ રાખોડી-કથ્થઈ ડાઘા."
        },
        "biological_control": {
            "en": "Spray bio-fungicide Pseudomonas @ 5 g/L.",
            "hi": "स्यूडोमोनास 5 ग्राम/ली का छिड़काव करें।",
            "gu": "સ્યુડોમોનાસ ૫ ગ્રામ/લી. છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Propiconazole 25% EC @ 1 ml/L or Azoxystrobin @ 1 ml/L.",
            "hi": "प्रोपिकोनाज़ोल 25% EC (1 मिली/ली) का छिड़काव करें।",
            "gu": "પ્રોપીકોનાઝોલ ૨૫% EC (૧ મિ.લી./લી.) છાંટવું."
        },
        "precautions": {
            "en": "Treat early when bottom leaves show first symptoms.",
            "hi": "निचली पत्तियों पर लक्षण दिखते ही उपचार करें।",
            "gu": "નીચેના પાન પર લક્ષણો દેખાય કે તરત દવા છાંટવી."
        },
        "preventive_measures": {
            "en": "Plow under old stalks after harvest to bury fungal inocula.",
            "hi": "कटाई के बाद खेत की गहरी जुताई करें।",
            "gu": "કાપણી બાદ ખેડ કરી અવશેષો દાટી દેવા."
        }
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (maize)",
        "disease_en": "Healthy Maize Crop",
        "disease_hi": "स्वस्थ मक्का की फसल",
        "disease_gu": "તંદુરસ્ત મકાઈનો પાક",
        "symptoms": {
            "en": "Broad, vibrant green leaves without rust pustules or necrotic streaks.",
            "hi": "पत्तियां पूरी तरह हरी और चौड़ी हैं, कोई रतुआ या धब्बा नहीं है।",
            "gu": "પહોળાં લીલાંછમ પાન, કોઈ ગેરુ કે સુકારો નથી."
        },
        "biological_control": {
            "en": "Apply Azotobacter and PSB bio-fertilizers during sowing and weeding.",
            "hi": "एज़ोटोबैक्टर और पीएसबी जैव उर्वरक का प्रयोग करें।",
            "gu": "એઝોટોબેક્ટર અને પીએસબી જૈવિક ખાતર આપવું."
        },
        "chemical_control": {
            "en": "No chemical application necessary.",
            "hi": "रासायनिक दवा की आवश्यकता नहीं है।",
            "gu": "રાસાયણિક દવાની જરૂર નથી."
        },
        "precautions": {
            "en": "Monitor for Fall Armyworm larvae in the central whorl.",
            "hi": "फॉल आर्मीवर्म (सैनिक कीट) के लिए पौधे के बीच की गोफ पर नजर रखें।",
            "gu": "લશ્કરી ઈયળ (ફોલ આર્મીવોર્મ) માટે મકાઈની પોંગ પર નજર રાખવી."
        },
        "preventive_measures": {
            "en": "Apply split nitrogen doses at knee-high and tasseling stages.",
            "hi": "घुटने तक ऊंचाई और भुट्टे निकलने के समय यूरिया दें।",
            "gu": "ગોઠણ જેવડી મકાઈ થાય ત્યારે અને ડોડો નીકળતી વખતે નાઈટ્રોજન ખાતર આપવું."
        }
    },

    # ------------------ GRAPE (4 CLASSES) ------------------
    "Grape___Black_rot": {
        "crop": "Grape",
        "disease_en": "Grape Black Rot (Guignardia bidwellii)",
        "disease_hi": "अंगूर का ब्लैक रॉट (काला सड़न)",
        "disease_gu": "દ્રાક્ષનો કાળો સડો (બ્લેક રોટ)",
        "symptoms": {
            "en": "Circular tan spots with dark brown borders on leaves. Berries shrivel into hard black mummies.",
            "hi": "पत्तियों पर भूरे धब्बे और अंगूर के दाने काले पड़कर सिकुड़ जाते हैं।",
            "gu": "પાન પર કથ્થઈ ડાઘા અને દ્રાક્ષના દાણા કાળા પડી સુકાઈને સંકોચાઈ જાય છે."
        },
        "biological_control": {
            "en": "Apply copper-based bio-fungicides or Ampelomyces quisqualis.",
            "hi": "कॉपर आधारित जैव कवकनाशी का छिड़काव करें।",
            "gu": "કોપર આધારિત જૈવિક ફૂગનાશકનો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "Spray Myclobutanil 10% WP @ 1 g/L or Kresoxim-methyl 44.3% SC @ 0.7 ml/L.",
            "hi": "माइक्लोब्यूटानिल 10% WP (1 ग्राम/ली) या क्रेसोक्सिम-मिथाइल (0.7 मिली/ली) का छिड़काव करें।",
            "gu": "માયક્લોબ્યુટાનીલ ૧૦% WP (૧ ગ્રામ/લી.) અથવા ક્રેસોક્સીમ મિથાઈલ (૦.૭ મિ.લી./લી.) છાંટવું."
        },
        "precautions": {
            "en": "Remove all mummified berries from the vines during winter pruning.",
            "hi": "छंटाई के समय सूखे और सड़े हुए अंगूरों के गुच्छों को बेल से हटाकर नष्ट करें।",
            "gu": "શિયાળુ છાંટણી વખતે સુકાયેલા રોગિષ્ટ દાણા અને ઝૂમખાં દૂર કરી બાળી નાખવા."
        },
        "preventive_measures": {
            "en": "Prune grapevines to allow sunlight and airflow through the canopy.",
            "hi": "बेलों की छंटाई ऐसी करें जिससे धूप और हवा अंदर तक पहुंच सके।",
            "gu": "દ્રાક્ષના માંડવામાં સૂર્યપ્રકાશ અને હવા ઉજાસ જળવાય તે રીતે છાંટણી કરવી."
        }
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape",
        "disease_en": "Esca (Black Measles / Trunk Disease)",
        "disease_hi": "अंगूर का एस्का (ब्लैक मीसल्स)",
        "disease_gu": "દ્રાક્ષનો એસ્કા (કાળા ડાઘાનો થડ રોગ)",
        "symptoms": {
            "en": "'Tiger-stripe' leaf pattern with yellow/brown necrotic areas between veins. Berries show dark speckled spots.",
            "hi": "पत्तियों पर 'बाघ की धारियों' जैसे पीले-कत्थई धब्बे। फलों पर काले चकत्ते।",
            "gu": "પાન પર વાઘના પટ્ટા જેવા પીળા-કથ્થઈ ડાઘા અને દ્રાક્ષના દાણા પર કાળા ટપકાં."
        },
        "biological_control": {
            "en": "Apply Trichoderma paste to pruning wounds immediately.",
            "hi": "छंटाई के तुरंत बाद कटे हुए भागों पर ट्राइकोडर्मा का लेप लगाएं।",
            "gu": "છાંટણી પછી તરત જ ડાળીઓના કાપેલા ભાગ પર ટ્રાઈકોડર્મા પેસ્ટ લગાવવી."
        },
        "chemical_control": {
            "en": "Paint pruning cuts with copper oxychloride paste or seal with wound sealant.",
            "hi": "छंटाई वाले घावों पर कॉपर ऑक्सीक्लोराइड का गाढ़ा लेप लगाएं।",
            "gu": "છાંટણી કરેલા ઘા પર કોપર ઓક્સીક્લોરાઇડનો લેપ કરવો."
        },
        "precautions": {
            "en": "Do not prune during wet rainy weather to prevent fungal entry.",
            "hi": "बारिश या अत्यधिक नमी के समय छंटाई न करें।",
            "gu": "ભેજવાળા વરસાદી વાતાવરણમાં છાંટણી ન કરવી."
        },
        "preventive_measures": {
            "en": "Disinfect pruning shears with 70% alcohol or bleach between each vine.",
            "hi": "प्रत्येक बेल के बाद कैंची को एल्कोहल या ब्लीच से साफ करें।",
            "gu": "દરેક વેલા પછી છાંટણીના કાતર-ઓજાર આલ્કોહોલથી સેનિટાઇઝ કરવા."
        }
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape",
        "disease_en": "Isariopsis Leaf Spot / Leaf Blight",
        "disease_hi": "पत्ती झुलसा (इसारिओप्सिस)",
        "disease_gu": "પાનનો સુકારો (ઇસારિઓપ્સીસ)",
        "symptoms": {
            "en": "Irregular dark brown lesions with indistinct edges, causing early leaf drop.",
            "hi": "पत्तियों पर अनियमित गहरे भूरे धब्बे, पत्तियां समय से पहले गिरती हैं।",
            "gu": "પાન પર અનિયમિત ઘાટા કથ્થઈ ડાઘા, પાન અકાળે ખરી પડે છે."
        },
        "biological_control": {
            "en": "Spray Neem seed kernel extract (NSKE 5%) or bio-agents.",
            "hi": "5% नीम अर्क या जैव नियंत्रक का छिड़काव करें।",
            "gu": "૫% લીંબોળી અર્ક અથવા જૈવિક ફૂગનાશક છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Mancozeb 75% WP @ 2.5 g/L or Carbendazim 50% WP @ 1 g/L.",
            "hi": "मैनकोजेब (2.5 ग्राम/ली) या कार्बेन्डाजिम (1 ग्राम/ली) का छिड़काव करें।",
            "gu": "મેન્કોઝેબ (૨.૫ ગ્રામ/લી.) અથવા કાર્બેન્ડાઝીમ (૧ ગ્રામ/લી.) છાંટવું."
        },
        "precautions": {
            "en": "Ensure proper spray coverage on both sides of foliage.",
            "hi": "पत्तियों की दोनों सतहों पर अच्छी तरह दवा पहुंचाएं।",
            "gu": "પાનની ઉપર અને નીચે બંને બાજુ પૂરતો છંટકાવ પહોંચાડવો."
        },
        "preventive_measures": {
            "en": "Maintain balanced potassium nutrition to strengthen leaf epidermis.",
            "hi": "पोटाश युक्त खाद देकर पत्तियों को मजबूत बनाएं।",
            "gu": "પોટાશ ખાતર આપી પાનની જાડાઈ અને પ્રતિકારક શક્તિ વધારવી."
        }
    },
    "Grape___healthy": {
        "crop": "Grape",
        "disease_en": "Healthy Grapevine",
        "disease_hi": "स्वस्थ अंगूर की बेल",
        "disease_gu": "તંદુરસ્ત દ્રાક્ષનો માંડવો",
        "symptoms": {
            "en": "Vibrant leaves, clear berries without powdery or downy mildew.",
            "hi": "हरी-भरी पत्तियां और साफ-सुथरे अंगूर के गुच्छे।",
            "gu": "સ્વસ્થ પાન અને કોઈપણ છારી કે ફૂગ વગરના ચોખ્ખા દાણા."
        },
        "biological_control": {
            "en": "Apply micronutrient foliar spray with fermented cow dung slurry.",
            "hi": "जीवामृत या सूक्ष्म पोषक तत्वों का पर्णीय छिड़काव करें।",
            "gu": "જીવામૃત અને સૂક્ષ્મ તત્વોનો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "No synthetic chemical required.",
            "hi": "किसी रासायनिक दवा की जरूरत नहीं है।",
            "gu": "રાસાયણિક દવાની જરૂર નથી."
        },
        "precautions": {
            "en": "Ensure canopy openness for good air circulation.",
            "hi": "बेलों में हवा और धूप के लिए उचित स्थान रखें।",
            "gu": "માંડવામાં હવા-ઉજાસ જળવાઈ રહે તેનું ધ્યાન રાખવું."
        },
        "preventive_measures": {
            "en": "Monitor humidity levels during monsoon or dewy mornings.",
            "hi": "झांक और ओस के दिनों में फफूंद के प्रति सतर्क रहें।",
            "gu": "ઝાકળવાળા દિવસોમાં પાનનું નિયમિત અવલોકન કરવું."
        }
    },

    # ------------------ APPLE (4 CLASSES) ------------------
    "Apple___Apple_scab": {
        "crop": "Apple",
        "disease_en": "Apple Scab (Venturia inaequalis)",
        "disease_hi": "सेब का स्कैब (खुरदरा दाग)",
        "disease_gu": "સફરજનનો સ્કેબ રોગ",
        "symptoms": {
            "en": "Olive-green to velvety brown spots on leaves and corky scabs on fruit.",
            "hi": "पत्तियों पर जैतून जैसे हरे-भूरे धब्बे और फलों पर खुरदरे पपड़ीदार दाग।",
            "gu": "પાન પર કથ્થઈ-લીલા ડાઘા અને ફળ પર ખરબચડા ફોલ્લા."
        },
        "biological_control": {
            "en": "Apply bio-fungicides or urea 5% spray on fallen leaves to accelerate leaf breakdown.",
            "hi": "गिरे पत्तों पर 5% यूरिया का छिड़काव करें ताकि वे जल्दी सड़ जाएं।",
            "gu": "ખરેલા પાન પર ૫% યુરિયા છાંટવું જેથી પાન સડી જાય અને ફૂગ નાશ પામે."
        },
        "chemical_control": {
            "en": "Spray Captan 50% WP @ 2.5 g/L or Difenoconazole 25% EC @ 0.5 ml/L.",
            "hi": "कैप्टान 50% WP (2.5 ग्राम/ली) या डिफेनोकोनाज़ोल (0.5 मिली/ली) छिड़कें।",
            "gu": "કેપ્ટાન (૨.૫ ગ્રામ/લી.) અથવા ડાયફેનોકોનાઝોલ (૦.૫ મિ.લી./લી.) છાંટવું."
        },
        "precautions": {
            "en": "Spray at green tip, pink bud, and petal fall stages.",
            "hi": "कली खिलने और पंखुड़ियां गिरने के समय सुरक्षात्मक छिड़काव करें।",
            "gu": "કળીઓ ફૂટે ત્યારે અને ફૂલ ખરી ગયા પછી તરત સાવચેતીરૂપ છંટકાવ કરવો."
        },
        "preventive_measures": {
            "en": "Rake up and destroy fallen infected leaves in autumn.",
            "hi": "पतझड़ में गिरे हुए रोगी पत्तों को इकट्ठा कर नष्ट करें।",
            "gu": "પાનખરમાં ખરેલા રોગવાળા પાન એકઠા કરી બાળી દેવા."
        }
    },
    "Apple___Black_rot": {
        "crop": "Apple",
        "disease_en": "Apple Black Rot (Botryosphaeria obtusa)",
        "disease_hi": "सेब का ब्लैक रॉट (काला सड़न)",
        "disease_gu": "સફરજનનો કાળો સડો",
        "symptoms": {
            "en": "Frog-eye circular leaf spots (purple border with tan center) and black mummified rotting fruit.",
            "hi": "पत्तियों पर मेंढक की आंख जैसे धब्बे और फलों का काला सड़ना।",
            "gu": "પાન પર ગોળ ડાઘા અને ફળોનો કાળો સડો."
        },
        "biological_control": {
            "en": "Spray Trichoderma @ 5 g/L.",
            "hi": "ट्राइकोडर्मा 5 ग्राम/ली छिड़कें।",
            "gu": "ટ્રાઈકોડર્મા ૫ ગ્રામ/લી. છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Mancozeb 75% WP @ 2.5 g/L or Thiophanate methyl 70% WP @ 1 g/L.",
            "hi": "मैनकोजेब 75% WP (2.5 ग्राम/ली) या थायोफिनेट मिथाइल (1 ग्राम/લી) छिड़कें।",
            "gu": "મેન્કોઝેબ (૨.૫ ગ્રામ/લી.) અથવા થાયોફીનેટ મિથાઈલ (૧ ગ્રામ/લી.) છાંટવું."
        },
        "precautions": {
            "en": "Prune out dead wood, cankers, and mummies during dormancy.",
            "hi": "सुखी शाखाओं और सड़े हुए फलों को तोड़कर नष्ट करें।",
            "gu": "સુકાયેલી ડાળીઓ અને સડેલા ફળ દૂર કરી બાળી દેવા."
        },
        "preventive_measures": {
            "en": "Avoid insect injury to fruit.",
            "hi": "फलों को कीटों के नुकसान से बचाएं।",
            "gu": "જીવાતથી ફળને થતું નુકસાન અટકાવવું."
        }
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "disease_en": "Cedar Apple Rust (Gymnosporangium juniperi-virginianae)",
        "disease_hi": "सेब का रतुआ रोग",
        "disease_gu": "સફરજનનો ગેરુ રોગ",
        "symptoms": {
            "en": "Bright yellow-orange spots on leaves with tube-like spore structures on lower surfaces.",
            "hi": "पत्तियों पर चमकीले पीले-नारंगी धब्बे।",
            "gu": "પાન પર તેજસ્વી પીળા-નારંગી ધબ્બા."
        },
        "biological_control": {
            "en": "Apply neem oil or sulfur-based organic sprays.",
            "hi": "नीम तेल या सल्फर आधारित घोल का छिड़काव करें।",
            "gu": "લીંબોળીનું તેલ અથવા સલ્ફરનો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "Spray Myclobutanil @ 1 g/L or Propiconazole @ 1 ml/L.",
            "hi": "माइक्लोब्यूटानिल या प्रोपिकोनाज़ोल का छिड़काव करें।",
            "gu": "માયક્લોબ્યુટાનીલ અથવા પ્રોપીકોનાઝોલ છાંટવું."
        },
        "precautions": {
            "en": "Remove nearby juniper bushes if possible.",
            "hi": "बगीचे के पास से जूनिपर झाड़ियों को हटाएं।",
            "gu": "બગીચાની આસપાસથી જ્યુનિપર છોડ દૂર કરવા."
        },
        "preventive_measures": {
            "en": "Plant rust-resistant apple rootstocks and cultivars.",
            "hi": "रोग प्रतिरोधी किस्में लगाएं।",
            "gu": "પ્રતિકારક જાતો પસંદ કરવી."
        }
    },
    "Apple___healthy": {
        "crop": "Apple",
        "disease_en": "Healthy Apple Tree",
        "disease_hi": "स्वस्थ सेब का पेड़",
        "disease_gu": "તંદુરસ્ત સફરજનનું ઝાડ",
        "symptoms": {
            "en": "Clean, crisp leaves with normal spur growth and clear fruit surfaces.",
            "hi": "पत्तियां और फल पूरी तरह स्वस्थ और दाग-धब्बे रहित हैं।",
            "gu": "સફરજનના પાન અને ફળ એકદમ સ્વસ્થ અને ડાઘમુક્ત છે."
        },
        "biological_control": {
            "en": "Apply dormant spray of mineral tree spray oil for overwintering pests.",
            "hi": "सर्दियों में ट्री स्प्रे ऑयल का छिड़काव करें।",
            "gu": "શિયાળામાં ટ્રી સ્પ્રે ઓઇલનો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "No synthetic chemical fungicide required.",
            "hi": "रासायनिक दवा की आवश्यकता नहीं है।",
            "gu": "રાસાયણિક દવાની જરૂર નથી."
        },
        "precautions": {
            "en": "Monitor for early sign of mites or aphids.",
            "hi": "माइट और माहू कीट पर नजर रखें।",
            "gu": "મોલોમશી અને કથીરી પર નજર રાખવી."
        },
        "preventive_measures": {
            "en": "Maintain balanced zinc, boron, and calcium foliar nourishment.",
            "hi": "जिंक, बोरॉन और कैल्शियम का संतुलित छिड़काव करें।",
            "gu": "ઝીંક, બોરોન અને કેલ્શિયમનું સંતુલિત પોષણ આપવું."
        }
    },

    # ------------------ ORANGE (1 CLASS) ------------------
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange",
        "disease_en": "Citrus Greening / Huanglongbing (HLB)",
        "disease_hi": "सिट्रस ग्रीनिंग रोग (एचएलबी)",
        "disease_gu": "સાઇટ્રસ ગ્રીનીંગ રોગ (લીંબુ વર્ગનો રોગ)",
        "symptoms": {
            "en": "Asymmetric blotchy yellowing on leaves (crossing leaf veins), stunted shoots, bitter lopsided small fruits.",
            "hi": "पत्तियों पर अनियमित पीलापन, टहनियों का सूखना, फल छोटे, तिरछे और कड़वे होना।",
            "gu": "પાન પર અનિયમિત પીળા ધબ્બા, ડાળીઓ સુકાવી અને ફળો નાના, ખાટા-કડવા અને વાંકાચૂંકા થવા."
        },
        "biological_control": {
            "en": "Spray Neem oil (10,000 ppm) @ 3 ml/L or release predatory parasitic wasp Tamarixia radiata to control psyllid vectors.",
            "hi": "नीम तेल (10,000 ppm) 3 मिली/ली छिड़कें। सिट्रस साइला कीट को नियंत्रित करें।",
            "gu": "૧૦,૦૦૦ ppm લીંબોળીનું તેલ ૩ મિ.લી./લી. મુજબ છાંટવું. સાઇટ્રસ સાયલા જીવાતનું નિયંત્રણ કરવું."
        },
        "chemical_control": {
            "en": "Control citrus psyllid vector: Spray Imidacloprid 17.8% SL @ 0.5 ml/L or Thiamethoxam 25% WG @ 0.3 g/L.",
            "hi": "साइला कीट नियंत्रण हेतु: इमिडाक्लोप्रिड (0.5 मिली/ली) या थायमेथोक्सम (0.3 ग्राम/ली) का छिड़काव करें।",
            "gu": "સાયલા કીટકના નિયંત્રણ માટે ઇમિડાક્લોપ્રિડ (૦.૫ મિ.લી./લી.) અથવા થાયામેથોક્ઝામ (૦.૩ ગ્રામ/લી.) છાંટવું."
        },
        "precautions": {
            "en": "Bacterial disease inside phloem has no direct chemical cure. Severely symptomatic trees must be uprooted.",
            "hi": "यह रोग ठीक नहीं होता, इसलिए गंभीर रूप से रोगी पेड़ों को उखाड़कर नष्ट करना ही एकमात्र उपाय है।",
            "gu": "આ રોગનો કોઈ રાસાયણિક ઈલાજ નથી, તેથી વધારે રોગિષ્ટ ઝાડ ઉપાડી બાળી નાખવા."
        },
        "preventive_measures": {
            "en": "Plant only certified disease-free grafted saplings from accredited government nurseries.",
            "hi": "प्रमाणित सरकारी नर्सरी से ही रोगमुक्त कलमी पौधे खरीदें।",
            "gu": "પ્રમાણિત સરકારી નર્સરીમાંથી જ રોગમુક્ત કલમો લાવી વાવવી."
        }
    },

    # ------------------ OTHER SUPPORTED CROPS ------------------
    "Squash___Powdery_mildew": {
        "crop": "Squash",
        "disease_en": "Powdery Mildew (Podosphaera xanthii)",
        "disease_hi": "चूर्णी फफूंद (पाउडरी मिल्ड्यू)",
        "disease_gu": "છાશિયો રોગ (પાવડરી માઇલ્ડ્યુ)",
        "symptoms": {
            "en": "White powdery fungal talc-like patches on leaves and stems.",
            "hi": "पत्तियों और तनों पर सफेद पाउडर जैसा चूर्ण दिखाई देना।",
            "gu": "પાન અને વેલા પર સફેદ પાઉડર (છાશ) જેવી ફૂગ છવાઈ જવી."
        },
        "biological_control": {
            "en": "Spray sour buttermilk (10%) or cow urine (5%) or Ampelomyces quisqualis.",
            "hi": "खट्टी छाछ (10%) या गोमूत्र (5%) का छिड़काव करें।",
            "gu": "ખાટી છાશ (૧૦%) અથવા ગૌમૂત્ર (૫%) નું દ્રાવણ બનાવી છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Wettable Sulfur 80% WP @ 2.5 g/L or Hexaconazole 5% SC @ 1 ml/L.",
            "hi": "घुलनशील गंधक 80% WP (2.5 ग्राम/ली) या हेक्साकोनाज़ोल (1 मिली/ली) छिड़कें।",
            "gu": "દ્રાવ્ય સલ્ફર ૮૦% WP (૨.૫ ગ્રામ/લી.) અથવા હેક્ઝાકોનાઝોલ (૧ મિ.લી./લી.) છાંટવું."
        },
        "precautions": {
            "en": "Do not apply sulfur when temperatures exceed 32°C to prevent phytotoxicity.",
            "hi": "32°C से अधिक तापमान में गंधक का छिड़काव न करें।",
            "gu": "૩૨ ડિગ્રીથી વધુ તાપમાન હોય ત્યારે સલ્ફર ન છાંટવું."
        },
        "preventive_measures": {
            "en": "Plant in full sunlight with adequate spacing for air movement.",
            "hi": "धूप वाली जगह पर पौधे लगाएं और उचित दूरी रखें।",
            "gu": "પૂરતો તડકો મળે તે જગ્યાએ વાવણી કરવી."
        }
    },
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry",
        "disease_en": "Strawberry Leaf Scorch (Diplocarpon earlianum)",
        "disease_hi": "स्ट्रॉबेरी पत्ती झुलसा",
        "disease_gu": "સ્ટ્રોબેરીનો પાન ઝુલસા રોગ",
        "symptoms": {
            "en": "Purplish-brown irregular blotches on leaves that enlarge and cause foliage to look burnt.",
            "hi": "पत्तियों पर बैंगनी-कत्थई धब्बे जिससे पत्तियां जली हुई दिखाई देती हैं।",
            "gu": "પાન પર જાંબલી-કથ્થઈ ડાઘા જેથી પાન દાઝેલાં જેવા દેખાય છે."
        },
        "biological_control": {
            "en": "Spray bio-fungicides Trichoderma viride @ 5 g/L.",
            "hi": "ट्राइकोडर्मा विरिडी 5 ग्राम/ली का छिड़काव करें।",
            "gu": "ટ્રાઈકોડર્મા ૫ ગ્રામ/લી. છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Captan 50% WP @ 2 g/L or Azoxystrobin @ 1 ml/L.",
            "hi": "कैप्टान 50% WP (2 ग्राम/ली) या एज़ोक्सीस्ट्रोबिन (1 मिली/ली) छिड़कें।",
            "gu": "કેપ્ટાન (૨ ગ્રામ/લી.) અથવા એઝોક્સીસ્ટ્રોબિન (૧ મિ.લી./લી.) છાંટવું."
        },
        "precautions": {
            "en": "Avoid overhead sprinkler irrigation on strawberry beds.",
            "hi": "क्यारियों पर फव्वारे से पानी न दें।",
            "gu": "ફુવારા પિયત પદ્ધતિ ન વાપરવી."
        },
        "preventive_measures": {
            "en": "Remove infected older foliage after harvest.",
            "hi": "तुड़ाई के बाद पुरानी रोगी पत्तियों को हटा दें।",
            "gu": "ફળ વીણ્યા પછી જૂના રોગવાળા પાન દૂર કરવા."
        }
    },
    "Peach___Bacterial_spot": {
        "crop": "Peach",
        "disease_en": "Bacterial Spot (Xanthomonas arboricola)",
        "disease_hi": "आड़ू का जीवाणु धब्बा रोग",
        "disease_gu": "પીચનો જીવાણુ ડાઘા રોગ",
        "symptoms": {
            "en": "Small water-soaked angular spots on leaves that drop out, leaving 'shot-hole' appearance.",
            "hi": "पत्तियों पर छोटे धब्बे जो सूखकर गिर जाते हैं और छलनी जैसे छेद बन जाते हैं।",
            "gu": "પાન પર નાના ડાઘા જે ખરી પડતા પાનમાં ગોળ કાણાં (શોટ-હોલ) દેખાય છે."
        },
        "biological_control": {
            "en": "Foliar spray with Pseudomonas fluorescens @ 5 g/L.",
            "hi": "स्यूडोमोनास 5 ग्राम/ली का छिड़काव करें।",
            "gu": "સ્યુડોમોનાસ ૫ ગ્રામ/લી. છાંટવું."
        },
        "chemical_control": {
            "en": "Spray Copper Oxychloride 50% WP @ 2.5 g/L + Streptocycline (1 g / 10 L water).",
            "hi": "कॉपर ऑक्सीक्लोराइड (2.5 ग्राम/ली) + स्ट्रेप्टोसाइक्लिन (1 ग्राम/10 ली) छिड़कें।",
            "gu": "કોપર ઓક્સીક્લોરાઇડ (૨.૫ ગ્રામ/લી.) + સ્ટ્રેપ્ટોસાઇક્લીન છાંટવું."
        },
        "precautions": {
            "en": "Do not apply heavy copper after fruit set to avoid copper russeting.",
            "hi": "फल बनने के बाद अधिक कॉपर न डालें।",
            "gu": "ફળ બેઠા પછી વધુ કોપર ન વાપરવું."
        },
        "preventive_measures": {
            "en": "Plant resistant cultivars and avoid sandy water-stressed soils.",
            "hi": "रोग प्रतिरोधी किस्में लगाएं।",
            "gu": "પ્રતિકારક જાતો વાવવી."
        }
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry (including sour)",
        "disease_en": "Cherry Powdery Mildew (Podosphaera clandestina)",
        "disease_hi": "चेरी चूर्णी फफूंद",
        "disease_gu": "ચેરીનો છાશિયો રોગ",
        "symptoms": {
            "en": "White powdery fungal growth on leaves and shoots, causing leaf curling and distorted twigs.",
            "hi": "पत्तियों पर सफेद पाउडर जैसी फफूंद, पत्तियां मुड़ जाती हैं।",
            "gu": "પાન પર સફેદ પાવડર જેવી ફૂગ અને પાન વળી જવા."
        },
        "biological_control": {
            "en": "Spray sour buttermilk or neem oil extract.",
            "hi": "खट्टी छाछ या नीम तेल का छिड़काવ करें।",
            "gu": "ખાટી છાશ અથવા લીંબોળીના તેલનો છંટકાવ કરવો."
        },
        "chemical_control": {
            "en": "Spray Myclobutanil 10% WP @ 1 g/L or Wettable Sulfur @ 2 g/L.",
            "hi": "माइक्लोब्यूटानिल या घुलनशील गंधक का छिड़काव करें।",
            "gu": "માયક્લોબ્યુટાનીલ અથવા દ્રાવ્ય સલ્ફર છાંટવું."
        },
        "precautions": {
            "en": "Ensure early spray before petal fall and shuck fall stages.",
            "hi": "पंखुड़ियां गिरने से पहले छिड़काव करें।",
            "gu": "ફૂલ ખરી પડતાં પહેલાં દવા છાંટવી."
        },
        "preventive_measures": {
            "en": "Prune interior branches to increase sunlight.",
            "hi": "धूप अंदर तक आने के लिए छंटाई करें।",
            "gu": "વચ્ચેની ડાળીઓની છાંટણી કરી સૂર્યપ્રકાશ પહોંચાડવો."
        }
    }
}

DEFAULT_HEALTHY_ADVISORY = {
    "symptoms": {
        "en": "Vibrant healthy green foliage with no fungal lesions, chlorosis, necrosis, or pest infestation.",
        "hi": "पत्तियां पूरी तरह हरी-भरी हैं। कोई धब्बा, पीलापन या कीट क्षति नहीं है।",
        "gu": "પાન એકદમ લીલુંછમ અને સ્વસ્થ છે. કોઈ ડાઘા, પીળાશ કે જીવાતનું નુકસાન નથી."
    },
    "biological_control": {
        "en": "Continue regular preventive maintenance with cow dung-urine slurry (Jivamrit) or Trichoderma soil application.",
        "hi": "जीवामृत या ट्राइकोडर्मा का नियमित प्रयोग जारी रखें ताकि रोग प्रतिरोधक क्षमता बनी रहे।",
        "gu": "જીવામૃત, ઘનજીવામૃત અને ટ્રાઈકોડર્માનો નિયમિત વપરાશ ચાલુ રાખવો જેથી પ્રતિકારક શક્તિ જળવાય."
    },
    "chemical_control": {
        "en": "No chemical pesticide or fungicide application is necessary. Save chemical costs and preserve beneficial insects.",
        "hi": "किसी भी रासायनिक कीटनाशक या फफूंदनाशी के प्रयोग की आवश्यकता नहीं है। खर्च बचाएं।",
        "gu": "કોઈપણ રાસાયણિક જંતુનાશક કે ફૂગનાશકની જરૂર નથી. ખર્ચ બચાવો અને મિત્ર કીટકોનું રક્ષણ કરો."
    },
    "precautions": {
        "en": "Regularly inspect the underside of leaves for early signs of sucking pests or fungal spores.",
        "hi": "सप्ताह में एक बार पत्तियों की निचली सतह की जांच अवश्य करें।",
        "gu": "અઠવાડિયામાં એકવાર પાનની નીચેની બાજુ ચૂસિયા જીવાત કે ફૂગ માટે અવલોકન કરવું."
    },
    "preventive_measures": {
        "en": "Maintain balanced NPK nutrition and avoid excess nitrogen fertilization which attracts sucking pests.",
        "hi": "संतुलित उर्वरक दें। अधिक यूरिया का प्रयोग न करें क्योंकि इससे रस चूसक कीट आकर्षित होते हैं।",
        "gu": "સંતુલિત ખાતર આપવું. વધુ પડતા યુરિયાનો ઉપયોગ ટાળવો જેથી ચૂસિયા જીવાતોનો ઉપદ્રવ ન વધે."
    }
}

DEFAULT_DISEASE_ADVISORY = {
    "symptoms": {
        "en": "Foliar discoloration, necrotic spots, or abnormal wilting.",
        "hi": "पत्तियों पर असामान्य धब्बे या पीलापन।",
        "gu": "પાન પર ડાઘા કે અસામાન્ય પીળાશ."
    },
    "biological_control": {
        "en": "Spray Neem seed kernel extract (NSKE 5%) or Trichoderma viride @ 5-10 g/L.",
        "hi": "5% नीम अर्क या ट्राइकोडर्मा विरिडी 5-10 ग्राम/ली का छिड़काव करें।",
        "gu": "૫% લીંબોળીનો અર્ક અથવા ટ્રાઈકોડર્મા વિરીડી ૫-૧૦ ગ્રામ/લીટર પાણીમાં છાંટવું."
    },
    "chemical_control": {
        "en": "Spray broad-spectrum protective fungicide Mancozeb 75% WP @ 2.5 g/L or Copper Oxychloride 50% WP @ 3 g/L.",
        "hi": "सुरक्षात्मक फफूंदनाशी मैनकोजेब 75% WP (2.5 ग्राम/ली) या कॉपर ऑक्सीक्लोराइड 50% WP (3 ग्राम/ली) छिड़कें।",
        "gu": "સાર્વત્રિક ફૂગનાશક મેન્કોઝેબ ૭૫% WP (૨.૫ ગ્રામ/લી.) અથવા કોપર ઓક્સીક્લોરાઇડ ૫૦% WP (૩ ગ્રામ/લી.) છાંટવું."
    },
    "precautions": {
        "en": "Always wear protective gloves and a face mask during spraying. Spray during calm, non-windy morning hours.",
        "hi": "दवा छिड़कते समय दस्ताने और मास्क पहनें। तेज धूप या हवा में छिड़काव न करें।",
        "gu": "છંટકાવ વખતે હાથમોજા અને માસ્ક પહેરવા. પવન કે તડકો ન હોય ત્યારે સવારે છંટકાવ કરવો."
    },
    "preventive_measures": {
        "en": "Collect and burn infected leaves. Avoid excessive overhead irrigation to prevent leaf wetness.",
        "hi": "रोगग्रस्त पत्तियों को इकट्ठा कर जलाएं। खेत में जलभराव न होने दें।",
        "gu": "રોગવાળા પાન એકઠા કરી બાળી દેવા. પાન પર પાણી છંટાય તે રીતે પિયત ન આપવું."
    }
}


def get_crop_localized_name(crop: str, language: str = "en") -> str:
    lang = language.lower()
    if lang not in ["en", "hi", "gu"]:
        lang = "en"
    if crop in CROP_TRANSLATIONS:
        return CROP_TRANSLATIONS[crop].get(lang, crop)
    return crop


def get_disease_treatment(
    raw_class_name: str, 
    detected_crop: Optional[str] = None, 
    is_healthy: Optional[bool] = None, 
    language: str = "en"
) -> Dict[str, Any]:
    """
    Returns verified agronomic treatment guidance localized to English, Hindi, or Gujarati.
    Guarantees that the detected crop is preserved and localized accurately.
    """
    lang = language.lower()
    if lang not in ["en", "hi", "gu"]:
        lang = "en"

    # Infer detected crop if omitted
    if not detected_crop:
        if raw_class_name in TREATMENT_DATABASE:
            detected_crop = TREATMENT_DATABASE[raw_class_name]["crop"]
        else:
            detected_crop = raw_class_name.split("___")[0].replace("_", " ")

    if is_healthy is None:
        is_healthy = "healthy" in raw_class_name.lower()

    # Localize crop name accurately
    crop_display = get_crop_localized_name(detected_crop, lang)

    # 1. Exact match in TREATMENT_DATABASE
    if raw_class_name in TREATMENT_DATABASE:
        data = TREATMENT_DATABASE[raw_class_name]
        disease_name = data.get(f"disease_{lang}", data["disease_en"])
        symptoms = data["symptoms"].get(lang, data["symptoms"]["en"])
        bio = data["biological_control"].get(lang, data["biological_control"]["en"])
        chem = data["chemical_control"].get(lang, data["chemical_control"]["en"])
        prec = data["precautions"].get(lang, data["precautions"]["en"])
        prev = data["preventive_measures"].get(lang, data["preventive_measures"]["en"])
    elif is_healthy or "healthy" in raw_class_name.lower():
        # Crop-specific healthy leaf description
        if lang == "gu":
            disease_name = f"તંદુરસ્ત {crop_display}નું પાન (કોઈ રોગ નથી)"
        elif lang == "hi":
            disease_name = f"स्वस्थ {crop_display} की पत्ती (रोग मुक्त)"
        else:
            disease_name = f"Healthy {detected_crop} Foliage"
        symptoms = DEFAULT_HEALTHY_ADVISORY["symptoms"].get(lang, DEFAULT_HEALTHY_ADVISORY["symptoms"]["en"])
        bio = DEFAULT_HEALTHY_ADVISORY["biological_control"].get(lang, DEFAULT_HEALTHY_ADVISORY["biological_control"]["en"])
        chem = DEFAULT_HEALTHY_ADVISORY["chemical_control"].get(lang, DEFAULT_HEALTHY_ADVISORY["chemical_control"]["en"])
        prec = DEFAULT_HEALTHY_ADVISORY["precautions"].get(lang, DEFAULT_HEALTHY_ADVISORY["precautions"]["en"])
        prev = DEFAULT_HEALTHY_ADVISORY["preventive_measures"].get(lang, DEFAULT_HEALTHY_ADVISORY["preventive_measures"]["en"])
    else:
        # Fallback for remaining diseases: clean the disease raw string nicely
        cleaned = raw_class_name.replace("___", " ").replace("_", " ").strip()
        if cleaned.lower().startswith(detected_crop.lower()):
            cleaned = cleaned[len(detected_crop):].strip()
        disease_name = cleaned.title() if cleaned else "Identified Condition"
        symptoms = DEFAULT_DISEASE_ADVISORY["symptoms"].get(lang, DEFAULT_DISEASE_ADVISORY["symptoms"]["en"])
        bio = DEFAULT_DISEASE_ADVISORY["biological_control"].get(lang, DEFAULT_DISEASE_ADVISORY["biological_control"]["en"])
        chem = DEFAULT_DISEASE_ADVISORY["chemical_control"].get(lang, DEFAULT_DISEASE_ADVISORY["chemical_control"]["en"])
        prec = DEFAULT_DISEASE_ADVISORY["precautions"].get(lang, DEFAULT_DISEASE_ADVISORY["precautions"]["en"])
        prev = DEFAULT_DISEASE_ADVISORY["preventive_measures"].get(lang, DEFAULT_DISEASE_ADVISORY["preventive_measures"]["en"])

    official_contact = {
        "en": "Kisan Call Centre: 1800-180-1551 (Toll Free) | Consult nearest Krishi Vigyan Kendra (KVK)",
        "hi": "किसान कॉल सेंटर: 1800-180-1551 (टोल फ्री) | नजदीकी कृषि विज्ञान केंद्र (KVK) से संपर्क करें",
        "gu": "કિસાન કૉલ સેન્ટર: ૧૮૦૦-૧૮૦-૧૫૫૧ (ટોલ ફ્રી) | નજીકના કૃષિ વિજ્ઞાન કેન્દ્ર (KVK) નો સંપર્ક કરવો"
    }[lang]

    return {
        "crop_name": crop_display,
        "disease_name": disease_name,
        "symptoms": symptoms,
        "biological_control": bio,
        "chemical_control": chem,
        "precautions": prec,
        "preventive_measures": prev,
        "official_contact": official_contact
    }
