// Application configuration and constants
const CONFIG = {
  // Cloudflare Worker URL — change this after deploying your worker
  API_BASE_URL: 'https://mathlearnlab-api.joycezhang.workers.dev',

  // Claude models
  DEFAULT_MODEL: 'claude-sonnet-4-20250514',
  FAST_MODEL: 'claude-haiku-4-5-20251001',

  MAX_GRADING_TOKENS: 2000,
  MAX_CHAT_TOKENS: 4096,

  // Topics mapping (sync with ocr_practice/config.py)
  TOPICS: {
    limits:        { zh: '极限与连续', icon: '📈', json: 'limits.json' },
    derivatives:   { zh: '微分学',     icon: '📉', json: 'derivatives.json' },
    integrals:     { zh: '积分学',     icon: '∫',  json: 'integrals.json' },
    series:        { zh: '无穷级数',   icon: 'Σ',  json: 'series.json' },
    multivariable: { zh: '多元微积分', icon: '🌐', json: 'multivariable.json' },
  },

  DIFFICULTY: {
    easy:   { zh: '简单', stars: '⭐', color: 'green' },
    medium: { zh: '中等', stars: '⭐⭐', color: 'orange' },
    hard:   { zh: '困难', stars: '⭐⭐⭐', color: 'red' },
  },

  // Routes to content file paths
  ROUTES: {
    'home': null,
    // Notebooks
    'notebooks/01-gaoshu/01-limits':            'content/notebooks/01-gaoshu/01-limits-continuity-differentiation.md',
    'notebooks/01-gaoshu/02-integration':        'content/notebooks/01-gaoshu/02-integration.md',
    'notebooks/01-gaoshu/03-series':             'content/notebooks/01-gaoshu/03-infinite-series.md',
    'notebooks/01-gaoshu/04-multivariable':      'content/notebooks/01-gaoshu/04-multivariable-calculus.md',
    // Notes
    'notes/01-gaoshu':   'content/notes/01-gaoshu/README.md',
    'notes/02-xiandai':  'content/notes/02-xiandai/README.md',
    'notes/03-gailvlun': 'content/notes/03-gailvlun/README.md',
    // Problems
    'problems/01-gaoshu/limits':         'content/problems/01-gaoshu/limits-problems.md',
    'problems/01-gaoshu/integration':    'content/problems/01-gaoshu/integration-problems.md',
    'problems/01-gaoshu/series':         'content/problems/01-gaoshu/series-problems.md',
    'problems/01-gaoshu/multivariable':  'content/problems/01-gaoshu/multivariable-problems.md',
    // Error log
    'error-log/01-gaoshu': 'content/error-log/01-gaoshu-errors.md',
    // Practice
    'practice/limits':        'practice:limits',
    'practice/derivatives':   'practice:derivatives',
    'practice/integrals':     'practice:integrals',
    'practice/series':        'practice:series',
    'practice/multivariable': 'practice:multivariable',
  },
};
