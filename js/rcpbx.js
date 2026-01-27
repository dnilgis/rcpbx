/**
 * rcpbx Interactive Features
 * Include this on all pages
 */

// ===== MOBILE LOGO TOUCH SUPPORT =====
document.addEventListener('DOMContentLoaded', function() {
  const logo = document.querySelector('.logo-container');
  if (logo) {
    logo.addEventListener('touchstart', function() {
      this.classList.add('active');
    });
    logo.addEventListener('touchend', function() {
      const el = this;
      setTimeout(function() {
        el.classList.remove('active');
      }, 1500);
    });
  }
});


// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
  const searchInput = document.getElementById('search');
  
  // Press / to focus search
  if (e.key === '/' && searchInput && document.activeElement !== searchInput) {
    e.preventDefault();
    searchInput.focus();
  }
  
  // Press Escape to blur search
  if (e.key === 'Escape' && searchInput) {
    searchInput.blur();
    searchInput.value = '';
    searchInput.dispatchEvent(new Event('input'));
  }
});


// ===== EASTER EGG SEARCH RESPONSES (homepage only) =====
const easterEggs = {
  'hello': 'Hey there, chef! 👋',
  'hi': 'Hello! Ready to cook something delicious?',
  'help': 'Try searching for "chicken" or "pasta"',
  'secret': '🤫 You found a secret!',
  'bacon': 'Bacon makes everything better.',
  'pizza': 'Pizza is always the answer.',
  'coffee': '☕ First coffee, then cooking.',
  'wine': '🍷 For the dish... and the chef.',
  'butter': 'More butter. Always more butter.',
  '42': 'The answer to life, the universe, and dinner.',
  'ramsay': '🔥 IT\'S RAW!',
  'gordon': '🔥 WHERE\'S THE LAMB SAUCE?!',
  'mama': 'Just like mama used to make 💚',
  'love': 'The secret ingredient is always love.',
  'hungry': 'Let\'s fix that! Pick a category above.'
};

function showToast(msg) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'search-toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(function() {
    toast.classList.remove('show');
  }, 2500);
}

// Attach to search input if on homepage
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search');
  if (searchInput && document.querySelector('.categories')) {
    searchInput.addEventListener('input', function(e) {
      const val = e.target.value.toLowerCase().trim();
      if (easterEggs[val]) {
        showToast(easterEggs[val]);
      }
    });
  }
});


// ===== KONAMI CODE =====
const konamiCode = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a'];
let konamiIndex = 0;

document.addEventListener('keydown', function(e) {
  if (e.key === konamiCode[konamiIndex]) {
    konamiIndex++;
    if (konamiIndex === konamiCode.length) {
      document.body.classList.add('flash');
      showToast('🎮 +30 lives! (just kidding, but nice moves)');
      setTimeout(function() {
        document.body.classList.remove('flash');
      }, 300);
      konamiIndex = 0;
    }
  } else {
    konamiIndex = 0;
  }
});


// ===== VIEW COUNTER (homepage only) =====
document.addEventListener('DOMContentLoaded', function() {
  const viewCountEl = document.getElementById('viewCount');
  if (viewCountEl) {
    fetch('https://api.counterapi.dev/v1/rcpbx/visits/up')
      .then(function(r) { return r.json(); })
      .then(function(d) {
        viewCountEl.textContent = d.count.toLocaleString() + ' views';
      })
      .catch(function() {
        // Silently fail
      });
  }
});
