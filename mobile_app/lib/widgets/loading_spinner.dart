import 'package:flutter/material.dart';

/// WaterLoadingSpinner — animated loading indicator used during API calls.
///
/// Shows a pulsing water-drop icon with a circular progress indicator.
class WaterLoadingSpinner extends StatelessWidget {
  const WaterLoadingSpinner({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          SizedBox(
            height: 40,
            width: 40,
            child: CircularProgressIndicator(
              color: Color(0xFF0077B6),
              strokeWidth: 3,
            ),
          ),
          SizedBox(height: 12),
          Text(
            'Calculating footprint…',
            style: TextStyle(color: Colors.grey, fontSize: 13),
          ),
        ],
      ),
    );
  }
}
