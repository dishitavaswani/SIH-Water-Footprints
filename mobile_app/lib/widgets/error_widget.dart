import 'package:flutter/material.dart';

/// FootprintErrorWidget — displays offline, 404, or generic error states.
///
/// Shows an appropriate icon and message. The caller can optionally provide
/// an [onRetry] callback to show a Retry button.
class FootprintErrorWidget extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const FootprintErrorWidget({
    super.key,
    required this.message,
    this.onRetry,
  });

  /// Detects whether the error is likely a connectivity problem.
  bool get _isOffline =>
      message.toLowerCase().contains('socket') ||
      message.toLowerCase().contains('connection') ||
      message.toLowerCase().contains('network') ||
      message.toLowerCase().contains('timeout');

  /// Detects whether the error is a 404 / not-found.
  bool get _isNotFound =>
      message.toLowerCase().contains('not found') ||
      message.toLowerCase().contains('no data');

  @override
  Widget build(BuildContext context) {
    final IconData icon = _isOffline
        ? Icons.wifi_off_rounded
        : _isNotFound
            ? Icons.search_off_rounded
            : Icons.error_outline_rounded;

    const Color errorColor = Color(0xFFD62246);

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: errorColor.withOpacity(0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: errorColor.withOpacity(0.3)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Icon(icon, color: errorColor, size: 22),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  message,
                  style: TextStyle(
                    color: errorColor,
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
            ],
          ),
          if (onRetry != null) ...[
            const SizedBox(height: 10),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh, size: 16),
                label: const Text('Retry'),
                style: TextButton.styleFrom(foregroundColor: errorColor),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
