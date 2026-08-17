import 'package:flutter/material.dart';
import '../models/footprint_result.dart';
import '../widgets/footprint_visual_bar.dart';

/// ResultScreen — Phase 1
///
/// Displays the water footprint breakdown for a searched food item.
/// Receives a [FootprintResult] via Navigator arguments.
///
/// Shows:
/// - Item name
/// - Green / Blue / Grey visual bars (coloured + %)
/// - Total footprint
/// - Comparison string (from DB)
/// - Eco tip
class ResultScreen extends StatelessWidget {
  final FootprintResult result;

  const ResultScreen({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    final total = result.totalWf;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          _capitalize(result.item),
          overflow: TextOverflow.ellipsis,
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            tooltip: 'Search again',
            onPressed: () => Navigator.pop(context),
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ── Title banner ──
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF0077B6), Color(0xFF00B4D8)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _capitalize(result.item),
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Total: ${total.toStringAsFixed(0)} ${result.unit}',
                      style: const TextStyle(
                        color: Colors.white70,
                        fontSize: 16,
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 28),

              // ── Breakdown header ──
              const Text(
                'Water Breakdown',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF003566),
                ),
              ),
              const SizedBox(height: 4),
              Text(
                'All values in ${result.unit}',
                style: const TextStyle(color: Colors.grey, fontSize: 13),
              ),
              const SizedBox(height: 16),

              // ── Visual bars ──
              FootprintVisualBar(
                label: 'Green Water',
                sublabel: 'Rain-fed (agriculture)',
                value: result.greenWf,
                total: total,
                color: const Color(0xFF2DC653),
                icon: Icons.grass,
              ),
              const SizedBox(height: 12),
              FootprintVisualBar(
                label: 'Blue Water',
                sublabel: 'Surface & groundwater',
                value: result.blueWf,
                total: total,
                color: const Color(0xFF0077B6),
                icon: Icons.water_drop,
              ),
              const SizedBox(height: 12),
              FootprintVisualBar(
                label: 'Grey Water',
                sublabel: 'Pollution dilution',
                value: result.greyWf,
                total: total,
                color: const Color(0xFF9A9A9A),
                icon: Icons.cloud,
              ),

              const SizedBox(height: 28),

              // ── Comparison card ──
              if (result.comparison != null) ...[
                _InfoCard(
                  icon: Icons.compare_arrows,
                  color: const Color(0xFF0077B6),
                  title: 'Put it in perspective',
                  body: result.comparison!,
                ),
                const SizedBox(height: 14),
              ],

              // ── Eco tip card ──
              if (result.tip != null) ...[
                _InfoCard(
                  icon: Icons.eco,
                  color: const Color(0xFF2DC653),
                  title: 'Eco Tip',
                  body: result.tip!,
                ),
                const SizedBox(height: 28),
              ],

              // ── Search again CTA ──
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () => Navigator.pop(context),
                  icon: const Icon(Icons.search),
                  label: const Text('Search Another Item'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _capitalize(String s) =>
      s.isEmpty ? s : s[0].toUpperCase() + s.substring(1);
}

// ─── Helper widget ─────────────────────────────────────────────────────────────

class _InfoCard extends StatelessWidget {
  final IconData icon;
  final Color color;
  final String title;
  final String body;

  const _InfoCard({
    required this.icon,
    required this.color,
    required this.title,
    required this.body,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.08),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: color.withOpacity(0.25)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 22),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: color,
                    fontSize: 14,
                  ),
                ),
                const SizedBox(height: 4),
                Text(body,
                    style: const TextStyle(fontSize: 14, height: 1.4)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
