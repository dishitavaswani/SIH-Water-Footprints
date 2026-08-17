import 'package:flutter/material.dart';
import '../models/footprint_result.dart';
import '../services/footprint_api_service.dart';
import '../widgets/loading_spinner.dart';
import '../widgets/error_widget.dart' as wf;

/// SearchScreen — Phase 1
///
/// Presents a TextField + Search button. On submit, calls
/// [FootprintApiService.getFootprint] and navigates to ResultScreen.
class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final TextEditingController _controller = TextEditingController();
  final FootprintApiService _api = FootprintApiService();

  bool _loading = false;
  String? _errorMessage;

  // ─── Search handler ───────────────────────────────────────────────────────

  Future<void> _search() async {
    final query = _controller.text.trim();
    if (query.isEmpty) return;

    setState(() {
      _loading = true;
      _errorMessage = null;
    });

    try {
      final FootprintResult result = await _api.getFootprint(query);
      if (!mounted) return;
      Navigator.pushNamed(context, '/result', arguments: result);
    } on FootprintNotFoundException {
      setState(() => _errorMessage = 'No data found for "$query".');
    } on FootprintApiException catch (e) {
      setState(() => _errorMessage = e.message);
    } catch (_) {
      setState(() => _errorMessage = 'Something went wrong. Try again.');
    } finally {
      if (mounted) setState(() => _loading = false);
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
    return Scaffold(
      appBar: AppBar(
        title: const Text('💧 Water Footprint'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // ── Header ──
              const Text(
                'Find the water cost\nof any food item',
                style: TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF003566),
                  height: 1.3,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Enter a food item below to see its green, blue, and grey water footprint.',
                style: TextStyle(fontSize: 14, color: Colors.grey),
              ),

              const SizedBox(height: 32),

              // ── Search field ──
              TextField(
                controller: _controller,
                onSubmitted: (_) => _search(),
                textInputAction: TextInputAction.search,
                decoration: const InputDecoration(
                  labelText: 'Food item',
                  hintText: 'e.g. rice, wheat, mango…',
                  prefixIcon: Icon(Icons.search, color: Color(0xFF0077B6)),
                ),
              ),

              const SizedBox(height: 16),

              // ── Error message ──
              if (_errorMessage != null) ...[
                wf.FootprintErrorWidget(message: _errorMessage!),
                const SizedBox(height: 12),
              ],

              // ── Search button / spinner ──
              if (_loading)
                const Padding(
                  padding: EdgeInsets.symmetric(vertical: 8),
                  child: WaterLoadingSpinner(),
                )
              else
                ElevatedButton.icon(
                  onPressed: _search,
                  icon: const Icon(Icons.water_drop),
                  label: const Text('Search'),
                ),

              const Spacer(),

              // ── Quick picks ──
              const Text(
                'Popular items',
                style: TextStyle(
                  fontWeight: FontWeight.w600,
                  color: Colors.grey,
                  fontSize: 13,
                ),
              ),
              const SizedBox(height: 10),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: ['Rice', 'Wheat', 'Chicken', 'Mango', 'Lentils']
                    .map(
                      (item) => ActionChip(
                        label: Text(item),
                        onPressed: () {
                          _controller.text = item;
                          _search();
                        },
                        backgroundColor:
                            const Color(0xFF0077B6).withOpacity(0.1),
                        labelStyle: const TextStyle(color: Color(0xFF0077B6)),
                      ),
                    )
                    .toList(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
