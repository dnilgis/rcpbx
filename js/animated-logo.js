/**
 * rcpbx Animated Logo
 * Resting state: rcpbx
 * Hover state: recipebox (vowels fill in)
 * Leave state: vowels fall away
 * 
 * USAGE:
 * 1. Add CSS to your stylesheet
 * 2. Use this HTML structure for the logo:
 * 
 * <a href="./" class="logo-container" tabindex="0">
 *   <span class="logo-text">
 *     <span class="logo-char">r</span><span class="logo-vowel v-e1">e</span><span class="logo-char">c</span><span class="logo-vowel v-i">i</span><span class="logo-char">p</span><span class="logo-vowel v-e2">e</span><span class="logo-char">b</span><span class="logo-vowel v-o">o</span><span class="logo-char">x</span>
 *   </span>
 * </a>
 * 
 * 3. Optional: Add JS for mobile touch support
 */

/* ===== CSS ===== */
/*
.logo-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
  text-decoration: none;
}

.logo-text {
  font-family: var(--font-mono, 'JetBrains Mono', monospace);
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text, #222);
  display: flex;
  align-items: baseline;
}

.logo-char {
  display: inline-block;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.3s ease;
}

.logo-vowel {
  opacity: 0;
  transform: translateY(-20px);
  width: 0;
  overflow: hidden;
  transition: width 0.3s ease, opacity 0.4s ease, transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Hover - vowels appear with staggered timing */
.logo-container:hover .logo-vowel,
.logo-container:focus .logo-vowel,
.logo-container.active .logo-vowel {
  opacity: 1;
  transform: translateY(0);
}

.logo-container:hover .logo-vowel.v-e1,
.logo-container.active .logo-vowel.v-e1 { width: 0.65em; transition-delay: 0s; }

.logo-container:hover .logo-vowel.v-i,
.logo-container.active .logo-vowel.v-i { width: 0.35em; transition-delay: 0.05s; }

.logo-container:hover .logo-vowel.v-e2,
.logo-container.active .logo-vowel.v-e2 { width: 0.65em; transition-delay: 0.1s; }

.logo-container:hover .logo-vowel.v-o,
.logo-container.active .logo-vowel.v-o { width: 0.65em; transition-delay: 0.15s; }

/* Leave - vowels fall away with reverse stagger */
.logo-container:not(:hover):not(.active) .logo-vowel {
  transform: translateY(30px);
  opacity: 0;
}

.logo-container:not(:hover):not(.active) .logo-vowel.v-e1 { transition-delay: 0.15s; }
.logo-container:not(:hover):not(.active) .logo-vowel.v-i { transition-delay: 0.1s; }
.logo-container:not(:hover):not(.active) .logo-vowel.v-e2 { transition-delay: 0.05s; }
.logo-container:not(:hover):not(.active) .logo-vowel.v-o { transition-delay: 0s; }
*/

/* ===== JavaScript for Mobile Touch Support ===== */
document.addEventListener('DOMContentLoaded', function() {
  const logo = document.querySelector('.logo-container');
  if (logo) {
    // Touch start - activate
    logo.addEventListener('touchstart', function() {
      this.classList.add('active');
    });
    
    // Touch end - deactivate after delay so animation completes
    logo.addEventListener('touchend', function() {
      const el = this;
      setTimeout(function() {
        el.classList.remove('active');
      }, 1500);
    });
  }
});

/* ===== Minified CSS (copy this) ===== */
const LOGO_CSS = `.logo-container{position:relative;display:inline-block;cursor:pointer;text-decoration:none}.logo-text{font-family:var(--font-mono,'JetBrains Mono',monospace);font-size:1.25rem;font-weight:600;letter-spacing:-0.02em;color:var(--text,#222);display:flex;align-items:baseline}.logo-char{display:inline-block;transition:transform .4s cubic-bezier(.34,1.56,.64,1),opacity .3s ease}.logo-vowel{opacity:0;transform:translateY(-20px);width:0;overflow:hidden;transition:width .3s ease,opacity .4s ease,transform .5s cubic-bezier(.34,1.56,.64,1)}.logo-container:hover .logo-vowel,.logo-container:focus .logo-vowel,.logo-container.active .logo-vowel{opacity:1;transform:translateY(0)}.logo-container:hover .logo-vowel.v-e1,.logo-container.active .logo-vowel.v-e1{width:.65em;transition-delay:0s}.logo-container:hover .logo-vowel.v-i,.logo-container.active .logo-vowel.v-i{width:.35em;transition-delay:.05s}.logo-container:hover .logo-vowel.v-e2,.logo-container.active .logo-vowel.v-e2{width:.65em;transition-delay:.1s}.logo-container:hover .logo-vowel.v-o,.logo-container.active .logo-vowel.v-o{width:.65em;transition-delay:.15s}.logo-container:not(:hover):not(.active) .logo-vowel{transform:translateY(30px);opacity:0}.logo-container:not(:hover):not(.active) .logo-vowel.v-e1{transition-delay:.15s}.logo-container:not(:hover):not(.active) .logo-vowel.v-i{transition-delay:.1s}.logo-container:not(:hover):not(.active) .logo-vowel.v-e2{transition-delay:.05s}.logo-container:not(:hover):not(.active) .logo-vowel.v-o{transition-delay:0s}`;

/* ===== HTML (copy this) ===== */
const LOGO_HTML = `<a href="./" class="logo-container" tabindex="0">
  <span class="logo-text">
    <span class="logo-char">r</span><span class="logo-vowel v-e1">e</span><span class="logo-char">c</span><span class="logo-vowel v-i">i</span><span class="logo-char">p</span><span class="logo-vowel v-e2">e</span><span class="logo-char">b</span><span class="logo-vowel v-o">o</span><span class="logo-char">x</span>
  </span>
</a>`;

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { LOGO_CSS, LOGO_HTML };
}
