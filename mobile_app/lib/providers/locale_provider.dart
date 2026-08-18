import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Language option metadata.
class LanguageOption {
  final String code;
  final String englishName;
  final String nativeName;
  final bool isVerified;

  const LanguageOption({
    required this.code,
    required this.englishName,
    required this.nativeName,
    required this.isVerified,
  });
}

/// App-wide locale state for all 10 supported Indian regional languages.
///
/// Holds the active [Locale], provides the list of all available languages
/// with their native script names, and persists selection throughout the session
/// and across application launches via SharedPreferences.
class LocaleProvider extends ChangeNotifier {
  static const String _prefKey = 'selected_language_code';

  Locale _locale = const Locale('en');

  Locale get locale => _locale;

  static const List<LanguageOption> supportedLanguages = [
    LanguageOption(code: 'en', englishName: 'English', nativeName: 'English', isVerified: true),
    LanguageOption(code: 'hi', englishName: 'Hindi', nativeName: 'हिन्दी', isVerified: true),
    LanguageOption(code: 'mr', englishName: 'Marathi', nativeName: 'मराठी', isVerified: false),
    LanguageOption(code: 'gu', englishName: 'Gujarati', nativeName: 'ગુજરાતી', isVerified: false),
    LanguageOption(code: 'bn', englishName: 'Bengali', nativeName: 'বাংলা', isVerified: false),
    LanguageOption(code: 'ta', englishName: 'Tamil', nativeName: 'தமிழ்', isVerified: false),
    LanguageOption(code: 'te', englishName: 'Telugu', nativeName: 'తెలుగు', isVerified: false),
    LanguageOption(code: 'kn', englishName: 'Kannada', nativeName: 'ಕನ್ನಡ', isVerified: false),
    LanguageOption(code: 'ml', englishName: 'Malayalam', nativeName: 'മലയാളം', isVerified: false),
    LanguageOption(code: 'pa', englishName: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ', isVerified: false),
  ];

  LocaleProvider() {
    _loadSavedLocale();
  }

  LanguageOption get currentLanguage =>
      supportedLanguages.firstWhere(
        (l) => l.code == _locale.languageCode,
        orElse: () => supportedLanguages.first,
      );

  bool get isHindi => _locale.languageCode == 'hi';

  Future<void> _loadSavedLocale() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedCode = prefs.getString(_prefKey);
      if (savedCode != null && supportedLanguages.any((l) => l.code == savedCode)) {
        _locale = Locale(savedCode);
        notifyListeners();
      }
    } catch (_) {
      // Graceful fallback to default locale
    }
  }

  Future<void> _saveLocale(String code) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_prefKey, code);
    } catch (_) {
      // Non-blocking fallback
    }
  }

  void setLocale(Locale locale) {
    if (_locale.languageCode == locale.languageCode) return;
    _locale = locale;
    _saveLocale(locale.languageCode);
    notifyListeners();
  }

  void setLanguageCode(String code) {
    setLocale(Locale(code));
  }

  /// Cycles or toggles to Hindi/English for quick switching
  void toggleLocale() {
    setLocale(isHindi ? const Locale('en') : const Locale('hi'));
  }
}
