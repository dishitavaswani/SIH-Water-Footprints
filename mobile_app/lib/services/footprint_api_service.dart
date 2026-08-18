import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/footprint_result.dart';

/// HTTP service for the Water Footprint FastAPI backend.
///
/// Base URL defaults to `http://10.0.2.2:8000` (Android emulator → localhost).
/// Change to Aryaveer's deployed URL (Render / Railway) when live.
///
/// [lang] is passed as a query param to support EN/HI server-side responses.
///
/// **Phase 1 mock:** If the server is unreachable, a realistic mock result
/// is returned automatically so the UI can be built and tested independently.
class FootprintApiService {
  final String baseUrl;
  final String lang;

  FootprintApiService({
    this.baseUrl = 'http://10.0.2.2:8000',
    this.lang = 'en',
  });

  // ─── GET /footprint ────────────────────────────────────────────────────────

  /// Looks up the water footprint for [item].
  ///
  /// Throws [FootprintNotFoundException] on 404.
  /// Falls back to [_mockResult] when the server is unreachable.
  Future<FootprintResult> getFootprint(String item, {String? lang}) async {
    final effectiveLang = lang ?? this.lang;
    final uri = Uri.parse(baseUrl).replace(
      path: '/footprint',
      queryParameters: {
        'item': item.trim().toLowerCase(),
        'lang': effectiveLang,
      },
    );

    try {
      final response =
          await http.get(uri).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return FootprintResult.fromJson(
            jsonDecode(response.body) as Map<String, dynamic>);
      } else if (response.statusCode == 404) {
        throw FootprintNotFoundException(item);
      } else {
        throw FootprintApiException(
            'Server error ${response.statusCode}');
      }
    } on FootprintNotFoundException {
      rethrow;
    } on FootprintApiException {
      rethrow;
    } catch (_) {
      // Server not available — return mock so UI is testable
      return _mockResult(item);
    }
  }

  // ─── POST /scan ────────────────────────────────────────────────────────────

  /// Sends [imageBytes] as multipart to POST /scan.
  ///
  /// Returns a [FootprintResult] with the detected food item.
  /// Falls back to [_mockResult] when server is unreachable.
  Future<FootprintResult> scanImage(
    List<int> imageBytes, {
    String filename = 'capture.jpg',
    String? lang,
  }) async {
    final effectiveLang = lang ?? this.lang;
    final uri = Uri.parse(baseUrl).replace(
      path: '/scan',
      queryParameters: {'lang': effectiveLang},
    );

    try {
      final request = http.MultipartRequest('POST', uri)
        ..files.add(http.MultipartFile.fromBytes(
          'file',
          imageBytes,
          filename: filename,
        ));

      final streamed =
          await request.send().timeout(const Duration(seconds: 20));
      final response = await http.Response.fromStream(streamed);

      if (response.statusCode == 200) {
        final Map<String, dynamic> data =
            jsonDecode(response.body) as Map<String, dynamic>;
        if (data['success'] == false) {
          final msg = data['message'] as String? ??
              'Could not confidently identify this item.';
          throw FootprintApiException(msg);
        }
        return FootprintResult.fromJson(data);
      } else if (response.statusCode == 404) {
        throw FootprintNotFoundException('scanned item');
      } else {
        throw FootprintApiException(
            'Scan error ${response.statusCode}');
      }
    } on FootprintNotFoundException {
      rethrow;
    } on FootprintApiException {
      rethrow;
    } catch (_) {
      return _mockResult('rice (detected)');
    }
  }

  // ─── Mock (Phase 1 / offline) ──────────────────────────────────────────────

  /// Realistic demo data keyed by a known set of food items.
  /// Falls back to a generic rice entry for unknown items.
  FootprintResult _mockResult(String item) {
    const data = <String, Map<String, dynamic>>{
      'rice': {
        'green_wf': 1200.0,
        'blue_wf': 300.0,
        'grey_wf': 100.0,
        'tip': 'Try lentils — they use ~50% less water than rice.',
        'comparison': 'Equivalent to ~13 full bathtubs of water.',
      },
      'wheat': {
        'green_wf': 790.0,
        'blue_wf': 140.0,
        'grey_wf': 90.0,
        'tip': 'Wholegrain wheat products are water-efficient and nutritious.',
        'comparison': 'About the same as 8 bathtubs of water.',
      },
      'chicken': {
        'green_wf': 3300.0,
        'blue_wf': 140.0,
        'grey_wf': 460.0,
        'tip': 'Reducing chicken intake once a week saves ~3500 L.',
        'comparison': 'Like leaving a tap running for 10 hours.',
      },
      'mango': {
        'green_wf': 1520.0,
        'blue_wf': 80.0,
        'grey_wf': 50.0,
        'tip': 'Mangoes are water-intensive — enjoy in moderation.',
        'comparison': 'About 16 bathtubs of water per kg.',
      },
      'lentils': {
        'green_wf': 920.0,
        'blue_wf': 80.0,
        'grey_wf': 50.0,
        'tip': 'Lentils are one of the most water-efficient proteins.',
        'comparison': 'Only ~10 bathtubs — much better than meat.',
      },
      'potato': {
        'green_wf': 180.0,
        'blue_wf': 40.0,
        'grey_wf': 30.0,
        'tip': 'Potatoes are among the most water-efficient staple foods.',
        'comparison': 'Less than 3 bathtubs per kg!',
      },
    };

    final key = item.toLowerCase().split(' ').first;
    final entry = data[key] ?? data['rice']!;

    return FootprintResult(
      item: item.isEmpty ? 'rice' : item,
      greenWf: entry['green_wf'] as double,
      blueWf: entry['blue_wf'] as double,
      greyWf: entry['grey_wf'] as double,
      unit: 'litres/kg',
      tip: entry['tip'] as String?,
      comparison: entry['comparison'] as String?,
    );
  }
}

// ─── Exceptions ───────────────────────────────────────────────────────────────

class FootprintNotFoundException implements Exception {
  final String item;
  FootprintNotFoundException(this.item);
  @override
  String toString() => 'FootprintNotFoundException: "$item" not in DB.';
}

class FootprintApiException implements Exception {
  final String message;
  FootprintApiException(this.message);
  @override
  String toString() => 'FootprintApiException: $message';
}
