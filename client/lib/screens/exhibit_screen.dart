library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config.dart';
import '../widgets/chat_panel.dart';

/// Museum exhibit screen — history + intuition + visualization + beauty.
class ExhibitScreen extends ConsumerStatefulWidget {
  final String exhibitKey;
  const ExhibitScreen({super.key, required this.exhibitKey});

  @override
  ConsumerState<ExhibitScreen> createState() => _ExhibitScreenState();
}

class _ExhibitScreenState extends ConsumerState<ExhibitScreen> {
  @override
  Widget build(BuildContext context) {
    final name = AppConfig.exhibitNames[widget.exhibitKey] ?? widget.exhibitKey;
    final icon = AppConfig.exhibitIcons[widget.exhibitKey] ?? '';
    final historians =
        AppConfig.exhibitHistorians[widget.exhibitKey] ?? '';
    final bigQ =
        AppConfig.exhibitBigQuestions[widget.exhibitKey] ?? '';
    final beauty =
        AppConfig.exhibitBeauties[widget.exhibitKey] ?? '';

    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Text(name.replaceAll('\n', ' — '),
              style: Theme.of(context).textTheme.headlineMedium),
          const SizedBox(height: 4),
          Text('核心问题', style: Theme.of(context).textTheme.labelSmall),
          const SizedBox(height: 4),
          Text('❓ $bigQ', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 24),

          // Historian card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  Text(icon,
                      style: const TextStyle(fontSize: 40),
                      textScaler: TextScaler.noScaling),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('关键人物',
                            style: Theme.of(context).textTheme.labelSmall),
                        const SizedBox(height: 4),
                        Text(historians,
                            style: Theme.of(context).textTheme.titleMedium),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Beauty moment
          Card(
            color: Theme.of(context)
                .colorScheme
                .primary
                .withAlpha(15),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Text('✨'),
                      const SizedBox(width: 8),
                      Text('美的瞬间',
                          style: Theme.of(context).textTheme.labelSmall),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(beauty,
                      style: Theme.of(context).textTheme.bodyLarge),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Visualization note
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Text('🎨'),
                      const SizedBox(width: 8),
                      Text('交互可视化',
                          style: Theme.of(context).textTheme.labelSmall),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '运行 jupyter lab 启动本地环境，可体验完整的交互式可视化（拖动滑块、3D 旋转、动画播放）。',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Enter practice
          Card(
            child: InkWell(
              borderRadius: BorderRadius.circular(8),
              onTap: () {
                // Navigate to practice
              },
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Row(
                  children: [
                    const Text('🧪'),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('进入动手实验室',
                            style:
                                Theme.of(context).textTheme.titleMedium),
                        Text('纸笔作答 → 拍照上传 → AI 批改验证',
                            style:
                                Theme.of(context).textTheme.bodyMedium),
                      ],
                    ),
                    const Spacer(),
                    const Icon(Icons.arrow_forward),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Jupyter notebook link
          OutlinedButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.code, size: 16),
            label: const Text('在 Jupyter 中打开交互 Notebook'),
          ),
        ],
      ),
    );
  }
}
