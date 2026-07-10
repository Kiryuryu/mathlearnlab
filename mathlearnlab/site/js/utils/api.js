// API client — calls Cloudflare Worker proxy

const API = {
  /**
   * Send a chat message with streaming response.
   * @param {Array} messages - [{role, content}, ...]
   * @param {string} systemPrompt
   * @param {string} model
   * @param {function} onChunk - called with each text chunk
   * @param {AbortSignal} signal
   * @returns {Promise<string>} - full response text
   */
  async chatStream(messages, systemPrompt, model, onChunk, signal) {
    const apiKey = Storage.getApiKey();
    if (!apiKey) throw new Error('请先设置 API Key');

    const resp = await fetch(CONFIG.API_BASE_URL + '/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
      },
      body: JSON.stringify({
        messages,
        system: systemPrompt,
        model: model || CONFIG.DEFAULT_MODEL,
        max_tokens: CONFIG.MAX_CHAT_TOKENS,
      }),
      signal,
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(`API 错误 (${resp.status}): ${errText}`);
    }

    // Read SSE stream
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
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') break;
          try {
            const parsed = JSON.parse(data);
            if (parsed.type === 'content_block_delta') {
              const text = parsed.delta?.text || '';
              fullText += text;
              onChunk(text, fullText);
            }
          } catch {
            // skip parse errors for partial chunks
          }
        }
      }
    }

    return fullText;
  },

  /**
   * Grade a handwritten answer.
   * @param {Object} problem - Problem object from problem bank
   * @param {string} imageBase64 - Base64-encoded JPEG
   * @returns {Promise<Object>} - grading result
   */
  async gradeSubmission(problem, imageBase64) {
    const apiKey = Storage.getApiKey();
    if (!apiKey) throw new Error('请先设置 API Key');

    const resp = await fetch(CONFIG.API_BASE_URL + '/api/grade', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
      },
      body: JSON.stringify({
        problem,
        image_base64: imageBase64,
        model: CONFIG.DEFAULT_MODEL,
        max_tokens: CONFIG.MAX_GRADING_TOKENS,
      }),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(`批改 API 错误 (${resp.status}): ${errText}`);
    }

    return resp.json();
  },

  /**
   * Non-streaming chat (for simple queries).
   */
  async chat(messages, systemPrompt, model) {
    const apiKey = Storage.getApiKey();
    if (!apiKey) throw new Error('请先设置 API Key');

    const resp = await fetch(CONFIG.API_BASE_URL + '/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
      },
      body: JSON.stringify({
        messages,
        system: systemPrompt,
        model: model || CONFIG.DEFAULT_MODEL,
        max_tokens: CONFIG.MAX_CHAT_TOKENS,
        stream: false,
      }),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(`API 错误 (${resp.status}): ${errText}`);
    }

    const data = await resp.json();
    return data.content?.[0]?.text || '';
  },
};
