import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

// ignore_for_file: non_constant_identifier_names

/// Hand-written localization class for all 10 supported regional languages.
///
/// Supported Locales:
/// - en: English
/// - hi: Hindi (हिन्दी)
/// - mr: Marathi (मराठी)
/// - gu: Gujarati (ગુજરાતી)
/// - bn: Bengali (বাংলা)
/// - ta: Tamil (தமிழ்)
/// - te: Telugu (తెలుగు)
/// - kn: Kannada (ಕನ್ನಡ)
/// - ml: Malayalam (മലയാളം)
/// - pa: Punjabi (ਪੰਜਾਬੀ)
abstract class AppLocalizations {
  // ── Flutter plumbing ───────────────────────────────────────────────────────

  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates = [
    _AppLocalizationsDelegate(),
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ];

  static const List<Locale> supportedLocales = [
    Locale('en'),
    Locale('hi'),
    Locale('mr'),
    Locale('gu'),
    Locale('bn'),
    Locale('ta'),
    Locale('te'),
    Locale('kn'),
    Locale('ml'),
    Locale('pa'),
  ];

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  // ── String getters (abstract) ──────────────────────────────────────────────

  String get appTitle;
  String get searchHeading;
  String get searchSubtitle;
  String get searchHint;
  String get searchLabel;
  String get searchButton;
  String get popularItems;
  String get searchTabLabel;
  String get scanTabLabel;
  String get scanHeading;
  String get scanInstruction;
  String get scanButtonCamera;
  String get scanButtonGallery;
  String get scanConfirm;
  String get scanAgain;
  String get detected;
  String get confidence;
  String get calculating;
  String get waterBreakdown;
  String get greenWater;
  String get greenWaterSub;
  String get blueWater;
  String get blueWaterSub;
  String get greyWater;
  String get greyWaterSub;
  String get totalLabel;
  String get perspective;
  String get ecoTip;
  String get searchAgain;
  String get backToSearch;
  String get errorGeneric;
  String get errorOffline;
  String get retry;
  String get switchToHindi;
  String get switchToEnglish;

  // Parameterised
  String noDataFound(String item);
  String allValuesIn(String unit);
}

// ─── English (Canonical Source) ──────────────────────────────────────────────

class _AppLocalizationsEn extends AppLocalizations {
  @override String get appTitle        => 'Water Footprint';
  @override String get searchHeading   => 'Find the water cost\nof any food item';
  @override String get searchSubtitle  => 'Enter a food item to see its green, blue, and grey water footprint.';
  @override String get searchHint      => 'e.g. rice, wheat, mango…';
  @override String get searchLabel     => 'Food item';
  @override String get searchButton    => 'Search';
  @override String get popularItems    => 'Popular items';
  @override String get searchTabLabel  => 'Search';
  @override String get scanTabLabel    => 'Scan';
  @override String get scanHeading     => 'Scan a Food Item';
  @override String get scanInstruction => 'Point your camera at any food item to identify it and instantly get its water footprint.';
  @override String get scanButtonCamera  => 'Take Photo';
  @override String get scanButtonGallery => 'Pick from Gallery';
  @override String get scanConfirm     => 'Get Water Footprint';
  @override String get scanAgain       => 'Scan Again';
  @override String get detected        => 'Detected';
  @override String get confidence      => 'Confidence';
  @override String get calculating     => 'Calculating footprint…';
  @override String get waterBreakdown  => 'Water Breakdown';
  @override String get greenWater      => 'Green Water';
  @override String get greenWaterSub   => 'Rain-fed (agriculture)';
  @override String get blueWater       => 'Blue Water';
  @override String get blueWaterSub    => 'Surface & groundwater';
  @override String get greyWater       => 'Grey Water';
  @override String get greyWaterSub    => 'Pollution dilution';
  @override String get totalLabel      => 'Total';
  @override String get perspective     => 'Put it in perspective';
  @override String get ecoTip          => 'Eco Tip';
  @override String get searchAgain     => 'Search Another Item';
  @override String get backToSearch    => 'Back to Search';
  @override String get errorGeneric    => 'Something went wrong. Please try again.';
  @override String get errorOffline    => 'You appear to be offline. Check your connection.';
  @override String get retry           => 'Retry';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => 'No data found for "$item".';
  @override String allValuesIn(String unit)  => 'All values in $unit';
}

// ─── Hindi (Verified) ────────────────────────────────────────────────────────

class _AppLocalizationsHi extends AppLocalizations {
  @override String get appTitle        => 'जल पदचिह्न';
  @override String get searchHeading   => 'किसी भी खाद्य पदार्थ का\nजल मूल्य जानें';
  @override String get searchSubtitle  => 'खाद्य पदार्थ दर्ज करें और हरे, नीले और ग्रे जल पदचिह्न देखें।';
  @override String get searchHint      => 'जैसे: चावल, गेहूँ, आम…';
  @override String get searchLabel     => 'खाद्य पदार्थ';
  @override String get searchButton    => 'खोजें';
  @override String get popularItems    => 'लोकप्रिय वस्तुएँ';
  @override String get searchTabLabel  => 'खोज';
  @override String get scanTabLabel    => 'स्कैन';
  @override String get scanHeading     => 'खाद्य पदार्थ स्कैन करें';
  @override String get scanInstruction => 'किसी खाद्य पदार्थ की फोटो लें और तुरंत उसका जल पदचिह्न जानें।';
  @override String get scanButtonCamera  => 'फ़ोटो लें';
  @override String get scanButtonGallery => 'गैलरी से चुनें';
  @override String get scanConfirm     => 'जल पदचिह्न देखें';
  @override String get scanAgain       => 'फिर से स्कैन करें';
  @override String get detected        => 'पहचाना गया';
  @override String get confidence      => 'विश्वास स्तर';
  @override String get calculating     => 'पदचिह्न गणना हो रही है…';
  @override String get waterBreakdown  => 'जल विभाजन';
  @override String get greenWater      => 'हरा जल';
  @override String get greenWaterSub   => 'वर्षा-आधारित (कृषि)';
  @override String get blueWater       => 'नीला जल';
  @override String get blueWaterSub    => 'सतह और भूजल';
  @override String get greyWater       => 'ग्रे जल';
  @override String get greyWaterSub    => 'प्रदूषण तनुकरण';
  @override String get totalLabel      => 'कुल';
  @override String get perspective     => 'परिप्रेक्ष्य में देखें';
  @override String get ecoTip          => 'पर्यावरण सुझाव';
  @override String get searchAgain     => 'अन्य वस्तु खोजें';
  @override String get backToSearch    => 'खोज पर वापस जाएं';
  @override String get errorGeneric    => 'कुछ गलत हो गया। पुनः प्रयास करें।';
  @override String get errorOffline    => 'आप ऑफ़लाइन हैं। अपना कनेक्शन जाँचें।';
  @override String get retry           => 'पुनः प्रयास';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" के लिए डेटा नहीं मिला।';
  @override String allValuesIn(String unit)  => 'सभी मान $unit में';
}

// ─── Marathi (Curated / In Progress) ──────────────────────────────────────────

class _AppLocalizationsMr extends AppLocalizations {
  @override String get appTitle        => 'पाण्याचा ठसा';
  @override String get searchHeading   => 'कोणत्याही अन्नपदार्थाचा\nपाण्याचा खर्च शोधा';
  @override String get searchSubtitle  => 'हिरवे, निळे आणि राखाडी पाण्याचा ठसा पाहण्यासाठी अन्नपदार्थ प्रविष्ट करा.';
  @override String get searchHint      => 'उदा. तांदूळ, गहू, आंबा…';
  @override String get searchLabel     => 'अन्नपदार्थ';
  @override String get searchButton    => 'शोधा';
  @override String get popularItems    => 'लोकप्रिय घटक';
  @override String get searchTabLabel  => 'शोध';
  @override String get scanTabLabel    => 'स्कॅन';
  @override String get scanHeading     => 'अन्नपदार्थ स्कॅन करा';
  @override String get scanInstruction => 'अन्नपदार्थ ओळखण्यासाठी आणि त्याचा पाण्याचा ठसा त्वरित मिळवण्यासाठी कॅमेरा समोर धरा.';
  @override String get scanButtonCamera  => 'फोटो काढा';
  @override String get scanButtonGallery => 'गॅलरीतून निवडा';
  @override String get scanConfirm     => 'पाण्याचा ठसा मिळवा';
  @override String get scanAgain       => 'पुन्हा स्कॅन करा';
  @override String get detected        => 'ओळखले गेले';
  @override String get confidence      => 'विश्वास पातळी';
  @override String get calculating     => 'पाण्याचा ठसा मोजत आहे…';
  @override String get waterBreakdown  => 'पाण्याचे विभाजन';
  @override String get greenWater      => 'हिरवे पाणी';
  @override String get greenWaterSub   => 'पावसाचे पाणी (शेती)';
  @override String get blueWater       => 'निळे पाणी';
  @override String get blueWaterSub    => 'भूजल आणि पृष्ठभागावरील पाणी';
  @override String get greyWater       => 'राखाडी पाणी';
  @override String get greyWaterSub    => 'प्रदूषण सौम्यीकरण';
  @override String get totalLabel      => 'एकूण';
  @override String get perspective     => 'तुलना करून पहा';
  @override String get ecoTip          => 'पर्यावरणपूरक सूचना';
  @override String get searchAgain     => 'दुसरा घटक शोधा';
  @override String get backToSearch    => 'शोधाकडे परत जा';
  @override String get errorGeneric    => 'काहीतरी चूक झाली. कृपया पुन्हा प्रयत्न करा.';
  @override String get errorOffline    => 'आपण ऑफलाइन आहात. आपले कनेक्शन तपासा.';
  @override String get retry           => 'पुन्हा प्रयत्न';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" साठी डेटा आढळला नाही.';
  @override String allValuesIn(String unit)  => 'सर्व मूल्ये $unit मध्ये';
}

// ─── Gujarati (Curated / In Progress) ─────────────────────────────────────────

class _AppLocalizationsGu extends AppLocalizations {
  @override String get appTitle        => 'વોટર ફૂટપ્રિન્ટ';
  @override String get searchHeading   => 'કોઈપણ ખોરાક વસ્તુનો\nપાણી ખર્ચ શોધો';
  @override String get searchSubtitle  => 'લીલું, વાદળી અને ગ્રે પાણીનો વપરાશ જોવા માટે ખોરાક દાખલ કરો.';
  @override String get searchHint      => 'દા.ત. ચોખા, ઘઉં, કેરી…';
  @override String get searchLabel     => 'ખોરાકની વસ્તુ';
  @override String get searchButton    => 'શોધો';
  @override String get popularItems    => 'લોકપ્રિય વસ્તુઓ';
  @override String get searchTabLabel  => 'શોધ';
  @override String get scanTabLabel    => 'સ્કેન';
  @override String get scanHeading     => 'ખોરાકની વસ્તુ સ્કેન કરો';
  @override String get scanInstruction => 'ખોરાકની ઓળખ કરવા અને તેનો વોટર ફૂટપ્રિન્ટ તરત મેળવવા માટે કેમેરો સામે રાખો.';
  @override String get scanButtonCamera  => 'ફોટો લો';
  @override String get scanButtonGallery => 'ગેલેરીમાંથી પસંદ કરો';
  @override String get scanConfirm     => 'વોટર ફૂટપ્રિન્ટ મેળવો';
  @override String get scanAgain       => 'ફરીથી સ્કેન કરો';
  @override String get detected        => 'ઓળખાયેલ';
  @override String get confidence      => 'વિશ્વાસ સ્તર';
  @override String get calculating     => 'ગણતરી કરી રહ્યાં છીએ…';
  @override String get waterBreakdown  => 'પાણીનું વિભાજન';
  @override String get greenWater      => 'લીલું પાણી';
  @override String get greenWaterSub   => 'વરસાદ આધારિત (ખેતી)';
  @override String get blueWater       => 'વાદળી પાણી';
  @override String get blueWaterSub    => 'ભૂગર્ભજળ અને સપાટીનું પાણી';
  @override String get greyWater       => 'ગ્રે પાણી';
  @override String get greyWaterSub    => 'પ્રદૂષણ ઘટાડો';
  @override String get totalLabel      => 'કુલ';
  @override String get perspective     => 'તુલનામાં જુઓ';
  @override String get ecoTip          => 'પર્યાવરણ ટિપ';
  @override String get searchAgain     => 'બીજી વસ્તુ શોધો';
  @override String get backToSearch    => 'શોધ પર પાછા જાઓ';
  @override String get errorGeneric    => 'કંઈક ખોટું થયું. કૃપા કરીને ફરી પ્રયાસ કરો.';
  @override String get errorOffline    => 'તમે ઑફલાઇન છો. તમારું કનેક્શન તપાસો.';
  @override String get retry           => 'ફરી પ્રયાસ કરો';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" માટે ડેટા મળ્યો નથી.';
  @override String allValuesIn(String unit)  => 'બધા મૂલ્યો $unit માં';
}

// ─── Bengali (Curated / In Progress) ──────────────────────────────────────────

class _AppLocalizationsBn extends AppLocalizations {
  @override String get appTitle        => 'পানির পদচিহ্ন';
  @override String get searchHeading   => 'যেকোনো খাদ্যদ্রব্যের\nপানির খরচ জানুন';
  @override String get searchSubtitle  => 'সবুজ, নীল এবং ধূসর পানির পদচিহ্ন দেখতে খাদ্যদ্রব্য লিখুন।';
  @override String get searchHint      => 'যেমন: চাল, গম, আম…';
  @override String get searchLabel     => 'খাদ্যদ্রব্য';
  @override String get searchButton    => 'অনুসন্ধান';
  @override String get popularItems    => 'জনপ্রিয় খাদ্যদ্রব্য';
  @override String get searchTabLabel  => 'অনুসন্ধান';
  @override String get scanTabLabel    => 'স্ক্যান';
  @override String get scanHeading     => 'খাদ্যদ্রব্য স্ক্যান করুন';
  @override String get scanInstruction => 'খাদ্যদ্রব্য শনাক্ত করতে এবং তাৎক্ষণিকভাবে পানির পদচিহ্ন জানতে ক্যামেরা সামনে ধরুন।';
  @override String get scanButtonCamera  => 'ছবি তুলুন';
  @override String get scanButtonGallery => 'গ্যালারি থেকে বেছে নিন';
  @override String get scanConfirm     => 'পানির পদচিহ্ন দেখুন';
  @override String get scanAgain       => 'আবার স্ক্যান করুন';
  @override String get detected        => 'শনাক্ত হয়েছে';
  @override String get confidence      => 'আস্থা মাত্রা';
  @override String get calculating     => 'গণনা করা হচ্ছে…';
  @override String get waterBreakdown  => 'পানির বিভাজন';
  @override String get greenWater      => 'সবুজ পানি';
  @override String get greenWaterSub   => 'বৃষ্টির পানি (কৃষি)';
  @override String get blueWater       => 'নীল পানি';
  @override String get blueWaterSub    => 'ভূগর্ভস্থ ও ভূ-পৃষ্ঠের পানি';
  @override String get greyWater       => 'ধূসর পানি';
  @override String get greyWaterSub    => 'দূষণ হ্রাসকরণ';
  @override String get totalLabel      => 'মোট';
  @override String get perspective     => 'তুলনামূলক বিশ্লেষণ';
  @override String get ecoTip          => 'পরিবেশবান্ধব পরামর্শ';
  @override String get searchAgain     => 'অন্য খাদ্যদ্রব্য অনুসন্ধান করুন';
  @override String get backToSearch    => 'অনুসন্ধানে ফিরে যান';
  @override String get errorGeneric    => 'কিছু ভুল হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।';
  @override String get errorOffline    => 'আপনি অফলাইনে আছেন। আপনার সংযোগ পরীক্ষা করুন।';
  @override String get retry           => 'পুনরায় চেষ্টা';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" এর জন্য ডেটা পাওয়া যায়নি।';
  @override String allValuesIn(String unit)  => 'সব মান $unit এ';
}

// ─── Tamil (Curated / In Progress) ────────────────────────────────────────────

class _AppLocalizationsTa extends AppLocalizations {
  @override String get appTitle        => 'நீர் தடம்';
  @override String get searchHeading   => 'எந்த உணவுப் பொருளின்\nநீர் செலவையும் கண்டறியவும்';
  @override String get searchSubtitle  => 'பச்சை, நீல மற்றும் சாம்பல் நீர் தடத்தை காண உணவுப் பெயரை உள்ளிடவும்.';
  @override String get searchHint      => 'எ.கா. அரிசி, கோதுமை, மாம்பழம்…';
  @override String get searchLabel     => 'உணவுப் பொருள்';
  @override String get searchButton    => 'தேடு';
  @override String get popularItems    => 'பிரபலமானவை';
  @override String get searchTabLabel  => 'தேடல்';
  @override String get scanTabLabel    => 'ஸ்கேன்';
  @override String get scanHeading     => 'உணவுப் பொருளை ஸ்கேன் செய்';
  @override String get scanInstruction => 'உணவை அடையாளம் காணவும் அதன் நீர் தடத்தை உடனடியாக அறியவும் கேமராவை காட்டுங்கள்.';
  @override String get scanButtonCamera  => 'புகைப்படம் எடு';
  @override String get scanButtonGallery => 'கேலரியில் இருந்து தேர்வு செய்';
  @override String get scanConfirm     => 'நீர் தடத்தை பெறு';
  @override String get scanAgain       => 'மீண்டும் ஸ்கேன் செய்';
  @override String get detected        => 'கண்டறியப்பட்டது';
  @override String get confidence      => 'நம்பகத்தன்மை';
  @override String get calculating     => 'கணக்கிடப்படுகிறது…';
  @override String get waterBreakdown  => 'நீர் பிரிவு';
  @override String get greenWater      => 'பச்சை நீர்';
  @override String get greenWaterSub   => 'மழைநீர் (வேளாண்மை)';
  @override String get blueWater       => 'நீல நீர்';
  @override String get blueWaterSub    => 'நிலத்தடி மற்றும் மேற்பரப்பு நீர்';
  @override String get greyWater       => 'சாம்பல் நீர்';
  @override String get greyWaterSub    => 'மாசு நீர்த்தல்';
  @override String get totalLabel      => 'மொத்தம்';
  @override String get perspective     => 'ஒப்பீடு செய்து பாருங்கள்';
  @override String get ecoTip          => 'சுற்றுச்சூழல் குறிப்பு';
  @override String get searchAgain     => 'மற்றொரு பொருளைத் தேடுங்கள்';
  @override String get backToSearch    => 'தேடலுக்கு திரும்பு';
  @override String get errorGeneric    => 'ஏதோ தவறு நடந்துவிட்டது. மீண்டும் முயற்சிக்கவும்.';
  @override String get errorOffline    => 'நீங்கள் ஆஃப்லைனில் உள்ளீர்கள். இணைப்பைச் சரிபார்க்கவும்.';
  @override String get retry           => 'மீண்டும் முயற்சி செய்';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" க்கான தரவு கிடைக்கவில்லை.';
  @override String allValuesIn(String unit)  => 'அனைத்து மதிப்புகளும் $unit இல்';
}

// ─── Telugu (Curated / In Progress) ───────────────────────────────────────────

class _AppLocalizationsTe extends AppLocalizations {
  @override String get appTitle        => 'నీటి పాదముద్ర';
  @override String get searchHeading   => 'ఏదైనా ఆహార పదార్థం యొక్క\nనీటి ఖర్చును కనుగొనండి';
  @override String get searchSubtitle  => 'ఆకుపచ్చ, నీలి మరియు బూడిద రంగు నీటి పాదముద్రను చూడటానికి ఆహార పదార్థాన్ని నమోదు చేయండి.';
  @override String get searchHint      => 'ఉదా. వరి, గోధుమ, మామిడి…';
  @override String get searchLabel     => 'ఆహార పదార్థం';
  @override String get searchButton    => 'శోధించండి';
  @override String get popularItems    => 'జనాదరణ పొందినవి';
  @override String get searchTabLabel  => 'శోధన';
  @override String get scanTabLabel    => 'స్కాన్';
  @override String get scanHeading     => 'ఆహార పదార్థాన్ని స్కాన్ చేయండి';
  @override String get scanInstruction => 'ఆహార పదార్థాన్ని గుర్తించడానికి మరియు దాని నీటి పాదముద్రను వెంటనే పొందడానికి కెమెరాను చూపించండి.';
  @override String get scanButtonCamera  => 'ఫోటో తీయండి';
  @override String get scanButtonGallery => 'గ్యాలరీ నుండి ఎంచుకోండి';
  @override String get scanConfirm     => 'నీటి పాదముద్ర పొందండి';
  @override String get scanAgain       => 'మళ్లీ స్కాన్ చేయండి';
  @override String get detected        => 'గుర్తించబడింది';
  @override String get confidence      => 'విశ్వసనీయత';
  @override String get calculating     => 'లెక్కిస్తోంది…';
  @override String get waterBreakdown  => 'నీటి విభజన';
  @override String get greenWater      => 'ఆకుపచ్చ నీరు';
  @override String get greenWaterSub   => 'వర్షపు నీరు (వ్యవసాయం)';
  @override String get blueWater       => 'నీలి నీరు';
  @override String get blueWaterSub    => 'భూగర్భ మరియు ఉపరితల జలాలు';
  @override String get greyWater       => 'బూడిద రంగు నీరు';
  @override String get greyWaterSub    => 'కాలుష్య తగ్గింపు';
  @override String get totalLabel      => 'మొత్తం';
  @override String get perspective     => 'పోలికను చూడండి';
  @override String get ecoTip          => 'పర్యావరణ చిట్కా';
  @override String get searchAgain     => 'మరో వస్తువును శోధించండి';
  @override String get backToSearch    => 'శోధనకు తిరిగి వెళ్లండి';
  @override String get errorGeneric    => 'ఏదో తప్పు జరిగింది. దయచేసి మళ్లీ ప్రయత్నించండి.';
  @override String get errorOffline    => 'మీరు ఆఫ్‌లైన్‌లో ఉన్నారు. ఇంటర్నెట్ తనిఖీ చేయండి.';
  @override String get retry           => 'మళ్ళీ ప్రయత్నించండి';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" కొరకు డేటా కనుగొనబడలేదు.';
  @override String allValuesIn(String unit)  => 'అన్ని విలువలు $unit లో';
}

// ─── Kannada (Curated / In Progress) ──────────────────────────────────────────

class _AppLocalizationsKn extends AppLocalizations {
  @override String get appTitle        => 'ನೀರಿನ ಹೆಜ್ಜೆಗುರುತು';
  @override String get searchHeading   => 'ಯಾವುದೇ ಆಹಾರ ಪದಾರ್ಥದ\nನೀರಿನ ವೆಚ್ಚವನ್ನು ತಿಳಿಯಿರಿ';
  @override String get searchSubtitle  => 'ಹಸಿರು, ನೀಲಿ ಮತ್ತು ಬೂದು ನೀರಿನ ಹೆಜ್ಜೆಗುರುತನ್ನು ನೋಡಲು ಆಹಾರ ಪದಾರ್ಥವನ್ನು ನಮೂದಿಸಿ.';
  @override String get searchHint      => 'ಉದಾ. ಅಕ್ಕಿ, ಗೋಧಿ, ಮಾವು…';
  @override String get searchLabel     => 'ಆಹಾರ ಪದಾರ್ಥ';
  @override String get searchButton    => 'ಹುಡುಕಿ';
  @override String get popularItems    => 'ಜನಪ್ರಿಯ ವಸ್ತುಗಳು';
  @override String get searchTabLabel  => 'ಹುಡುಕಾಟ';
  @override String get scanTabLabel    => 'ಸ್ಕ್ಯಾನ್';
  @override String get scanHeading     => 'ಆಹಾರ ಪದಾರ್ಥವನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ';
  @override String get scanInstruction => 'ಆಹಾರ ಪದಾರ್ಥವನ್ನು ಗುರುತಿಸಲು ಮತ್ತು ಅದರ ನೀರಿನ ಹೆಜ್ಜೆಗುರುತನ್ನು ತಕ್ಷಣ ಪಡೆಯಲು ಕ್ಯಾಮೆರಾ ತೋರಿಸಿ.';
  @override String get scanButtonCamera  => 'ಫೋಟೋ ತೆಗೆಯಿರಿ';
  @override String get scanButtonGallery => 'ಗ್ಯಾಲರಿಯಿಂದ ಆರಿಸಿ';
  @override String get scanConfirm     => 'ನೀರಿನ ಹೆಜ್ಜೆಗುರುತು ಪಡೆಯಿರಿ';
  @override String get scanAgain       => 'ಮತ್ತೆ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ';
  @override String get detected        => 'ಗುರುತಿಸಲಾಗಿದೆ';
  @override String get confidence      => 'ವಿಶ್ವಾಸಾರ್ಹತೆ';
  @override String get calculating     => 'ಲೆಕ್ಕಾಚಾರ ಮಾಡಲಾಗುತ್ತಿದೆ…';
  @override String get waterBreakdown  => 'ನೀರಿನ ವಿಭಜನೆ';
  @override String get greenWater      => 'ಹಸಿರು ನೀರು';
  @override String get greenWaterSub   => 'ಮಳೆ ಆಧಾರಿತ (ಕೃಷಿ)';
  @override String get blueWater       => 'ನೀಲಿ ನೀರು';
  @override String get blueWaterSub    => 'ಅಂತರ್ಜಲ ಮತ್ತು ಮೇಲ್ಮೈ ನೀರು';
  @override String get greyWater       => 'ಬೂದು ನೀರು';
  @override String get greyWaterSub    => 'ಮಾಲಿನ್ಯ ದುರ್ಬಲಗೊಳಿಸುವಿಕೆ';
  @override String get totalLabel      => 'ಒಟ್ಟು';
  @override String get perspective     => 'ಹೋಲಿಕೆಯಲ್ಲಿ ನೋಡಿ';
  @override String get ecoTip          => 'ಪರಿಸರ ಸಲಹೆ';
  @override String get searchAgain     => 'ಮತ್ತೊಂದು ಐಟಂ ಹುಡುಕಿ';
  @override String get backToSearch    => 'ಹುಡುಕಾಟಕ್ಕೆ ಹಿಂತಿರುಗಿ';
  @override String get errorGeneric    => 'ಏನೋ ತಪ್ಪಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.';
  @override String get errorOffline    => 'ನೀವು ಆಫ್‌ಲೈನ್‌ನಲ್ಲಿದ್ದೀರಿ. ಸಂಪರ್ಕವನ್ನು ಪರಿಶೀಲಿಸಿ.';
  @override String get retry           => 'ಮರುಪ್ರಯತ್ನಿಸಿ';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" ಗಾಗಿ ಯಾವುದೇ ಡೇಟಾ ಕಂಡುಬಂದಿಲ್ಲ.';
  @override String allValuesIn(String unit)  => 'ಎಲ್ಲಾ ಮೌಲ್ಯಗಳು $unit ನಲ್ಲಿ';
}

// ─── Malayalam (Curated / In Progress) ────────────────────────────────────────

class _AppLocalizationsMl extends AppLocalizations {
  @override String get appTitle        => 'ജല കാൽപ്പാട്';
  @override String get searchHeading   => 'ഏതൊരു ഭക്ഷണ സാധനത്തിന്റെയും\nജലച്ചെലവ് കണ്ടെത്തുക';
  @override String get searchSubtitle  => 'പച്ച, നീല, ചാര ജല കാൽപ്പാടുകൾ കാണാൻ ഭക്ഷണ സാധനത്തിന്റെ പേര് നൽകുക.';
  @override String get searchHint      => 'ഉദാ. അരി, ഗോതമ്പ്, മാങ്ങ…';
  @override String get searchLabel     => 'ഭക്ഷണ സാധനം';
  @override String get searchButton    => 'തിരയുക';
  @override String get popularItems    => 'ജനപ്രിയ ഇനങ്ങൾ';
  @override String get searchTabLabel  => 'തിരയൽ';
  @override String get scanTabLabel    => 'സ്കാൻ';
  @override String get scanHeading     => 'ഭക്ഷണ സാധനം സ്കാൻ ചെയ്യുക';
  @override String get scanInstruction => 'ഭക്ഷണം തിരിച്ചറിയാനും അതിന്റെ ജല കാൽപ്പാട് തത്സമയം അറിയാനും ക്യാമറ കാണിക്കുക.';
  @override String get scanButtonCamera  => 'ഫോട്ടോ എടുക്കുക';
  @override String get scanButtonGallery => 'ഗാലറിയിൽ നിന്ന് തിരഞ്ഞെടുക്കുക';
  @override String get scanConfirm     => 'ജല കാൽപ്പാട് കണ്ടെത്തുക';
  @override String get scanAgain       => 'വീണ്ടും സ്കാൻ ചെയ്യുക';
  @override String get detected        => 'തിരിച്ചറിഞ്ഞു';
  @override String get confidence      => 'വിശ്വാസ്യത';
  @override String get calculating     => 'കണക്കാക്കുന്നു…';
  @override String get waterBreakdown  => 'ജല വിഭജനം';
  @override String get greenWater      => 'പച്ച വെള്ളം';
  @override String get greenWaterSub   => 'മഴവെള്ളം (കൃഷി)';
  @override String get blueWater       => 'നീല ജലം';
  @override String get blueWaterSub    => 'ഭൂഗർഭജലവും ഉപരിതല ജലവും';
  @override String get greyWater       => 'ചാര ജലം';
  @override String get greyWaterSub    => 'മലിനീകരണ ലഘൂകരണം';
  @override String get totalLabel      => 'ആകെ';
  @override String get perspective     => 'താരതമ്യം ചെയ്തു കാണുക';
  @override String get ecoTip          => 'പരിസ്ഥിതി സൗഹൃദ നിർദ്ദേശം';
  @override String get searchAgain     => 'മറ്റൊരു ഇനം തിരയുക';
  @override String get backToSearch    => 'തിരയലിലേക്ക് മടങ്ങുക';
  @override String get errorGeneric    => 'എന്തോ തകരാറുണ്ടായി. ദയവായി വീണ്ടും ശ്രമിക്കുക.';
  @override String get errorOffline    => 'നിങ്ങൾ ഓഫ്‌ലൈനിലാണ്. കണക്ഷൻ പരിശോധിക്കുക.';
  @override String get retry           => 'വീണ്ടും ശ്രമിക്കുക';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" ന് ഡാറ്റ കണ്ടെത്തിയില്ല.';
  @override String allValuesIn(String unit)  => 'എല്ലാ മൂല്യങ്ങളും $unit ൽ';
}

// ─── Punjabi (Curated / In Progress) ──────────────────────────────────────────

class _AppLocalizationsPa extends AppLocalizations {
  @override String get appTitle        => 'ਜਲ ਪੈਰ-ਚਿੰਨ੍ਹ';
  @override String get searchHeading   => 'ਕਿਸੇ ਵੀ ਭੋਜਨ ਵਸਤੂ ਦੀ\nਪਾਣੀ ਲਾਗਤ ਜਾਣੋ';
  @override String get searchSubtitle  => 'ਹਰਾ, ਨੀਲਾ ਅਤੇ ਸਲੇਟੀ ਪਾਣੀ ਪੈਰ-ਚਿੰਨ੍ਹ ਦੇਖਣ ਲਈ ਭੋਜਨ ਦਰਜ ਕਰੋ।';
  @override String get searchHint      => 'ਜਿਵੇਂ: ਚੌਲ, ਕਣਕ, ਅੰਬ…';
  @override String get searchLabel     => 'ਭੋਜਨ ਵਸਤੂ';
  @override String get searchButton    => 'ਖੋਜੋ';
  @override String get popularItems    => 'ਪ੍ਰਸਿੱਧ ਵਸਤਾਂ';
  @override String get searchTabLabel  => 'ਖੋਜ';
  @override String get scanTabLabel    => 'ਸਕੈਨ';
  @override String get scanHeading     => 'ਭੋਜਨ ਵਸਤੂ ਸਕੈਨ ਕਰੋ';
  @override String get scanInstruction => 'ਭੋਜਨ ਦੀ ਪਛਾਣ ਕਰਨ ਅਤੇ ਤੁਰੰਤ ਉਸਦਾ ਜਲ ਪੈਰ-ਚਿੰਨ੍ਹ ਪ੍ਰਾਪਤ ਕਰਨ ਲਈ ਕੈਮਰਾ ਦਿਖਾਓ।';
  @override String get scanButtonCamera  => 'ਫ਼ੋਟੋ ਖਿੱਚੋ';
  @override String get scanButtonGallery => 'ਗੈਲਰੀ ਵਿੱਚੋਂ ਚੁਣੋ';
  @override String get scanConfirm     => 'ਜਲ ਪੈਰ-ਚਿੰਨ੍ਹ ਪ੍ਰਾਪਤ ਕਰੋ';
  @override String get scanAgain       => 'ਦੁਬਾਰਾ ਸਕੈਨ ਕਰੋ';
  @override String get detected        => 'ਪਛਾਣਿਆ ਗਿਆ';
  @override String get confidence      => 'ਭਰੋਸੇ ਦਾ ਪੱਧਰ';
  @override String get calculating     => 'ਪੈਰ-ਚਿੰਨ੍ਹ ਦੀ ਗਣਨਾ ਹੋ ਰਹੀ ਹੈ…';
  @override String get waterBreakdown  => 'ਪਾਣੀ ਦੀ ਵੰਡ';
  @override String get greenWater      => 'ਹਰਾ ਪਾਣੀ';
  @override String get greenWaterSub   => 'ਮੀਂਹ \'ਤੇ ਆਧਾਰਿਤ (ਖੇਤੀ)';
  @override String get blueWater       => 'ਨੀਲਾ ਪਾਣੀ';
  @override String get blueWaterSub    => 'ਧਰਤੀ ਹੇਠਲਾ ਅਤੇ ਸਤਹੀ ਪਾਣੀ';
  @override String get greyWater       => 'ਸਲੇਟੀ ਪਾਣੀ';
  @override String get greyWaterSub    => 'ਪ੍ਰਦੂਸ਼ਣ ਨਿਵਾਰਣ';
  @override String get totalLabel      => 'ਕੁੱਲ';
  @override String get perspective     => 'ਤੁਲਨਾ ਕਰਕੇ ਦੇਖੋ';
  @override String get ecoTip          => 'ਵਾਤਾਵਰਣ ਸੁਝਾਅ';
  @override String get searchAgain     => 'ਕੋਈ ਹੋਰ ਵਸਤੂ ਖੋਜੋ';
  @override String get backToSearch    => 'ਖੋਜ \'ਤੇ ਵਾਪਸ ਜਾਓ';
  @override String get errorGeneric    => 'ਕੁਝ ਗਲਤ ਹੋ ਗਿਆ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।';
  @override String get errorOffline    => 'ਤੁਸੀਂ ਔਫਲਾਈਨ ਹੋ। ਆਪਣਾ ਕਨੈਕਸ਼ਨ ਜਾਂਚੋ।';
  @override String get retry           => 'ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼';
  @override String get switchToHindi   => 'हिंदी';
  @override String get switchToEnglish => 'English';

  @override String noDataFound(String item) => '"$item" ਲਈ ਕੋਈ ਡਾਟਾ ਨਹੀਂ ਮਿਲਿਆ।';
  @override String allValuesIn(String unit)  => 'ਸਾਰੇ ਮੁੱਲ $unit ਵਿੱਚ';
}

// ─── Delegate ─────────────────────────────────────────────────────────────────

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) => [
        'en',
        'hi',
        'mr',
        'gu',
        'bn',
        'ta',
        'te',
        'kn',
        'ml',
        'pa',
      ].contains(locale.languageCode);

  @override
  Future<AppLocalizations> load(Locale locale) async {
    switch (locale.languageCode) {
      case 'hi':
        return _AppLocalizationsHi();
      case 'mr':
        return _AppLocalizationsMr();
      case 'gu':
        return _AppLocalizationsGu();
      case 'bn':
        return _AppLocalizationsBn();
      case 'ta':
        return _AppLocalizationsTa();
      case 'te':
        return _AppLocalizationsTe();
      case 'kn':
        return _AppLocalizationsKn();
      case 'ml':
        return _AppLocalizationsMl();
      case 'pa':
        return _AppLocalizationsPa();
      default:
        return _AppLocalizationsEn();
    }
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
