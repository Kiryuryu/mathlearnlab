library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';

class ErrorLogScreen extends ConsumerStatefulWidget {
  const ErrorLogScreen({super.key});

  @override
  ConsumerState<ErrorLogScreen> createState() => _ErrorLogScreenState();
}

class _ErrorLogScreenState extends ConsumerState<ErrorLogScreen> {
  List<Map<String, dynamic>> _errors = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final token = ref.read(authStateProvider).token;
      final data = await ref.read(apiServiceProvider).getErrors(token: token);
      setState(() {
        _errors = (data['errors'] as List).cast<Map<String, dynamic>>();
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(32, 24, 32, 0),
          child: Text('错题本',
              style: Theme.of(context).textTheme.titleLarge),
        ),
        const Padding(
          padding: EdgeInsets.fromLTRB(32, 4, 32, 0),
          child: Text('查看答错的题目和分析，针对性复习',
              style: TextStyle(color: Color(0xFF8C8C8C))),
        ),
        Expanded(
          child: _loading
              ? const Center(child: CircularProgressIndicator())
              : _errors.isEmpty
                  ? const Center(child: Text('暂无错题记录'))
                  : ListView.builder(
                      padding: const EdgeInsets.all(32),
                      itemCount: _errors.length,
                      itemBuilder: (context, i) {
                        final e = _errors[i];
                        return Card(
                          margin: const EdgeInsets.only(bottom: 8),
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Text(e['problem_id'] ?? '',
                                        style: Theme.of(context)
                                            .textTheme
                                            .titleMedium),
                                    const Spacer(),
                                    Text(e['verdict'] ?? '',
                                        style: TextStyle(
                                            color: e['verdict'] == 'incorrect'
                                                ? Colors.red
                                                : Colors.orange)),
                                  ],
                                ),
                                if (e['what_is_wrong'] is String)
                                  Padding(
                                    padding: const EdgeInsets.only(top: 8),
                                    child: Text(e['what_is_wrong']),
                                  ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
        ),
      ],
    );
  }
}
