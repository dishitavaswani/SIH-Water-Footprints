import 'package:flutter/material.dart';
import 'home_screen.dart';

/// SplashScreen — Improvement #2
///
/// Animated water-drop launch screen shown for ~2 seconds.
/// Uses a combined Scale + Fade + Ripple animation before
/// replacing itself with HomeScreen.
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with TickerProviderStateMixin {
  late final AnimationController _dropController;
  late final AnimationController _rippleController;
  late final AnimationController _textController;

  late final Animation<double> _dropScale;
  late final Animation<double> _dropOpacity;
  late final Animation<double> _rippleScale;
  late final Animation<double> _rippleOpacity;
  late final Animation<double> _textOpacity;
  late final Animation<Offset> _textSlide;

  @override
  void initState() {
    super.initState();

    // Drop: scale from 0.2 → 1.0, fade in
    _dropController = AnimationController(
      duration: const Duration(milliseconds: 700),
      vsync: this,
    );
    _dropScale = Tween<double>(begin: 0.2, end: 1.0).animate(
      CurvedAnimation(parent: _dropController, curve: Curves.elasticOut),
    );
    _dropOpacity = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
          parent: _dropController,
          curve: const Interval(0.0, 0.5, curve: Curves.easeIn)),
    );

    // Ripple: expand outward from the drop
    _rippleController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _rippleScale = Tween<double>(begin: 0.8, end: 2.5).animate(
      CurvedAnimation(parent: _rippleController, curve: Curves.easeOut),
    );
    _rippleOpacity = Tween<double>(begin: 0.4, end: 0.0).animate(
      CurvedAnimation(parent: _rippleController, curve: Curves.easeOut),
    );

    // Text: fade + slide up
    _textController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _textOpacity = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _textController, curve: Curves.easeIn),
    );
    _textSlide = Tween<Offset>(
      begin: const Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(parent: _textController, curve: Curves.easeOut));

    _runSequence();
  }

  Future<void> _runSequence() async {
    await Future.delayed(const Duration(milliseconds: 200));
    _dropController.forward();

    await Future.delayed(const Duration(milliseconds: 500));
    _rippleController.forward();

    await Future.delayed(const Duration(milliseconds: 300));
    _textController.forward();

    // Wait, then navigate
    await Future.delayed(const Duration(milliseconds: 1200));
    if (mounted) {
      Navigator.pushReplacement(
        context,
        PageRouteBuilder(
          pageBuilder: (_, __, ___) => const HomeScreen(),
          transitionsBuilder: (_, anim, __, child) =>
              FadeTransition(opacity: anim, child: child),
          transitionDuration: const Duration(milliseconds: 600),
        ),
      );
    }
  }

  @override
  void dispose() {
    _dropController.dispose();
    _rippleController.dispose();
    _textController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF023E8A),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // ── Drop + ripple ──────────────────────────────────────
            SizedBox(
              width: 160,
              height: 160,
              child: Stack(
                alignment: Alignment.center,
                children: [
                  // Ripple ring
                  AnimatedBuilder(
                    animation: _rippleController,
                    builder: (_, __) => Transform.scale(
                      scale: _rippleScale.value,
                      child: Opacity(
                        opacity: _rippleOpacity.value,
                        child: Container(
                          width: 80,
                          height: 80,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            border: Border.all(
                              color: const Color(0xFF90E0EF),
                              width: 3,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),

                  // Water drop icon
                  AnimatedBuilder(
                    animation: _dropController,
                    builder: (_, __) => Transform.scale(
                      scale: _dropScale.value,
                      child: Opacity(
                        opacity: _dropOpacity.value,
                        child: Container(
                          width: 90,
                          height: 90,
                          decoration: const BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: RadialGradient(
                              colors: [Color(0xFF90E0EF), Color(0xFF0096C7)],
                            ),
                          ),
                          child: const Icon(
                            Icons.water_drop,
                            size: 48,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 28),

            // ── App title text ─────────────────────────────────────
            AnimatedBuilder(
              animation: _textController,
              builder: (_, child) => SlideTransition(
                position: _textSlide,
                child: FadeTransition(
                  opacity: _textOpacity,
                  child: child,
                ),
              ),
              child: Column(
                children: [
                  const Text(
                    'Water Footprint',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 0.5,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Know your food\'s water cost',
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.7),
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 60),

            // ── Loading dots ──────────────────────────────────────
            AnimatedBuilder(
              animation: _textController,
              builder: (_, child) => FadeTransition(
                opacity: _textOpacity,
                child: child,
              ),
              child: const _LoadingDots(),
            ),
          ],
        ),
      ),
    );
  }
}

class _LoadingDots extends StatefulWidget {
  const _LoadingDots();

  @override
  State<_LoadingDots> createState() => _LoadingDotsState();
}

class _LoadingDotsState extends State<_LoadingDots>
    with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      duration: const Duration(milliseconds: 900),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _ctrl,
      builder: (_, __) {
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: List.generate(3, (i) {
            final delay = i / 3;
            final opacity = (((_ctrl.value - delay) % 1.0 + 1.0) % 1.0 < 0.4)
                ? 1.0
                : 0.3;
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4),
              child: Opacity(
                opacity: opacity,
                child: const CircleAvatar(
                  radius: 4,
                  backgroundColor: Color(0xFF90E0EF),
                ),
              ),
            );
          }),
        );
      },
    );
  }
}
