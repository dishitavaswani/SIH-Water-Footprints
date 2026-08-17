import 'package:flutter/material.dart';
import '../l10n/app_localizations.dart';
import '../models/footprint_result.dart';
import '../models/load_state.dart';
import '../services/footprint_api_service.dart';
import '../services/history_service.dart';
import '../widgets/loading_spinner.dart';
import '../widgets/error_widget.dart' as wf;
import '../widgets/fun_facts_ticker.dart';

/// SearchScreen — Phase 1 + 3 + 4 + Improvements 3, 8, 11
///
/// • Coloured category chips (green=plant, red=meat, amber=fruit)
/// • Recent search history (last 5, persisted via SharedPreferences)
/// • Rotating fun facts ticker at the top
class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final TextEditingController _controller = TextEditingController();
  final FootprintApiService _api = FootprintApiService();

  LoadState _state = LoadState.idle;
  String? _errorMessage;
  List<String> _history = [];

  // ── Chip data: (label, emoji, color, category) ─────────────────────────
  static const _quickPicks = [
    ('Rice',    '🌾', Color(0xFF2DC653)),
    ('Wheat',   '🌾', Color(0xFF2DC653)),
    ('Lentils', '🫘', Color(0xFF2DC653)),
    ('Potato',  '🥔', Color(0xFF2DC653)),
    ('Mango',   '🥭', Color(0xFFFF9500)),
    ('Chicken', '🍗', Color(0xFFD62246)),
  ];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final h = await HistoryService.getHistory();
    if (mounted) setState(() => _history = h);
  }

  // ─── Search ───────────────────────────────────────────────────────────────

  Future<void> _search([String? override]) async {
    final query = (override ?? _controller.text).trim();
    if (query.isEmpty) return;

    setState(() {
      _state = LoadState.loading;
      _errorMessage = null;
    });

    // Save to history immediately
    await HistoryService.saveSearch(query);
    _loadHistory();

    try {
      final result = await _api.getFootprint(query);
      if (!mounted) return;
      await Navigator.pushNamed(context, '/result', arguments: result);
      if (mounted) setState(() => _state = LoadState.idle);
    } on FootprintNotFoundException {
      final l10n = AppLocalizations.of(context)!;
      setState(() {
        _state = LoadState.error;
        _errorMessage = l10n.noDataFound(query);
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

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  // ─── Build ────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // ── Improvement #11: Fun facts ticker ──────────────────────────
            const FunFactsTicker(),

            // ── Heading ────────────────────────────────────────────────────
            Text(
              l10n.searchHeading,
              style: const TextStyle(
                fontSize: 25,
                fontWeight: FontWeight.bold,
                color: Color(0xFF003566),
                height: 1.3,
              ),
            ),
            const SizedBox(height: 7),
            Text(
              l10n.searchSubtitle,
              style: const TextStyle(fontSize: 13.5, color: Colors.grey),
            ),

            const SizedBox(height: 22),

            // ── Search field ───────────────────────────────────────────────
            TextField(
              controller: _controller,
              onSubmitted: (_) => _search(),
              textInputAction: TextInputAction.search,
              decoration: InputDecoration(
                labelText: l10n.searchLabel,
                hintText: l10n.searchHint,
                prefixIcon:
                    const Icon(Icons.search, color: Color(0xFF0077B6)),
                suffixIcon: _controller.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear, size: 18),
                        onPressed: () {
                          _controller.clear();
                          setState(() {
                            _state = LoadState.idle;
                            _errorMessage = null;
                          });
                        },
                      )
                    : null,
              ),
              onChanged: (_) => setState(() {}),
            ),

            const SizedBox(height: 12),

            // ── Error ──────────────────────────────────────────────────────
            if (_state == LoadState.error && _errorMessage != null) ...[
              wf.FootprintErrorWidget(
                message: _errorMessage!,
                onRetry: () => _search(),
              ),
              const SizedBox(height: 10),
            ],

            // ── Search button / spinner ────────────────────────────────────
            if (_state == LoadState.loading)
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 4),
                child: WaterLoadingSpinner(),
              )
            else
              ElevatedButton.icon(
                onPressed: _search,
                icon: const Icon(Icons.water_drop, size: 18),
                label: Text(l10n.searchButton),
              ),

            const SizedBox(height: 24),

            // ── Improvement #8: Recent history ─────────────────────────────
            if (_history.isNotEmpty) ...[
              _SectionHeader(
                title: 'Recent',
                trailing: TextButton(
                  onPressed: () async {
                    await HistoryService.clearHistory();
                    _loadHistory();
                  },
                  style: TextButton.styleFrom(
                    foregroundColor: Colors.grey,
                    padding: EdgeInsets.zero,
                    minimumSize: Size.zero,
                    tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  ),
                  child: const Text('Clear', style: TextStyle(fontSize: 12)),
                ),
              ),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: _history
                    .map(
                      (item) => ActionChip(
                        label: Text(item),
                        avatar: const Icon(Icons.history,
                            size: 14, color: Colors.grey),
                        onPressed: () {
                          _controller.text = item;
                          _search(item);
                        },
                        backgroundColor: Colors.grey.withOpacity(0.1),
                        labelStyle: const TextStyle(fontSize: 13),
                      ),
                    )
                    .toList(),
              ),
              const SizedBox(height: 20),
            ],

            // ── Improvement #3: Colour-coded quick picks ───────────────────
            const _SectionHeader(title: 'Popular items'),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _quickPicks
                  .map(
                    (pick) => _CategoryChip(
                      label: pick.$1,
                      emoji: pick.$2,
                      color: pick.$3,
                      onTap: () {
                        _controller.text = pick.$1;
                        _search(pick.$1);
                      },
                    ),
                  )
                  .toList(),
            ),

            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}

// ─── Sub-widgets ──────────────────────────────────────────────────────────────

class _SectionHeader extends StatelessWidget {
  final String title;
  final Widget? trailing;

  const _SectionHeader({required this.title, this.trailing});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontWeight: FontWeight.w700,
            color: Colors.grey,
            fontSize: 12,
            letterSpacing: 0.5,
          ),
        ),
        if (trailing != null) trailing!,
      ],
    );
  }
}

/// Improvement #3 — colour-coded chip by food category.
class _CategoryChip extends StatelessWidget {
  final String label;
  final String emoji;
  final Color color;
  final VoidCallback onTap;

  const _CategoryChip({
    required this.label,
    required this.emoji,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: color.withOpacity(0.35)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(emoji, style: const TextStyle(fontSize: 14)),
            const SizedBox(width: 6),
            Text(
              label,
              style: TextStyle(
                color: color.withOpacity(0.85),
                fontWeight: FontWeight.w600,
                fontSize: 13,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
