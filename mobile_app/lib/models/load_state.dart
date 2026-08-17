/// Tracks async operation state in all screens.
///
/// Used to drive the UI between loading, success, and error states
/// without boolean flags scattered across widgets.
enum LoadState {
  /// No operation in progress — show default UI.
  idle,

  /// API call is in flight — show spinner.
  loading,

  /// API call succeeded — show result.
  success,

  /// API call failed — show error widget.
  error,
}
