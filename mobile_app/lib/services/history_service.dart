import 'package:shared_preferences/shared_preferences.dart';

/// Persists recent food searches across sessions using SharedPreferences.
///
/// Stores up to [maxItems] searches. Newest entries appear first.
/// Uses localStorage on web, platform storage on mobile.
class HistoryService {
  static const String _key = 'wf_search_history';
  static const int maxItems = 5;

  /// Returns the stored search history (newest first).
  static Future<List<String>> getHistory() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getStringList(_key) ?? [];
  }

  /// Adds [item] to history.
  /// Removes duplicates and trims to [maxItems].
  static Future<void> saveSearch(String item) async {
    if (item.trim().isEmpty) return;
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList(_key) ?? [];

    // Normalise and dedup
    final normalised = item.trim().toLowerCase();
    list.removeWhere((e) => e.toLowerCase() == normalised);
    list.insert(0, item.trim());

    if (list.length > maxItems) {
      list.removeRange(maxItems, list.length);
    }

    await prefs.setStringList(_key, list);
  }

  /// Clears the entire search history.
  static Future<void> clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_key);
  }
}
