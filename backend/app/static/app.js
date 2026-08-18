// AquaFootprint Frontend Application Logic

let currentLang = localStorage.getItem('aquafootprint_lang') || 'en';
let selectedFile = null;

const i18n = {
    en: {
        brand: 'AquaFootprint',
        heroBadge: '💧 Sustainable Water Intelligence',
        heroHeading: 'Discover the Hidden <span class="gradient-text">Water Footprint</span> of Your Food',
        heroDesc: 'Calculate total rainwater, groundwater, and pollution assimilation required to produce agricultural items. Search by name or scan using AI vision.',
        tabSearch: 'Search Product',
        tabScan: 'AI Camera Scan',
        searchPlaceholder: 'Type a food item (e.g., Rice, Coffee, Apple, Chicken, Chocolate)...',
        searchBtn: 'Analyze',
        popular: 'Popular:',
        dropTitle: 'Upload or Take a Photo',
        dropSub: 'Drag & drop product image or click to browse',
        scanBtn: 'Run AI Recognition Scan',
        totalWf: 'Total Water Footprint',
        green: 'Green Water',
        descGreen: 'Rainwater consumed',
        blue: 'Blue Water',
        descBlue: 'Surface & groundwater irrigation',
        grey: 'Grey Water',
        descGrey: 'Freshwater to dilute pollution',
        tipHeading: 'Actionable Sustainability Tip',
        dbTitle: 'Database Catalog (41 Standardized Items)',
        dbSubtitle: 'Click any item to inspect its complete water footprint profile',
        loadingText: 'Retrieving water footprint metrics...',
        notFoundTitle: 'Item Not Found',
        notFoundDesc: 'Could not find water footprint data for this item.',
    },
    hi: {
        brand: 'जल पदचिह्न ट्रैकर',
        heroBadge: '💧 जल स्थिरता एवं विश्लेषण',
        heroHeading: 'अपने भोजन का छिपा हुआ <span class="gradient-text">जल पदचिह्न</span> जानें',
        heroDesc: 'कृषि उत्पादों के उत्पादन में उपयोग किए गए वर्षा जल, भूजल और प्रदूषण जल की गणना करें। नाम से खोजें या एआई कैमरा से स्कैन करें।',
        tabSearch: 'उत्पाद खोजें',
        tabScan: 'एआई कैमरा स्कैन',
        searchPlaceholder: 'खाद्य पदार्थ का नाम लिखें (जैसे चावल, कॉफ़ी, सेब, चिकन, चॉकलेट)...',
        searchBtn: 'विश्लेषण करें',
        popular: 'लोकप्रिय खोजें:',
        dropTitle: 'फ़ोटो अपलोड करें या खींचें',
        dropSub: 'उत्पाद की छवि खींचें और यहाँ छोड़ें या फ़ाइल चुनें',
        scanBtn: 'एआई पहचान व पदचिह्न गणना करें',
        totalWf: 'कुल जल पदचिह्न',
        green: 'हरा जल (वर्षा जल)',
        descGreen: 'उपभोग किया गया वर्षा जल',
        blue: 'नीला जल (भूजल/सतही जल)',
        descBlue: 'सिंचाई में प्रयुक्त भूजल एवं सतही जल',
        grey: 'धूसर जल (प्रदूषण जल)',
        descGrey: 'प्रदूषण को साफ़ करने हेतु आवश्यक जल',
        tipHeading: 'सतत जल संरक्षण सुझाव',
        dbTitle: 'डेटाबेस सूची (41 मानकीकृत उत्पाद)',
        dbSubtitle: 'किसी भी खाद्य वस्तु पर क्लिक करके उसका पूरा विवरण देखें',
        loadingText: 'जल पदचिह्न डेटा प्राप्त किया जा रहा है...',
        notFoundTitle: 'वस्तु नहीं मिली',
        notFoundDesc: 'इस खाद्य वस्तु के लिए डेटाबेस में कोई रिकॉर्ड नहीं मिला।',
    },
    mr: {
        brand: 'पाण्याचा ठसा ट्रॅकर',
        heroBadge: '💧 जल संवर्धन आणि विश्लेषण',
        heroHeading: 'तुमच्या अन्नाचा लपलेला <span class="gradient-text">पाण्याचा ठसा</span> शोधा',
        heroDesc: 'कृषी उत्पादने तयार करण्यासाठी लागणारे पावसाचे पाणी, भूजल आणि प्रदूषण जल मोजा. नावाने शोधा किंवा कॅमेऱ्याने स्कॅन करा.',
        tabSearch: 'अन्नपदार्थ शोधा',
        tabScan: 'कॅमेरा स्कॅन',
        searchPlaceholder: 'अन्नपदार्थाचे नाव लिहा (उदा. तांदूळ, सफरचंद, कॉफी)...',
        searchBtn: 'विश्लेषण करा',
        popular: 'लोकप्रिय:',
        dropTitle: 'फोटो अपलोड करा किंवा काढा',
        dropSub: 'उत्पादनाची प्रतिमा येथे ड्रॅग करा किंवा निवडा',
        scanBtn: 'एआय ओळख आणि पाण्याचा ठसा शोधा',
        totalWf: 'एकूण पाण्याचा ठसा',
        green: 'हिरवे पाणी',
        descGreen: 'पावसाचे पाणी (शेती)',
        blue: 'निळे पाणी',
        descBlue: 'भूजल आणि पृष्ठभागावरील पाणी',
        grey: 'राखाडी पाणी',
        descGrey: 'प्रदूषण सौम्यीकरण',
        tipHeading: 'पर्यावरणपूरक सूचना',
        dbTitle: 'डेटाबेस सूची (41 उत्पादने)',
        dbSubtitle: 'पूर्ण तपशील पाहण्यासाठी कोणत्याही घटकावर क्लिक करा',
        loadingText: 'पाण्याचा ठसा मोजत आहे...',
        notFoundTitle: 'घटक आढळला नाही',
        notFoundDesc: 'या घटकासाठी डेटाबेसमध्ये नोंद आढळली नाही.',
    },
    gu: {
        brand: 'વોટર ફૂટપ્રિન્ટ ટ્રેકર',
        heroBadge: '💧 જળ સંરક્ષણ અને બુદ્ધિમત્તા',
        heroHeading: 'તમારા ખોરાકનો છુપાયેલ <span class="gradient-text">વોટર ફૂટપ્રિન્ટ</span> શોધો',
        heroDesc: 'કૃષિ ઉત્પાદનોના ઉત્પાદન માટે વપરાતા વરસાદી પાણી, ભૂગર્ભજળ અને પ્રદૂષણ પાણીની ગણતરી કરો.',
        tabSearch: 'ખોરાક શોધો',
        tabScan: 'કેમેરા સ્કેન',
        searchPlaceholder: 'ખોરાકનું નામ લખો (દા.ત. ચોખા, સફરજન, દૂધ)...',
        searchBtn: 'વિશ્લેષણ',
        popular: 'લોકપ્રિય:',
        dropTitle: 'ફોટો અપલોડ કરો',
        dropSub: 'છબી અહીં ખેંચો અથવા પસંદ કરો',
        scanBtn: 'ઓળખ અને ગણતરી કરો',
        totalWf: 'કુલ વોટર ફૂટપ્રિન્ટ',
        green: 'લીલું પાણી',
        descGreen: 'વરસાદ આધારિત વપરાશ',
        blue: 'વાદળી પાણી',
        descBlue: 'ભૂગર્ભજળ અને સપાટીનું પાણી',
        grey: 'ગ્રે પાણી',
        descGrey: 'પ્રદૂષણ ઘટાડો પાણી',
        tipHeading: 'પર્યાવરણ ટિપ',
        dbTitle: 'ડેટાબેઝ યાદી (41 વસ્તુઓ)',
        dbSubtitle: 'વિગતવાર માહિતી માટે કોઈપણ વસ્તુ પર ક્લિક કરો',
        loadingText: 'ગણતરી કરી રહ્યાં છીએ...',
        notFoundTitle: 'વસ્તુ મળી નથી',
        notFoundDesc: 'આ વસ્તુ માટે ડેટાબેઝમાં કોઈ રેકોર્ડ મળ્યો નથી.',
    },
    bn: {
        brand: 'পানির পদচিহ্ন ট্র্যাকার',
        heroBadge: '💧 টেকসই পানি বুদ্ধিমত্তা',
        heroHeading: 'আপনার খাদ্যের লুকানো <span class="gradient-text">পানির পদচিহ্ন</span> জানুন',
        heroDesc: 'কৃষি পণ্য উৎপাদনে ব্যবহৃত বৃষ্টির পানি, ভূগর্ভস্থ পানি এবং দূষণ নিবারণ পানির হিসাব করুন।',
        tabSearch: 'খাদ্য অনুসন্ধান',
        tabScan: 'ক্যামেরা স্ক্যান',
        searchPlaceholder: 'খাদ্যদ্রব্যের নাম লিখুন (যেমন চাল, আপেল, কফি)...',
        searchBtn: 'বিশ্লেষণ',
        popular: 'জনপ্রিয়:',
        dropTitle: 'ছবি আপলোড করুন',
        dropSub: 'ছবির ফাইল এখানে ড্রপ করুন বা বেছে নিন',
        scanBtn: 'শনাক্ত ও হিসাব করুন',
        totalWf: 'মোট পানির পদচিহ্ন',
        green: 'সবুজ পানি',
        descGreen: 'ব্যবহৃত বৃষ্টির পানি',
        blue: 'নীল পানি',
        descBlue: 'ভূগর্ভস্থ ও ভূ-পৃষ্ঠের পানি',
        grey: 'ধূসর পানি',
        descGrey: 'দূষণ হ্রাসকরণ পানি',
        tipHeading: 'পরিবেশবান্ধব পরামর্শ',
        dbTitle: 'ডাটাবেজ ক্যাটালগ (৪১টি পণ্য)',
        dbSubtitle: 'সম্পূর্ণ বিবরণ দেখতে যেকোনো পণ্যে ক্লিক করুন',
        loadingText: 'গণনা করা হচ্ছে...',
        notFoundTitle: 'খাদ্য পাওয়া যায়নি',
        notFoundDesc: 'এই খাদ্যদ্রব্যের জন্য কোনো তথ্য পাওয়া যায়নি।',
    },
    ta: {
        brand: 'நீர் தடம் கண்காணிப்பாளர்',
        heroBadge: '💧 நிலையான நீர் நுண்ணறிவு',
        heroHeading: 'உங்கள் உணவின் மறைக்கப்பட்ட <span class="gradient-text">நீர் தடத்தை</span> கண்டறியவும்',
        heroDesc: 'விவசாயப் பொருட்களை உற்பத்தி செய்ய தேவைப்படும் மழைநீர், நிலத்தடி நீர் மற்றும் மாசு நீர்த்தல் அளவை கணக்கிடுங்கள்.',
        tabSearch: 'பொருள் தேடு',
        tabScan: 'கேமரா ஸ்கேன்',
        searchPlaceholder: 'உணவின் பெயரை உள்ளிடவும் (எ.கா. அரிசி, ஆப்பிள், பால்)...',
        searchBtn: 'ஆராய்',
        popular: 'பிரபலமானவை:',
        dropTitle: 'புகைப்படம் பதிவேற்றவும்',
        dropSub: 'படத்தை இங்கே இழுக்கவும் அல்லது தேர்வு செய்யவும்',
        scanBtn: 'அடையாளம் கண்டு கணக்கிடு',
        totalWf: 'மொத்த நீர் தடம்',
        green: 'பச்சை நீர்',
        descGreen: 'மழைநீர் பயன்பாடு',
        blue: 'நீல நீர்',
        descBlue: 'நிலத்தடி மற்றும் மேற்பரப்பு நீர்',
        grey: 'சாம்பல் நீர்',
        descGrey: 'மாசு நீர்த்தல் நீர்',
        tipHeading: 'சுற்றுச்சூழல் குறிப்பு',
        dbTitle: 'தரவுத்தள பட்டியல் (41 பொருட்கள்)',
        dbSubtitle: 'முழு விவரங்களைக் காண ஏதேனும் ஒரு பொருளை கிளிக் செய்யவும்',
        loadingText: 'கணக்கிடப்படுகிறது...',
        notFoundTitle: 'பொருள் கிடைக்கவில்லை',
        notFoundDesc: 'இந்த உணவுப் பொருளுக்கான தரவு எதுவும் கிடைக்கவில்லை.',
    },
    te: {
        brand: 'నీటి పాదముద్ర ట్రాకర్',
        heroBadge: '💧 స్థిరమైన నీటి మేధస్సు',
        heroHeading: 'మీ ఆహారంలో దాగి ఉన్న <span class="gradient-text">నీటి పాదముద్రను</span> కనుగొనండి',
        heroDesc: 'వ్యవసాయ ఉత్పత్తుల తయారీకి అవసరమైన వర్షపు నీరు, భూగర్భ జలాలు మరియు కాలుష్య నీటిని లెక్కించండి.',
        tabSearch: 'ఆహారాన్ని శోధించండి',
        tabScan: 'కెమెరా స్కాన్',
        searchPlaceholder: 'ఆహార పదార్థాన్ని నమోదు చేయండి (ఉదా. వరి, ఆపిల్, పాలు)...',
        searchBtn: 'విశ్లేషించండి',
        popular: 'జనాదరణ పొందినవి:',
        dropTitle: 'ఫోటో అప్‌లోడ్ చేయండి',
        dropSub: 'చిత్రాన్ని ఇక్కడ వేయండి లేదా ఎంచుకోండి',
        scanBtn: 'గుర్తించి లెక్కించండి',
        totalWf: 'మొత్తం నీటి పాదముద్ర',
        green: 'ఆకుపచ్చ నీరు',
        descGreen: 'వర్షపు నీటి వినియోగం',
        blue: 'నీలి నీరు',
        descBlue: 'భూగర్భ మరియు ఉపరితల జలాలు',
        grey: 'బూడిద రంగు నీరు',
        descGrey: 'కాలుష్య తగ్గింపు నీరు',
        tipHeading: 'పర్యావరణ చిట్కా',
        dbTitle: 'డేటాబేస్ జాబితా (41 అంశాలు)',
        dbSubtitle: 'పూర్తి వివరాల కోసం ఏదైనా అంశంపై క్లిక్ చేయండి',
        loadingText: 'లెక్కిస్తోంది...',
        notFoundTitle: 'వస్తువు కనుగొనబడలేదు',
        notFoundDesc: 'ఈ వస్తువుకు సంబంధించిన సమాచారం అందుబాటులో లేదు.',
    },
    kn: {
        brand: 'ನೀರಿನ ಹೆಜ್ಜೆಗುರುತು ಟ್ರ್ಯಾಕರ್',
        heroBadge: '💧 ಸುಸ್ಥಿರ ನೀರಿನ ಬುದ್ಧಿಮತ್ತೆ',
        heroHeading: 'ನಿಮ್ಮ ಆಹಾರದ ಗುಪ್ತ <span class="gradient-text">ನೀರಿನ ಹೆಜ್ಜೆಗುರುತನ್ನು</span> ತಿಳಿಯಿರಿ',
        heroDesc: 'ಕೃಷಿ ಉತ್ಪನ್ನಗಳನ್ನು ಬೆಳೆಯಲು ಅಗತ್ಯವಿರುವ ಮಳೆನೀರು, ಅಂತರ್ಜಲ ಮತ್ತು ಮಾಲಿನ್ಯ ನಿಯಂತ್ರಣ ನೀರನ್ನು ಲೆಕ್ಕಹಾಕಿ.',
        tabSearch: 'ಆಹಾರ ಹುಡುಕಿ',
        tabScan: 'ಕ್ಯಾಮೆರಾ ಸ್ಕ್ಯಾನ್',
        searchPlaceholder: 'ಆಹಾರದ ಹೆಸರನ್ನು ನಮೂದಿಸಿ (ಉದಾ. ಅಕ್ಕಿ, ಸೇಬು, ಹಾಲು)...',
        searchBtn: 'ವಿಶ್ಲೇಷಿಸಿ',
        popular: 'ಜನಪ್ರಿಯ:',
        dropTitle: 'ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        dropSub: 'ಚಿತ್ರವನ್ನು ಇಲ್ಲಿಗೆ ಎಳೆಯಿರಿ ಅಥವಾ ಆರಿಸಿ',
        scanBtn: 'ಗುರುತಿಸಿ ಲೆಕ್ಕಹಾಕಿ',
        totalWf: 'ಒಟ್ಟು ನೀರಿನ ಹೆಜ್ಜೆಗುರುತು',
        green: 'ಹಸಿರು ನೀರು',
        descGreen: 'ಮಳೆನೀರಿನ ಬಳಕೆ',
        blue: 'ನೀಲಿ ನೀರು',
        descBlue: 'ಅಂತರ್ಜಲ ಮತ್ತು ಮೇಲ್ಮೈ ನೀರು',
        grey: 'ಬೂದು ನೀರು',
        descGrey: 'ಮಾಲಿನ್ಯ ನಿಯಂತ್ರಣ ನೀರು',
        tipHeading: 'ಪರಿಸರ ಸಲಹೆ',
        dbTitle: 'ಡೇಟಾಬೇಸ್ ಪಟ್ಟಿ (41 ಐಟಂಗಳು)',
        dbSubtitle: 'ಸಂಪೂರ್ಣ ವಿವರಗಳಿಗಾಗಿ ಯಾವುದೇ ಐಟಂ ಕ್ಲಿಕ್ ಮಾಡಿ',
        loadingText: 'ಲೆಕ್ಕಾಚಾರ ಮಾಡಲಾಗುತ್ತಿದೆ...',
        notFoundTitle: 'ಐಟಂ ಕಂಡುಬಂದಿಲ್ಲ',
        notFoundDesc: 'ಈ ಆಹಾರ ಪದಾರ್ಥಕ್ಕೆ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ.',
    },
    ml: {
        brand: 'വാട്ടർ ഫുട്പ്രിന്റ് ട്രാക്കർ',
        heroBadge: '💧 സുസ്ഥിര ജല വിജ്ഞാനം',
        heroHeading: 'നിങ്ങളുടെ ഭക്ഷണത്തിലെ മറഞ്ഞിരിക്കുന്ന <span class="gradient-text">ജല കാൽപ്പാട്</span> കണ്ടെത്തുക',
        heroDesc: 'കാർഷിക ഉൽപ്പന്നങ്ങൾ ഉൽപ്പാദിപ്പിക്കാൻ ആവശ്യമായ മഴവെള്ളം, ഭൂഗർഭജലം, മലിനീകരണ നിയന്ത്രണ ജലം എന്നിവ കണക്കാക്കുക.',
        tabSearch: 'ഭക്ഷണം തിരയുക',
        tabScan: 'ക്യാമറ സ്കാൻ',
        searchPlaceholder: 'ഭക്ഷണത്തിന്റെ പേര് നൽകുക (ഉദാ. അരി, ആപ്പിൾ, പാൽ)...',
        searchBtn: 'വിശകലനം ചെയ്യുക',
        popular: 'ജനപ്രിയ ഇനങ്ങൾ:',
        dropTitle: 'ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക',
        dropSub: 'ചിത്രം ഇവിടെ ഡ്രോപ്പ് ചെയ്യുക അല്ലെങ്കിൽ തിരഞ്ഞെടുക്കുക',
        scanBtn: 'തിരിച്ചറിഞ്ഞ് കണക്കാക്കുക',
        totalWf: 'ആകെ ജല കാൽപ്പാട്',
        green: 'പച്ച വെള്ളം',
        descGreen: 'മഴവെള്ള ഉപഭോഗം',
        blue: 'നീല ജലം',
        descBlue: 'ഭൂഗർഭജലവും ഉപരിതല ജലവും',
        grey: 'ചാര ജലം',
        descGrey: 'മലിനീകരണ ലഘൂകരണ ജലം',
        tipHeading: 'പരിസ്ഥിതി സൗഹൃദ നിർദ്ദേശം',
        dbTitle: 'ഡാറ്റാബേസ് പട്ടിക (41 ഇനങ്ങൾ)',
        dbSubtitle: 'വിശദാംശങ്ങൾക്ക് ഏതെങ്കിലും ഇനത്തിൽ ക്ലിക്ക് ചെയ്യുക',
        loadingText: 'കണക്കാക്കുന്നു...',
        notFoundTitle: 'ഇനം കണ്ടെത്തിയില്ല',
        notFoundDesc: 'ഈ ഭക്ഷണ സാധനത്തിന് ഡാറ്റ ലഭ്യമല്ല.',
    },
    pa: {
        brand: 'ਵਾਟਰ ਫੁੱਟਪ੍ਰਿੰਟ ਟਰੈਕਰ',
        heroBadge: '💧 ਟਿਕਾਊ ਜਲ ਸੂਝ',
        heroHeading: 'ਆਪਣੇ ਭੋਜਨ ਦਾ ਲੁਕਿਆ ਹੋਇਆ <span class="gradient-text">ਜਲ ਪੈਰ-ਚਿੰਨ੍ਹ</span> ਜਾਣੋ',
        heroDesc: 'ਖੇਤੀਬਾੜੀ ਵਸਤਾਂ ਦੇ ਉਤਪਾਦਨ ਲਈ ਲੋੜੀਂਦੇ ਮੀਂਹ ਦੇ ਪਾਣੀ, ਧਰਤੀ ਹੇਠਲੇ ਪਾਣੀ ਅਤੇ ਪ੍ਰਦੂਸ਼ਣ ਨਿਵਾਰਣ ਪਾਣੀ ਦੀ ਗਣਨਾ ਕਰੋ।',
        tabSearch: 'ਭੋਜਨ ਖੋਜੋ',
        tabScan: 'ਕੈਮਰਾ ਸਕੈਨ',
        searchPlaceholder: 'ਭੋਜਨ ਦਾ ਨਾਂ ਦਰਜ ਕਰੋ (ਜਿਵੇਂ ਚੌਲ, ਸੇਬ, ਦੁੱਧ)...',
        searchBtn: 'ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ',
        popular: 'ਪ੍ਰਸਿੱਧ:',
        dropTitle: 'ਫ਼ੋਟੋ ਅੱਪਲੋਡ ਕਰੋ',
        dropSub: 'ਤਸਵੀਰ ਇੱਥੇ ਖਿੱਚੋ ਜਾਂ ਫ਼ਾਈਲ ਚੁਣੋ',
        scanBtn: 'ਪਛਾਣ ਤੇ ਗਣਨਾ ਕਰੋ',
        totalWf: 'ਕੁੱਲ ਜਲ ਪੈਰ-ਚਿੰਨ੍ਹ',
        green: 'ਹਰਾ ਪਾਣੀ',
        descGreen: 'ਵਰਤਿਆ ਗਿਆ ਮੀਂਹ ਦਾ ਪਾਣੀ',
        blue: 'ਨੀਲਾ ਪਾਣੀ',
        descBlue: 'ਧਰਤੀ ਹੇਠਲਾ ਅਤੇ ਸਤਹੀ ਪਾਣੀ',
        grey: 'ਸਲੇਟੀ ਪਾਣੀ',
        descGrey: 'ਪ੍ਰਦੂਸ਼ਣ ਨਿਵਾਰਣ ਪਾਣੀ',
        tipHeading: 'ਵਾਤਾਵਰਣ ਸੁਝਾਅ',
        dbTitle: 'ਡੇਟਾਬੇਸ ਸੂਚੀ (41 ਵਸਤਾਂ)',
        dbSubtitle: 'ਪੂਰੇ ਵੇਰਵੇ ਦੇਖਣ ਲਈ ਕਿਸੇ ਵੀ ਵਸਤੂ \'ਤੇ ਕਲਿੱਕ ਕਰੋ',
        loadingText: 'ਪੈਰ-ਚਿੰਨ੍ਹ ਗਣਨਾ ਹੋ ਰਹੀ ਹੈ...',
        notFoundTitle: 'ਵਸਤੂ ਨਹੀਂ ਮਿਲੀ',
        notFoundDesc: 'ਇਸ ਭੋਜਨ ਵਸਤੂ ਦਾ ਕੋਈ ਡਾਟਾ ਨਹੀਂ ਮਿਲਿਆ।',
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupLanguageSelector();
    setupDropzone();
    loadDatabaseCatalog();
    checkBackendHealth();

    // Set initial language from storage or default
    setLanguage(currentLang, false);

    // Load default item
    searchItem('rice');
});

async function checkBackendHealth() {
    try {
        const res = await fetch('/health');
        if (res.ok) {
            document.getElementById('status-text').textContent = 'FastAPI Live';
        }
    } catch (e) {
        document.getElementById('status-text').textContent = 'FastAPI Offline';
    }
}

function setupLanguageSelector() {
    const langSelect = document.getElementById('lang-select');
    if (langSelect) {
        langSelect.value = currentLang;
        langSelect.addEventListener('change', (e) => {
            setLanguage(e.target.value, true);
        });
    }
}

function setLanguage(lang, shouldRefresh = true) {
    currentLang = lang;
    try {
        localStorage.setItem('aquafootprint_lang', lang);
    } catch (_) {}

    const langSelect = document.getElementById('lang-select');
    if (langSelect) {
        langSelect.value = lang;
    }

    const t = i18n[lang] || i18n.en;
    if (document.getElementById('brand-title')) document.getElementById('brand-title').innerHTML = t.brand;
    if (document.getElementById('hero-badge')) document.getElementById('hero-badge').innerHTML = t.heroBadge;
    if (document.getElementById('hero-heading')) document.getElementById('hero-heading').innerHTML = t.heroHeading;
    if (document.getElementById('hero-desc')) document.getElementById('hero-desc').innerHTML = t.heroDesc;
    if (document.getElementById('tab-search-label')) document.getElementById('tab-search-label').innerHTML = t.tabSearch;
    if (document.getElementById('tab-scan-label')) document.getElementById('tab-scan-label').innerHTML = t.tabScan;
    if (document.getElementById('search-input')) document.getElementById('search-input').placeholder = t.searchPlaceholder;
    if (document.getElementById('search-btn-text')) document.getElementById('search-btn-text').innerHTML = t.searchBtn;
    if (document.getElementById('popular-label')) document.getElementById('popular-label').innerHTML = t.popular;
    if (document.getElementById('dropzone-title')) document.getElementById('dropzone-title').innerHTML = t.dropTitle;
    if (document.getElementById('dropzone-subtitle')) document.getElementById('dropzone-subtitle').innerHTML = t.dropSub;
    if (document.getElementById('scan-btn-text')) document.getElementById('scan-btn-text').innerHTML = t.scanBtn;
    if (document.getElementById('lbl-total-wf')) document.getElementById('lbl-total-wf').innerHTML = t.totalWf;
    if (document.getElementById('lbl-green')) document.getElementById('lbl-green').innerHTML = t.green;
    if (document.getElementById('desc-green')) document.getElementById('desc-green').innerHTML = t.descGreen;
    if (document.getElementById('lbl-blue')) document.getElementById('lbl-blue').innerHTML = t.blue;
    if (document.getElementById('desc-blue')) document.getElementById('desc-blue').innerHTML = t.descBlue;
    if (document.getElementById('lbl-grey')) document.getElementById('lbl-grey').innerHTML = t.grey;
    if (document.getElementById('desc-grey')) document.getElementById('desc-grey').innerHTML = t.descGrey;
    if (document.getElementById('lbl-tip-heading')) document.getElementById('lbl-tip-heading').innerHTML = t.tipHeading;
    if (document.getElementById('lbl-db-title')) document.getElementById('lbl-db-title').innerHTML = t.dbTitle;
    if (document.getElementById('lbl-db-subtitle')) document.getElementById('lbl-db-subtitle').innerHTML = t.dbSubtitle;

    if (shouldRefresh) {
        const currentQuery = document.getElementById('search-input').value.trim() || 'rice';
        searchItem(currentQuery);
    }
}

function switchTab(mode) {
    const searchTab = document.getElementById('tab-search');
    const scanTab = document.getElementById('tab-scan');
    const searchBtn = document.getElementById('tab-search-btn');
    const scanBtn = document.getElementById('tab-scan-btn');

    if (mode === 'search') {
        searchTab.classList.remove('hidden');
        scanTab.classList.add('hidden');
        searchBtn.classList.add('active');
        scanBtn.classList.remove('active');
    } else {
        searchTab.classList.add('hidden');
        scanTab.classList.remove('hidden');
        searchBtn.classList.remove('active');
        scanBtn.classList.add('active');
    }
}

function triggerFileInput() {
    document.getElementById('file-input').click();
}

function setupDropzone() {
    const dropzone = document.getElementById('dropzone');

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.style.borderColor = 'var(--primary-light)';
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.style.borderColor = 'rgba(56, 189, 248, 0.3)';
        });
    });

    dropzone.addEventListener('drop', async (e) => {
        e.preventDefault();
        
        // Case 1: Local file drag & drop (from File Explorer)
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
            return;
        }

        // Case 2: Dragging an image directly from Google Images or another website
        const urlData = e.dataTransfer.getData('text/uri-list') || e.dataTransfer.getData('text/plain');
        const htmlData = e.dataTransfer.getData('text/html');
        let imageUrl = null;

        if (urlData && (urlData.startsWith('http://') || urlData.startsWith('https://') || urlData.startsWith('data:image/'))) {
            imageUrl = urlData;
        } else if (htmlData) {
            const doc = new DOMParser().parseFromString(htmlData, 'text/html');
            const img = doc.querySelector('img');
            if (img && img.src) {
                imageUrl = img.src;
            }
        }

        if (imageUrl) {
            try {
                showLoading();
                const resp = await fetch(imageUrl);
                const blob = await resp.blob();
                const file = new File([blob], 'google_image.jpg', { type: blob.type || 'image/jpeg' });
                document.getElementById('result-loading').classList.add('hidden');
                document.getElementById('result-placeholder').classList.remove('hidden');
                handleFile(file);
            } catch (err) {
                document.getElementById('result-loading').classList.add('hidden');
                document.getElementById('result-placeholder').classList.remove('hidden');
                alert('Could not download image from the web link directly due to browser CORS policies. Please right-click the image on Google, choose "Save Image As...", and drop the downloaded file.');
            }
        }
    });

    // Case 3: Clipboard paste support (Ctrl + V)
    window.addEventListener('paste', (e) => {
        const items = e.clipboardData && e.clipboardData.items;
        if (!items) return;

        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                const file = items[i].getAsFile();
                if (file) {
                    handleFile(file);
                    break;
                }
            }
        }
    });
}

function handleFileSelected(event) {
    if (event.target.files && event.target.files.length > 0) {
        handleFile(event.target.files[0]);
    }
}

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file (JPEG/PNG).');
        return;
    }

    selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('preview-image').src = e.target.result;
        document.getElementById('dropzone-content').classList.add('hidden');
        document.getElementById('dropzone-preview').classList.remove('hidden');
        document.getElementById('btn-run-scan').disabled = false;
    };
    reader.readAsDataURL(file);
}

function removeFile(event) {
    event.stopPropagation();
    selectedFile = null;
    document.getElementById('file-input').value = '';
    document.getElementById('dropzone-preview').classList.add('hidden');
    document.getElementById('dropzone-content').classList.remove('hidden');
    document.getElementById('btn-run-scan').disabled = true;
}

function selectChip(itemName) {
    document.getElementById('search-input').value = itemName;
    searchItem(itemName);
}

async function handleSearch(event) {
    event.preventDefault();
    const query = document.getElementById('search-input').value.trim();
    if (query) {
        searchItem(query);
    }
}

async function searchItem(itemName) {
    showLoading();

    try {
        const res = await fetch(`/footprint?item=${encodeURIComponent(itemName)}&lang=${currentLang}`);
        if (res.ok) {
            const data = await res.json();
            renderResult(data);
        } else {
            renderNotFound(itemName);
        }
    } catch (error) {
        renderNotFound(itemName);
    }
}

async function runScan() {
    if (!selectedFile) return;

    showLoading();

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const res = await fetch(`/scan?lang=${currentLang}`, {
            method: 'POST',
            body: formData,
        });

        if (res.ok) {
            const data = await res.json();
            if (data.success) {
                renderResult(data);
                // Switch to search tab to view rendered result nicely
                switchTab('search');
            } else {
                renderNotFound(data.suggested_label || 'Unrecognized Image');
            }
        } else {
            renderNotFound('Image Scan');
        }
    } catch (error) {
        renderNotFound('Image Scan');
    }
}

function showLoading() {
    document.getElementById('result-placeholder').classList.add('hidden');
    document.getElementById('result-content').classList.add('hidden');
    document.getElementById('result-notfound').classList.add('hidden');
    document.getElementById('result-loading').classList.remove('hidden');

    const t = i18n[currentLang] || i18n.en;
    document.getElementById('loading-message').textContent = t.loadingText;
}

function renderResult(data) {
    document.getElementById('result-loading').classList.add('hidden');
    document.getElementById('result-placeholder').classList.add('hidden');
    document.getElementById('result-notfound').classList.add('hidden');
    document.getElementById('result-content').classList.remove('hidden');

    // Title & Confidence badge
    document.getElementById('res-item-title').textContent = capitalize(data.item);
    
    const confBadge = document.getElementById('res-conf-badge');
    if (data.confidence !== undefined) {
        confBadge.classList.remove('hidden');
        document.getElementById('res-conf-val').textContent = `${Math.round(data.confidence * 100)}%`;
    } else {
        confBadge.classList.add('hidden');
    }

    // Totals
    const total = Number(data.total_litres_per_kg);
    document.getElementById('res-total-val').textContent = total.toLocaleString();
    document.getElementById('res-total-unit').textContent = data.unit || 'litres/kg';

    // Breakdown values
    const green = Number(data.green_wf || data.green_water_litres || 0);
    const blue = Number(data.blue_wf || data.blue_water_litres || 0);
    const grey = Number(data.grey_wf || data.grey_water_litres || 0);

    document.getElementById('val-green').textContent = `${green.toLocaleString()} L`;
    document.getElementById('val-blue').textContent = `${blue.toLocaleString()} L`;
    document.getElementById('val-grey').textContent = `${grey.toLocaleString()} L`;

    // Percentage bars
    const safeTotal = total > 0 ? total : 1;
    const pctGreen = Math.round((green / safeTotal) * 100);
    const pctBlue = Math.round((blue / safeTotal) * 100);
    const pctGrey = Math.round((grey / safeTotal) * 100);

    document.getElementById('pct-green').textContent = `${pctGreen}%`;
    document.getElementById('pct-blue').textContent = `${pctBlue}%`;
    document.getElementById('pct-grey').textContent = `${pctGrey}%`;

    document.getElementById('bar-green').style.width = `${pctGreen}%`;
    document.getElementById('bar-blue').style.width = `${pctBlue}%`;
    document.getElementById('bar-grey').style.width = `${pctGrey}%`;

    // Comparison benchmark
    document.getElementById('res-comparison-text').textContent = data.comparison || 'Data calculated based on standard agricultural yields.';

    // Sustainability Tip
    document.getElementById('res-tip-text').textContent = data.tip || 'Choosing locally sourced produce significantly reduces overall water stress.';
}

function renderNotFound(item) {
    document.getElementById('result-loading').classList.add('hidden');
    document.getElementById('result-placeholder').classList.add('hidden');
    document.getElementById('result-content').classList.add('hidden');
    document.getElementById('result-notfound').classList.remove('hidden');

    const t = i18n[currentLang] || i18n.en;
    document.getElementById('notfound-title').textContent = `${t.notFoundTitle}: "${item}"`;
    document.getElementById('notfound-desc').textContent = t.notFoundDesc;
}

async function loadDatabaseCatalog() {
    const grid = document.getElementById('catalog-grid');
    if (!grid) return;

    try {
        const res = await fetch('/items');
        if (res.ok) {
            const data = await res.json();
            grid.innerHTML = '';
            
            data.items.forEach(it => {
                const card = document.createElement('div');
                card.className = 'catalog-card';
                card.onclick = () => {
                    document.getElementById('search-input').value = it.item;
                    searchItem(it.item);
                    window.scrollTo({ top: 400, behavior: 'smooth' });
                };

                card.innerHTML = `
                    <div class="catalog-card-header">
                        <span class="catalog-card-name">${capitalize(it.item)}</span>
                        <span class="catalog-card-wf">${Number(it.total_litres_per_kg).toLocaleString()} L/kg</span>
                    </div>
                    <div class="catalog-mini-bar">
                        <div class="mini-bar-green" style="width: ${(it.green_wf / it.total_litres_per_kg) * 100}%"></div>
                        <div class="mini-bar-blue" style="width: ${(it.blue_wf / it.total_litres_per_kg) * 100}%"></div>
                        <div class="mini-bar-grey" style="width: ${(it.grey_wf / it.total_litres_per_kg) * 100}%"></div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }
    } catch (e) {
        console.error('Could not load database catalog', e);
    }
}

function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}
