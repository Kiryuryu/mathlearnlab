/// Main shell — responsive layout with sidebar drawer + main content + chat panel.
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../widgets/sidebar.dart';
import '../widgets/chat_panel.dart';
import '../services/auth_service.dart';
import 'home_screen.dart';
import 'exhibit_screen.dart';
import 'practice_screen.dart';
import 'error_log_screen.dart';
import 'settings_screen.dart';
import 'login_screen.dart';

enum AppRoute { home, exhibit, practice, errorLog, settings }

class ShellState {
  final AppRoute route;
  final AppRoute? prevRoute;
  final String? exhibitKey;
  final String? practiceTopic;

  const ShellState({
    this.route = AppRoute.home,
    this.prevRoute,
    this.exhibitKey,
    this.practiceTopic,
  });

  ShellState copyWith({
    AppRoute? route,
    AppRoute? prevRoute,
    String? exhibitKey,
    String? practiceTopic,
  }) {
    return ShellState(
      route: route ?? this.route,
      prevRoute: prevRoute,
      exhibitKey: exhibitKey ?? this.exhibitKey,
      practiceTopic: practiceTopic,
    );
  }
}

final shellProvider = StateNotifierProvider<ShellNotifier, ShellState>((ref) {
  return ShellNotifier();
});

class ShellNotifier extends StateNotifier<ShellState> {
  ShellNotifier() : super(const ShellState());

  void goHome() =>
      state = ShellState(route: AppRoute.home, prevRoute: state.route);
  void goExhibit(String key) => state = ShellState(
      route: AppRoute.exhibit, prevRoute: state.route, exhibitKey: key);
  void goPractice(String topic) => state = ShellState(
      route: AppRoute.practice,
      prevRoute: state.route,
      practiceTopic: topic);
  void goErrorLog() =>
      state = ShellState(route: AppRoute.errorLog, prevRoute: state.route);
  void goSettings() =>
      state = ShellState(route: AppRoute.settings, prevRoute: state.route);

  void goBack() {
    if (state.prevRoute != null) {
      final prev = state.prevRoute!;
      final prevExhibitKey = state.exhibitKey;
      final prevPracticeTopic = state.practiceTopic;
      state = ShellState(
        route: prev,
        prevRoute: null,
        exhibitKey: prevExhibitKey,
        practiceTopic: prevPracticeTopic,
      );
    }
  }
}

class MainShell extends ConsumerWidget {
  const MainShell({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authStateProvider);
    final shell = ref.watch(shellProvider);

    // Not logged in → show login screen
    if (!auth.isLoggedIn) {
      return const LoginScreen();
    }

    return Scaffold(
      appBar: AppBar(
        leading: shell.route != AppRoute.home
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: () => ref.read(shellProvider.notifier).goBack(),
              )
            : null,
        title: Row(
          children: [
            const Text('数学博物馆'),
            const SizedBox(width: 8),
            Text(
              '知其然，知其所以然',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
        actions: [
          // Dark mode toggle
          IconButton(
            icon: const Icon(Icons.brightness_6),
            onPressed: () {
              // Theme is system by default — toggle is a nice-to-have
            },
            tooltip: '切换明暗',
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => ref.read(shellProvider.notifier).goSettings(),
            tooltip: '设置',
          ),
        ],
      ),
      drawer: const Sidebar(),
      body: _buildPage(shell),
    );
  }

  Widget _buildPage(ShellState shell) {
    switch (shell.route) {
      case AppRoute.home:
        return const HomeScreen();
      case AppRoute.exhibit:
        return ExhibitScreen(key: ValueKey(shell.exhibitKey), exhibitKey: shell.exhibitKey ?? 'limits');
      case AppRoute.practice:
        return PracticeScreen(topic: shell.practiceTopic ?? 'integrals');
      case AppRoute.errorLog:
        return const ErrorLogScreen();
      case AppRoute.settings:
        return const SettingsScreen();
    }
  }
}
