import 'package:flutter/material.dart';

/// ScanScreen — Phase 2 placeholder.
///
/// Camera capture UI will be implemented in Phase 2 using image_picker.
/// The POST /scan API integration and ResultScreen navigation will be added then.
class ScanScreen extends StatelessWidget {
  const ScanScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📷 Scan Food Item')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.camera_alt_outlined,
                size: 72, color: Color(0xFF0077B6)),
            const SizedBox(height: 16),
            const Text(
              'Camera scan coming in Phase 2',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 8),
            const Text(
              'Will call POST /scan with image_picker capture.',
              style: TextStyle(fontSize: 13, color: Colors.grey),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.arrow_back),
              label: const Text('Back to Search'),
            ),
          ],
        ),
      ),
    );
  }
}
