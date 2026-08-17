import 'package:flutter/material.dart';

/// Color-coded water footprint bar with animated fill — Improvement #1.
///
/// On mount the bar animates from 0 → [value/total] over 900ms
/// using an elastic ease curve for a satisfying reveal.
class FootprintVisualBar extends StatelessWidget {
  final String label;
  final String sublabel;
  final double value;
  final double total;
  final Color color;
  final IconData icon;

  const FootprintVisualBar({
    super.key,
    required this.label,
    required this.sublabel,
    required this.value,
    required this.total,
    required this.color,
    required this.icon,
  });

  double get _fraction =>
      total == 0 ? 0 : (value / total).clamp(0.0, 1.0);

  @override
  Widget build(BuildContext context) {
    final pct = (_fraction * 100).toStringAsFixed(1);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      decoration: BoxDecoration(
        color: isDark
            ? color.withOpacity(0.12)
            : color.withOpacity(0.07),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: color.withOpacity(isDark ? 0.3 : 0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ── Label row ──
          Row(
            children: [
              Icon(icon, color: color, size: 18),
              const SizedBox(width: 8),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      label,
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: color,
                        fontSize: 14,
                      ),
                    ),
                    Text(
                      sublabel,
                      style: const TextStyle(color: Colors.grey, fontSize: 11),
                    ),
                  ],
                ),
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(
                    '${value.toStringAsFixed(0)} L/kg',
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  Text(
                    '$pct%',
                    style: TextStyle(
                      color: color,
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ],
          ),

          const SizedBox(height: 10),

          // ── Animated progress bar — Improvement #1 ──
          TweenAnimationBuilder<double>(
            tween: Tween<double>(begin: 0.0, end: _fraction),
            duration: const Duration(milliseconds: 900),
            curve: Curves.easeOutCubic,
            builder: (context, animValue, _) {
              return ClipRRect(
                borderRadius: BorderRadius.circular(6),
                child: LinearProgressIndicator(
                  value: animValue,
                  minHeight: 10,
                  backgroundColor: color.withOpacity(isDark ? 0.2 : 0.15),
                  valueColor: AlwaysStoppedAnimation<Color>(color),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
