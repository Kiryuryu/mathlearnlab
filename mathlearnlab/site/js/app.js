// Main app router and initialization

document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

function initApp() {
  // API Key modal
  setupApiKeyModal();

  // Route on hash change
  window.addEventListener('hashchange', handleRoute);

  // Initial route
  handleRoute();

  // If no API key is set, show the modal on first visit
  if (!Storage.getApiKey()) {
    // Don't force modal — user can use content without API key
    // Chat and OCR will prompt when needed
  }
}

function handleRoute() {
  const route = window.location.hash.slice(1) || 'home';
  ContentViewer.render(route);

  // Update sidebar highlight
  updateSidebarActive();

  // Update chat context
  updateChatContextHint();
}

// === API Key Modal ===
function setupApiKeyModal() {
  const modal = document.getElementById('apiKeyModal');
  const btn = document.getElementById('apiKeyBtn');
  const saveBtn = document.getElementById('apiKeySave');
  const cancelBtn = document.getElementById('apiKeyCancel');
  const input = document.getElementById('apiKeyInput');

  if (!modal || !btn) return;

  // Show modal
  btn.addEventListener('click', () => {
    const currentKey = Storage.getApiKey();
    if (input) input.value = currentKey;
    modal.removeAttribute('hidden');
  });

  // Save
  saveBtn?.addEventListener('click', () => {
    const key = input?.value?.trim() || '';
    Storage.setApiKey(key);
    modal.setAttribute('hidden', '');
    const keyBtn = document.getElementById('apiKeyBtn');
    if (keyBtn) keyBtn.textContent = key ? '🔑✓' : '🔑';
  });

  // Cancel
  cancelBtn?.addEventListener('click', () => {
    modal.setAttribute('hidden', '');
  });

  // Click outside to close
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.setAttribute('hidden', '');
    }
  });

  // Update key button state
  const currentKey = Storage.getApiKey();
  if (currentKey && btn) btn.textContent = '🔑✓';
}

// === Responsive sidebar toggle ===
document.addEventListener('click', (e) => {
  const toggle = document.getElementById('menuToggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  if (toggle && toggle.contains(e.target)) {
    const isOpen = sidebar?.classList.toggle('open');
    if (overlay) {
      if (isOpen) overlay.removeAttribute('hidden');
      else overlay.setAttribute('hidden', '');
    }
  }

  if (overlay && e.target === overlay) {
    sidebar?.classList.remove('open');
    overlay.setAttribute('hidden', '');
  }
});
