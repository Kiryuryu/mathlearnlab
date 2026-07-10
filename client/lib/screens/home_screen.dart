library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../config.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  Map<String, dynamic>? _stats;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadStats();
  }

  Future<void> _loadStats() async {
    try {
      final auth = ref.read(authStateProvider);
      final stats = await ref.read(apiServiceProvider).getStats(token: auth.token);
      setState(() { _stats = stats; _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('MathLearnLab', style: Theme.of(context).textTheme.headlineMedium),
          const SizedBox(height: 4),
          Text('高等数学复习 · 交互可视化 · AI 答疑 · OCR 刷题',
              style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 24),

          // Stats
          Text('学习概览', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          if (_loading)
            const Center(child: CircularProgressIndicator())
          else if (_stats != null)
            _buildStats(context),
          const SizedBox(height: 24),

          // Topics
          Text('高等数学', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          ...AppConfig.topicKeys.map((t) => _buildTopicCard(context, t)),

          const SizedBox(height: 24),
          // Quick links
          Text('快速入口', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: _buildQuickCard(
                  context,
                  icon: Icons.edit_note,
                  title: 'OCR 刷题',
                  subtitle: '纸笔作答 → 拍照上传 → AI 批改',
                  onTap: () {},
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildQuickCard(
                  context,
                  icon: Icons.error_outline,
                  title: '错题本',
                  subtitle: '查看答错的题目和分析',
                  onTap: () {},
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStats(BuildContext context) {
    final s = _stats!;
    return Row(
      children: [
        _statCard(context, '${s['total'] ?? 0}', '总答题数'),
        _statCard(context, '${s['accuracy'] ?? 0}%', '正确率'),
        _statCard(context, '${s['correct'] ?? 0}', '正确'),
        _statCard(context, '${(s['total']??0) - (s['correct']??0)}', '需复习'),
      ],
    );
  }

  Widget _statCard(BuildContext context, String value, String label) {
    return Expanded(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 8),
          child: Column(
            children: [
              Text(value,
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      color: Theme.of(context).colorScheme.primary)),
              const SizedBox(height: 2),
              Text(label, style: Theme.of(context).textTheme.labelSmall),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTopicCard(BuildContext context, String topic) {
    final name = AppConfig.topicNames[topic] ?? topic;
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: () {},
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Text(name, style: Theme.of(context).textTheme.titleMedium),
        ),
      ),
    );
  }

  Widget _buildQuickCard(BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 8),
              Text(title, style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 4),
              Text(subtitle, style: Theme.of(context).textTheme.bodyMedium),
            ],
          ),
        ),
      ),
    );
  }
}
