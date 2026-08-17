import 'dart:typed_data';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import '../l10n/app_localizations.dart';
import 'package:image_picker/image_picker.dart';

import '../models/footprint_result.dart';
import '../models/load_state.dart';
import '../services/footprint_api_service.dart';
import '../widgets/loading_spinner.dart';
import '../widgets/error_widget.dart' as wf;

/// ScanScreen — Phase 2 + 4
///
/// Camera / gallery capture UI. On image selection the image is sent
/// to POST /scan. Uses [LoadState] enum to drive UI states.
/// Does NOT own a Scaffold — lives inside HomeScreen's body.
class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final ImagePicker _picker = ImagePicker();
  final FootprintApiService _api = FootprintApiService();

  XFile? _pickedFile;
  Uint8List? _imageBytes;
  LoadState _state = LoadState.idle;
  String? _errorMessage;

  // ─── Image picking ────────────────────────────────────────────────────────

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? file = await _picker.pickImage(
        source: source,
        maxWidth: 800,
        maxHeight: 800,
        imageQuality: 85,
      );
      if (file == null) return; // user cancelled

      final bytes = await file.readAsBytes();
      setState(() {
        _pickedFile = file;
        _imageBytes = bytes;
        _state = LoadState.idle;
        _errorMessage = null;
      });
    } catch (e) {
      final l10n = AppLocalizations.of(context)!;
      setState(() {
        _state = LoadState.error;
        _errorMessage = l10n.errorGeneric;
      });
    }
  }

  // ─── Submit to API ────────────────────────────────────────────────────────

  Future<void> _submit() async {
    if (_imageBytes == null) return;

    setState(() {
      _state = LoadState.loading;
      _errorMessage = null;
    });

    try {
      final FootprintResult result = await _api.scanImage(
        _imageBytes!,
        filename: _pickedFile?.name ?? 'capture.jpg',
      );
      if (!mounted) return;
      await Navigator.pushNamed(context, '/result', arguments: result);
      // Back from result — reset
      if (mounted) {
        setState(() {
          _state = LoadState.idle;
          _pickedFile = null;
          _imageBytes = null;
        });
      }
    } on FootprintNotFoundException {
      final l10n = AppLocalizations.of(context)!;
      setState(() {
        _state = LoadState.error;
        _errorMessage = l10n.noDataFound('this item');
      });
    } on FootprintApiException catch (e) {
      setState(() {
        _state = LoadState.error;
        _errorMessage = e.message;
      });
    } catch (_) {
      final l10n = AppLocalizations.of(context)!;
      setState(() {
        _state = LoadState.error;
        _errorMessage = l10n.errorGeneric;
      });
    }
  }

  void _reset() {
    setState(() {
      _pickedFile = null;
      _imageBytes = null;
      _state = LoadState.idle;
      _errorMessage = null;
    });
  }

  // ─── Build ────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return SafeArea(
      child: SingleChildScrollView(
        padding:
            const EdgeInsets.symmetric(horizontal: 24, vertical: 28),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // ── Heading ──
            Text(
              l10n.scanHeading,
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Color(0xFF003566),
              ),
            ),
            const SizedBox(height: 8),
            Text(
              l10n.scanInstruction,
              style: const TextStyle(fontSize: 14, color: Colors.grey),
            ),

            const SizedBox(height: 24),

            // ── Image preview / placeholder ──
            _imageBytes != null
                ? _ImagePreview(
                    bytes: _imageBytes!,
                    onClear: _reset,
                  )
                : _CameraPlaceholder(l10n: l10n),

            const SizedBox(height: 20),

            // ── Error ──
            if (_state == LoadState.error && _errorMessage != null) ...[
              wf.FootprintErrorWidget(
                message: _errorMessage!,
                onRetry: _imageBytes != null ? _submit : null,
              ),
              const SizedBox(height: 12),
            ],

            // ── Action buttons ──
            if (_state == LoadState.loading) ...[
              const WaterLoadingSpinner(),
            ] else if (_imageBytes != null) ...[
              // Confirm: get footprint
              ElevatedButton.icon(
                onPressed: _submit,
                icon: const Icon(Icons.water_drop, size: 18),
                label: Text(l10n.scanConfirm),
              ),
              const SizedBox(height: 10),
              OutlinedButton.icon(
                onPressed: _reset,
                icon: const Icon(Icons.refresh, size: 18),
                label: Text(l10n.scanAgain),
              ),
            ] else ...[
              // Photo / gallery buttons
              ElevatedButton.icon(
                onPressed: kIsWeb
                    ? () => _pickImage(ImageSource.gallery)
                    : () => _pickImage(ImageSource.camera),
                icon: const Icon(Icons.camera_alt, size: 18),
                label: Text(
                    kIsWeb ? l10n.scanButtonGallery : l10n.scanButtonCamera),
              ),
              if (!kIsWeb) ...[
                const SizedBox(height: 10),
                OutlinedButton.icon(
                  onPressed: () => _pickImage(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library_outlined, size: 18),
                  label: Text(l10n.scanButtonGallery),
                ),
              ],
            ],

            const SizedBox(height: 24),

            // ── How it works card ──
            _HowItWorksCard(),
          ],
        ),
      ),
    );
  }
}

// ─── Sub-widgets ──────────────────────────────────────────────────────────────

class _CameraPlaceholder extends StatelessWidget {
  final AppLocalizations l10n;
  const _CameraPlaceholder({required this.l10n});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 220,
      decoration: BoxDecoration(
        color: const Color(0xFF0077B6).withOpacity(0.06),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: const Color(0xFF0077B6).withOpacity(0.2),
          style: BorderStyle.solid,
        ),
      ),
      child: const Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.camera_alt_outlined,
              size: 64, color: Color(0xFF0077B6)),
          SizedBox(height: 12),
          Text(
            'No image selected',
            style: TextStyle(color: Colors.grey, fontSize: 14),
          ),
        ],
      ),
    );
  }
}

class _ImagePreview extends StatelessWidget {
  final Uint8List bytes;
  final VoidCallback onClear;

  const _ImagePreview({required this.bytes, required this.onClear});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(20),
          child: Image.memory(
            bytes,
            height: 260,
            width: double.infinity,
            fit: BoxFit.cover,
          ),
        ),
        Positioned(
          top: 10,
          right: 10,
          child: GestureDetector(
            onTap: onClear,
            child: Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: Colors.black54,
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Icon(Icons.close, color: Colors.white, size: 18),
            ),
          ),
        ),
      ],
    );
  }
}

class _HowItWorksCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    const steps = [
      (Icons.camera_alt, 'Take a photo of any food item'),
      (Icons.psychology, 'AI identifies the food (MobileNet V2)'),
      (Icons.water_drop, 'Get green, blue & grey water footprint'),
    ];

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF0077B6).withOpacity(0.05),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
            color: const Color(0xFF0077B6).withOpacity(0.15)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'How it works',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: Color(0xFF003566),
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 10),
          ...steps.map(
            (step) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(
                children: [
                  Icon(step.$1, size: 18, color: const Color(0xFF0077B6)),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(step.$2,
                        style: const TextStyle(fontSize: 13)),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
