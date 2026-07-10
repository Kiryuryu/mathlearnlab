// App initialization
(function() {
  // Responsive: show chat float button on mobile
  function handleResize() {
    const floatBtn = document.getElementById('chatFloatBtn');
    const panel = document.getElementById('chatPanel');
    if (!floatBtn || !panel) return;
    if (window.innerWidth <= 768) {
      floatBtn.hidden = false;
      panel?.classList.remove('collapsed');
    } else {
      floatBtn.hidden = true;
    }
  }

  window.addEventListener('resize', handleResize);
  document.addEventListener('DOMContentLoaded', handleResize);
})();
