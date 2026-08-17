import 'package:flutter/material.dart';

/// App-wide locale state. Holds the current [Locale] and exposes
/// [toggleLocale] to switch between English and Hindi.
///
/// Consumed by [WaterFootprintApp] via [ChangeNotifierProvider].
class LocaleProvider extends ChangeNotifier {
  Locale _locale = const Locale('en');

  Locale get locale => _locale;

  bool get isHindi => _locale.languageCode == 'hi';

  void setLocale(Locale locale) {
    if (_locale.languageCode == locale.languageCode) return;
    _locale = locale;
    notifyListeners();
  }

  /// Toggles between English and Hindi.
  void toggleLocale() {
    setLocale(isHindi ? const Locale('en') : const Locale('hi'));
  }
}
