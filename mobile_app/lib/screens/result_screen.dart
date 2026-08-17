import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';

import '../l10n/app_localizations.dart';
import '../models/footprint_result.dart';
import '../widgets/footprint_visual_bar.dart';

/// ResultScreen — Phase 1 + 2 + 3 + 4 + Improvements 6 & 7
///
/// • Improvement #6: Water footprint severity badge (Low/Medium/High/Very High)
/// • Improvement #7: Share button — copies formatted summary via share_plus
class ResultScreen extends StatelessWidget {
  final FootprintResult result;

  const ResultScreen({super.key, required this.result});

  // ── Improvement #6: severity classification ───────────────────────────────
  _Severity _getSeverity(double total) {
    if (total < 500)  return _Severity('Low',       const Color(0xFF2DC653), Icons.water_drop_outlined);
    if (total < 1500) return _Severity('Medium',    const Color(0xFFFFB800), Icons.water_outlined);
    if (total < 3000) return _Severity('High',      const Color(0xFFFF6B35), Icons.waves);
    return              _Severity('Very High',       const Color(0xFFD62246), Icons.warning_amber_rounded);
  }

  // ── Improvement #7: share ─────────────────────────────────────────────────
  void _share(AppLocalizations l10n) {
    final total = result.totalWf;
    final severity = _getSeverity(total);
    final text = '💧 Water Footprint: ${_cap(result.item)}\n'
        '${severity.icon == Icons.water_drop_outlined ? '🟢' : severity.icon == Icons.water_outlined ? '🟡' : severity.icon == Icons.waves ? '🟠' : '🔴'} '
        'Severity: ${severity.label}\n\n'
        'Total: ${total.toStringAsFixed(0)} ${result.unit}\n'
        '🟢 Green: ${result.greenWf.toStringAsFixed(0)} L/kg\n'
        '🔵 Blue:  ${result.blueWf.toStringAsFixed(0)} L/kg\n'
        '⚫ Grey:  ${result.greyWf.toStringAsFixed(0)} L/kg\n'
        '${result.tip != null ? '\n💡 Tip: ${result.tip}' : ''}\n\n'
        'Checked with Water Footprint App (SIH 2024)';

    Share.share(text, subject: 'Water Footprint of ${_cap(result.item)}');
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final total = result.totalWf;
    final severity = _getSeverity(total);

    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      appBar: AppBar(
        title: Text(_cap(result.item), overflow: TextOverflow.ellipsis),
        actions: [
          // Improvement #7 — share icon
          IconButton(
            icon: const Icon(Icons.share_outlined),
            tooltip: 'Share',
            onPressed: () => _share(l10n),
          ),
          IconButton(
            icon: const Icon(Icons.search),
            tooltip: l10n.searchAgain,
            onPressed: () => Navigator.pop(context),
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ── Hero banner ──────────────────────────────────────────────
              _HeroBanner(
                result: result,
                total: total,
                severity: severity,
                l10n: l10n,
              ),

              const SizedBox(height: 22),

              // ── Breakdown heading ─────────────────────────────────────────
              Text(
                l10n.waterBreakdown,
                style: const TextStyle(
                  fontSize: 17,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF003566),
                ),
              ),
              const SizedBox(height: 3),
              Text(
                l10n.allValuesIn(result.unit),
                style: const TextStyle(color: Colors.grey, fontSize: 12.5),
              ),
              const SizedBox(height: 12),

              // ── Animated visual bars — Improvement #1 ────────────────────
              FootprintVisualBar(
                label: l10n.greenWater,
                sublabel: l10n.greenWaterSub,
                value: result.greenWf,
                total: total,
                color: const Color(0xFF2DC653),
                icon: Icons.grass,
              ),
              const SizedBox(height: 10),
              FootprintVisualBar(
                label: l10n.blueWater,
                sublabel: l10n.blueWaterSub,
                value: result.blueWf,
                total: total,
                color: const Color(0xFF0077B6),
                icon: Icons.water_drop,
              ),
              const SizedBox(height: 10),
              FootprintVisualBar(
                label: l10n.greyWater,
                sublabel: l10n.greyWaterSub,
                value: result.greyWf,
                total: total,
                color: const Color(0xFF8B8B8B),
                icon: Icons.cloud,
              ),

              const SizedBox(height: 22),

              // ── Comparison card ───────────────────────────────────────────
              if (result.comparison != null) ...[
                _InfoCard(
                  icon: Icons.compare_arrows_rounded,
                  color: const Color(0xFF0077B6),
                  title: l10n.perspective,
                  body: result.comparison!,
                ),
                const SizedBox(height: 10),
              ],

              // ── Eco tip card ──────────────────────────────────────────────
              if (result.tip != null) ...[
                _InfoCard(
                  icon: Icons.eco_rounded,
                  color: const Color(0xFF2DC653),
                  title: l10n.ecoTip,
                  body: result.tip!,
                ),
                const SizedBox(height: 22),
              ],

              // ── CTA ───────────────────────────────────────────────────────
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: () => Navigator.pop(context),
                      icon: const Icon(Icons.search, size: 18),
                      label: Text(l10n.searchAgain),
                    ),
                  ),
                  const SizedBox(width: 10),
                  OutlinedButton(
                    onPressed: () => _share(l10n),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.all(14),
                      minimumSize: Size.zero,
                    ),
                    child: const Icon(Icons.share_outlined, size: 20),
                  ),
                ],
              ),

              const SizedBox(height: 8),
            ],
          ),
        ),
      ),
    );
  }

  String _cap(String s) =>
      s.isEmpty ? s : s[0].toUpperCase() + s.substring(1);
}

// ─── Severity data class ──────────────────────────────────────────────────────

class _Severity {
  final String label;
  final Color color;
  final IconData icon;
  const _Severity(this.label, this.color, this.icon);
}

// ─── Hero banner ──────────────────────────────────────────────────────────────

class _HeroBanner extends StatelessWidget {
  final FootprintResult result;
  final double total;
  final _Severity severity;
  final AppLocalizations l10n;

  const _HeroBanner({
    required this.result,
    required this.total,
    required this.severity,
    required this.l10n,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF023E8A), Color(0xFF0096C7)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF0077B6).withOpacity(0.3),
            blurRadius: 16,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Item name
          Row(
            children: [
              const Icon(Icons.water_drop, color: Colors.white70, size: 20),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  _cap(result.item),
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),

          const SizedBox(height: 12),

          // Improvement #6: Severity badge
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
            decoration: BoxDecoration(
              color: severity.color.withOpacity(0.25),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: severity.color.withOpacity(0.6)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(severity.icon, size: 14, color: severity.color),
                const SizedBox(width: 6),
                Text(
                  '${severity.label} water footprint',
                  style: TextStyle(
                    color: severity.color,
                    fontWeight: FontWeight.bold,
                    fontSize: 12.5,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 14),

          // G / B / Gr mini stats
          Row(
            children: [
              _MiniStat(label: 'Green', value: result.greenWf, color: const Color(0xFF52CE6D)),
              const SizedBox(width: 8),
              _MiniStat(label: 'Blue',  value: result.blueWf,  color: const Color(0xFF90E0EF)),
              const SizedBox(width: 8),
              _MiniStat(label: 'Grey',  value: result.greyWf,  color: const Color(0xFFBBBBBB)),
            ],
          ),

          const Divider(color: Colors.white24, height: 22),

          // Total
          Row(
            children: [
              Text('${l10n.totalLabel}: ',
                  style: const TextStyle(color: Colors.white70, fontSize: 14)),
              Text(
                '${total.toStringAsFixed(0)} ${result.unit}',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  String _cap(String s) =>
      s.isEmpty ? s : s[0].toUpperCase() + s.substring(1);
}

class _MiniStat extends StatelessWidget {
  final String label;
  final double value;
  final Color color;

  const _MiniStat({required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.15),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        children: [
          Text(
            value.toStringAsFixed(0),
            style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 14),
          ),
          Text(label,
              style: const TextStyle(color: Colors.white60, fontSize: 10)),
        ],
      ),
    );
  }
}

// ─── Info card ────────────────────────────────────────────────────────────────

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
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(isDark ? 0.12 : 0.07),
        borderRadius: BorderRadius.circular(16),
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
                Text(title,
                    style: TextStyle(fontWeight: FontWeight.bold, color: color, fontSize: 14)),
                const SizedBox(height: 4),
                Text(body, style: const TextStyle(fontSize: 14, height: 1.45)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
