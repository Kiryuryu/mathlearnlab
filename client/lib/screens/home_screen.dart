library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config.dart';
import '../screens/main_shell.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final shellNotifier = ref.read(shellProvider.notifier);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('数学博物馆', style: Theme.of(context).textTheme.headlineMedium),
          const SizedBox(height: 4),
          Text('知其然，知其所以然',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: Theme.of(context).colorScheme.primary)),
          const SizedBox(height: 12),
          Text(
            '欢迎来到数学博物馆。这里不是教你怎么做题，而是带你理解数学概念从何而来、为什么这样定义、美在哪里。',
            style: Theme.of(context).textTheme.bodyLarge,
          ),
          const SizedBox(height: 8),
          Text(
            '微积分是人类思想史上最伟大的成就之一。从芝诺的飞矢不动悖论，到牛顿和莱布尼茨的激烈争论，到柯西和魏尔斯特拉斯用 ε-δ 语言为它打下坚实根基——这是一个跨越两千年的故事。',
            style: Theme.of(context).textTheme.bodyLarge,
          ),
          const SizedBox(height: 24),

          // Exhibits
          Card(
            color: Theme.of(context).colorScheme.primary.withAlpha(15),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text('🏛 展厅导览',
                  style: Theme.of(context).textTheme.labelSmall),
            ),
          ),
          const SizedBox(height: 8),
          ...AppConfig.exhibitKeys.map(
              (key) => _buildExhibitCard(context, key, shellNotifier)),

          const SizedBox(height: 24),

          // Lab
          Card(
            color: Theme.of(context).colorScheme.secondary.withAlpha(20),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text('🧪 动手实验室',
                  style: Theme.of(context).textTheme.labelSmall),
            ),
          ),
          const SizedBox(height: 8),
          ...AppConfig.exhibitKeys.map(
              (key) => _buildLabCard(context, key, shellNotifier)),
          const SizedBox(height: 24),

          // Footer
          Text('使用说明', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          _hint(context, '左侧导航', '浏览博物馆各展厅，自由探索'),
          _hint(context, '右侧"页边笔记"', 'AI 助手，随时回答你的好奇'),
          _hint(context, '动手实验室', '纸笔作答后拍照，AI 批改验证理解'),
          _hint(context, 'Jupyter Lab', '运行 jupyter lab 体验完整交互可视化'),
        ],
      ),
    );
  }

  Widget _buildExhibitCard(
      BuildContext context, String key, ShellNotifier nav) {
    final name = AppConfig.exhibitNames[key] ?? key;
    final icon = AppConfig.exhibitIcons[key] ?? '';
    final q = AppConfig.exhibitBigQuestions[key] ?? '';
    final h = AppConfig.exhibitHistorians[key] ?? '';

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: () => nav.goExhibit(key),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Text(icon,
                  style: const TextStyle(fontSize: 32),
                  textScaler: TextScaler.noScaling),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(name.replaceAll('\n', ' — '),
                        style: Theme.of(context).textTheme.titleMedium),
                    const SizedBox(height: 4),
                    Text(q,
                        style: Theme.of(context).textTheme.bodyMedium),
                    Text('提出者：$h',
                        style: Theme.of(context).textTheme.labelSmall),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLabCard(
      BuildContext context, String key, ShellNotifier nav) {
    final name = AppConfig.exhibitNames[key] ?? key;
    final icon = AppConfig.exhibitIcons[key] ?? '';

    return Card(
      margin: const EdgeInsets.only(bottom: 6),
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: () => nav.goPractice(key),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              Text(icon, style: const TextStyle(fontSize: 20)),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  name.replaceAll('\n', ' — ') + ' · 动手区',
                ),
              ),
              Text('纸笔作答 → AI 批改',
                  style: Theme.of(context).textTheme.labelSmall),
              const SizedBox(width: 8),
              const Icon(Icons.chevron_right, size: 18),
            ],
          ),
        ),
      ),
    );
  }

  Widget _hint(BuildContext context, String title, String desc) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('• '),
          Expanded(
            child: RichText(
              text: TextSpan(
                children: [
                  TextSpan(
                    text: title,
                    style: const TextStyle(fontWeight: FontWeight.w600),
                  ),
                  TextSpan(text: ' — $desc'),
                ],
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
