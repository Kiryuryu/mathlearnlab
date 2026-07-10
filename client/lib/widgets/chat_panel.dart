library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';

/// Chat panel — SSE streaming chat, shown on wide screens as a side panel
/// and as a bottom sheet / full-screen on narrow screens.
class ChatPanel extends ConsumerStatefulWidget {
  const ChatPanel({super.key});

  @override
  ConsumerState<ChatPanel> createState() => _ChatPanelState();
}

class _ChatPanelState extends ConsumerState<ChatPanel> {
  final _controller = TextEditingController();
  final _scrollController = ScrollController();
  final List<Map<String, String>> _messages = [];
  bool _streaming = false;
  String _streamText = '';

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _send() async {
    final text = _controller.text.trim();
    if (text.isEmpty || _streaming) return;
    _controller.clear();

    setState(() {
      _messages.add({'role': 'user', 'content': text});
      _streaming = true;
      _streamText = '';
    });
    _scrollToBottom();

    try {
      final token = ref.read(authStateProvider).token;
      final response = await ref.read(apiServiceProvider).chatStream(
            _messages,
            contextRoute: '',
            token: token,
          );

      final stream = response.data.stream;
      final buffer = StringBuffer();
      String lineBuffer = '';

      await for (final chunk in stream) {
        lineBuffer += String.fromCharCodes(chunk);
        while (lineBuffer.contains('\n')) {
          final newline = lineBuffer.indexOf('\n');
          final line = lineBuffer.substring(0, newline).trim();
          lineBuffer = lineBuffer.substring(newline + 1);

          if (line.startsWith('data: ')) {
            final data = line.substring(6);
            if (data == '[DONE]') break;
            try {
              // Parse SSE JSON delta
              // Simplified: just append raw text
              buffer.write(data);
              setState(() => _streamText = buffer.toString());
              _scrollToBottom();
            } catch (_) {}
          }
        }
      }

      setState(() {
        _messages.add({'role': 'assistant', 'content': _streamText});
        _streaming = false;
        _streamText = '';
      });
    } catch (e) {
      setState(() {
        _messages.add({
          'role': 'assistant',
          'content': '错误: ${e.toString()}',
        });
        _streaming = false;
        _streamText = '';
      });
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 340,
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        border: Border(
          left: BorderSide(color: Theme.of(context).dividerColor),
        ),
      ),
      child: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            decoration: BoxDecoration(
              border: Border(
                bottom: BorderSide(color: Theme.of(context).dividerColor),
              ),
            ),
            child: Row(
              children: [
                Text('页边笔记',
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        color: Theme.of(context).colorScheme.primary)),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.add, size: 16),
                  onPressed: () => setState(() {
                    _messages.clear();
                    _streamText = '';
                  }),
                  tooltip: '新对话',
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(),
                ),
              ],
            ),
          ),
          // Messages
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(12),
              itemCount: _messages.length + (_streaming ? 1 : 0) +
                  (_messages.isEmpty && !_streaming ? 1 : 0),
              itemBuilder: (context, i) {
                if (_messages.isEmpty && !_streaming && i == 0) {
                  return const Padding(
                    padding: EdgeInsets.all(24),
                    child: Text('有不懂的概念随时问。',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: Color(0xFF8C8C8C))),
                  );
                }
                if (i < _messages.length) {
                  final m = _messages[i];
                  final isUser = m['role'] == 'user';
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Align(
                      alignment: isUser
                          ? Alignment.centerRight
                          : Alignment.centerLeft,
                      child: Container(
                        constraints: BoxConstraints(
                            maxWidth: MediaQuery.of(context).size.width * 0.7),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 6),
                        decoration: BoxDecoration(
                          color: isUser
                              ? Theme.of(context)
                                  .colorScheme
                                  .primary
                                  .withAlpha(20)
                              : null,
                          borderRadius: BorderRadius.circular(4),
                          border: isUser
                              ? null
                              : Border(
                                  left: BorderSide(
                                    color:
                                        Theme.of(context).colorScheme.primary,
                                    width: 2,
                                  ),
                                ),
                        ),
                        child: Text(
                          m['content'] ?? '',
                          style: const TextStyle(fontSize: 13),
                        ),
                      ),
                    ),
                  );
                }
                // Streaming text
                return Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Container(
                    constraints: BoxConstraints(
                        maxWidth: MediaQuery.of(context).size.width * 0.7),
                    padding: const EdgeInsets.symmetric(
                        horizontal: 10, vertical: 6),
                    decoration: BoxDecoration(
                      border: Border(
                        left: BorderSide(
                          color: Theme.of(context).colorScheme.primary,
                          width: 2,
                        ),
                      ),
                    ),
                    child: Text(
                      _streamText,
                      style: const TextStyle(fontSize: 13),
                    ),
                  ),
                );
              },
            ),
          ),
          // Input
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              border:
                  Border(top: BorderSide(color: Theme.of(context).dividerColor)),
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    maxLines: 2,
                    minLines: 1,
                    decoration: const InputDecoration(
                      hintText: '输入问题...',
                      border: InputBorder.none,
                      contentPadding: EdgeInsets.symmetric(horizontal: 8),
                    ),
                    onSubmitted: (_) => _send(),
                    style: const TextStyle(fontSize: 13),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send, size: 18),
                  onPressed: _streaming ? null : _send,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
