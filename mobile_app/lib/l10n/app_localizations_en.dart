// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appTitle => 'Water Footprint';

  @override
  String get searchHeading => 'Find the water cost\nof any food item';

  @override
  String get searchSubtitle =>
      'Enter a food item to see its green, blue, and grey water footprint.';

  @override
  String get searchHint => 'e.g. rice, wheat, mango…';

  @override
  String get searchLabel => 'Food item';

  @override
  String get searchButton => 'Search';

  @override
  String get popularItems => 'Popular items';

  @override
  String get scanTabLabel => 'Scan';

  @override
  String get searchTabLabel => 'Search';

  @override
  String get scanHeading => 'Scan a Food Item';

  @override
  String get scanInstruction =>
      'Point your camera at any food item to identify it and instantly get its water footprint.';

  @override
  String get scanButtonCamera => 'Take Photo';

  @override
  String get scanButtonGallery => 'Pick from Gallery';

  @override
  String get scanConfirm => 'Get Water Footprint';

  @override
  String get scanAgain => 'Scan Again';

  @override
  String get detected => 'Detected';

  @override
  String get confidence => 'Confidence';

  @override
  String get calculating => 'Calculating footprint…';

  @override
  String get waterBreakdown => 'Water Breakdown';

  @override
  String allValuesIn(String unit) {
    return 'All values in $unit';
  }

  @override
  String get greenWater => 'Green Water';

  @override
  String get greenWaterSub => 'Rain-fed (agriculture)';

  @override
  String get blueWater => 'Blue Water';

  @override
  String get blueWaterSub => 'Surface & groundwater';

  @override
  String get greyWater => 'Grey Water';

  @override
  String get greyWaterSub => 'Pollution dilution';

  @override
  String get totalLabel => 'Total';

  @override
  String get perspective => 'Put it in perspective';

  @override
  String get ecoTip => 'Eco Tip';

  @override
  String get searchAgain => 'Search Another Item';

  @override
  String get backToSearch => 'Back to Search';

  @override
  String noDataFound(String item) {
    return 'No data found for \"$item\".';
  }

  @override
  String get errorGeneric => 'Something went wrong. Please try again.';

  @override
  String get errorOffline => 'You appear to be offline. Check your connection.';

  @override
  String get retry => 'Retry';

  @override
  String get switchToHindi => 'हिंदी';

  @override
  String get switchToEnglish => 'English';
}
