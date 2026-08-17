/// Data model for a water footprint API response.
///
/// Mirrors the JSON returned by GET /footprint:
/// {
///   "item": "rice",
///   "green_wf": 1200,
///   "blue_wf": 300,
///   "grey_wf": 100,
///   "unit": "litres/kg",
///   "tip": "..."
/// }
class FootprintResult {
  final String item;
  final double greenWf;  // Rain-fed water (agriculture)
  final double blueWf;   // Surface/ground water
  final double greyWf;   // Pollution dilution water
  final String unit;
  final String? tip;
  final String? comparison;

  const FootprintResult({
    required this.item,
    required this.greenWf,
    required this.blueWf,
    required this.greyWf,
    required this.unit,
    this.tip,
    this.comparison,
  });

  /// Total water footprint in the given unit.
  double get totalWf => greenWf + blueWf + greyWf;

  factory FootprintResult.fromJson(Map<String, dynamic> json) {
    return FootprintResult(
      item: json['item'] as String? ?? '',
      greenWf: (json['green_wf'] as num?)?.toDouble() ?? 0,
      blueWf: (json['blue_wf'] as num?)?.toDouble() ?? 0,
      greyWf: (json['grey_wf'] as num?)?.toDouble() ?? 0,
      unit: json['unit'] as String? ?? 'litres/kg',
      tip: json['tip'] as String?,
      comparison: json['comparison'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'item': item,
        'green_wf': greenWf,
        'blue_wf': blueWf,
        'grey_wf': greyWf,
        'unit': unit,
        if (tip != null) 'tip': tip,
        if (comparison != null) 'comparison': comparison,
      };
}
