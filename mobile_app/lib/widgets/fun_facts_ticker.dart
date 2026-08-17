import 'dart:async';
import 'package:flutter/material.dart';

/// FunFactsTicker — Improvement #11
///
/// Auto-rotating banner of water-related facts.
/// Cycles every [intervalSeconds] using an AnimatedSwitcher fade+slide.
class FunFactsTicker extends StatefulWidget {
  final int intervalSeconds;

  const FunFactsTicker({super.key, this.intervalSeconds = 5});

  @override
  State<FunFactsTicker> createState() => _FunFactsTickerState();
}

class _FunFactsTickerState extends State<FunFactsTicker> {
  static const _facts = [
    ('💧', 'It takes 1,600 L of water to produce 1 kg of wheat.'),
    ('🌾', 'Agriculture uses 70% of all freshwater on Earth.'),
    ('🍗', 'Producing 1 kg of chicken requires ~4,300 L of water.'),
    ('🌍', 'Water scarcity affects over 2 billion people globally.'),
    ('🥬', 'Switching one beef meal to lentils saves ~15,000 L of water.'),
    ('🚿', 'A 5-minute shower uses ~65 L — rice uses 25× that per kg.'),
  ];

  int _currentIndex = 0;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(
      Duration(seconds: widget.intervalSeconds),
      (_) {
        if (mounted) {
          setState(() {
            _currentIndex = (_currentIndex + 1) % _facts.length;
          });
        }
      },
    );
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final (emoji, text) = _facts[_currentIndex];

    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: isDark
              ? [const Color(0xFF023E8A), const Color(0xFF0077B6)]
              : [const Color(0xFFE0F4FF), const Color(0xFFCAEEFF)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: const Color(0xFF0077B6).withOpacity(isDark ? 0.4 : 0.2),
        ),
      ),
      child: AnimatedSwitcher(
        duration: const Duration(milliseconds: 500),
        transitionBuilder: (child, anim) => FadeTransition(
          opacity: anim,
          child: SlideTransition(
            position: Tween<Offset>(
              begin: const Offset(0.08, 0),
              end: Offset.zero,
            ).animate(anim),
            child: child,
          ),
        ),
        child: Row(
          key: ValueKey<int>(_currentIndex),
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Text(emoji, style: const TextStyle(fontSize: 20)),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                text,
                style: TextStyle(
                  fontSize: 12.5,
                  color: isDark ? Colors.white : const Color(0xFF003566),
                  height: 1.35,
                ),
              ),
            ),
            const SizedBox(width: 6),
            // Dot indicator
            Column(
              mainAxisSize: MainAxisSize.min,
              children: List.generate(_facts.length, (i) {
                return Container(
                  width: 4,
                  height: 4,
                  margin: const EdgeInsets.symmetric(vertical: 2),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: i == _currentIndex
                        ? const Color(0xFF0077B6)
                        : const Color(0xFF0077B6).withOpacity(0.25),
                  ),
                );
              }),
            ),
          ],
        ),
      ),
    );
  }
}
