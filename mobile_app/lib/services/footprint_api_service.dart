import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import '../models/footprint_result.dart';

/// HTTP service for the Water Footprint FastAPI backend.
///
/// Base URL defaults to `http://10.0.2.2:8000` (Android emulator → localhost).
/// Change to Aryaveer's deployed URL (Render / Railway) when live.
///
/// [lang] is passed as a query param to support EN/HI server-side responses.
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
  /// Throws [FootprintNotFoundException] if not in DB.
  /// Throws [FootprintApiException] on error.
  Future<FootprintResult> getFootprint(String item, {String? lang}) async {
    final effectiveLang = lang ?? this.lang;
    final Uri uri;
    if (baseUrl.endsWith('/')) {
      uri = Uri.parse('${baseUrl}footprint?item=${Uri.encodeComponent(item)}&lang=$effectiveLang');
    } else {
      uri = Uri.parse('$baseUrl/footprint?item=${Uri.encodeComponent(item)}&lang=$effectiveLang');
    }

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
            'Unable to connect to the recognition service. Please check your connection.');
      }
    } on FootprintNotFoundException {
      rethrow;
    } on FootprintApiException {
      rethrow;
    } catch (_) {
      throw FootprintApiException(
          'Unable to connect to the recognition service. Please check your connection.');
    }
  }

  // ─── POST /scan ────────────────────────────────────────────────────────────

  /// Sends raw image bytes [imageBytes] to `POST /scan`.
  ///
  /// Returns a [FootprintResult] with the detected food item.
  Future<FootprintResult> scanImage(
    List<int> imageBytes, {
    String filename = 'capture.jpg',
    String? lang,
  }) async {
    final effectiveLang = lang ?? this.lang;
    final String cleanBase = baseUrl.endsWith('/') ? baseUrl.substring(0, baseUrl.length - 1) : baseUrl;
    final Uri uri = Uri.parse('$cleanBase/scan?lang=$effectiveLang');

    String subType = 'jpeg';
    final String ext = filename.split('.').last.toLowerCase();
    if (ext == 'png') {
      subType = 'png';
    } else if (ext == 'webp') {
      subType = 'webp';
    }

    try {
      final request = http.MultipartRequest('POST', uri)
        ..files.add(http.MultipartFile.fromBytes(
          'file',
          imageBytes,
          filename: filename,
          contentType: MediaType('image', subType),
        ));

      final streamed =
          await request.send().timeout(const Duration(seconds: 20));
      final response = await http.Response.fromStream(streamed);

      if (response.statusCode == 200) {
        final Map<String, dynamic> data =
            jsonDecode(response.body) as Map<String, dynamic>;
        if (data['success'] == false) {
          final msg = data['message'] as String? ??
              "Couldn't process this image. Please try another photo.";
          throw FootprintApiException(msg);
        }
        return FootprintResult.fromJson(data);
      } else if (response.statusCode == 400) {
        throw FootprintApiException(
            "Couldn't process this image. Please try another photo.");
      } else if (response.statusCode == 413) {
        throw FootprintApiException(
            "The image file is too large. Please select a smaller photo.");
      } else if (response.statusCode == 415) {
        throw FootprintApiException(
            "This image format isn't supported. Please choose a JPG or PNG image.");
      } else if (response.statusCode == 404) {
        throw FootprintNotFoundException('scanned item');
      } else {
        throw FootprintApiException(
            "Unable to connect to the recognition service. Please check your connection.");
      }
    } on FootprintNotFoundException {
      rethrow;
    } on FootprintApiException {
      rethrow;
    } catch (_) {
      throw FootprintApiException(
          "Unable to connect to the recognition service. Please check your connection.");
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
