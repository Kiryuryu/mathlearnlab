/// API service — all HTTP calls to the FastAPI backend.
library;

import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config.dart';

final apiServiceProvider = Provider<ApiService>((ref) => ApiService());

class ApiService {
  final Dio _dio;

  ApiService({Dio? dio})
      : _dio = dio ??
            Dio(BaseOptions(
              baseUrl: AppConfig.apiBaseUrl,
              connectTimeout: const Duration(seconds: 30),
              receiveTimeout: const Duration(seconds: 120),
              headers: {'Content-Type': 'application/json'},
            ));

  // ── Auth ──

  Future<Map<String, dynamic>> register(
      String username, String password, {String email = ''}) async {
    final r = await _dio.post('/api/auth/register', data: {
      'username': username,
      'password': password,
      'email': email,
    });
    return r.data;
  }

  Future<Map<String, dynamic>> login(String username, String password) async {
    final r = await _dio.post('/api/auth/login', data: {
      'username': username,
      'password': password,
    });
    return r.data;
  }

  Future<Map<String, dynamic>> me(String token) async {
    final r = await _dio.get('/api/auth/me',
        options: Options(headers: {'Authorization': 'Bearer $token'}));
    return r.data;
  }

  // ── Practice ──

  Future<Map<String, dynamic>> listProblems(String topic,
      {String? difficulty, String? token}) async {
    final params = <String, dynamic>{};
    if (difficulty != null && difficulty != 'all') {
      params['difficulty'] = difficulty;
    }
    final r = await _dio.get('/api/practice/$topic/problems',
        queryParameters: params.isEmpty ? null : params,
        options: _auth(token));
    return r.data;
  }

  Future<Map<String, dynamic>> randomProblem(String topic,
      {String? difficulty, String? token}) async {
    final params = <String, dynamic>{};
    if (difficulty != null && difficulty != 'all') {
      params['difficulty'] = difficulty;
    }
    final r = await _dio.get('/api/practice/$topic/problems/random',
        queryParameters: params.isEmpty ? null : params,
        options: _auth(token));
    return r.data;
  }

  Future<Map<String, dynamic>> getProblem(String topic, String problemId,
      {String? token}) async {
    final r = await _dio.get('/api/practice/$topic/problems/$problemId',
        options: _auth(token));
    return r.data;
  }

  // ── Grade ──

  Future<Map<String, dynamic>> gradeSubmission(
      String topicKey, String problemId, String imageBase64,
      {String? token}) async {
    final r = await _dio.post('/api/grade',
        data: {
          'topic_key': topicKey,
          'problem_id': problemId,
          'image_base64': imageBase64,
        },
        options: _auth(token));
    return r.data;
  }

  // ── Content ──

  Future<Map<String, dynamic>> getContent(String path) async {
    final r = await _dio.get('/api/content/$path');
    return r.data;
  }

  // ── Stats ──

  Future<Map<String, dynamic>> getStats({String? token}) async {
    final r = await _dio.get('/api/stats', options: _auth(token));
    return r.data;
  }

  Future<Map<String, dynamic>> getHistory({int n = 10, String? token}) async {
    final r = await _dio.get('/api/stats/history',
        queryParameters: {'n': n}, options: _auth(token));
    return r.data;
  }

  Future<Map<String, dynamic>> getErrors({String? token}) async {
    final r = await _dio.get('/api/stats/errors', options: _auth(token));
    return r.data;
  }

  // ── Chat (SSE) ──

  /// Stream chat messages via SSE.
  /// Returns the raw [Response] for streaming.
  Future<Response> chatStream(
      List<Map<String, String>> messages, {
        String? model,
        String? contextRoute,
        String? token,
      }) async {
    return _dio.post(
      '/api/chat/stream',
      data: {
        'messages': messages,
        if (model != null) 'model': model,
        if (contextRoute != null) 'context_route': contextRoute,
      },
      options: Options(
        headers: {
          ..._authHeaders(token),
        },
        responseType: ResponseType.stream,
      ),
    );
  }

  Options? _auth(String? token) {
    if (token == null) return null;
    return Options(headers: {'Authorization': 'Bearer $token'});
  }

  Map<String, String> _authHeaders(String? token) {
    if (token == null) return {};
    return {'Authorization': 'Bearer $token'};
  }
}
