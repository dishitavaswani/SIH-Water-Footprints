// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Hindi (`hi`).
class AppLocalizationsHi extends AppLocalizations {
  AppLocalizationsHi([String locale = 'hi']) : super(locale);

  @override
  String get appTitle => 'जल पदचिह्न';

  @override
  String get searchHeading => 'किसी भी खाद्य पदार्थ का\nजल मूल्य जानें';

  @override
  String get searchSubtitle =>
      'खाद्य पदार्थ दर्ज करें और हरे, नीले और ग्रे जल पदचिह्न देखें।';

  @override
  String get searchHint => 'जैसे: चावल, गेहूँ, आम…';

  @override
  String get searchLabel => 'खाद्य पदार्थ';

  @override
  String get searchButton => 'खोजें';

  @override
  String get popularItems => 'लोकप्रिय वस्तुएँ';

  @override
  String get scanTabLabel => 'स्कैन';

  @override
  String get searchTabLabel => 'खोज';

  @override
  String get scanHeading => 'खाद्य पदार्थ स्कैन करें';

  @override
  String get scanInstruction =>
      'किसी खाद्य पदार्थ की फोटो लें और तुरंत उसका जल पदचिह्न जानें।';

  @override
  String get scanButtonCamera => 'फ़ोटो लें';

  @override
  String get scanButtonGallery => 'गैलरी से चुनें';

  @override
  String get scanConfirm => 'जल पदचिह्न देखें';

  @override
  String get scanAgain => 'फिर से स्कैन करें';

  @override
  String get detected => 'पहचाना गया';

  @override
  String get confidence => 'विश्वास स्तर';

  @override
  String get calculating => 'पदचिह्न गणना हो रही है…';

  @override
  String get waterBreakdown => 'जल विभाजन';

  @override
  String allValuesIn(String unit) {
    return 'सभी मान $unit में';
  }

  @override
  String get greenWater => 'हरा जल';

  @override
  String get greenWaterSub => 'वर्षा-आधारित (कृषि)';

  @override
  String get blueWater => 'नीला जल';

  @override
  String get blueWaterSub => 'सतह और भूजल';

  @override
  String get greyWater => 'ग्रे जल';

  @override
  String get greyWaterSub => 'प्रदूषण तनुकरण';

  @override
  String get totalLabel => 'कुल';

  @override
  String get perspective => 'परिप्रेक्ष्य में देखें';

  @override
  String get ecoTip => 'पर्यावरण सुझाव';

  @override
  String get searchAgain => 'अन्य वस्तु खोजें';

  @override
  String get backToSearch => 'खोज पर वापस जाएं';

  @override
  String noDataFound(String item) {
    return '\"$item\" के लिए डेटा नहीं मिला।';
  }

  @override
  String get errorGeneric => 'कुछ गलत हो गया। पुनः प्रयास करें।';

  @override
  String get errorOffline => 'आप ऑफ़लाइन हैं। अपना कनेक्शन जाँचें।';

  @override
  String get retry => 'पुनः प्रयास';

  @override
  String get switchToHindi => 'हिंदी';

  @override
  String get switchToEnglish => 'English';
}
