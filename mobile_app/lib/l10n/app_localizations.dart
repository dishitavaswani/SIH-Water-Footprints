import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

// ignore_for_file: non_constant_identifier_names

/// Hand-written localisation class for EN and HI.
///
/// Covers all strings used in SearchScreen, ScanScreen, ResultScreen,
/// HomeScreen, and the error/loading widgets.
///
/// To add a new language:
///   1. Add a `Locale('xx')` to [supportedLocales].
///   2. Add an `_AppLocalizationsXx` subclass with the translations.
///   3. Register it in [_AppLocalizationsDelegate.load].
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

// ─── English ──────────────────────────────────────────────────────────────────

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

// ─── Hindi ────────────────────────────────────────────────────────────────────

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

// ─── Delegate ─────────────────────────────────────────────────────────────────

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) =>
      ['en', 'hi'].contains(locale.languageCode);

  @override
  Future<AppLocalizations> load(Locale locale) async {
    switch (locale.languageCode) {
      case 'hi':
        return _AppLocalizationsHi();
      default:
        return _AppLocalizationsEn();
    }
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
