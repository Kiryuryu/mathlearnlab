library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config.dart';
import '../screens/main_shell.dart';

class Sidebar extends ConsumerWidget {
  const Sidebar({super.key});

  static final _navGroups = [
    {
      'section': '高等数学',
      'items': [
        {'label': '极限、连续与微分', 'path': 'notebooks/01-gaoshu/01-limits-continuity-differentiation'},
        {'label': '积分学', 'path': 'notebooks/01-gaoshu/02-integration'},
        {'label': '无穷级数', 'path': 'notebooks/01-gaoshu/03-infinite-series'},
        {'label': '多元微积分', 'path': 'notebooks/01-gaoshu/04-multivariable-calculus'},
      ],
    },
    {
      'section': '知识笔记',
      'items': [
        {'label': '高等数学', 'path': 'notes/01-gaoshu/README'},
        {'label': '线性代数', 'path': 'notes/02-xiandai/README'},
        {'label': '概率论', 'path': 'notes/03-gailvlun/README'},
      ],
    },
    {
      'section': '解题集',
      'items': [
        {'label': '极限与连续', 'path': 'problems/01-gaoshu/limits-problems'},
        {'label': '积分学', 'path': 'problems/01-gaoshu/integration-problems'},
        {'label': '无穷级数', 'path': 'problems/01-gaoshu/series-problems'},
        {'label': '多元微积分', 'path': 'problems/01-gaoshu/multivariable-problems'},
      ],
    },
    {
      'section': 'OCR 刷题',
      'items': AppConfig.topicKeys
          .map((t) => {'label': AppConfig.topicNames[t]!, 'topic': t})
          .toList(),
    },
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final shell = ref.watch(shellProvider);
    final shellNotifier = ref.read(shellProvider.notifier);

    return Drawer(
      child: SafeArea(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            // Header
            Container(
              padding: const EdgeInsets.fromLTRB(16, 24, 16, 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('MathLearnLab',
                      style: Theme.of(context).textTheme.titleMedium),
                  Text('高等数学复习',
                      style: Theme.of(context).textTheme.labelSmall),
                ],
              ),
            ),
            const Divider(),
            // Home
            ListTile(
              leading: const Icon(Icons.home_outlined, size: 18),
              title: const Text('首页'),
              selected: shell.route == AppRoute.home,
              onTap: () {
                shellNotifier.goHome();
                Navigator.pop(context);
              },
            ),
            // Error log
            ListTile(
              leading: const Icon(Icons.error_outline, size: 18),
              title: const Text('错题本'),
              selected: shell.route == AppRoute.errorLog,
              onTap: () {
                shellNotifier.goErrorLog();
                Navigator.pop(context);
              },
            ),
            const Divider(),
            // Section groups
            for (final group in _navGroups) ...[
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
                child: Text(
                  group['section'] as String,
                  style: Theme.of(context).textTheme.labelSmall,
                ),
              ),
              for (final item in (group['items'] as List<Map<String, dynamic>>))
                ListTile(
                  dense: true,
                  title: Text(item['label'] as String,
                      style: const TextStyle(fontSize: 14)),
                  onTap: () {
                    if (item.containsKey('topic')) {
                      shellNotifier.goPractice(item['topic'] as String);
                    } else {
                      shellNotifier.goContent(item['path'] as String);
                    }
                    Navigator.pop(context);
                  },
                ),
            ],
          ],
        ),
      ),
    );
  }
}
