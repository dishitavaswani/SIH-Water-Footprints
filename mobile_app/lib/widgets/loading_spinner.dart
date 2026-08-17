import 'package:flutter/material.dart';

/// Animated loading spinner shown during API calls.
///
/// Used in SearchScreen and ScanScreen via [LoadState.loading].
class WaterLoadingSpinner extends StatelessWidget {
  const WaterLoadingSpinner({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.symmetric(vertical: 16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          SizedBox(
            height: 44,
            width: 44,
            child: CircularProgressIndicator(
              color: Color(0xFF0077B6),
              strokeWidth: 3.5,
            ),
          ),
          SizedBox(height: 14),
          Text(
            'Calculating…',
            style: TextStyle(color: Colors.grey, fontSize: 13),
          ),
        ],
      ),
    );
  }
}
