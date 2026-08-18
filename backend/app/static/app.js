// AquaFootprint Frontend Application Logic

let currentLang = localStorage.getItem('aquafootprint_lang') || 'en';
let selectedFile = null;

const i18n = {
    en: {
        mapTitle: 'Crop Suitability & Water Stress Map',
        mapSubtitle: 'Explore where crops thrive — and where water, soil and climate constraints create agricultural risk.',
        selectCrop: 'Select Crop:',
        layer: 'Layer:',
        cropSuitability: '🌾 Crop Suitability',
        waterStress: '💧 Water Stress',
        compareCrop: '⚔️ Compare Crop',
        mapOverviewTitle: 'India Regional Suitability Overview',
        highlySuitable: '🟢 Highly Suitable',
        moderatelySuitable: '🔵 Moderately Suitable',
        marginalRisky: '🟠 Marginal / Risky',
        unsuitableHighStress: '🔴 Unsuitable / High Stress',
        lowWaterStress: '🟢 Low Water Stress',
        moderateWaterStress: '🔵 Moderate Water Stress',
        highWaterStress: '🟠 High Water Stress',
        severeWaterStress: '🔴 Severe Water Stress',
        waterAvailability: 'Water Availability',
        rainfallSuitability: 'Rainfall Suitability',
        temperatureSuitability: 'Temperature Suitability',
        soilSuitability: 'Soil Suitability',
        irrigationDependency: 'Irrigation Dependency',
        valHigh: 'High',
        valModerate: 'Moderate',
        valLow: 'Low',
        whyCropRisky: '❓ Why is this crop risky / suitable here?',
        potentialRegionalImpact: '🌊 Potential Regional Impact',
        potentialCropImpact: '🌾 Potential Crop Impact',
        betterSuitedAlternatives: '🌱 Better-Suited Alternatives',
        selectRegionEmptyTitle: 'Select a Region on the Map',
        selectRegionEmptySub: 'Click on any Indian state to inspect crop suitability, water availability, sub-metrics, and risk analysis.',
        catalogAccordionLabel: 'View Standardized Footprint Database Catalog (41 Items)',
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
        mapTitle: 'फ़सल उपयुक्तता एवं जल तनाव मानचित्र',
        mapSubtitle: 'जानें कहाँ फ़सलें पनपती हैं — और कहाँ जल, मिट्टी व जलवायु संबंधी जोखिम उत्पन्न होते हैं।',
        selectCrop: 'फ़सल चुनें:',
        layer: 'मानचित्र परत:',
        cropSuitability: '🌾 फ़सल उपयुक्तता',
        waterStress: '💧 जल तनाव',
        compareCrop: '⚔️ तुलना करें',
        mapOverviewTitle: 'भारत क्षेत्रीय उपयुक्तता विवरण',
        highlySuitable: '🟢 अत्यधिक उपयुक्त',
        moderatelySuitable: '🔵 मध्यम उपयुक्त',
        marginalRisky: '🟠 सीमांत / जोखिमपूर्ण',
        unsuitableHighStress: '🔴 अनुपयुक्त / अत्यधिक जल तनाव',
        lowWaterStress: '🟢 कम जल तनाव',
        moderateWaterStress: '🔵 मध्यम जल तनाव',
        highWaterStress: '🟠 उच्च जल तनाव',
        severeWaterStress: '🔴 गंभीर जल तनाव',
        waterAvailability: 'जल उपलब्धता',
        rainfallSuitability: 'वर्षा उपयुक्तता',
        temperatureSuitability: 'तापमान उपयुक्तता',
        soilSuitability: 'मृदा उपयुक्तता',
        irrigationDependency: 'सिंचाई निर्भरता',
        valHigh: 'उच्च',
        valModerate: 'मध्यम',
        valLow: 'निम्न',
        whyCropRisky: '❓ यह फ़सल यहाँ जोखिमपूर्ण / उपयुक्त क्यों है?',
        potentialRegionalImpact: '🌊 संभावित क्षेत्रीय प्रभाव',
        potentialCropImpact: '🌾 संभावित फ़सल प्रभाव',
        betterSuitedAlternatives: '🌱 अधिक उपयुक्त विकल्प',
        selectRegionEmptyTitle: 'मानचित्र पर कोई राज्य चुनें',
        selectRegionEmptySub: 'किसी भी भारतीय राज्य पर क्लिक करके फ़सल उपयुक्तता और जल तनाव का विवरण देखें।',
        catalogAccordionLabel: 'मानकीकृत जल पदचिह्न डेटाबेस सूची (41 उत्पाद)',
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
        mapTitle: 'पिक अनुकूलता आणि जल ताण नकाशा',
        mapSubtitle: 'पिके कुठे उत्तम येतात — आणि कुठे पाणी, माती व हवामानाचे धोके आहेत ते शोधा.',
        selectCrop: 'पिक निवडा:',
        layer: 'नकाशा थर:',
        cropSuitability: '🌾 पिक अनुकूलता',
        waterStress: '💧 जल ताण',
        compareCrop: '⚔️ तुलना करा',
        mapOverviewTitle: 'भारत प्रादेशिक अनुकूलता तपशील',
        highlySuitable: '🟢 अत्यंत अनुकूल',
        moderatelySuitable: '🔵 मध्यम अनुकूल',
        marginalRisky: '🟠 मध्यम / धोकादायक',
        unsuitableHighStress: '🔴 अयोग्य / तीव्र जल ताण',
        lowWaterStress: '🟢 कमी जल ताण',
        moderateWaterStress: '🔵 मध्यम जल ताण',
        highWaterStress: '🟠 जास्त जल ताण',
        severeWaterStress: '🔴 तीव्र जल ताण',
        waterAvailability: 'पाण्याची उपलब्धता',
        rainfallSuitability: 'पावसाची अनुकूलता',
        temperatureSuitability: 'तापमान अनुकूलता',
        soilSuitability: 'मातीची अनुकूलता',
        irrigationDependency: 'सिंचनावर अवलंबित्व',
        valHigh: 'जास्त',
        valModerate: 'मध्यम',
        valLow: 'कमी',
        whyCropRisky: '❓ हे पिक येथे धोक्याचे / योग्य का आहे?',
        potentialRegionalImpact: '🌊 संभाव्य प्रादेशिक परिणाम',
        potentialCropImpact: '🌾 संभाव्य पिकावरील परिणाम',
        betterSuitedAlternatives: '🌱 अधिक योग्य पर्याय',
        selectRegionEmptyTitle: 'नकाशावरील राज्य निवडा',
        selectRegionEmptySub: 'कोणत्याही भारतीय राज्यावर क्लिक करून पिक अनुकूलता व जल ताण विश्लेषण पहा.',
        catalogAccordionLabel: 'मानकीकृत डेटाबेस सूची (41 उत्पादने)',
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
        mapTitle: 'પાક અનુકૂળતા અને જળ તણાવ નકશો',
        mapSubtitle: 'પાક ક્યાં ઉત્તમ થાય છે — અને ક્યાં પાણી, માટી અને આબોહવાના જોખમો છે તે શોધો.',
        selectCrop: 'પાક પસંદ કરો:',
        layer: 'નકશા સ્તર:',
        cropSuitability: '🌾 પાક અનુકૂળતા',
        waterStress: '💧 જળ તણાવ',
        compareCrop: '⚔️ સરખામણી કરો',
        mapOverviewTitle: 'ભારત પ્રાદેશિક અનુકૂળતા વિગત',
        highlySuitable: '🟢 અત્યંત અનુકૂળ',
        moderatelySuitable: '🔵 મધ્યમ અનુકૂળ',
        marginalRisky: '🟠 સીમાંત / જોખમી',
        unsuitableHighStress: '🔴 અયોગ્ય / ઉચ્ચ જળ તણાવ',
        lowWaterStress: '🟢 ઓછું જળ તણાવ',
        moderateWaterStress: '🔵 મધ્યમ જળ તણાવ',
        highWaterStress: '🟠 ઉચ્ચ જળ તણાવ',
        severeWaterStress: '🔴 ગંભીર જળ તણાવ',
        waterAvailability: 'પાણીની ઉપલબ્ધતા',
        rainfallSuitability: 'વરસાદની અનુકૂળતા',
        temperatureSuitability: 'તાપમાનની અનુકૂળતા',
        soilSuitability: 'જમીનની અનુકૂળતા',
        irrigationDependency: 'સિંચાઈ પર નિર્ભરતા',
        valHigh: 'ઉચ્ચ',
        valModerate: 'મધ્યમ',
        valLow: 'ઓછું',
        whyCropRisky: '❓ આ પાક અહીં જોખમી / યોગ્ય શા માટે છે?',
        potentialRegionalImpact: '🌊 સંભવિત પ્રાદેશિક અસર',
        potentialCropImpact: '🌾 સંભવિત પાક અસર',
        betterSuitedAlternatives: '🌱 વધુ અનુકૂળ વિકલ્પો',
        selectRegionEmptyTitle: 'નકશા પર રાજ્ય પસંદ કરો',
        selectRegionEmptySub: 'કોઈપણ ભારતીય રાજ્ય પર ક્લિક કરીને વિગતવાર વિશ્લેષણ જુઓ.',
        catalogAccordionLabel: 'ડેટાબેઝ યાદી (41 વસ્તુઓ)',
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
        mapTitle: 'ফসল উপযোগিতা ও পানি মানসিক চাপ মানচিত্র',
        mapSubtitle: 'কোথায় ফসল ভালো হয় — এবং কোথায় পানি, মাটি ও জলবায়ু ঝুঁকি রয়েছে তা জানুন।',
        selectCrop: 'ফসল নির্বাচন করুন:',
        layer: 'মানচিত্র স্তর:',
        cropSuitability: '🌾 ফসল উপযোগিতা',
        waterStress: '💧 পানি চাপ',
        compareCrop: '⚔️ তুলনা করুন',
        mapOverviewTitle: 'ভারত আঞ্চলিক উপযোগিতা বিবরণ',
        highlySuitable: '🟢 অত্যন্ত উপযুক্ত',
        moderatelySuitable: '🔵 মাঝারি উপযুক্ত',
        marginalRisky: '🟠 সীমান্তবর্তী / ঝুঁকিপূর্ণ',
        unsuitableHighStress: '🔴 অনুপযুক্ত / তীব্র পানি চাপ',
        lowWaterStress: '🟢 কম পানি চাপ',
        moderateWaterStress: '🔵 মাঝারি পানি চাপ',
        highWaterStress: '🟠 উচ্চ পানি চাপ',
        severeWaterStress: '🔴 তীব্র পানি চাপ',
        waterAvailability: 'পানির প্রাপ্যতা',
        rainfallSuitability: 'বৃষ্টিপাত উপযোগিতা',
        temperatureSuitability: 'তাপমাত্রা উপযোগিতা',
        soilSuitability: 'মাটি উপযোগিতা',
        irrigationDependency: 'সেচ নির্ভরতা',
        valHigh: 'উচ্চ',
        valModerate: 'মাঝারি',
        valLow: 'কম',
        whyCropRisky: '❓ কেন এই ফসল এখানে ঝুঁকিপূর্ণ / উপযুক্ত?',
        potentialRegionalImpact: '🌊 সম্ভাব্য আঞ্চলিক প্রভাব',
        potentialCropImpact: '🌾 সম্ভাব্য ফসল প্রভাব',
        betterSuitedAlternatives: '🌱 আরও উপযুক্ত বিকল্প',
        selectRegionEmptyTitle: 'মানচিত্রে একটি রাজ্য নির্বাচন করুন',
        selectRegionEmptySub: 'যেকোনো ভারতীয় রাজ্যে ক্লিক করে বিস্তারিত বিশ্লেষণ দেখুন।',
        catalogAccordionLabel: 'ডাটাবেজ ক্যাটালগ (৪১টি পণ্য)',
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
        mapTitle: 'பயிர் பொருத்தம் மற்றும் நீர் அழுத்த வரைபடம்',
        mapSubtitle: 'பயிர்கள் எங்கு செழித்து வளர்கின்றன — மற்றும் நீர், மண் மற்றும் காலநிலை அபாயங்கள் எங்கு உள்ளன என்பதை ஆராயுங்கள்.',
        selectCrop: 'பயிரைத் தேர்ந்தெடுக்கவும்:',
        layer: 'வரைபட அடுக்கு:',
        cropSuitability: '🌾 பயிர் பொருத்தம்',
        waterStress: '💧 நீர் அழுத்தம்',
        compareCrop: '⚔️ ஒப்பிடுக',
        mapOverviewTitle: 'இந்திய பிராந்திய பொருத்தம் மேலோட்டம்',
        highlySuitable: '🟢 மிகவும் ஏற்றது',
        moderatelySuitable: '🔵 மிதமான ஏற்றது',
        marginalRisky: '🟠 எல்லைக்குட்பட்ட / ஆபத்தானது',
        unsuitableHighStress: '🔴 பொருத்தமற்றது / அதிக நீர் அழுத்தம்',
        lowWaterStress: '🟢 குறைந்த நீர் அழுத்தம்',
        moderateWaterStress: '🔵 மிதமான நீர் அழுத்தம்',
        highWaterStress: '🟠 அதிக நீர் அழுத்தம்',
        severeWaterStress: '🔴 கடுமையான நீர் அழுத்தம்',
        waterAvailability: 'நீர் கிடைக்கும் தன்மை',
        rainfallSuitability: 'மழைப்பொழிவு பொருத்தம்',
        temperatureSuitability: 'வெப்பநிலை பொருத்தம்',
        soilSuitability: 'மண் பொருத்தம்',
        irrigationDependency: 'பாசன சார்பு',
        valHigh: 'அதிகம்',
        valModerate: 'மிதமான',
        valLow: 'குறைவு',
        whyCropRisky: '❓ இந்தப் பயிர் இங்கு ஆபத்தானது / ஏற்றது ஏன்?',
        potentialRegionalImpact: '🌊 சாத்தியமான பிராந்திய தாக்கம்',
        potentialCropImpact: '🌾 சாத்தியமான பயிர் தாக்கம்',
        betterSuitedAlternatives: '🌱 சிறந்த மாற்றுப் பயிர்கள்',
        selectRegionEmptyTitle: 'வரைபடத்தில் ஒரு மாநிலத்தைத் தேர்ந்தெடுக்கவும்',
        selectRegionEmptySub: 'விவரங்களை ஆராய எந்தவொரு இந்திய மாநிலத்தையும் கிளிக் செய்யவும்.',
        catalogAccordionLabel: 'தரவுத்தள பட்டியல் (41 பொருட்கள்)',
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
        mapTitle: 'పంట అనుకూలత & నీటి ఒత్తిడి మ్యాప్',
        mapSubtitle: 'పంటలు ఎక్కడ బాగా పండుతాయో — మరియు నీరు, నేల, వాతావరణ పరిమితులు ఎక్కడ ప్రమాదాన్ని కలిగిస్తాయో తెలుసుకోండి.',
        selectCrop: 'పంటను ఎంచుకోండి:',
        layer: 'మ్యాప్ లేయర్:',
        cropSuitability: '🌾 పంట అనుకూలత',
        waterStress: '💧 నీటి ఒత్తిడి',
        compareCrop: '⚔️ పోల్చండి',
        mapOverviewTitle: 'భారత ప్రాంతీయ అనుకూలత వివరాలు',
        highlySuitable: '🟢 అత్యంత అనుకూలం',
        moderatelySuitable: '🔵 మధ్యస్థ అనుకూలం',
        marginalRisky: '🟠 సరిహద్దు / ప్రమాదకరం',
        unsuitableHighStress: '🔴 అనుకూలం కాదు / అధిక నీటి ఒత్తిడి',
        lowWaterStress: '🟢 తక్కువ నీటి ఒత్తిడి',
        moderateWaterStress: '🔵 మధ్యస్థ నీటి ఒత్తిడి',
        highWaterStress: '🟠 అధిక నీటి ఒత్తిడి',
        severeWaterStress: '🔴 తీవ్రమైన నీటి ఒత్తిడి',
        waterAvailability: 'నీటి లభ్యత',
        rainfallSuitability: 'వర్షపాతం అనుకూలత',
        temperatureSuitability: 'ఉష్ణోగ్రత అనుకూలత',
        soilSuitability: 'నేల అనుకూలత',
        irrigationDependency: 'సాగునీటి ఆధారపడటం',
        valHigh: 'అధికం',
        valModerate: 'మధ్యస్థం',
        valLow: 'తక్కువ',
        whyCropRisky: '❓ ఈ పంట ఇక్కడ ఎందుకు ప్రమాదకరం / అనుకూలం?',
        potentialRegionalImpact: '🌊 సంభావ్య ప్రాంతీయ ప్రభావం',
        potentialCropImpact: '🌾 సంభావ్య పంట ప్రభావం',
        betterSuitedAlternatives: '🌱 మెరుగైన ప్రత్యామ్నాయాలు',
        selectRegionEmptyTitle: 'మ్యాప్‌లో ఒక రాష్ట్రాన్ని ఎంచుకోండి',
        selectRegionEmptySub: 'వివరాలను చూడటానికి ఏదైనా భారతీయ రాష్ట్రంపై క్లిక్ చేయండి.',
        catalogAccordionLabel: 'డేటాబేస్ జాబితా (41 అంశాలు)',
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
        mapTitle: 'ಬೆಳೆ ಸೂಕ್ತತೆ ಮತ್ತು ನೀರಿನ ಒತ್ತಡದ ನಕ್ಷೆ',
        mapSubtitle: 'ಬೆಳೆಗಳು ಎಲ್ಲಿ ಚೆನ್ನಾಗಿ ಬೆಳೆಯುತ್ತವೆ — ಮತ್ತು ನೀರು, ಮಣ್ಣು ಮತ್ತು ಹವಾಮಾನ ಅಪಾಯಗಳು ಎಲ್ಲಿವೆ ಎಂಬುದನ್ನು ತಿಳಿಯಿರಿ.',
        selectCrop: 'ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:',
        layer: 'ನಕ್ಷೆಯ ಪದರ:',
        cropSuitability: '🌾 ಬೆಳೆ ಸೂಕ್ತತೆ',
        waterStress: '💧 ನೀರಿನ ಒತ್ತಡ',
        compareCrop: '⚔️ ಹೋಲಿಕೆ ಮಾಡಿ',
        mapOverviewTitle: 'ಭಾರತ ಪ್ರಾದೇಶಿಕ ಸೂಕ್ತತೆಯ ವಿವರ',
        highlySuitable: '🟢 ಅತ್ಯಂತ ಸೂಕ್ತ',
        moderatelySuitable: '🔵 ಮಧ್ಯಮ ಸೂಕ್ತ',
        marginalRisky: '🟠 ಗಡಿರೇಖೆ / ಅಪಾಯಕಾರಿ',
        unsuitableHighStress: '🔴 ಅಸಮಂಜಸ / ಅಧಿಕ ನೀರಿನ ಒತ್ತಡ',
        lowWaterStress: '🟢 ಕಡಿಮೆ ನೀರಿನ ಒತ್ತಡ',
        moderateWaterStress: '🔵 ಮಧ್ಯಮ ನೀರಿನ ಒತ್ತಡ',
        highWaterStress: '🟠 ಅಧಿಕ ನೀರಿನ ಒತ್ತಡ',
        severeWaterStress: '🔴 ತೀವ್ರ ನೀರಿನ ಒತ್ತಡ',
        waterAvailability: 'ನೀರಿನ ಲಭ್ಯತೆ',
        rainfallSuitability: 'ಮಳೆ ಸೂಕ್ತತೆ',
        temperatureSuitability: 'ತಾಪಮಾನ ಸೂಕ್ತತೆ',
        soilSuitability: 'ಮಣ್ಣಿನ ಸೂಕ್ತತೆ',
        irrigationDependency: 'ನೀರಾವರಿ ಅವಲಂಬನೆ',
        valHigh: 'ಹೆಚ್ಚು',
        valModerate: 'ಮಧ್ಯಮ',
        valLow: 'ಕಡಿಮೆ',
        whyCropRisky: '❓ ಈ ಬೆಳೆ ಇಲ್ಲೇಕೆ ಅಪಾಯಕಾರಿ / ಸೂಕ್ತ?',
        potentialRegionalImpact: '🌊 ಸಂಭಾವ್ಯ ಪ್ರಾದೇಶಿಕ ಪರಿಣಾಮ',
        potentialCropImpact: '🌾 ಸಂಭಾವ್ಯ ಬೆಳೆ ಪರಿಣಾಮ',
        betterSuitedAlternatives: '🌱 ಉತ್ತಮ ಪರ್ಯಾಯ ಬೆಳೆಗಳು',
        selectRegionEmptyTitle: 'ನಕ್ಷೆಯಲ್ಲಿ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        selectRegionEmptySub: 'ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಯಾವುದೇ ಭಾರತೀಯ ರಾಜ್ಯವನ್ನು ಕ್ಲಿಕ್ ಮಾಡಿ.',
        catalogAccordionLabel: 'ಡೇಟಾಬೇಸ್ ಪಟ್ಟಿ (41 ಐಟಂಗಳು)',
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
        mapTitle: 'വിള അനുയോജ്യതയും ജല സമ്മർദ്ദ ഭൂപടവും',
        mapSubtitle: 'വിളകൾ എവിടെ നന്നായി വളരുന്നു — എവിടെ വെള്ളം, മണ്ണ്, കാലാവസ്ഥാ അപകടസാധ്യതകൾ നിലനിൽക്കുന്നുവെന്ന് കണ്ടെത്തുക.',
        selectCrop: 'വിള തിരഞ്ഞെടുക്കുക:',
        layer: 'ഭൂപട പാളി:',
        cropSuitability: '🌾 വിള അനുയോജ്യത',
        waterStress: '💧 ജല സമ്മർദ്ദം',
        compareCrop: '⚔️ താരതമ്യം ചെയ്യുക',
        mapOverviewTitle: 'ഇന്ത്യൻ പ്രാദേശിക അനുയോജ്യതാ അവലോകനം',
        highlySuitable: '🟢 വളരെ അനുയോജ്യം',
        moderatelySuitable: '🔵 മിതമായ അനുയോജ്യം',
        marginalRisky: '🟠 അരികിലെ / അപകടസാധ്യതയുള്ളത്',
        unsuitableHighStress: '🔴 അനുയോജ്യമല്ല / ഉയർന്ന ജല സമ്മർദ്ദം',
        lowWaterStress: '🟢 കുറഞ്ഞ ജല സമ്മർദ്ദം',
        moderateWaterStress: '🔵 മിതമായ ജല സമ്മർദ്ദം',
        highWaterStress: '🟠 ഉയർന്ന ജല സമ്മർദ്ദം',
        severeWaterStress: '🔴 രൂക്ഷമായ ജല സമ്മർദ്ദം',
        waterAvailability: 'ജല ലഭ്യത',
        rainfallSuitability: 'മഴ അനുയോജ്യത',
        temperatureSuitability: 'താപനില അനുയോജ്യത',
        soilSuitability: 'മണ്ണ് അനുയോജ്യത',
        irrigationDependency: 'നനയ്ക്കൽ ആശ്രയത്വം',
        valHigh: 'ഉയർന്നത്',
        valModerate: 'മിതമായത്',
        valLow: 'കുറഞ്ഞത്',
        whyCropRisky: '❓ എന്തുകൊണ്ട് ഈ വിള ഇവിടെ അപകടകരമാണ് / അനുയോജ്യമാണ്?',
        potentialRegionalImpact: '🌊 സാധ്യതയുള്ള പ്രാദേശിക പ്രഭാവം',
        potentialCropImpact: '🌾 സാധ്യതയുള്ള വിള പ്രഭാവം',
        betterSuitedAlternatives: '🌱 കൂടുതൽ അനുയോജ്യമായ ബദലുകൾ',
        selectRegionEmptyTitle: 'ഭൂപടത്തിൽ ഒരു സംസ്ഥാനം തിരഞ്ഞെടുക്കുക',
        selectRegionEmptySub: 'വിശദാംശങ്ങൾ കാണുന്നതിന് ഏതെങ്കിലും ഇന്ത്യൻ സംസ്ഥാനത്തിൽ ക്ലിക്ക് ചെയ്യുക.',
        catalogAccordionLabel: 'ഡാറ്റാബേസ് പട്ടിക (41 ഇനങ്ങൾ)',
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
        mapTitle: 'ਫ਼ਸਲ ਢੁਕਵੇਂਪਣ ਅਤੇ ਜਲ ਤਣਾਅ ਨਕਸ਼ਾ',
        mapSubtitle: 'ਜਾਣੋ ਕਿ ਫ਼ਸਲਾਂ ਕਿੱਥੇ ਵਧੀਆ ਹੁੰਦੀਆਂ ਹਨ — ਅਤੇ ਕਿੱਥੇ ਪਾਣੀ, ਮਿੱਟੀ ਅਤੇ ਜਲਵਾਯੂ ਦੇ ਖ਼ਤਰੇ ਹਨ।',
        selectCrop: 'ਫ਼ਸਲ ਚੁਣੋ:',
        layer: 'ਨਕਸ਼ਾ ਪਰਤ:',
        cropSuitability: '🌾 ਫ਼ਸਲ ਢੁਕਵਾਂਪਣ',
        waterStress: '💧 ਜਲ ਤਣਾਅ',
        compareCrop: '⚔️ ਤੁਲਨਾ ਕਰੋ',
        mapOverviewTitle: 'ਭਾਰਤ ਖੇਤਰੀ ਢੁਕਵਾਂਪਣ ਵੇਰਵਾ',
        highlySuitable: '🟢 ਬਹੁਤ ਢੁਕਵਾਂ',
        moderatelySuitable: '🔵 ਦਰਮਿਆਨਾ ਢੁਕਵਾਂ',
        marginalRisky: '🟠 ਸੀਮਾਂਤ / ਖ਼ਤਰਨਾਕ',
        unsuitableHighStress: '🔴 ਅਣਢੁਕਵਾਂ / ਉੱਚ ਜਲ ਤਣਾਅ',
        lowWaterStress: '🟢 ਘੱਟ ਜਲ ਤਣਾਅ',
        moderateWaterStress: '🔵 ਦਰਮਿਆਨਾ ਜਲ ਤਣਾਅ',
        highWaterStress: '🟠 ਉੱਚ ਜਲ ਤਣਾਅ',
        severeWaterStress: '🔴 ਗੰਭੀਰ ਜਲ ਤਣਾਅ',
        waterAvailability: 'ਪਾਣੀ ਦੀ ਉਪਲਬਧਤਾ',
        rainfallSuitability: 'ਮੀਂਹ ਦੀ ਢੁਕਵਾਂਪਣ',
        temperatureSuitability: 'ਤਾਪਮਾਨ ਦੀ ਢੁਕਵਾਂਪਣ',
        soilSuitability: 'ਮਿੱਟੀ ਦੀ ਢੁਕਵਾਂਪਣ',
        irrigationDependency: 'ਸਿੰਚਾਈ \'ਤੇ ਨਿਰਭਰਤਾ',
        valHigh: 'ਉੱਚ',
        valModerate: 'ਦਰਮਿਆਨਾ',
        valLow: 'ਘੱਟ',
        whyCropRisky: '❓ ਇਹ ਫ਼ਸਲ ਇੱਥੇ ਖ਼ਤਰਨਾਕ / ਢੁਕਵੀਂ ਕਿਉਂ ਹੈ?',
        potentialRegionalImpact: '🌊 ਸੰਭਾਵੀ ਖੇਤਰੀ ਪ੍ਰਭਾਵ',
        potentialCropImpact: '🌾 ਸੰਭਾਵੀ ਫ਼ਸਲ ਪ੍ਰਭਾਵ',
        betterSuitedAlternatives: '🌱 ਬਿਹਤਰ ਢੁਕਵੇਂ ਬਦਲ',
        selectRegionEmptyTitle: 'ਨਕਸ਼ੇ \'ਤੇ ਕੋਈ ਰਾਜ ਚੁਣੋ',
        selectRegionEmptySub: 'ਕਿਸੇ ਵੀ ਭਾਰਤੀ ਰਾਜ \'ਤੇ ਕਲਿੱਕ ਕਰਕੇ ਵੇਰਵੇ ਦੇਖੋ।',
        catalogAccordionLabel: 'ਡੇਟਾਬੇਸ ਸੂਚੀ (41 ਵਸਤਾਂ)',
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
    setupSearchForm();
    setupDropzone();
    loadDatabaseCatalog();
    initRegionalMap();
    checkBackendHealth();

    // Set initial language from storage or default
    setLanguage(currentLang, false);

    // Load default item
    searchItem('rice');
});

function setupSearchForm() {
    const form = document.getElementById('search-form');
    const btn = document.getElementById('search-submit-btn');
    const input = document.getElementById('search-input');

    if (form) {
        form.onsubmit = function(e) {
            if (e) e.preventDefault();
            handleSearch(e);
            return false;
        };
    }
    if (btn) {
        btn.onclick = function(e) {
            if (e) e.preventDefault();
            handleSearch(e);
            return false;
        };
    }
    if (input) {
        input.onkeydown = function(e) {
            if (e.key === 'Enter') {
                if (e) e.preventDefault();
                handleSearch(e);
                return false;
            }
        };
    }
}

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
    
    if (document.getElementById('lbl-map-title')) document.getElementById('lbl-map-title').innerHTML = t.mapTitle || 'Crop Suitability & Water Stress Map';
    if (document.getElementById('lbl-map-subtitle')) document.getElementById('lbl-map-subtitle').innerHTML = t.mapSubtitle || '';
    if (document.getElementById('lbl-crop-select-title')) document.getElementById('lbl-crop-select-title').innerHTML = t.selectCrop || 'Select Crop:';
    if (document.getElementById('lbl-layer-select-title')) document.getElementById('lbl-layer-select-title').innerHTML = t.layer || 'Layer:';
    if (document.getElementById('btn-layer-suitability')) document.getElementById('btn-layer-suitability').innerHTML = t.cropSuitability || '🌾 Crop Suitability';
    if (document.getElementById('btn-layer-water-stress')) document.getElementById('btn-layer-water-stress').innerHTML = t.waterStress || '💧 Water Stress';
    if (document.getElementById('btn-toggle-compare')) document.getElementById('btn-toggle-compare').innerHTML = t.compareCrop || '⚔️ Compare Crop';
    if (document.getElementById('map-active-title')) document.getElementById('map-active-title').innerHTML = t.mapOverviewTitle || 'India Regional Suitability Overview';
    if (document.getElementById('lbl-catalog-accordion')) document.getElementById('lbl-catalog-accordion').innerHTML = t.catalogAccordionLabel || 'View Standardized Footprint Database Catalog (41 Items)';

    renderMapLegend();
    if (activeStateId) selectRegionalState(activeStateId);

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

function triggerFileInput() {
    console.log('[AI Lens Debug] Triggering file-input click event');
    const fileInput = document.getElementById('file-input');
    if (fileInput) {
        fileInput.click();
    } else {
        console.error('[AI Lens Debug] CRITICAL: file-input element not found in DOM');
    }
}

function handleFileSelected(event) {
    if (event.target.files && event.target.files.length > 0) {
        console.log('[AI Lens Debug] Change event triggered on file-input');
        handleFile(event.target.files[0]);
    } else {
        console.log('[AI Lens Debug] File selection cancelled or empty');
    }
}

function handleFile(file) {
    if (!file) {
        console.log('[AI Lens Debug] No file object passed');
        return;
    }

    console.log('[AI Lens Debug] IMAGE SELECTED:', {
        name: file.name,
        type: file.type || 'unknown',
        size: file.size,
    });

    if (file.type && !file.type.startsWith('image/')) {
        alert("This image format isn't supported. Please choose a JPG, PNG, or WebP image.");
        return;
    }

    selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        const previewImg = document.getElementById('preview-img') || document.getElementById('preview-image');
        const dropzoneIdle = document.getElementById('dropzone-idle') || document.getElementById('dropzone-content');
        const dropzonePreview = document.getElementById('dropzone-preview');
        const scanActions = document.getElementById('scan-actions');

        if (previewImg) previewImg.src = e.target.result;
        if (dropzoneIdle) dropzoneIdle.classList.add('hidden');
        if (dropzonePreview) dropzonePreview.classList.remove('hidden');
        if (scanActions) scanActions.classList.remove('hidden');

        console.log('[AI Lens Debug] PREVIEW CREATED & DISPLAYED FOR:', file.name);
    };
    reader.onerror = (err) => {
        console.error('[AI Lens Debug] FileReader error:', err);
        alert("Couldn't process this image. Please try another photo.");
    };
    reader.readAsDataURL(file);
}

function removeFile(event) {
    if (event) event.stopPropagation();
    selectedFile = null;
    const fileInput = document.getElementById('file-input');
    if (fileInput) fileInput.value = '';

    const dropzoneIdle = document.getElementById('dropzone-idle') || document.getElementById('dropzone-content');
    const dropzonePreview = document.getElementById('dropzone-preview');
    const scanActions = document.getElementById('scan-actions');

    if (dropzonePreview) dropzonePreview.classList.add('hidden');
    if (dropzoneIdle) dropzoneIdle.classList.remove('hidden');
    if (scanActions) scanActions.classList.add('hidden');

    console.log('[AI Lens Debug] Image state reset');
}

function executeScan() {
    console.log('[AI Lens Debug] executeScan triggered');
    runScan();
}

function switchTab(tab) {
    const tabSearchBtn = document.getElementById('tab-search-btn');
    const tabScanBtn = document.getElementById('tab-scan-btn');
    const tabSearch = document.getElementById('tab-search');
    const tabScan = document.getElementById('tab-scan');

    if (tab === 'search') {
        if (tabSearchBtn) tabSearchBtn.classList.add('active');
        if (tabScanBtn) tabScanBtn.classList.remove('active');
        if (tabSearch) tabSearch.classList.remove('hidden');
        if (tabScan) tabScan.classList.add('hidden');
    } else {
        if (tabScanBtn) tabScanBtn.classList.add('active');
        if (tabSearchBtn) tabSearchBtn.classList.remove('active');
        if (tabScan) tabScan.classList.remove('hidden');
        if (tabSearch) tabSearch.classList.add('hidden');
    }
}

function selectChip(itemName) {
    const input = document.getElementById('search-input');
    if (input) {
        input.value = itemName;
    }
    searchItem(itemName);
}

async function handleSearch(event) {
    if (event) event.preventDefault();
    const query = document.getElementById('search-input')?.value?.trim();
    if (!query) {
        renderError("No Input Entered", "Enter a product to analyze.");
        return;
    }
    searchItem(query);
}

async function searchItem(itemName) {
    const cleanName = itemName ? itemName.trim() : '';
    if (!cleanName) {
        renderError("No Input Entered", "Enter a product to analyze.");
        return;
    }

    showLoading("Searching product database...");

    try {
        const res = await fetch(`/footprint?item=${encodeURIComponent(cleanName)}&lang=${currentLang}`);
        if (res.ok) {
            const data = await res.json();
            renderResult(data);
        } else if (res.status === 404) {
            renderError("Product Not Found", `We couldn't find "${cleanName}" in our database.`);
        } else {
            renderError("Search Failed", "Unable to connect to the recognition service. Please try again.");
        }
    } catch (error) {
        console.error('Search API fetch error:', error);
        renderError("Service Unavailable", "Unable to connect to the recognition service. Please try again.");
    }
}

async function runScan() {
    if (!selectedFile) {
        renderError("No Image Selected", "Choose an image to scan.");
        return;
    }

    showLoading("Running AI visual recognition & calculating footprint...");

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
            } else {
                const title = data.reason === 'low_confidence' ? "Low Confidence Recognition" : "Recognition Failure";
                const msg = data.message || "I couldn't confidently identify this item. Try a clearer image.";
                renderError(title, msg);
            }
        } else if (res.status === 413) {
            renderError("Image Too Large", "Image is too large. Please choose a smaller image.");
        } else if (res.status === 415) {
            renderError("Invalid Image Format", "Please select a valid JPG or PNG image.");
        } else {
            renderError("Scan Error", "I couldn't confidently identify this item. Try a clearer image.");
        }
    } catch (error) {
        console.error('Scan API upload error:', error);
        renderError("Service Unavailable", "Unable to connect to the recognition service. Please try again.");
    }
}

function showLoading(messageText) {
    const loadingCard = document.getElementById('loading-state');
    const loadingMsg = document.getElementById('loading-text');
    const errorCard = document.getElementById('error-card');
    const resultCard = document.getElementById('result-card');

    if (errorCard) errorCard.classList.add('hidden');
    if (resultCard) resultCard.classList.add('hidden');
    if (loadingMsg) loadingMsg.textContent = messageText || "Retrieving water footprint metrics...";
    if (loadingCard) loadingCard.classList.remove('hidden');
}

function renderResult(data) {
    const loadingCard = document.getElementById('loading-state');
    const errorCard = document.getElementById('error-card');
    const resultCard = document.getElementById('result-card');

    if (loadingCard) loadingCard.classList.add('hidden');
    if (errorCard) errorCard.classList.add('hidden');
    if (resultCard) resultCard.classList.remove('hidden');

    // Product Title & Description
    const itemNameEl = document.getElementById('res-item-name');
    const itemDescEl = document.getElementById('res-description');

    const displayName = data.item || data.item_name || data.item_details?.display_name || 'Agricultural Item';
    if (itemNameEl) itemNameEl.textContent = capitalize(displayName);
    
    const descriptionText = data.description || data.item_details?.description || data.comparison || '';
    if (itemDescEl) itemDescEl.textContent = descriptionText;

    // Total Water Footprint
    const totalValEl = document.getElementById('res-total-wf');
    const totalUnitEl = document.getElementById('res-unit');
    const comparisonEl = document.getElementById('res-comparison');

    const total = Number(data.total_litres_per_kg || data.water_footprint?.total || 0);
    if (totalValEl) totalValEl.textContent = total.toLocaleString();
    if (totalUnitEl) totalUnitEl.textContent = data.unit || data.water_footprint?.unit || 'litres/kg';
    if (comparisonEl) comparisonEl.textContent = data.comparison || 'Data calculated based on standard agricultural yields.';

    // Breakdown values
    const green = Number(data.green_wf ?? data.green_water_litres ?? data.water_footprint?.green ?? 0);
    const blue = Number(data.blue_wf ?? data.blue_water_litres ?? data.water_footprint?.blue ?? 0);
    const grey = Number(data.grey_wf ?? data.grey_water_litres ?? data.water_footprint?.grey ?? 0);

    const greenValEl = document.getElementById('res-green-val');
    const blueValEl = document.getElementById('res-blue-val');
    const greyValEl = document.getElementById('res-grey-val');

    if (greenValEl) greenValEl.textContent = `${green.toLocaleString()} L`;
    if (blueValEl) blueValEl.textContent = `${blue.toLocaleString()} L`;
    if (greyValEl) greyValEl.textContent = `${grey.toLocaleString()} L`;

    // Breakdown percentages & progress fills
    const safeTotal = total > 0 ? total : (green + blue + grey) || 1;
    const pctGreen = Math.round((green / safeTotal) * 100);
    const pctBlue = Math.round((blue / safeTotal) * 100);
    const pctGrey = Math.round((grey / safeTotal) * 100);

    const pctGreenEl = document.getElementById('res-green-pct');
    const pctBlueEl = document.getElementById('res-blue-pct');
    const pctGreyEl = document.getElementById('res-grey-pct');

    if (pctGreenEl) pctGreenEl.textContent = `${pctGreen}%`;
    if (pctBlueEl) pctBlueEl.textContent = `${pctBlue}%`;
    if (pctGreyEl) pctGreyEl.textContent = `${pctGrey}%`;

    const fillGreenEl = document.getElementById('fill-green');
    const fillBlueEl = document.getElementById('fill-blue');
    const fillGreyEl = document.getElementById('fill-grey');

    if (fillGreenEl) fillGreenEl.style.width = `${pctGreen}%`;
    if (fillBlueEl) fillBlueEl.style.width = `${pctBlue}%`;
    if (fillGreyEl) fillGreyEl.style.width = `${pctGrey}%`;

    // Actionable Sustainability Tip
    const tipEl = document.getElementById('res-tip');
    if (tipEl) tipEl.textContent = data.tip || 'Choosing locally sourced produce significantly reduces overall water stress.';

    // Water Impact Insights Rendering
    const insights = data.insights || {};
    const explanationEl = document.getElementById('res-explanation');
    const compIconEl = document.getElementById('res-comp-icon');
    const compTextEl = document.getElementById('res-comp-text');
    const severityBadgeEl = document.getElementById('res-severity-badge');
    const severityLabelEl = document.getElementById('res-severity-label');
    const altNameEl = document.getElementById('res-alt-name');
    const altTextEl = document.getElementById('res-alt-display-text');
    const savingsBadgeEl = document.getElementById('res-savings-badge');
    const savingsValEl = document.getElementById('res-savings-val');

    if (explanationEl && insights.explanation) {
        explanationEl.textContent = insights.explanation;
    }

    if (insights.comparison) {
        if (compIconEl) compIconEl.textContent = insights.comparison.icon || '🛁';
        if (compTextEl) compTextEl.textContent = insights.comparison.display_text || '';
    }

    if (insights.severity && severityBadgeEl) {
        severityBadgeEl.className = `severity-badge ${insights.severity.badge_class || 'severity-high'}`;
        if (severityLabelEl) severityLabelEl.textContent = insights.severity.label || 'High Water Impact';
    }

    if (insights.alternative) {
        const alt = insights.alternative;
        if (altNameEl) altNameEl.textContent = alt.name || 'Sustainable Produce';
        if (altTextEl) altTextEl.textContent = alt.display_text || '';

        if (alt.has_savings_percentage && alt.savings_percentage !== null) {
            if (savingsBadgeEl) savingsBadgeEl.classList.remove('hidden');
            if (savingsValEl) savingsValEl.textContent = `≈ ${alt.savings_percentage}%`;
        } else {
            if (savingsBadgeEl) savingsBadgeEl.classList.add('hidden');
        }
    }

    // Scroll smoothly to the result section
    if (resultCard) {
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

function renderError(titleText, messageText) {
    const loadingCard = document.getElementById('loading-state');
    const resultCard = document.getElementById('result-card');
    const errorCard = document.getElementById('error-card');
    const errorTitleEl = document.getElementById('error-title');
    const errorMsgEl = document.getElementById('error-message');

    if (loadingCard) loadingCard.classList.add('hidden');
    if (resultCard) resultCard.classList.add('hidden');

    if (errorTitleEl) errorTitleEl.textContent = titleText || "Item Not Found";
    if (errorMsgEl) errorMsgEl.textContent = messageText || "Could not find water footprint data for this item.";
    if (errorCard) {
        errorCard.classList.remove('hidden');
        errorCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
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
                    selectChip(it.item);
                    window.scrollTo({ top: 300, behavior: 'smooth' });
                };

                const totalVal = Number(it.total_litres_per_kg || 0);
                const gVal = Number(it.green_wf || 0);
                const bVal = Number(it.blue_wf || 0);
                const grVal = Number(it.grey_wf || 0);
                const sTot = totalVal > 0 ? totalVal : 1;

                card.innerHTML = `
                    <div class="catalog-card-header">
                        <span class="catalog-card-name">${capitalize(it.item)}</span>
                        <span class="catalog-card-wf">${totalVal.toLocaleString()} L/kg</span>
                    </div>
                    <div class="catalog-mini-bar">
                        <div class="mini-bar-green" style="width: ${(gVal / sTot) * 100}%"></div>
                        <div class="mini-bar-blue" style="width: ${(bVal / sTot) * 100}%"></div>
                        <div class="mini-bar-grey" style="width: ${(grVal / sTot) * 100}%"></div>
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

// Regional Agriculture Map State
let activeRegionalCrop = 'rice';
let activeMapLayer = 'suitability';
let activeStateId = null;
let isCompareMode = false;
let regionalCropsList = [];
let regionalMapData = {};

const INDIA_SVG_STATES = [
    { id: "PB", name: "Punjab", d: "M 190 120 L 235 110 L 250 145 L 220 170 L 185 150 Z" },
    { id: "HR", name: "Haryana", d: "M 220 170 L 250 145 L 270 175 L 240 200 L 210 185 Z" },
    { id: "JK", name: "Jammu & Kashmir", d: "M 195 40 L 260 50 L 275 105 L 225 115 L 190 85 Z" },
    { id: "RJ", name: "Rajasthan", d: "M 115 155 L 210 185 L 220 250 L 160 295 L 95 235 Z" },
    { id: "GJ", name: "Gujarat", d: "M 75 245 L 155 285 L 140 350 L 55 335 L 45 280 Z" },
    { id: "UP", "name": "Uttar Pradesh", d: "M 270 175 L 365 185 L 385 240 L 290 255 L 240 200 Z" },
    { id: "BR", "name": "Bihar", d: "M 385 240 L 460 245 L 450 290 L 375 285 Z" },
    { id: "WB", "name": "West Bengal", d: "M 460 245 L 490 250 L 480 330 L 450 290 Z" },
    { id: "MP", "name": "Madhya Pradesh", d: "M 160 295 L 290 255 L 340 320 L 250 360 L 150 320 Z" },
    { id: "MH", "name": "Maharashtra", d: "M 140 350 L 250 360 L 280 430 L 150 420 Z" },
    { id: "KA", "name": "Karnataka", d: "M 160 430 L 240 440 L 220 515 L 170 495 Z" },
    { id: "TN", "name": "Tamil Nadu", d: "M 220 515 L 275 505 L 265 575 L 210 565 Z" },
    { id: "AP", "name": "Andhra Pradesh", d: "M 250 440 L 325 410 L 315 495 L 260 505 Z" },
    { id: "TS", "name": "Telangana", d: "M 260 365 L 325 365 L 315 425 L 250 425 Z" },
    { id: "KL", "name": "Kerala", d: "M 170 495 L 210 505 L 200 565 L 165 545 Z" },
    { id: "OR", "name": "Odisha", d: "M 340 320 L 430 330 L 400 395 L 325 365 Z" },
    { id: "AS", "name": "Assam", d: "M 495 215 L 565 220 L 555 260 L 490 250 Z" },
];

async function initRegionalMap() {
    await loadRegionalCrops();
    await fetchAndRenderMap();
}

async function loadRegionalCrops() {
    try {
        const res = await fetch('/regional/crops');
        if (res.ok) {
            const data = await res.json();
            regionalCropsList = data.crops || [];
            populateCropDropdowns();
        }
    } catch (err) {
        console.error("Failed to load regional crops:", err);
    }
}

function populateCropDropdowns() {
    const selector = document.getElementById('crop-selector');
    const compareSelector = document.getElementById('compare-crop-b-selector');
    if (!selector) return;

    selector.innerHTML = '';
    if (compareSelector) compareSelector.innerHTML = '';

    regionalCropsList.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c.crop_id;
        opt.textContent = `${c.crop_name} (${c.total_wf.toLocaleString()} ${c.unit})`;
        if (c.crop_id === activeRegionalCrop) opt.selected = true;
        selector.appendChild(opt);

        if (compareSelector) {
            const optB = document.createElement('option');
            optB.value = c.crop_id;
            optB.textContent = `${c.crop_name} (${c.total_wf.toLocaleString()} ${c.unit})`;
            if (c.crop_id === 'jowar' || c.crop_id === 'wheat') optB.selected = true;
            compareSelector.appendChild(optB);
        }
    });
}

async function handleCropChange() {
    const selector = document.getElementById('crop-selector');
    if (selector) activeRegionalCrop = selector.value;

    const labelA = document.getElementById('compare-crop-a-label');
    if (labelA) labelA.textContent = capitalize(activeRegionalCrop);

    await fetchAndRenderMap();
    if (activeStateId) selectRegionalState(activeStateId);
}

function switchMapLayer(layer) {
    activeMapLayer = layer;
    const btnSuit = document.getElementById('btn-layer-suitability');
    const btnStress = document.getElementById('btn-layer-water-stress');

    if (layer === 'suitability') {
        if (btnSuit) btnSuit.classList.add('active');
        if (btnStress) btnStress.classList.remove('active');
    } else {
        if (btnStress) btnStress.classList.add('active');
        if (btnSuit) btnSuit.classList.remove('active');
    }
    fetchAndRenderMap();
}

async function fetchAndRenderMap() {
    try {
        const res = await fetch(`/regional/map-data?crop=${activeRegionalCrop}&layer=${activeMapLayer}`);
        if (res.ok) {
            const data = await res.json();
            regionalMapData = data.states || {};
            renderIndiaVectorSVG();
            renderMapLegend();
        }
    } catch (err) {
        console.error("Map fetch error:", err);
    }
}

function renderIndiaVectorSVG() {
    const container = document.getElementById('india-map-container');
    if (!container) return;

    let svgHtml = `<svg class="map-svg" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">`;

    INDIA_SVG_STATES.forEach(st => {
        const stateInfo = regionalMapData[st.id] || { color: '#38bdf8', category: 'moderately_suitable' };
        const isSelected = activeStateId === st.id;
        const selClass = isSelected ? 'selected' : '';
        const centroid = getCentroid(st.d);

        svgHtml += `
            <path id="state-path-${st.id}"
                  class="state-path ${selClass}"
                  d="${st.d}"
                  fill="${stateInfo.color}"
                  fill-opacity="0.85"
                  onclick="selectRegionalState('${st.id}')">
                <title>${st.name}: ${stateInfo.category || stateInfo.water_stress}</title>
            </path>
            <text x="${centroid.x}" y="${centroid.y}" font-size="11" fill="#ffffff" font-weight="800" text-anchor="middle" pointer-events="none">${st.id}</text>
        `;
    });

    svgHtml += `</svg>`;
    container.innerHTML = svgHtml;
}

function getCentroid(pathD) {
    const matches = pathD.match(/(-?\d+(\.\d+)?)/g);
    if (!matches || matches.length < 4) return { x: 300, y: 300 };
    let sumX = 0, sumY = 0, count = 0;
    for (let i = 0; i < matches.length - 1; i += 2) {
        sumX += parseFloat(matches[i]);
        sumY += parseFloat(matches[i+1]);
        count++;
    }
    return { x: sumX / count, y: sumY / count };
}

function renderMapLegend() {
    const legendEl = document.getElementById('map-legend');
    if (!legendEl) return;

    const t = i18n[currentLang] || i18n.en;

    if (activeMapLayer === 'suitability') {
        legendEl.innerHTML = `
            <div class="legend-item"><span class="legend-dot" style="background:#10b981"></span> ${t.highlySuitable || '🟢 Highly Suitable'}</div>
            <div class="legend-item"><span class="legend-dot" style="background:#38bdf8"></span> ${t.moderatelySuitable || '🔵 Moderately Suitable'}</div>
            <div class="legend-item"><span class="legend-dot" style="background:#f59e0b"></span> ${t.marginalRisky || '🟠 Marginal / Risky'}</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ef4444"></span> ${t.unsuitableHighStress || '🔴 Unsuitable / High Stress'}</div>
        `;
    } else {
        legendEl.innerHTML = `
            <div class="legend-item"><span class="legend-dot" style="background:#10b981"></span> ${t.lowWaterStress || '🟢 Low Water Stress'}</div>
            <div class="legend-item"><span class="legend-dot" style="background:#38bdf8"></span> ${t.moderateWaterStress || '🔵 Moderate Water Stress'}</div>
            <div class="legend-item"><span class="legend-dot" style="background:#f97316"></span> ${t.highWaterStress || '🟠 High Water Stress'}</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ef4444"></span> ${t.severeWaterStress || '🔴 Severe Water Stress'}</div>
        `;
    }
}

async function selectRegionalState(stateId) {
    activeStateId = stateId;
    renderIndiaVectorSVG();

    const emptyState = document.getElementById('detail-empty-state');
    const contentBody = document.getElementById('detail-content-body');
    if (emptyState) emptyState.classList.add('hidden');
    if (contentBody) contentBody.classList.remove('hidden');

    try {
        const res = await fetch(`/regional/detail?crop=${activeRegionalCrop}&state=${stateId}&lang=${currentLang}`);
        if (res.ok) {
            const data = await res.json();
            renderRegionDetailPanel(data);
        }
    } catch (err) {
        console.error("State detail error:", err);
    }
}

function renderRegionDetailPanel(data) {
    const t = i18n[currentLang] || i18n.en;

    const stateNameEl = document.getElementById('detail-state-name');
    const cropTitleEl = document.getElementById('detail-crop-title');
    const suitPillEl = document.getElementById('detail-suitability-pill');
    const wfChipEl = document.getElementById('detail-wf-chip');

    const mWater = document.getElementById('m-water-avail');
    const mRain = document.getElementById('m-rainfall');
    const mTemp = document.getElementById('m-temperature');
    const mSoil = document.getElementById('m-soil');
    const mIrrig = document.getElementById('m-irrigation');

    const whyText = document.getElementById('analysis-why-text');
    const regImpact = document.getElementById('analysis-regional-impact');
    const cropImpact = document.getElementById('analysis-crop-impact');
    const betterAlts = document.getElementById('analysis-better-alts');
    const attribution = document.getElementById('detail-source-attribution');

    const localizeVal = (val) => {
        if (!val) return '';
        const v = val.toString().trim().toLowerCase();
        if (v === 'high') return t.valHigh || 'High';
        if (v === 'moderate') return t.valModerate || 'Moderate';
        if (v === 'low') return t.valLow || 'Low';
        if (v === 'severe') return t.severeWaterStress || 'Severe';
        return val;
    };

    if (stateNameEl) stateNameEl.textContent = data.region.name;
    if (cropTitleEl) cropTitleEl.textContent = data.crop.name;
    if (suitPillEl) suitPillEl.textContent = data.suitability.category_label;
    if (wfChipEl) wfChipEl.textContent = `${data.crop.water_footprint_total.toLocaleString()} ${data.crop.unit}`;

    if (mWater) mWater.textContent = localizeVal(data.sub_metrics.water_availability);
    if (mRain) mRain.textContent = localizeVal(data.sub_metrics.rainfall_suitability);
    if (mTemp) mTemp.textContent = localizeVal(data.sub_metrics.temperature_suitability);
    if (mSoil) mSoil.textContent = localizeVal(data.sub_metrics.soil_suitability);
    if (mIrrig) mIrrig.textContent = localizeVal(data.sub_metrics.irrigation_dependency);

    if (whyText) whyText.textContent = data.analysis.why_explanation;
    if (regImpact) regImpact.textContent = data.analysis.regional_impact;
    if (cropImpact) cropImpact.textContent = data.analysis.crop_impact;
    if (betterAlts) betterAlts.textContent = data.analysis.better_suited_alternatives;

    if (attribution) {
        attribution.textContent = `Data Source: ${data.data_attribution.source} (${data.data_attribution.source_date})`;
    }
}

function toggleCompareMode() {
    isCompareMode = !isCompareMode;
    const compareBar = document.getElementById('compare-bar');
    const btn = document.getElementById('btn-toggle-compare');
    if (compareBar) {
        if (isCompareMode) {
            compareBar.classList.remove('hidden');
            if (btn) btn.classList.add('active');
        } else {
            compareBar.classList.add('hidden');
            if (btn) btn.classList.remove('active');
        }
    }
}

function updateComparison() {
    const compB = document.getElementById('compare-crop-b-selector')?.value;
    if (activeStateId && compB) {
        fetch(`/regional/compare?crop_a=${activeRegionalCrop}&crop_b=${compB}&state=${activeStateId}`)
            .then(res => res.json())
            .then(data => {
                if (data.crop_a && data.crop_b) {
                    alert(`Comparison in ${data.crop_a.region.name}:\n\n` +
                          `${data.crop_a.crop.name}: ${data.crop_a.suitability.category_label} (${data.crop_a.crop.water_footprint_total} L/kg)\n` +
                          `${data.crop_b.crop.name}: ${data.crop_b.suitability.category_label} (${data.crop_b.crop.water_footprint_total} L/kg)`);
                }
            }).catch(e => console.error("Compare error:", e));
    }
}

function toggleCatalogExplorer() {
    const grid = document.getElementById('catalog-grid');
    const arrow = document.getElementById('catalog-arrow');
    if (grid) {
        grid.classList.toggle('hidden');
        if (arrow) arrow.textContent = grid.classList.contains('hidden') ? '▼' : '▲';
    }
}
