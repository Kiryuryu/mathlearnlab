// AI Chat Panel

let _chatAbortController = null;

document.addEventListener('DOMContentLoaded', () => {
  initChatPanel();
});

function initChatPanel() {
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('chatSendBtn');
  const newBtn = document.getElementById('chatNewBtn');
  const toggleBtn = document.getElementById('chatToggleBtn');
  const floatingBtn = document.getElementById('chatFloatingBtn');
  const messagesContainer = document.getElementById('chatMessages');

  if (!input || !sendBtn) return;

  // Send message on button click
  sendBtn.addEventListener('click', () => sendChatMessage());

  // Send on Enter (Shift+Enter for newline)
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendChatMessage();
    }
  });

  // New conversation
  newBtn?.addEventListener('click', () => {
    Storage.clearChatHistory();
    if (messagesContainer) {
      messagesContainer.innerHTML = getWelcomeHtml();
    }
  });

  // Toggle panel
  toggleBtn?.addEventListener('click', toggleChatPanel);
  floatingBtn?.addEventListener('click', toggleChatPanel);

  // Load chat history
  loadChatHistory();
}

function getWelcomeHtml() {
  return `
    <div class="chat-welcome">
      <p>👋 你好！我是你的考研数学 AI 助手。</p>
      <p>有不懂的概念、题目随时问我，比如：</p>
      <ul>
        <li>"华里士公式是什么？"</li>
        <li>"帮我解释一下格林公式"</li>
        <li>"这道题怎么做？∫x·eˣ dx"</li>
        <li>"中值定理的几何意义"</li>
      </ul>
      <p class="chat-context-hint" id="chatContextHint"></p>
    </div>
  `;
}

function toggleChatPanel() {
  const panel = document.getElementById('chatPanel');
  const floatingBtn = document.getElementById('chatFloatingBtn');

  if (window.innerWidth <= 768) {
    // Mobile: toggle full-width overlay
    panel?.classList.toggle('mobile-open');
  } else {
    // Desktop: collapse/expand
    panel?.classList.toggle('collapsed');
    if (panel?.classList.contains('collapsed')) {
      floatingBtn?.removeAttribute('hidden');
    } else {
      floatingBtn?.setAttribute('hidden', '');
    }
  }
}

function loadChatHistory() {
  const messages = Storage.getChatHistory();
  const container = document.getElementById('chatMessages');
  if (!container) return;

  if (messages.length === 0) {
    container.innerHTML = getWelcomeHtml();
    updateChatContextHint();
    return;
  }

  let html = '';
  messages.forEach(msg => {
    html += renderChatMessage(msg.role, msg.content);
  });
  container.innerHTML = html;
  container.scrollTop = container.scrollHeight;
  updateChatContextHint();
}

function renderChatMessage(role, content) {
  const label = role === 'user' ? '你' : '🤖 AI';
  const escaped = escapeHtml(content);
  // Simple markdown-like rendering for inline code and paragraphs
  let formatted = escaped
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  formatted = '<p>' + formatted + '</p>';

  return `<div class="chat-message ${role}">
    <div class="msg-label">${label}</div>
    <div class="msg-content">${formatted}</div>
  </div>`;
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;

  const apiKey = Storage.getApiKey();
  if (!apiKey) {
    alert('请先点击右上角 🔑 设置 API Key');
    return;
  }

  input.value = '';
  input.disabled = true;
  document.getElementById('chatSendBtn').disabled = true;

  const container = document.getElementById('chatMessages');
  if (!container) return;

  // Remove welcome message if present
  const welcome = container.querySelector('.chat-welcome');
  if (welcome) welcome.remove();

  // Add user message
  container.innerHTML += renderChatMessage('user', text);
  Storage.addChatMessage({ role: 'user', content: text });

  // Add streaming assistant message placeholder
  const streamingId = 'stream-' + Date.now();
  container.innerHTML += `<div class="chat-message assistant chat-streaming" id="${streamingId}">
    <div class="msg-label">🤖 AI</div>
    <div class="msg-content"><p></p></div>
  </div>`;
  container.scrollTop = container.scrollHeight;

  // Build message history
  const history = Storage.getChatHistory();
  const messages = history.filter(m => m.role === 'user' || m.role === 'assistant').slice(-20);

  // System prompt with context
  const currentRoute = window.location.hash.slice(1) || 'home';
  const systemPrompt = getChatSystemPrompt(currentRoute);

  // Create abort controller
  _chatAbortController = new AbortController();

  try {
    let fullText = '';
    const streamEl = document.getElementById(streamingId);

    await API.chatStream(
      messages,
      systemPrompt,
      document.getElementById('chatModel')?.value || CONFIG.DEFAULT_MODEL,
      (chunk, accumulated) => {
        fullText = accumulated;
        if (streamEl) {
          const contentEl = streamEl.querySelector('.msg-content');
          if (contentEl) {
            contentEl.innerHTML = '<p>' + escapeHtml(fullText)
              .replace(/\n\n/g, '</p><p>')
              .replace(/\n/g, '<br>')
              .replace(/`([^`]+)`/g, '<code>$1</code>')
              .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>') + '</p>';
          }
        }
        container.scrollTop = container.scrollHeight;
      },
      _chatAbortController.signal
    );

    // Replace streaming element with final rendered message
    if (streamEl) {
      streamEl.classList.remove('chat-streaming');
      streamEl.querySelector('.msg-content').innerHTML = '<p>' + escapeHtml(fullText)
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>') + '</p>';
    }

    // Save assistant message
    Storage.addChatMessage({ role: 'assistant', content: fullText });

    // Re-render MathJax
    if (streamEl) {
      await typesetMath(streamEl);
    }
  } catch (err) {
    if (err.name === 'AbortError') {
      container.innerHTML += renderChatMessage('assistant', '⏹️ 已停止生成。');
    } else {
      const streamEl = document.getElementById(streamingId);
      if (streamEl) {
        streamEl.classList.remove('chat-streaming');
        streamEl.querySelector('.msg-content').innerHTML = `<p style="color:var(--danger)">❌ 错误: ${escapeHtml(err.message)}</p>`;
      }
    }
  } finally {
    input.disabled = false;
    document.getElementById('chatSendBtn').disabled = false;
    input.focus();
    _chatAbortController = null;
  }
}

function getChatSystemPrompt(currentRoute) {
  let contextInfo = '';
  if (currentRoute && currentRoute !== 'home') {
    // Try to extract topic info from route
    const routeParts = currentRoute.split('/');
    const topicMap = {
      'limits': '极限与连续',
      'derivatives': '微分学',
      'integration': '积分学',
      'integrals': '积分学',
      'series': '无穷级数',
      'multivariable': '多元微积分',
    };
    for (const [key, name] of Object.entries(topicMap)) {
      if (currentRoute.includes(key)) {
        contextInfo = `学生当前正在浏览：${name}。`;
        break;
      }
    }
  }

  return `你是 MathLearnLab 的考研数学 AI 助手。${contextInfo}

你的角色：
- 用中文回答，语言通俗易懂，帮助考研学生理解数学概念
- 数学公式用 LaTeX 格式（\`$...$\` 行内，\`$$...$$\` 块级）
- 回答要有层次：先给简短结论，再展开详细解释
- 主动指出常见错误和易混淆的概念
- 举例说明抽象概念（如华里士公式、格林公式等）
- 如果学生问题目，先给思路引导，不要直接给完整答案
- 保持鼓励和支持的语气

考试范围：考研数学一/二/三（高等数学、线性代数、概率论与数理统计）`;
}

function updateChatContextHint() {
  const hint = document.getElementById('chatContextHint');
  if (!hint) return;
  const currentRoute = window.location.hash.slice(1) || 'home';
  if (currentRoute && currentRoute !== 'home') {
    const parts = currentRoute.split('/');
    const last = parts[parts.length - 1];
    const nameMap = {
      'limits': '极限与连续',
      'integration': '积分学', 'integrals': '积分学',
      'series': '无穷级数',
      'multivariable': '多元微积分',
      'derivatives': '微分学',
    };
    const topicName = nameMap[last] || last;
    hint.textContent = `📍 当前：${topicName} — 可以问我相关内容`;
  } else {
    hint.textContent = '';
  }
}

// Update chat context when route changes
window.addEventListener('hashchange', () => {
  updateChatContextHint();
});
