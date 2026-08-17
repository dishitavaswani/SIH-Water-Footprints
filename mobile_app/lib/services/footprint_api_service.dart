import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/footprint_result.dart';

/// HTTP service for the Water Footprint backend API.
///
/// The [baseUrl] should point to Aryaveer's FastAPI server.
/// During Phase 1, a mock response is returned when the server
/// is not yet available (see [_mockFallback]).
class FootprintApiService {
  /// Base URL of the FastAPI backend. Override via constructor or change to
  /// Aryaveer's deployed Render/Railway URL when ready.
  final String baseUrl;

  /// Optional language code to pass as `lang` query param (e.g. 'hi').
  final String lang;

  FootprintApiService({
    this.baseUrl = 'http://10.0.2.2:8000', // Android emulator → localhost
    this.lang = 'en',
  });

  // ─── GET /footprint ────────────────────────────────────────────────────────

  /// Looks up the water footprint for [item].
  ///
  /// Returns a [FootprintResult] on success.
  /// Throws a [FootprintNotFoundException] if the API returns 404.
  /// Throws a [FootprintApiException] on any other error.
  Future<FootprintResult> getFootprint(String item) async {
    final uri = Uri.parse(baseUrl).replace(
      path: '/footprint',
      queryParameters: {
        'item': item.trim().toLowerCase(),
        'lang': lang,
      },
    );

    try {
      final response = await http.get(uri).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body) as Map<String, dynamic>;
        return FootprintResult.fromJson(json);
      } else if (response.statusCode == 404) {
        throw FootprintNotFoundException(item);
      } else {
        throw FootprintApiException(
            'Server error ${response.statusCode}: ${response.body}');
      }
    } on FootprintNotFoundException {
      rethrow;
    } catch (e) {
      // Server unavailable during Phase 1 — return mock data so UI can be built
      if (e is! FootprintApiException) {
        return _mockFallback(item);
      }
      rethrow;
    }
  }

  // ─── POST /scan ────────────────────────────────────────────────────────────

  /// Sends an image file [imageBytes] to POST /scan and returns the result.
  ///
  /// The multipart field name is `file`, matching Aryaveer's FastAPI endpoint.
  Future<FootprintResult> scanImage(
    List<int> imageBytes, {
    String filename = 'capture.jpg',
  }) async {
    final uri = Uri.parse(baseUrl).replace(
      path: '/scan',
      queryParameters: {'lang': lang},
    );

    try {
      final request = http.MultipartRequest('POST', uri)
        ..files.add(http.MultipartFile.fromBytes(
          'file',
          imageBytes,
          filename: filename,
        ));

      final streamedResponse =
          await request.send().timeout(const Duration(seconds: 20));
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body) as Map<String, dynamic>;
        return FootprintResult.fromJson(json);
      } else if (response.statusCode == 404) {
        throw FootprintNotFoundException('scanned item');
      } else {
        throw FootprintApiException(
            'Scan error ${response.statusCode}: ${response.body}');
      }
    } on FootprintNotFoundException {
      rethrow;
    } catch (e) {
      if (e is! FootprintApiException) {
        // Phase 1 mock
        return _mockFallback('rice (mock scan)');
      }
      rethrow;
    }
  }

  // ─── Mock fallback (Phase 1 only) ─────────────────────────────────────────

  /// Returns a realistic mock [FootprintResult] so Shaurya can build and test
  /// the UI before Aryaveer's backend is deployed.
  FootprintResult _mockFallback(String item) {
    return FootprintResult(
      item: item.isEmpty ? 'rice' : item,
      greenWf: 1200,
      blueWf: 300,
      greyWf: 100,
      unit: 'litres/kg',
      tip: 'Try lentils — they use 50% less water than rice.',
      comparison: 'Equivalent to ~10 full bathtubs.',
    );
  }
}

// ─── Custom exceptions ────────────────────────────────────────────────────────

class FootprintNotFoundException implements Exception {
  final String item;
  FootprintNotFoundException(this.item);

  @override
  String toString() => 'FootprintNotFoundException: "$item" not found in DB.';
}

class FootprintApiException implements Exception {
  final String message;
  FootprintApiException(this.message);

  @override
  String toString() => 'FootprintApiException: $message';
}
