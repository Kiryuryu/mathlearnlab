// AI Chat — SSE streaming, marginal note style

(function() {
  let abortController = null;

  function $(id) { return document.getElementById(id); }

  function getApiKey() {
    try { return localStorage.getItem('mathlearnlab:apikey') || ''; }
    catch { return ''; }
  }

  function getChatHistory() {
    try { return JSON.parse(sessionStorage.getItem('mathlearnlab:chatHistory') || '[]'); }
    catch { return []; }
  }

  function saveChatMessage(msg) {
    try {
      const h = getChatHistory();
      h.push(msg);
      if (h.length > 100) h.splice(0, h.length - 100);
      sessionStorage.setItem('mathlearnlab:chatHistory', JSON.stringify(h));
    } catch {}
  }

  function clearChatHistory() {
    try { sessionStorage.removeItem('mathlearnlab:chatHistory'); } catch {}
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function renderMessage(role, content) {
    const label = role === 'user' ? '你' : '';
    const cls = role === 'user' ? 'chat-message user' : 'chat-message assistant';
    const formatted = escapeHtml(content)
      .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    return `<div class="${cls}"><p>${formatted}</p></div>`;
  }

  function loadHistory() {
    const container = $('chatMessages');
    if (!container) return;
    const history = getChatHistory();
    if (history.length === 0) {
      container.innerHTML = `<div class="chat-welcome">
        <p>有不懂的概念随时问。</p>
        <p class="chat-context-hint" id="chatContextHint"></p>
      </div>`;
      return;
    }
    container.innerHTML = history.map(m => renderMessage(m.role, m.content)).join('');
    container.scrollTop = container.scrollHeight;
  }

  async function sendMessage() {
    const input = $('chatInput');
    const text = input?.value?.trim();
    if (!text) return;

    const apiKey = getApiKey();
    if (!apiKey) { alert('请先点击右上角"钥"设置 API Key'); return; }

    input.value = '';
    input.disabled = true;
    $('chatSendBtn').disabled = true;

    const container = $('chatMessages');
    const welcome = container?.querySelector('.chat-welcome');
    if (welcome) welcome.remove();

    // Add user message
    container.innerHTML += renderMessage('user', text);
    saveChatMessage({ role: 'user', content: text });
    container.scrollTop = container.scrollHeight;

    // Streaming placeholder
    const msgId = 'stream-' + Date.now();
    container.innerHTML += `<div class="chat-message assistant" id="${msgId}"><p></p></div>`;

    // Build messages from history
    const history = getChatHistory();
    const messages = history.slice(-20);

    const contextRoute = window.location.pathname;
    abortController = new AbortController();

    try {
      const resp = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey,
        },
        body: JSON.stringify({
          messages,
          model: $('chatModel')?.value,
          context_route: contextRoute,
        }),
        signal: abortController.signal,
      });

      if (!resp.ok) {
        throw new Error(`API 错误 (${resp.status})`);
      }

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let fullText = '';
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const data = line.slice(6);
          if (data === '[DONE]') break;
          try {
            const parsed = JSON.parse(data);
            if (parsed.error) throw new Error(parsed.error);
            if (parsed.type === 'content_block_delta') {
              fullText += parsed.delta.text || '';
              const el = $(msgId);
              if (el) {
                el.innerHTML = '<p>' + escapeHtml(fullText)
                  .replace(/\n\n/g, '</p><p>')
                  .replace(/\n/g, '<br>')
                  .replace(/`([^`]+)`/g, '<code>$1</code>') + '</p>';
              }
              container.scrollTop = container.scrollHeight;
            }
          } catch {}
        }
      }

      saveChatMessage({ role: 'assistant', content: fullText });
      // Re-render MathJax
      const el = $(msgId);
      if (el && window.MathJax) MathJax.typesetPromise([el]);
    } catch (err) {
      if (err.name !== 'AbortError') {
        const el = $(msgId);
        if (el) el.innerHTML = `<p style="color:var(--accent-error);">错误: ${escapeHtml(err.message)}</p>`;
      }
    } finally {
      input.disabled = false;
      $('chatSendBtn').disabled = false;
      input.focus();
    }
  }

  function togglePanel() {
    const panel = $('chatPanel');
    const floatBtn = $('chatFloatBtn');
    if (window.innerWidth <= 768) {
      panel?.classList.toggle('mobile-open');
    } else {
      panel?.classList.toggle('collapsed');
      if (floatBtn) floatBtn.hidden = !panel?.classList.contains('collapsed');
    }
  }

  function updateContextHint() {
    const hint = $('chatContextHint');
    if (!hint) return;
    const path = window.location.pathname;
    const hints = {
      limits: '极限与连续', derivatives: '微分学', integrals: '积分学',
      integration: '积分学', series: '无穷级数', multivariable: '多元微积分',
    };
    for (const [key, name] of Object.entries(hints)) {
      if (path.includes(key)) { hint.textContent = '当前: ' + name; return; }
    }
    hint.textContent = '';
  }

  // Init
  document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    updateContextHint();

    $('chatSendBtn')?.addEventListener('click', sendMessage);
    $('chatInput')?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
    $('chatNewBtn')?.addEventListener('click', () => {
      clearChatHistory();
      loadHistory();
    });
    $('chatToggleBtn')?.addEventListener('click', togglePanel);
    $('chatFloatBtn')?.addEventListener('click', togglePanel);

    // API Key modal
    setupApiKeyModal();
  });

  function setupApiKeyModal() {
    const modal = $('apiKeyModal');
    const btn = $('apiKeyBtn');
    if (!modal || !btn) return;

    btn.addEventListener('click', () => {
      const input = $('apiKeyInput');
      if (input) input.value = getApiKey();
      modal.hidden = false;
    });

    $('apiKeySave')?.addEventListener('click', () => {
      const key = $('apiKeyInput')?.value?.trim() || '';
      try { localStorage.setItem('mathlearnlab:apikey', key); } catch {}
      modal.hidden = true;
      $('apiKeyBtn').textContent = key ? '钥✓' : '钥';
    });

    $('apiKeyCancel')?.addEventListener('click', () => { modal.hidden = true; });
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.hidden = true; });

    if (getApiKey()) btn.textContent = '钥✓';
  }
})();
