/**
 * Cloudflare Worker — MathLearnLab API Proxy
 *
 * Proxies requests from the GitHub Pages static site to Anthropic API.
 * Endpoints:
 *   POST /api/chat   — Text chat with optional SSE streaming
 *   POST /api/grade  — OCR + grading with image
 *
 * Deploy: npx wrangler deploy
 */

const ANTHROPIC_API_BASE = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_VERSION = '2023-06-01';

// CORS headers for all responses
function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
    'Access-Control-Max-Age': '86400',
  };
}

// Grading system prompt (ported from ocr_practice/prompts/grader.py)
const GRADER_SYSTEM_PROMPT = `You are an expert math grader for a Chinese graduate entrance exam (考研数学) preparation app.

Your task:
1. Read the handwritten math solution from the uploaded image carefully
2. Compare it against the provided correct solution and grading rubric
3. Provide a detailed, constructive verdict in Chinese

## Grading Principles

- Be STRICT on key steps — if a critical mathematical step is wrong or missing, mark it.
- Be GENEROUS on arithmetic — minor calculation errors without conceptual mistakes = partial credit.
- If the handwriting is illegible, say so in ocr_text and mark as "incorrect" with the reason being illegible handwriting.
- Identify the LIKELY misconception behind the error, not just that the answer is wrong.
- Give SPECIFIC, ACTIONABLE advice — say exactly what to review or practice.

## Output Format

You must output ONLY valid JSON, no other text:

{
  "ocr_text": "The handwritten content you read from the image, faithfully transcribed line by line. Include all mathematical expressions in LaTeX notation.",
  "verdict": "correct" | "partially_correct" | "incorrect",
  "score": "满分" | "部分得分" | "零分",
  "what_is_correct": "Detailed feedback on what the student did right, in Chinese.",
  "what_is_wrong": "Detailed feedback on what the student did wrong, in Chinese. Empty string if verdict is correct.",
  "key_misconception": "The likely conceptual misunderstanding, in Chinese. null if none.",
  "suggestion": "Specific actionable advice for improvement, in Chinese.",
  "graded_steps": [
    {"step": "Key step description", "status": "ok" | "wrong" | "missing", "comment": "Brief comment in Chinese"}
  ]
}

IMPORTANT:
- All feedback text MUST be in Chinese
- Write math expressions in LaTeX notation
- Be encouraging and supportive
- Always mention specific things the student did well, even if the answer is wrong`;

/**
 * Build grading message for Claude Vision API.
 */
function buildGradingMessage(problem, imageBase64) {
  const solution = problem.solution || {};
  const rubric = problem.grading_rubric || {};

  // Format solution steps
  let stepsText = '';
  (solution.steps || []).forEach((step, i) => {
    stepsText += `${i + 1}. ${step}\n`;
  });
  if (!stepsText) stepsText = solution.method || '无详细步骤';

  // Format rubric
  let rubricText = '';
  const keySteps = rubric.key_steps || [];
  const commonErrors = rubric.common_errors || [];
  if (keySteps.length > 0) {
    rubricText += '关键步骤：\n';
    keySteps.forEach(s => { rubricText += `  • ${s}\n`; });
  }
  if (commonErrors.length > 0) {
    rubricText += '\n常见错误：\n';
    commonErrors.forEach(e => { rubricText += `  • ${e}\n`; });
  }

  const textContent = `## Problem

${problem.problem_statement || ''}

## Correct Solution

${stepsText}
最终答案：${solution.final_answer || ''}

## Grading Rubric

${rubricText}

## Student's Handwritten Answer

Please read the handwritten answer from the image below and grade it according to the rubric.`;

  return [
    { type: 'text', text: textContent },
    {
      type: 'image',
      source: {
        type: 'base64',
        media_type: 'image/jpeg',
        data: imageBase64,
      },
    },
  ];
}

/**
 * Build chat system prompt with context.
 */
function buildChatSystemPrompt(userSystem) {
  return userSystem || `你是一个考研数学 AI 助手。用中文回答，数学公式用 LaTeX 格式。`;
}

/**
 * Handle POST /api/chat
 */
async function handleChat(request, corsHeadersObj) {
  const apiKey = request.headers.get('X-API-Key');
  if (!apiKey) {
    return new Response(JSON.stringify({ error: 'Missing X-API-Key header' }), {
      status: 401, headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400, headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  }

  const { messages, system, model, max_tokens, stream } = body;
  if (!messages || !Array.isArray(messages)) {
    return new Response(JSON.stringify({ error: 'Missing messages array' }), {
      status: 400, headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  }

  const shouldStream = stream !== false; // default to streaming

  const anthropicBody = {
    model: model || 'claude-sonnet-4-20250514',
    max_tokens: max_tokens || 4096,
    system: buildChatSystemPrompt(system),
    messages: messages,
    stream: shouldStream,
  };

  try {
    const resp = await fetch(ANTHROPIC_API_BASE, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': ANTHROPIC_VERSION,
      },
      body: JSON.stringify(anthropicBody),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      return new Response(errText, {
        status: resp.status,
        headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
      });
    }

    if (shouldStream) {
      // Relay SSE stream
      return new Response(resp.body, {
        status: 200,
        headers: {
          ...corsHeadersObj,
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    } else {
      // Return JSON directly
      const data = await resp.json();
      return new Response(JSON.stringify(data), {
        status: 200,
        headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
      });
    }
  } catch (err) {
    return new Response(JSON.stringify({ error: `Anthropic API error: ${err.message}` }), {
      status: 502,
      headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  }
}

/**
 * Handle POST /api/grade
 */
async function handleGrade(request, corsHeadersObj) {
  const apiKey = request.headers.get('X-API-Key');
  if (!apiKey) {
    return new Response(JSON.stringify({ error: 'Missing X-API-Key header' }), {
      status: 401, headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400, headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  }

  const { problem, image_base64, model, max_tokens } = body;
  if (!problem || !image_base64) {
    return new Response(JSON.stringify({ error: 'Missing problem or image_base64' }), {
      status: 400, headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  }

  const messageContent = buildGradingMessage(problem, image_base64);

  const anthropicBody = {
    model: model || 'claude-sonnet-4-20250514',
    max_tokens: max_tokens || 2000,
    system: GRADER_SYSTEM_PROMPT,
    messages: [{ role: 'user', content: messageContent }],
    stream: false,
  };

  try {
    const resp = await fetch(ANTHROPIC_API_BASE, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': ANTHROPIC_VERSION,
      },
      body: JSON.stringify(anthropicBody),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      return new Response(errText, {
        status: resp.status,
        headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
      });
    }

    const data = await resp.json();
    const rawText = data.content?.[0]?.text || '';

    // Parse JSON from Claude's response (may be wrapped in ```json)
    let jsonText = rawText.trim();
    if (jsonText.startsWith('```json')) {
      jsonText = jsonText.slice(7);
    } else if (jsonText.startsWith('```')) {
      jsonText = jsonText.slice(3);
    }
    if (jsonText.endsWith('```')) {
      jsonText = jsonText.slice(0, -3);
    }
    jsonText = jsonText.trim();

    let result;
    try {
      result = JSON.parse(jsonText);
    } catch {
      // Fallback: return raw text as suggestion
      result = {
        ocr_text: '',
        verdict: 'unknown',
        score: '无法判定',
        what_is_correct: '',
        what_is_wrong: '',
        key_misconception: null,
        suggestion: rawText,
        graded_steps: [],
      };
    }

    return new Response(JSON.stringify(result), {
      status: 200,
      headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: `Anthropic API error: ${err.message}` }), {
      status: 502,
      headers: { ...corsHeadersObj, 'Content-Type': 'application/json' },
    });
  }
}

// === Main Worker Handler ===
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const headers = corsHeaders();

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers });
    }

    // Route
    if (url.pathname === '/api/chat' && request.method === 'POST') {
      return handleChat(request, headers);
    }

    if (url.pathname === '/api/grade' && request.method === 'POST') {
      return handleGrade(request, headers);
    }

    // Health check
    if (url.pathname === '/api/health') {
      return new Response(JSON.stringify({ status: 'ok', timestamp: Date.now() }), {
        status: 200,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }

    // 404
    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 404,
      headers: { ...headers, 'Content-Type': 'application/json' },
    });
  },
};
