/**
 * rcpbx Easter Eggs & Delightful Interactions
 * Because cooking should be fun
 */

(function() {
  'use strict';

  // ============================================
  // CONFIG - Change this to your site name
  // ============================================
  
  const CONFIG = {
    // Counter namespace (letters, numbers, hyphens only)
    // This creates YOUR unique counter at counterapi.dev
    counterNamespace: 'rcpbx-com',
    counterKey: 'visits',
  };

  // ============================================
  // LOGO HOVER - EXPAND/COLLAPSE ANIMATION
  // ============================================
  
  function initLogoAnimation() {
    const logo = document.querySelector('.logo');
    if (!logo || logo.dataset.initialized) return;
    logo.dataset.initialized = 'true';
    
    const original = 'rcpbx';
    const expanded = 'recipe box';
    
    logo.innerHTML = `<span class="logo-text">${original}</span>`;
    const textEl = logo.querySelector('.logo-text');
    
    const style = document.createElement('style');
    style.textContent = `
      .logo { overflow: hidden; }
      .logo::before {
        content: '>' !important;
        margin-right: 0.25rem;
        color: var(--accent);
        display: inline-block;
        transition: transform 0.2s;
      }
      .logo:hover::before { transform: translateX(2px); }
      .logo-text { display: inline-block; transition: opacity 0.15s; }
      .logo-letter {
        display: inline-block;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        opacity: 1;
        transform: translateY(0) rotate(0deg);
      }
      .logo-letter.falling {
        opacity: 0;
        transform: translateY(20px) rotate(15deg);
      }
      .logo-letter.space { width: 0.25em; }
      .logo-tooltip {
        position: absolute;
        top: 100%;
        left: 0;
        background: var(--text);
        color: var(--bg);
        font-size: 0.65rem;
        padding: 0.3rem 0.5rem;
        border-radius: 4px;
        white-space: nowrap;
        opacity: 0;
        transform: translateY(-5px);
        transition: all 0.2s;
        pointer-events: none;
        font-family: var(--font-sans, system-ui);
        font-weight: 400;
        letter-spacing: 0;
      }
      .logo-tooltip::before {
        content: '';
        position: absolute;
        top: -4px;
        left: 12px;
        border: 4px solid transparent;
        border-bottom-color: var(--text);
      }
      .logo:hover .logo-tooltip {
        opacity: 1;
        transform: translateY(4px);
      }
    `;
    document.head.appendChild(style);
    
    const tooltip = document.createElement('span');
    tooltip.className = 'logo-tooltip';
    tooltip.textContent = 'the recipe box — stripped of stories';
    logo.style.position = 'relative';
    logo.appendChild(tooltip);
    
    logo.addEventListener('mouseenter', () => {
      textEl.innerHTML = expanded.split('').map((char, i) => 
        char === ' ' 
          ? `<span class="logo-letter space"> </span>`
          : `<span class="logo-letter" style="transition-delay: ${i * 0.02}s">${char}</span>`
      ).join('');
    });
    
    logo.addEventListener('mouseleave', () => {
      const letters = textEl.querySelectorAll('.logo-letter');
      letters.forEach((letter, i) => {
        setTimeout(() => letter.classList.add('falling'), i * 30 + Math.random() * 50);
      });
      setTimeout(() => { textEl.innerHTML = original; }, 400);
    });
  }

  // ============================================
  // CATEGORY COUNT BOUNCE
  // ============================================
  
  function initCountBounce() {
    const style = document.createElement('style');
    style.textContent = `
      .category-link .count {
        transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
      }
      .category-link:hover .count {
        transform: scale(1.15);
      }
    `;
    document.head.appendChild(style);
  }

  // ============================================
  // SEARCH EASTER EGGS
  // ============================================
  
  function initSearchEasterEggs() {
    const searchInput = document.getElementById('search');
    const resultsEl = document.getElementById('search-results');
    if (!searchInput || !resultsEl) return;
    
    const easterEggs = {
      'life story': '🙄 Not here. Just recipes.',
      'blog': '📝 Wrong site. We cook, not write novels.',
      'my grandmother': '👵 We love grandma, but skip to the recipe.',
      'advertisement': '🚫 Ad-free zone.',
      'ads': '🚫 Nope. Never.',
      'subscribe': '📧 No newsletter. Bookmark us instead.',
      'newsletter': '📧 We don\'t do that here.',
      'pinterest': '📌 Just save the URL. Simpler.',
      'scroll': '⬇️ No endless scrolling required.',
      'video': '🎬 No autoplay videos. You\'re welcome.',
      '42': '🌌 The answer to cooking, the universe, and everything.',
      'hello': '👋 Hey! Ready to cook something?',
      'hi': '👋 Hello there, chef!',
      'hungry': '🍽️ Same. Pick a recipe, any recipe.',
      'help': '🆘 Search for an ingredient or dish. We got you.',
      'secret': '🤫 You found one! Try the Konami code.',
      'easter egg': '🥚 There might be a few hidden around...',
      'konami': '🎮 ↑↑↓↓←→←→BA — try it.',
      'love': '❤️ We love you too. Now eat.',
    };
    
    searchInput.addEventListener('input', function() {
      const q = this.value.toLowerCase().trim();
      
      for (const [trigger, response] of Object.entries(easterEggs)) {
        if (q === trigger) {
          resultsEl.innerHTML = `
            <div class="search-result-item" style="justify-content: center; color: var(--text-muted); font-style: italic; padding: 1rem;">
              ${response}
            </div>
          `;
          resultsEl.classList.add('active');
          return;
        }
      }
    });
  }

  // ============================================
  // KONAMI CODE
  // ============================================
  
  function initKonamiCode() {
    const code = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];
    let index = 0;
    
    document.addEventListener('keydown', (e) => {
      if (e.code === code[index]) {
        index++;
        if (index === code.length) {
          triggerKonamiEasterEgg();
          index = 0;
        }
      } else {
        index = 0;
      }
    });
  }
  
  function triggerKonamiEasterEgg() {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
      position: fixed;
      inset: 0;
      background: var(--bg);
      z-index: 9999;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      animation: fadeIn 0.3s;
      cursor: pointer;
    `;
    
    overlay.innerHTML = `
      <div style="font-size: 4rem; margin-bottom: 1rem;">🍳</div>
      <div style="font-family: var(--font-mono); font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--accent);">Achievement Unlocked</div>
      <div style="font-family: var(--font-mono); font-size: 0.9rem; color: var(--text-muted); margin-bottom: 2rem;">Secret Chef Mode</div>
      <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-dim);">click anywhere to continue cooking</div>
      <style>
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
      </style>
    `;
    
    document.body.appendChild(overlay);
    
    overlay.addEventListener('click', () => {
      overlay.style.opacity = '0';
      overlay.style.transition = 'opacity 0.3s';
      setTimeout(() => overlay.remove(), 300);
    });
    
    const dismiss = () => {
      overlay.style.opacity = '0';
      overlay.style.transition = 'opacity 0.3s';
      setTimeout(() => overlay.remove(), 300);
      document.removeEventListener('keydown', dismiss);
    };
    setTimeout(() => document.addEventListener('keydown', dismiss), 500);
  }

  // ============================================
  // INGREDIENT COMPLETION CELEBRATION
  // ============================================
  
  function initIngredientCelebration() {
    const ingredientsList = document.querySelector('.ingredients-list');
    if (!ingredientsList) return;
    
    ingredientsList.addEventListener('click', () => {
      setTimeout(() => {
        const items = ingredientsList.querySelectorAll('li');
        const checked = ingredientsList.querySelectorAll('li.checked');
        
        if (items.length > 0 && items.length === checked.length) {
          celebrate();
        }
      }, 100);
    });
  }
  
  function celebrate() {
    const colors = ['#16a34a', '#22c55e', '#4ade80', '#86efac'];
    const container = document.createElement('div');
    container.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden;';
    document.body.appendChild(container);
    
    for (let i = 0; i < 50; i++) {
      const confetti = document.createElement('div');
      const color = colors[Math.floor(Math.random() * colors.length)];
      confetti.style.cssText = `
        position: absolute;
        width: ${Math.random() * 8 + 4}px;
        height: ${Math.random() * 8 + 4}px;
        background: ${color};
        left: ${Math.random() * 100}%;
        top: -20px;
        border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
        animation: confettiFall 1.5s ease-out ${Math.random() * 0.3}s forwards;
      `;
      container.appendChild(confetti);
    }
    
    const style = document.createElement('style');
    style.textContent = `
      @keyframes confettiFall {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
      }
    `;
    document.head.appendChild(style);
    
    const msg = document.createElement('div');
    msg.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: var(--text);
      color: var(--bg);
      padding: 1rem 2rem;
      border-radius: 8px;
      font-family: var(--font-mono);
      font-size: 0.9rem;
      z-index: 10000;
      animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    `;
    msg.textContent = '✓ Mise en place complete!';
    document.body.appendChild(msg);
    
    const popStyle = document.createElement('style');
    popStyle.textContent = `
      @keyframes popIn {
        0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
      }
    `;
    document.head.appendChild(popStyle);
    
    setTimeout(() => {
      container.remove();
      msg.style.opacity = '0';
      msg.style.transition = 'opacity 0.3s';
      setTimeout(() => msg.remove(), 300);
    }, 2000);
  }

  // ============================================
  // FOOTER EASTER EGG (click to cycle messages)
  // ============================================
  
  function initFooterEasterEgg() {
    const footer = document.querySelector('.site-footer');
    if (!footer) return;
    
    let clicks = 0;
    const messages = [
      null,
      'still no bullshit',
      'seriously, none',
      'stop clicking',
      'fine, have a cookie 🍪',
      'not that kind of cookie',
      'go cook something',
      'okay you win',
      '🎉 persistence unlocked',
    ];
    
    const tagline = footer.querySelector('p');
    if (!tagline) return;
    
    const originalText = tagline.innerHTML;
    footer.style.cursor = 'default';
    
    footer.addEventListener('click', (e) => {
      if (e.target.closest('.never-acquired')) return;
      
      clicks++;
      if (clicks < messages.length && messages[clicks]) {
        tagline.innerHTML = `rcpbx <span class="sep">·</span> ${messages[clicks]}`;
      } else if (clicks >= messages.length) {
        tagline.innerHTML = originalText;
        clicks = 0;
      }
    });
  }

  // ============================================
  // REAL VIEW COUNTER
  // Uses counterapi.dev - free, no signup, real data
  // ============================================
  
  function initViewCounter() {
    const counterEl = document.querySelector('#view-counter, .counter-num');
    if (!counterEl) return;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
      .counter-num.bump {
        animation: counterBump 0.3s ease;
      }
      @keyframes counterBump {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); color: var(--accent); }
      }
      .counter-num.loading {
        opacity: 0.5;
      }
    `;
    document.head.appendChild(style);
    
    counterEl.classList.add('loading');
    counterEl.textContent = '...';
    
    const { counterNamespace, counterKey } = CONFIG;
    
    // Only count once per session (not every page load)
    const sessionKey = `rcpbx_counted`;
    const alreadyCounted = sessionStorage.getItem(sessionKey);
    
    const baseUrl = `https://api.counterapi.dev/v1/${counterNamespace}/${counterKey}`;
    
    if (alreadyCounted) {
      // Already counted this session - just fetch current value
      fetch(baseUrl)
        .then(res => res.json())
        .then(data => {
          counterEl.classList.remove('loading');
          counterEl.textContent = (data.count || 0).toLocaleString();
        })
        .catch(() => {
          counterEl.classList.remove('loading');
          counterEl.textContent = '—';
        });
    } else {
      // New session - increment counter
      fetch(`${baseUrl}/up`)
        .then(res => res.json())
        .then(data => {
          sessionStorage.setItem(sessionKey, 'true');
          counterEl.classList.remove('loading');
          counterEl.textContent = (data.count || 0).toLocaleString();
          
          // Celebration bump
          counterEl.classList.add('bump');
          setTimeout(() => counterEl.classList.remove('bump'), 300);
        })
        .catch(() => {
          counterEl.classList.remove('loading');
          counterEl.textContent = '—';
        });
    }
  }

  // ============================================
  // ACQUISITION STATUS EASTER EGG
  // ============================================
  
  function initAcquisitionEasterEgg() {
    const acquired = document.querySelector('.never-acquired');
    if (!acquired) return;
    
    const tooltip = document.createElement('span');
    tooltip.className = 'hover-text';
    tooltip.textContent = 'and we\'d like to keep it that way';
    acquired.style.position = 'relative';
    acquired.appendChild(tooltip);
    
    const style = document.createElement('style');
    style.textContent = `
      .never-acquired .hover-text {
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: var(--text);
        color: var(--bg);
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
        font-size: 0.65rem;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: all 0.2s;
        margin-bottom: 0.4rem;
        z-index: 100;
      }
      .never-acquired .hover-text::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 4px solid transparent;
        border-top-color: var(--text);
      }
      .never-acquired:hover .hover-text {
        opacity: 1;
      }
    `;
    document.head.appendChild(style);
    
    const messages = [
      'and we\'d like to keep it that way',
      'not for sale',
      'priceless, actually',
      'our exit strategy is dinner',
    ];
    let msgIndex = 0;
    
    acquired.addEventListener('click', (e) => {
      e.stopPropagation();
      msgIndex = (msgIndex + 1) % messages.length;
      tooltip.style.opacity = '0';
      setTimeout(() => {
        tooltip.textContent = messages[msgIndex];
        tooltip.style.opacity = '1';
      }, 150);
    });
  }

  // ============================================
  // CONSOLE MESSAGE
  // ============================================
  
  function initConsoleMessage() {
    console.log('%c\n  > rcpbx\n\n  recipes, no bullshit\n\n  🍳 Happy cooking!\n', 'color: #16a34a; font-family: monospace; font-size: 12px;');
    console.log('%c👋 Hey, curious dev! Try the Konami code.', 'color: #666; font-size: 10px;');
  }

  // ============================================
  // INIT ALL
  // ============================================
  
  document.addEventListener('DOMContentLoaded', () => {
    initLogoAnimation();
    initCountBounce();
    initSearchEasterEggs();
    initKonamiCode();
    initIngredientCelebration();
    initFooterEasterEgg();
    initViewCounter();
    initAcquisitionEasterEgg();
    initConsoleMessage();
  });

})();
