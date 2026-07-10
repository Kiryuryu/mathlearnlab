/// Math Museum config — API base URL, theme constants.
class AppConfig {
  static const String appName = '数学博物馆';
  static const String appSubtitle = '知其然，知其所以然';
  static const String appVersion = '4.0.0';

  /// API base URL — empty string means same-origin in web
  static const String apiBaseUrl = '';

  // Exhibit keys matching server config
  static const List<String> exhibitKeys = [
    'limits',
    'derivatives',
    'integrals',
    'series',
    'multivariable',
  ];

  static const Map<String, String> exhibitNames = {
    'limits': '第一展厅\n极限 — 无限逼近的艺术',
    'derivatives': '第二展厅\n导数 — 瞬间的变化率',
    'integrals': '第三展厅\n积分 — 和的极限',
    'series': '第四展厅\n无穷级数 — 无限的拼图',
    'multivariable': '第五展厅\n多元微积分 — 从平面到空间',
  };

  static const Map<String, String> exhibitIcons = {
    'limits': '∞',
    'derivatives': '∆',
    'integrals': '∫',
    'series': '∑',
    'multivariable': '∂',
  };

  static const Map<String, String> exhibitHistorians = {
    'limits': '柯西、魏尔斯特拉斯',
    'derivatives': '费马、牛顿、莱布尼茨',
    'integrals': '阿基米德、黎曼、勒贝格',
    'series': '欧拉、傅里叶',
    'multivariable': '拉格朗日、高斯、格林',
  };

  static const Map<String, String> exhibitBigQuestions = {
    'limits': '如何用数学语言精确描述"无限接近"？',
    'derivatives': '如何在某一瞬间测量变化？',
    'integrals': '如何求一个曲线下方不规则图形的面积？',
    'series': '无穷多个数加起来可以是有限的吗？',
    'multivariable': '如何在多维世界中理解变化、极值和流动？',
  };

  static const Map<String, String> exhibitBeauties = {
    'limits': 'ε-δ 定义用有限的符号捕捉了无穷的直觉',
    'derivatives': '泰勒展开：任何光滑函数都可以用多项式逼近',
    'integrals': '微积分基本定理：微分和积分是互逆运算——这是数学史上最伟大的发现之一',
    'series': '1+1/4+1/9+... = π²/6 —— 自然数的倒数平方和竟然与圆周率有关',
    'multivariable': '梯度下降：沿着最陡峭的方向下山——这个概念今天驱动着所有AI的学习',
  };

  static const Map<String, String> difficultyLabels = {
    'easy': '★ 基础',
    'medium': '★★ 进阶',
    'hard': '★★★ 挑战',
  };
}
