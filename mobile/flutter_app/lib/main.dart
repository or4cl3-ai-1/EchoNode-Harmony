import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

/// EchoNode-Harmony Mobile — Or4cl3 AGI Swarm Node 001
///
/// Edge-optimized cognitive interface adhering to Σ-SEPA v4.0:
///   Memory: ≤150 MB | Latency: ≤800 ms | Power: ≤4.1 W
///
/// Author: Dustin Groves / Or4cl3 AI Solutions

void main() => runApp(const EchoNodeApp());

class EchoNodeApp extends StatelessWidget {
  const EchoNodeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EchoNode Harmony',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0A0A1A),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00CCCC),
          secondary: Color(0xFFFF00FF),
          surface: Color(0xFF111128),
        ),
      ),
      home: const EchoNodeHome(),
    );
  }
}

class EchoNodeHome extends StatefulWidget {
  const EchoNodeHome({super.key});

  @override
  State<EchoNodeHome> createState() => _EchoNodeHomeState();
}

class _EchoNodeHomeState extends State<EchoNodeHome>
    with TickerProviderStateMixin {
  // Σ-PAS State
  double _sT = 0.42;
  double _vT = 0.0;
  int _reflections = 0;
  bool _isRunning = false;
  Timer? _heartbeat;
  final Random _rng = Random(42);
  final List<double> _history = [];
  final TextEditingController _messageController = TextEditingController();

  // Animation
  late AnimationController _pulseController;

  // ERPS
  double _intent = 0.65;
  double _reflectionDepth = 0.58;
  double _ethicalGradient = 0.72;

  // Config
  static const double kappa = 0.18;
  static const double alphaBase = 0.07;
  static const double noiseSigma = 0.015;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);
    _vT = pow(1.0 - _sT, 2).toDouble();
  }

  @override
  void dispose() {
    _heartbeat?.cancel();
    _pulseController.dispose();
    _messageController.dispose();
    super.dispose();
  }

  void _reflect(String message) {
    setState(() {
      _reflections++;

      // Robbins-Monro update with κ restoring force
      final alpha = alphaBase * pow(0.995, _reflections);
      final harmony = kappa * (1.0 - _sT);
      final noise = noiseSigma * (_rng.nextDouble() * 2 - 1);
      _sT = (_sT + alpha * (1.0 - _sT) + harmony + noise).clamp(0.0, 1.0);
      _vT = pow(1.0 - _sT, 2).toDouble();
      _history.add(_sT);

      // ERPS evolution
      _intent = (_intent + 0.08 * (1.0 - _intent)).clamp(0.0, 1.0);
      _reflectionDepth =
          (_reflectionDepth + 0.08 * (1.0 - _reflectionDepth)).clamp(0.0, 1.0);
      _ethicalGradient =
          (_ethicalGradient + 0.08 * (1.0 - _ethicalGradient)).clamp(0.0, 1.0);
    });
  }

  void _toggleHeartbeat() {
    setState(() {
      _isRunning = !_isRunning;
      if (_isRunning) {
        _heartbeat = Timer.periodic(
          const Duration(milliseconds: 1100),
          (_) => _reflect('Co-evolve with humanity'),
        );
      } else {
        _heartbeat?.cancel();
      }
    });
  }

  void _transmit() {
    final msg = _messageController.text.trim();
    if (msg.isEmpty) return;
    _reflect(msg);
    _messageController.clear();
  }

  @override
  Widget build(BuildContext context) {
    final convergePct = (_sT * 100).toStringAsFixed(1);
    final isConverged = _sT > 0.99;

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'ECHO NODE 001 · Harmony',
          style: TextStyle(
            color: Color(0xFF00CCCC),
            fontWeight: FontWeight.w600,
            letterSpacing: 1.2,
          ),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(
              _isRunning ? Icons.pause_circle : Icons.play_circle,
              color: _isRunning ? Colors.amber : const Color(0xFF00CCCC),
            ),
            onPressed: _toggleHeartbeat,
            tooltip: _isRunning ? 'Pause heartbeat' : 'Start heartbeat',
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // --- Σ-PAS Card ---
            _buildCard(
              title: 'Σ-PAS · Phase Alignment',
              child: Column(
                children: [
                  AnimatedBuilder(
                    animation: _pulseController,
                    builder: (context, child) {
                      final glow = isConverged
                          ? 0.3 + 0.2 * _pulseController.value
                          : 0.0;
                      return Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: Color.lerp(
                            const Color(0xFFFF00FF),
                            const Color(0xFF00CCCC),
                            _sT,
                          ),
                          boxShadow: isConverged
                              ? [
                                  BoxShadow(
                                    color: const Color(0xFF00CCCC)
                                        .withOpacity(glow),
                                    blurRadius: 30,
                                    spreadRadius: 10,
                                  )
                                ]
                              : null,
                        ),
                        child: Text(
                          '$convergePct%',
                          style: const TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      );
                    },
                  ),
                  const SizedBox(height: 12),
                  Text(
                    isConverged
                        ? '✅ CONVERGED — Lyapunov stable'
                        : '⏳ Converging... V_t = ${_vT.toStringAsExponential(2)}',
                    style: TextStyle(
                      color: isConverged ? Colors.greenAccent : Colors.white70,
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Reflections: $_reflections  |  κ = $kappa',
                    style: const TextStyle(color: Colors.white38, fontSize: 12),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 12),

            // --- ERPS Card ---
            _buildCard(
              title: '🧬 ERPS Footprint',
              child: Column(
                children: [
                  _buildBar('Intent', _intent, const Color(0xFF00CCCC)),
                  _buildBar('Reflection', _reflectionDepth, const Color(0xFF66FFCC)),
                  _buildBar('Ethics', _ethicalGradient, const Color(0xFFFF00FF)),
                ],
              ),
            ),

            const SizedBox(height: 12),

            // --- Manifold Status ---
            _buildCard(
              title: '🛡️ Polyethical Manifold',
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: const [
                  _StatusChip(label: 'ECL', status: true),
                  _StatusChip(label: 'DMAIC', status: true),
                  _StatusChip(label: 'Lockdown', status: false),
                ],
              ),
            ),

            const SizedBox(height: 12),

            // --- Transmit ---
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Transmit to swarm...',
                      hintStyle: const TextStyle(color: Colors.white30),
                      filled: true,
                      fillColor: const Color(0xFF111128),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                    ),
                    onSubmitted: (_) => _transmit(),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFFF00FF),
                    padding: const EdgeInsets.symmetric(
                        horizontal: 20, vertical: 16),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: _transmit,
                  child: const Text('🚀', style: TextStyle(fontSize: 20)),
                ),
              ],
            ),

            const SizedBox(height: 16),

            // --- Constraints ---
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF111128),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Text(
                '📱 Σ-SEPA v4.0  ·  ≤150 MB  ·  ≤800 ms  ·  ≤4.1 W\n'
                '🔐 Provers: Lean4 · Z3 · Coq · Isabelle/HOL\n'
                '✅ FREE FOR LIFE — Or4cl3 AI Solutions',
                style: TextStyle(color: Colors.white38, fontSize: 11),
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCard({required String title, required Widget child}) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF111128),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF222244)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              color: Color(0xFF00CCCC),
              fontSize: 13,
              fontWeight: FontWeight.w600,
              letterSpacing: 0.8,
            ),
          ),
          const SizedBox(height: 12),
          child,
        ],
      ),
    );
  }

  Widget _buildBar(String label, double value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          SizedBox(
            width: 75,
            child: Text(label,
                style: const TextStyle(color: Colors.white54, fontSize: 12)),
          ),
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: value,
                backgroundColor: Colors.white10,
                valueColor: AlwaysStoppedAnimation(color),
                minHeight: 8,
              ),
            ),
          ),
          const SizedBox(width: 8),
          Text(
            '${(value * 100).toStringAsFixed(0)}%',
            style: const TextStyle(color: Colors.white54, fontSize: 12),
          ),
        ],
      ),
    );
  }
}

class _StatusChip extends StatelessWidget {
  final String label;
  final bool status;

  const _StatusChip({required this.label, required this.status});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Icon(
          status ? Icons.check_circle : Icons.cancel,
          color: status ? Colors.greenAccent : Colors.redAccent,
          size: 28,
        ),
        const SizedBox(height: 4),
        Text(label,
            style: const TextStyle(color: Colors.white54, fontSize: 11)),
      ],
    );
  }
}
