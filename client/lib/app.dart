/// Main app entry point.
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'theme.dart';
import 'services/auth_service.dart';
import 'screens/main_shell.dart';

class MathLearnLabApp extends ConsumerStatefulWidget {
  const MathLearnLabApp({super.key});

  @override
  ConsumerState<MathLearnLabApp> createState() => _MathLearnLabAppState();
}

class _MathLearnLabAppState extends ConsumerState<MathLearnLabApp> {
  bool _initialized = false;

  @override
  void initState() {
    super.initState();
    _restoreAuth();
  }

  Future<void> _restoreAuth() async {
    await ref.read(authStateProvider.notifier).tryRestore();
    setState(() => _initialized = true);
  }

  @override
  Widget build(BuildContext context) {
    if (!_initialized) {
      return MaterialApp(
        theme: AppTheme.light,
        darkTheme: AppTheme.dark,
        home: const Scaffold(
            body: Center(child: CircularProgressIndicator())),
      );
    }
    return MaterialApp(
      title: 'MathLearnLab',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      home: const MainShell(),
    );
  }
}
