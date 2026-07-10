library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config.dart';
import '../screens/main_shell.dart';

class Sidebar extends ConsumerWidget {
  const Sidebar({super.key});

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
                  Text('数学博物馆',
                      style: Theme.of(context).textTheme.titleMedium),
                  Text('知其然，知其所以然',
                      style: Theme.of(context).textTheme.labelSmall),
                ],
              ),
            ),
            const Divider(),
            // Home
            ListTile(
              leading: const Icon(Icons.museum_outlined, size: 18),
              title: const Text('序幕大厅'),
              selected: shell.route == AppRoute.home,
              onTap: () {
                shellNotifier.goHome();
                Navigator.pop(context);
              },
            ),
            const Divider(),
            // Exhibits
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
              child: Text('🏛 展厅', style: Theme.of(context).textTheme.labelSmall),
            ),
            for (final key in AppConfig.exhibitKeys)
              ListTile(
                dense: true,
                leading: Text(AppConfig.exhibitIcons[key] ?? '',
                    style: const TextStyle(fontSize: 18)),
                title: Text(
                  _exhibitLabel(key),
                  style: const TextStyle(fontSize: 14),
                ),
                onTap: () {
                  shellNotifier.goExhibit(key);
                  Navigator.pop(context);
                },
              ),
            const Divider(),
            // Practice lab
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
              child: Text('🧪 动手实验室',
                  style: Theme.of(context).textTheme.labelSmall),
            ),
            for (final key in AppConfig.exhibitKeys)
              ListTile(
                dense: true,
                leading: const Icon(Icons.edit_note, size: 18),
                title: Text(
                  '${_shortName(key)} — 刷题',
                  style: const TextStyle(fontSize: 14),
                ),
                onTap: () {
                  shellNotifier.goPractice(key);
                  Navigator.pop(context);
                },
              ),
            const Divider(),
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
          ],
        ),
      ),
    );
  }

  String _exhibitLabel(String key) {
    const labels = {
      'limits': '第一展厅：极限',
      'derivatives': '第二展厅：导数',
      'integrals': '第三展厅：积分',
      'series': '第四展厅：无穷级数',
      'multivariable': '第五展厅：多元微积分',
    };
    return labels[key] ?? key;
  }

  String _shortName(String key) {
    const names = {
      'limits': '极限',
      'derivatives': '导数',
      'integrals': '积分',
      'series': '级数',
      'multivariable': '多元',
    };
    return names[key] ?? key;
  }
}
