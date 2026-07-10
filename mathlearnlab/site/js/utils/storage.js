// localStorage helpers

const Storage = {
  get(key, fallback = null) {
    try {
      const val = localStorage.getItem('mathlearnlab:' + key);
      return val !== null ? JSON.parse(val) : fallback;
    } catch { return fallback; }
  },

  set(key, value) {
    try {
      localStorage.setItem('mathlearnlab:' + key, JSON.stringify(value));
    } catch { /* storage full, ignore */ }
  },

  remove(key) {
    localStorage.removeItem('mathlearnlab:' + key);
  },

  // --- API Key ---
  getApiKey() {
    return localStorage.getItem('mathlearnlab:apikey') || '';
  },

  setApiKey(key) {
    if (key) {
      localStorage.setItem('mathlearnlab:apikey', key);
    } else {
      localStorage.removeItem('mathlearnlab:apikey');
    }
  },

  // --- Grade history ---
  getGradeHistory() {
    return Storage.get('gradeHistory', []);
  },

  addGradeRecord(record) {
    const history = Storage.getGradeHistory();
    history.push({ ...record, timestamp: new Date().toISOString() });
    Storage.set('gradeHistory', history);
  },

  getGradeStats() {
    const history = Storage.getGradeHistory();
    const total = history.length;
    if (total === 0) return { total: 0, correct: 0, partial: 0, incorrect: 0, accuracy: 0 };
    const correct = history.filter(h => h.verdict === 'correct').length;
    const partial = history.filter(h => h.verdict === 'partially_correct').length;
    const incorrect = history.filter(h => h.verdict === 'incorrect').length;
    return {
      total, correct, partial, incorrect,
      accuracy: Math.round(correct / total * 100),
    };
  },

  // --- Chat history ---
  getChatHistory() {
    return Storage.get('chatHistory', []);
  },

  addChatMessage(msg) {
    const history = Storage.getChatHistory();
    history.push(msg);
    if (history.length > 200) history.splice(0, history.length - 200);
    Storage.set('chatHistory', history);
  },

  clearChatHistory() {
    Storage.remove('chatHistory');
  },

  // --- Theme ---
  getTheme() {
    return localStorage.getItem('mathlearnlab:theme') || 'light';
  },

  setTheme(theme) {
    localStorage.setItem('mathlearnlab:theme', theme);
  },
};
