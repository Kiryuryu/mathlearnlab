library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../config.dart';

enum PracticePhase { select, solve, results }

class PracticeScreen extends ConsumerStatefulWidget {
  final String topic;
  const PracticeScreen({super.key, required this.topic});

  @override
  ConsumerState<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends ConsumerState<PracticeScreen> {
  PracticePhase _phase = PracticePhase.select;
  List<Map<String, dynamic>> _problems = [];
  Map<String, dynamic>? _currentProblem;
  String? _imageBase64;
  Map<String, dynamic>? _result;
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _loadProblems();
  }

  Future<void> _loadProblems() async {
    setState(() => _loading = true);
    try {
      final token = ref.read(authStateProvider).token;
      final data = await ref
          .read(apiServiceProvider)
          .listProblems(widget.topic, token: token);
      setState(() {
        _problems = (data['problems'] as List).cast<Map<String, dynamic>>();
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _selectProblem(String id) async {
    setState(() => _loading = true);
    try {
      final token = ref.read(authStateProvider).token;
      final data = await ref
          .read(apiServiceProvider)
          .getProblem(widget.topic, id, token: token);
      setState(() {
        _currentProblem = data['problem'] as Map<String, dynamic>;
        _imageBase64 = null;
        _result = null;
        _phase = PracticePhase.solve;
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _randomProblem() async {
    setState(() => _loading = true);
    try {
      final token = ref.read(authStateProvider).token;
      final data = await ref
          .read(apiServiceProvider)
          .randomProblem(widget.topic, token: token);
      setState(() {
        _currentProblem = data['problem'] as Map<String, dynamic>;
        _imageBase64 = null;
        _result = null;
        _phase = PracticePhase.solve;
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _pickImage() async {
    // Web: use file input via html
    // For simplicity, we accept base64 from clipboard or use image_picker
    // This is a placeholder — real app would use image_picker package
  }

  Future<void> _submitGrade() async {
    if (_imageBase64 == null || _currentProblem == null) return;
    setState(() => _loading = true);
    try {
      final token = ref.read(authStateProvider).token;
      final result = await ref.read(apiServiceProvider).gradeSubmission(
            widget.topic,
            _currentProblem!['id'] as String,
            _imageBase64!,
            token: token,
          );
      setState(() {
        _result = result;
        _phase = PracticePhase.results;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text('批改失败: $e')));
      }
    }
  }

  void _goBack() => setState(() {
        _phase = PracticePhase.select;
        _currentProblem = null;
        _imageBase64 = null;
        _result = null;
      });

  @override
  Widget build(BuildContext context) {
    final topicName = AppConfig.exhibitNames[widget.topic]?.replaceAll('\n', ' — ') ?? widget.topic;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(32, 24, 32, 0),
          child: Text('$topicName — 刷题',
              style: Theme.of(context).textTheme.titleLarge),
        ),
        Expanded(
          child: _loading
              ? const Center(child: CircularProgressIndicator())
              : _buildPhase(),
        ),
      ],
    );
  }

  Widget _buildPhase() {
    switch (_phase) {
      case PracticePhase.select:
        return _buildSelect();
      case PracticePhase.solve:
        return _buildSolve();
      case PracticePhase.results:
        return _buildResults();
    }
  }

  Widget _buildSelect() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        children: [
          ElevatedButton(
            onPressed: _randomProblem,
            child: const Text('随机抽题'),
          ),
          const SizedBox(height: 16),
          if (_problems.isEmpty)
            const Text('暂无题目')
          else
            ..._problems.map((p) => _buildProblemItem(p)),
        ],
      ),
    );
  }

  Widget _buildProblemItem(Map<String, dynamic> p) {
    return Card(
      margin: const EdgeInsets.only(bottom: 6),
      child: ListTile(
        title: Text(p['id'] ?? ''),
        subtitle: Text(p['preview'] ?? ''),
        trailing: const Icon(Icons.chevron_right),
        onTap: () => _selectProblem(p['id'] as String),
      ),
    );
  }

  Widget _buildSolve() {
    final p = _currentProblem!;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextButton.icon(
            onPressed: _goBack,
            icon: const Icon(Icons.arrow_back, size: 16),
            label: const Text('返回选题'),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(p['id'] ?? '', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 8),
                  Text(p['problem_statement'] ?? ''),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          // Image upload area
          Card(
            child: InkWell(
              onTap: _pickImage,
              borderRadius: BorderRadius.circular(8),
              child: Container(
                height: 120,
                alignment: Alignment.center,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.camera_alt_outlined,
                        size: 32, color: Theme.of(context).colorScheme.primary),
                    const SizedBox(height: 8),
                    const Text('点击拍照或上传图片'),
                    Text('JPG / PNG',
                        style: Theme.of(context).textTheme.labelSmall),
                  ],
                ),
              ),
            ),
          ),
          if (_imageBase64 != null) ...[
            const SizedBox(height: 8),
            Text('图片已就绪', textAlign: TextAlign.center),
          ],
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: _imageBase64 != null ? _submitGrade : null,
            child: const Text('提交批改'),
          ),
        ],
      ),
    );
  }

  Widget _buildResults() {
    final r = _result!;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _verdictCard(context, r['verdict'] ?? 'unknown'),
          if (r['what_is_correct'] is String && (r['what_is_correct'] as String).isNotEmpty)
            _feedbackCard(context, '正确的部分', r['what_is_correct'], Colors.green),
          if (r['what_is_wrong'] is String && (r['what_is_wrong'] as String).isNotEmpty)
            _feedbackCard(context, '存在的问题', r['what_is_wrong'], Colors.red),
          if (r['suggestion'] is String && (r['suggestion'] as String).isNotEmpty)
            _feedbackCard(context, '改进建议', r['suggestion'],
                Theme.of(context).colorScheme.primary),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: ElevatedButton(
                  onPressed: _goBack,
                  child: const Text('再做一题'),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: OutlinedButton(
                  onPressed: () =>
                      setState(() => _phase = PracticePhase.solve),
                  child: const Text('重做此题'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _verdictCard(BuildContext context, String verdict) {
    final texts = {
      'correct': '回答正确',
      'partially_correct': '部分正确',
      'incorrect': '回答有误',
    };
    final colors = {
      'correct': Colors.green.shade50,
      'partially_correct': Colors.orange.shade50,
      'incorrect': Colors.red.shade50,
    };
    return Card(
      color: colors[verdict] ?? Colors.grey.shade50,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Text(
          texts[verdict] ?? verdict,
          style: Theme.of(context).textTheme.headlineSmall,
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  Widget _feedbackCard(
      BuildContext context, String title, String content, Color accent) {
    return Card(
      margin: const EdgeInsets.only(top: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 3,
              height: 20,
              color: accent,
              margin: const EdgeInsets.only(right: 8),
              child: const SizedBox.shrink(),
            ),
            Text(title, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 6),
            Text(content, style: Theme.of(context).textTheme.bodyLarge),
          ].cast<Widget>(),
        ),
      ),
    );
  }
}
