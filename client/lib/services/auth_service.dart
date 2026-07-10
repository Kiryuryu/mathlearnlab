/// Auth service — manages JWT token storage and auth state.
library;

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'api_service.dart';

final authServiceProvider = Provider<AuthService>((ref) {
  return AuthService(api: ref.read(apiServiceProvider));
});

final authStateProvider =
    StateNotifierProvider<AuthStateNotifier, AuthState>((ref) {
  return AuthStateNotifier(auth: ref.read(authServiceProvider));
});

class AuthState {
  final bool isLoggedIn;
  final String? userId;
  final String? username;
  final String? token;

  const AuthState({
    this.isLoggedIn = false,
    this.userId,
    this.username,
    this.token,
  });

  AuthState copyWith({
    bool? isLoggedIn,
    String? userId,
    String? username,
    String? token,
  }) {
    return AuthState(
      isLoggedIn: isLoggedIn ?? this.isLoggedIn,
      userId: userId ?? this.userId,
      username: username ?? this.username,
      token: token ?? this.token,
    );
  }
}

class AuthStateNotifier extends StateNotifier<AuthState> {
  final AuthService _auth;

  AuthStateNotifier({required AuthService auth})
      : _auth = auth,
        super(const AuthState());

  Future<void> tryRestore() async {
    final token = await _auth.getToken();
    if (token != null) {
      final username = await _auth.getUsername();
      state = state.copyWith(
          isLoggedIn: true, token: token, username: username);
    }
  }

  Future<void> login(String username, String password) async {
    final data = await _auth.api.login(username, password);
    final token = data['token'] as String;
    final user = data['user'] as Map<String, dynamic>;
    await _auth.saveToken(token);
    await _auth.saveUsername(user['username'] as String);
    state = AuthState(
      isLoggedIn: true,
      token: token,
      userId: user['id'] as String,
      username: user['username'] as String,
    );
  }

  Future<void> register(
      String username, String password, {String email = ''}) async {
    final data = await _auth.api.register(username, password, email: email);
    final token = data['token'] as String;
    final user = data['user'] as Map<String, dynamic>;
    await _auth.saveToken(token);
    await _auth.saveUsername(user['username'] as String);
    state = AuthState(
      isLoggedIn: true,
      token: token,
      userId: user['id'] as String,
      username: user['username'] as String,
    );
  }

  Future<void> logout() async {
    await _auth.clearToken();
    state = const AuthState();
  }
}

class AuthService {
  final ApiService api;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  AuthService({required this.api});

  Future<void> saveToken(String token) async {
    await _storage.write(key: 'jwt_token', value: token);
  }

  Future<String?> getToken() async {
    return await _storage.read(key: 'jwt_token');
  }

  Future<void> saveUsername(String username) async {
    await _storage.write(key: 'username', value: username);
  }

  Future<String?> getUsername() async {
    return await _storage.read(key: 'username');
  }

  Future<void> clearToken() async {
    await _storage.deleteAll();
  }
}
