import 'package:flutter/material.dart';

/// Error widget for offline, 404, and generic API errors.
///
/// Auto-selects icon based on error message content.
/// Shows optional [onRetry] button.
class FootprintErrorWidget extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const FootprintErrorWidget({
    super.key,
    required this.message,
    this.onRetry,
  });

  bool get _isOffline =>
      message.toLowerCase().contains('socket') ||
      message.toLowerCase().contains('connection') ||
      message.toLowerCase().contains('network') ||
      message.toLowerCase().contains('timeout') ||
      message.toLowerCase().contains('offline');

  bool get _isNotFound =>
      message.toLowerCase().contains('not found') ||
      message.toLowerCase().contains('no data') ||
      message.toLowerCase().contains('नहीं मिला'); // Hindi 404

  @override
  Widget build(BuildContext context) {
    const errorColor = Color(0xFFD62246);

    final IconData icon = _isOffline
        ? Icons.wifi_off_rounded
        : _isNotFound
            ? Icons.search_off_rounded
            : Icons.error_outline_rounded;

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: errorColor.withOpacity(0.07),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: errorColor.withOpacity(0.3)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Icon(icon, color: errorColor, size: 22),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  message,
                  style: const TextStyle(
                    color: errorColor,
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
            ],
          ),
          if (onRetry != null) ...[
            const SizedBox(height: 8),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh, size: 16),
                label: const Text('Retry'),
                style: TextButton.styleFrom(
                  foregroundColor: errorColor,
                  padding: const EdgeInsets.symmetric(
                      horizontal: 12, vertical: 4),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
