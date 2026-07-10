// MuseumChat — Floating chat popup with multi-model support
var MuseumChat = (function() {
  var messages = [];
  var abortController = null;
  var currentModel = 'claude-sonnet-4-20250514';
  var customModelId = '';
  var customApiKey = '';
  var initialized = false;

  function $(id) { return document.getElementById(id); }

  function init() {
    if (initialized) return;
    initialized = true;
    // Ensure popup starts hidden
    var p = $('chatPopup');
    if (p) p.hidden = true;
    // Restore custom model config
    try { customModelId = localStorage.getItem('museum:customModelId') || ''; } catch(e) {}
    try { customApiKey = localStorage.getItem('museum:customApiKey') || ''; } catch(e) {}
    if (customModelId) {
      currentModel = customModelId;
      $('chatModelSelect').value = 'custom';
      $('customModelConfig').style.display = 'block';
      $('customModelId').value = customModelId;
      $('customApiKey').value = customApiKey;
    }
    updateContextHint();
  }

  function toggle() {
    var p = $('chatPopup');
    if (!p) return;
    var hidden = p.hidden;
    var display = p.style.display;
    if (display === 'none') {
      // Was hidden via style, show it
      p.style.display = '';
      p.hidden = false;
    } else if (p.hidden) {
      p.hidden = false;
      p.style.display = '';
    } else {
      p.hidden = true;
      p.style.display = 'none';
    }
  }

  function setModel(val) {
    if (val === 'custom') {
      $('customModelConfig').style.display = 'block';
    } else {
      $('customModelConfig').style.display = 'none';
      currentModel = val;
    }
  }

  function saveCustomModel() {
    customModelId = $('customModelId').value.trim();
    customApiKey = $('customApiKey').value.trim();
    currentModel = customModelId || 'claude-sonnet-4-20250514';
    try { localStorage.setItem('museum:customModelId', customModelId); } catch(e) {}
    try { localStorage.setItem('museum:customApiKey', customApiKey); } catch(e) {}
    $('customModelConfig').style.display = 'none';
    addSystemMsg('已切换模型: ' + currentModel);
  }

  function newSession() {
    messages = [];
    $('chatPopupMessages').innerHTML = '<div style="text-align:center;color:var(--text-muted);padding:24px 12px;font-size:13px;"><p>新会话开始</p></div>';
  }

  function onKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  }

  function updateContextHint() {
    var hint = $('chatContextHint');
    if (!hint) return;
    var path = window.location.pathname;
    var hints = { limits:'极限', derivatives:'导数', integrals:'积分', series:'级数', multivariable:'多元' };
    for (var k in hints) { if (path.includes(k)) { hint.textContent = '当前浏览: ' + hints[k]; return; } }
    hint.textContent = '';
  }

  function addSystemMsg(text) {
    var div = document.createElement('div');
    div.style.cssText = 'text-align:center;font-size:11px;color:var(--text-muted);padding:4px;';
    div.textContent = text;
    $('chatPopupMessages').appendChild(div);
  }

  function renderMessage(role, content) {
    var div = document.createElement('div');
    div.className = 'chat-msg ' + role;
    div.textContent = content;
    $('chatPopupMessages').appendChild(div);
  }

  async function send() {
    var input = $('chatPopupInput');
    var text = input.value.trim();
    if (!text || abortController) return;

    input.value = '';
    input.disabled = true;
    $('chatPopupSend').disabled = true;

    messages.push({ role: 'user', content: text });
    renderMessage('user', text);

    // Streaming placeholder
    var streamDiv = document.createElement('div');
    streamDiv.className = 'chat-msg assistant';
    streamDiv.id = 'streamMsg-' + Date.now();
    $('chatPopupMessages').appendChild(streamDiv);

    var container = $('chatPopupMessages');
    container.scrollTop = container.scrollHeight;

    abortController = new AbortController();

    try {
      var apiKey = '';
      try { apiKey = localStorage.getItem('mathlearnlab:apikey') || ''; } catch(e) {}
      if (customApiKey) apiKey = customApiKey;

      var resp = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
        body: JSON.stringify({
          messages: messages.slice(-30),
          model: currentModel,
          context_route: window.location.pathname,
        }),
        signal: abortController.signal,
      });

      if (!resp.ok) throw new Error('API error ' + resp.status);

      var reader = resp.body.getReader();
      var decoder = new TextDecoder();
      var fullText = '';
      var buffer = '';

      while (true) {
        var { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        var lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (var i = 0; i < lines.length; i++) {
          var line = lines[i];
          if (!line.startsWith('data: ')) continue;
          var data = line.slice(6);
          if (data === '[DONE]') { abortController = null; break; }
          try {
            var parsed = JSON.parse(data);
            if (parsed.error) throw new Error(parsed.error);
            if (parsed.type === 'content_block_delta') {
              fullText += parsed.delta.text || '';
              streamDiv.textContent = fullText;
              container.scrollTop = container.scrollHeight;
            }
          } catch(e) {}
        }
      }
      messages.push({ role: 'assistant', content: fullText });
    } catch(e) {
      if (e.name !== 'AbortError') {
        streamDiv.textContent = '错误: ' + e.message;
        streamDiv.style.color = 'var(--accent-error)';
      }
    } finally {
      input.disabled = false;
      $('chatPopupSend').disabled = false;
      abortController = null;
      input.focus();
    }
  }

  document.addEventListener('DOMContentLoaded', init);
  // Also init immediately in case DOMContentLoaded already fired
  if (document.readyState === 'interactive' || document.readyState === 'complete') {
    setTimeout(init, 100);
  }
  return { toggle: toggle, send: send, onKeydown: onKeydown, setModel: setModel, saveCustomModel: saveCustomModel, newSession: newSession };
})();
