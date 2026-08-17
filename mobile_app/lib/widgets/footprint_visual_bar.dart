import 'package:flutter/material.dart';

/// FootprintVisualBar — coloured progress bar for one water footprint tier.
///
/// Used in [ResultScreen] to display green / blue / grey breakdown visually.
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

  double get _fraction => total == 0 ? 0 : (value / total).clamp(0.0, 1.0);

  @override
  Widget build(BuildContext context) {
    final pct = (_fraction * 100).toStringAsFixed(1);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      decoration: BoxDecoration(
        color: color.withOpacity(0.07),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: color.withOpacity(0.2)),
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
              Text(
                '${value.toStringAsFixed(0)} L/kg',
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(width: 8),
              Text(
                '$pct%',
                style: TextStyle(color: color, fontWeight: FontWeight.bold),
              ),
            ],
          ),

          const SizedBox(height: 10),

          // ── Progress bar ──
          ClipRRect(
            borderRadius: BorderRadius.circular(6),
            child: LinearProgressIndicator(
              value: _fraction,
              minHeight: 10,
              backgroundColor: color.withOpacity(0.15),
              valueColor: AlwaysStoppedAnimation<Color>(color),
            ),
          ),
        ],
      ),
    );
  }
}
