// Museum global utilities
var Museum = (function() {
  // Theme is handled by theme.js exclusively

  // Enable exhibit card click navigation
  document.addEventListener('click', function(e) {
    var card = e.target.closest('.exhibit-card');
    if (card && card.dataset.href && !card.classList.contains('coming-soon')) {
      window.location.href = card.dataset.href;
    }
  });

  return {};
})();
