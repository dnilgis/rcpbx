/**
 * rcpbx Contextual Kitchen Hints
 * Auto-surfaces relevant reference info on recipe pages
 */

const KitchenHints = {
  substitutions: {
    'buttermilk': { hint: '1c milk + 1T lemon, 5 min', cat: 'dairy' },
    'heavy cream': { hint: '¾c milk + ⅓c butter', cat: 'dairy' },
    'sour cream': { hint: 'Greek yogurt 1:1', cat: 'dairy' },
    'cream cheese': { hint: 'Strained Greek yogurt', cat: 'dairy' },
    'half and half': { hint: '½c cream + ½c milk', cat: 'dairy' },
    'half & half': { hint: '½c cream + ½c milk', cat: 'dairy' },
    'cake flour': { hint: '1c AP - 2T + 2T cornstarch', cat: 'flour' },
    'self-rising flour': { hint: '1c AP + 1.5t BP + ¼t salt', cat: 'flour' },
    'self rising flour': { hint: '1c AP + 1.5t BP + ¼t salt', cat: 'flour' },
    'bread flour': { hint: 'AP + 1T wheat gluten', cat: 'flour' },
    'fish sauce': { hint: 'Sub: soy + lime + pinch sugar', cat: 'asian' },
    'miso': { hint: 'Sub: tahini + splash soy', cat: 'asian' },
    'shallot': { hint: 'Sub: ½ onion + pinch garlic', cat: 'aromatics' }
  },

  temps: {
    'chicken breast': { temp: '160°F', note: 'Pull at 155°F, carryover finishes' },
    'chicken thigh': { temp: '175°F', note: 'Thighs are forgiving' },
    'whole chicken': { temp: '165°F thigh', note: 'Rest 10-15 min' },
    'pork chop': { temp: '145°F', note: 'Brine for juicier results' },
    'pork shoulder': { temp: '195-205°F', note: '1.5 hrs/lb at 275°F' },
    'beef steak': { temp: 'Rare 120° | Med 140°', note: 'Pull 5°F early' },
    'ground beef': { temp: '160°F', note: 'No pink' },
    'salmon': { temp: '125°F med', note: 'Pull early' },
    'fish': { temp: '145°F', note: 'Flakes when done' }
  },

  times: {
    'hard boiled': '12 min → ice bath',
    'soft boiled': '6 min → ice bath',
    'marinate chicken': '2-4 hours max',
    'marinate fish': '15-30 min MAX — acid breaks it down'
  },

  init: function(opts = {}) {
    const ings = document.querySelector(opts.ingredients || '.ingredients-list');
    const steps = document.querySelector(opts.instructions || '.steps-list');
    if (ings) this.scanIngredients(ings);
    if (steps) this.scanInstructions(steps);
  },

  scanIngredients: function(el) {
    el.querySelectorAll('li').forEach(li => {
      const t = li.textContent.toLowerCase();
      Object.entries(this.substitutions).forEach(([ing, d]) => {
        if (t.includes(ing)) this.addHint(li, d.hint, 'sub');
      });
    });
  },

  scanInstructions: function(el) {
    el.querySelectorAll('li').forEach(li => {
      const t = li.textContent.toLowerCase();
      Object.entries(this.temps).forEach(([item, d]) => {
        if (t.includes(item)) this.addHint(li, d.temp, 'temp', d.note);
      });
      Object.entries(this.times).forEach(([item, hint]) => {
        if (t.includes(item)) this.addHint(li, hint, 'time');
      });
    });
  },

  addHint: function(el, text, type, note) {
    if (el.querySelector('.kitchen-hint')) return;
    const hint = document.createElement('span');
    hint.className = `kitchen-hint hint-${type}`;
    hint.innerHTML = `<span class="hint-text">${text}</span>`;
    if (note) hint.title = note;
    el.appendChild(hint);
  }
};

// Inject styles using rcpbx CSS variables
(function(){
  const css = `
.kitchen-hint{display:inline-flex;align-items:center;gap:0.25em;font-family:var(--font-mono);font-size:0.7rem;background:var(--accent-dim);color:var(--accent);padding:0.2em 0.5em;border-radius:4px;margin-left:0.5em;cursor:help;white-space:nowrap}
.hint-temp{background:rgba(249,115,22,0.1);color:#f97316}
.hint-time{background:rgba(59,130,246,0.1);color:#3b82f6}
.hint-sub{background:var(--accent-dim);color:var(--accent)}
@media(max-width:768px){.kitchen-hint{display:flex;margin:0.3em 0 0;width:fit-content}}
@media print{.kitchen-hint{background:#f5f5f5!important;color:#666!important;border:1px solid #ddd}}
@media(prefers-color-scheme:dark){.hint-temp{background:rgba(249,115,22,0.15);color:#fb923c}.hint-time{background:rgba(59,130,246,0.15);color:#60a5fa}}
`;
  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);
})();

if(typeof module!=='undefined'&&module.exports)module.exports=KitchenHints;
