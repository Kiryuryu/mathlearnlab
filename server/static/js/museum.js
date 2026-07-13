// Museum global utilities
var Museum = (function() {
  function toggleTheme() {
    var html = document.documentElement;
    var current = html.getAttribute('data-theme') || 'light';
    html.setAttribute('data-theme', current === 'light' ? 'dark' : 'light');
    try { localStorage.setItem('mathlearnlab:theme', current === 'light' ? 'dark' : 'light'); } catch(e) {}
  }


  // Enable exhibit card click navigation
  document.addEventListener('click', function(e) {
    var card = e.target.closest('.exhibit-card');
    if (card && card.dataset.href && !card.classList.contains('coming-soon')) {
      window.location.href = card.dataset.href;
    }
  });

  return { toggleTheme: toggleTheme };
})();
