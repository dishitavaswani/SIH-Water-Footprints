import 'package:flutter/material.dart';
import '../l10n/app_localizations.dart';

import '../models/footprint_result.dart';
import '../models/load_state.dart';
import '../services/footprint_api_service.dart';
import '../widgets/loading_spinner.dart';
import '../widgets/error_widget.dart' as wf;

/// SearchScreen — Phase 1 + 3 + 4
///
/// Text search for food items. Fully localised (EN/HI).
/// Drives UI via [LoadState] enum.
/// Does NOT own a Scaffold — lives inside HomeScreen's body.
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

  // ─── Search ───────────────────────────────────────────────────────────────

  Future<void> _search([String? override]) async {
    final query = (override ?? _controller.text).trim();
    if (query.isEmpty) return;

    setState(() {
      _state = LoadState.loading;
      _errorMessage = null;
    });

    try {
      final result = await _api.getFootprint(query);
      if (!mounted) return;
      // Pass the result to ResultScreen via Navigator args
      await Navigator.pushNamed(context, '/result', arguments: result);
      // Back on SearchScreen — reset to idle
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
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 28),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // ── Heading ──
            Text(
              l10n.searchHeading,
              style: const TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold,
                color: Color(0xFF003566),
                height: 1.3,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              l10n.searchSubtitle,
              style: const TextStyle(fontSize: 14, color: Colors.grey),
            ),

            const SizedBox(height: 28),

            // ── Search field ──
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
              onChanged: (_) => setState(() {}), // rebuild for suffix icon
            ),

            const SizedBox(height: 14),

            // ── Error ──
            if (_state == LoadState.error && _errorMessage != null) ...[
              wf.FootprintErrorWidget(
                message: _errorMessage!,
                onRetry: () => _search(),
              ),
              const SizedBox(height: 10),
            ],

            // ── Search button / spinner ──
            if (_state == LoadState.loading)
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 6),
                child: WaterLoadingSpinner(),
              )
            else
              ElevatedButton.icon(
                onPressed: _search,
                icon: const Icon(Icons.water_drop, size: 18),
                label: Text(l10n.searchButton),
              ),

            const Spacer(),

            // ── Quick picks ──
            Text(
              l10n.popularItems,
              style: const TextStyle(
                fontWeight: FontWeight.w600,
                color: Colors.grey,
                fontSize: 13,
              ),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _quickPicks(l10n)
                  .map(
                    (item) => ActionChip(
                      label: Text(item),
                      avatar: const Icon(Icons.water_drop_outlined,
                          size: 14, color: Color(0xFF0077B6)),
                      onPressed: () {
                        _controller.text = item;
                        _search(item);
                      },
                      backgroundColor:
                          const Color(0xFF0077B6).withOpacity(0.08),
                      labelStyle:
                          const TextStyle(color: Color(0xFF0077B6)),
                    ),
                  )
                  .toList(),
            ),
          ],
        ),
      ),
    );
  }

  // English labels for quick picks (search by English regardless of locale
  // since the API expects English item names)
  List<String> _quickPicks(AppLocalizations l10n) =>
      ['Rice', 'Wheat', 'Chicken', 'Mango', 'Lentils', 'Potato'];
}
