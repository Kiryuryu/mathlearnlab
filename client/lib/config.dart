/// MathLearnLab config — API base URL, theme constants.
///
/// In debug mode, points to localhost:8000.
/// In release mode, API is on the same host (nginx proxy).
class AppConfig {
  static const String appName = 'MathLearnLab';
  static const String appVersion = '3.0.0';

  /// API base URL — empty string means same-origin in web
  static const String apiBaseUrl = '';

  // Topic keys matching server config
  static const List<String> topicKeys = [
    'limits',
    'derivatives',
    'integrals',
    'series',
    'multivariable',
  ];

  static const Map<String, String> topicNames = {
    'limits': '极限与连续',
    'derivatives': '微分学',
    'integrals': '积分学',
    'series': '无穷级数',
    'multivariable': '多元微积分',
  };

  static const Map<String, String> topicIcons = {
    'limits': '§',
    'derivatives': '¶',
    'integrals': '∫',
    'series': '∑',
    'multivariable': '∂',
  };

  static const Map<String, String> difficultyLabels = {
    'easy': '★ 简单',
    'medium': '★★ 中等',
    'hard': '★★★ 困难',
  };
}
