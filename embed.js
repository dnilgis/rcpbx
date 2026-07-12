/**
 * rcpbx Embed Widget
 * Drop this on any site to embed a recipe card:
 * <div class="rcpbx-embed" data-recipe="chicken-parmesan"></div>
 * <script src="https://rcpbx.com/embed.js"></script>
 */
(function() {
  const style = document.createElement('style');
  style.textContent = `
    .rcpbx-card {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 1rem;
      max-width: 400px;
      background: #fff;
    }
    .rcpbx-card a { color: #16a34a; text-decoration: none; }
    .rcpbx-card a:hover { text-decoration: underline; }
    .rcpbx-card h3 { margin: 0 0 0.5rem; font-size: 1.1rem; }
    .rcpbx-card p { margin: 0 0 0.75rem; color: #666; font-size: 0.9rem; }
    .rcpbx-card .meta { font-size: 0.8rem; color: #999; }
    .rcpbx-card .meta span { margin-right: 1rem; }
    .rcpbx-branding { font-size: 0.7rem; color: #999; margin-top: 0.5rem; }
  `;
  document.head.appendChild(style);

  document.querySelectorAll('.rcpbx-embed').forEach(async (el) => {
    const id = el.dataset.recipe;
    if (!id) return;
    
    try {
      const res = await fetch(`https://rcpbx.com/data/${id}.json`);
      const recipe = await res.json();
      
      el.innerHTML = `
        <div class="rcpbx-card">
          <h3><a href="https://rcpbx.com/recipes/${id}/" target="_blank">${recipe.title}</a></h3>
          <p>${recipe.tagline || ''}</p>
          <div class="meta">
            <span>⏱ ${recipe.prep || ''} + ${recipe.cook || ''}</span>
            <span>🍽 ${recipe.serves || recipe.makes || ''}</span>
          </div>
          <div class="rcpbx-branding">via <a href="https://rcpbx.com" target="_blank">rcpbx.com</a></div>
        </div>
      `;
    } catch (e) {
      el.innerHTML = `<p>Recipe not found. <a href="https://rcpbx.com">Browse rcpbx →</a></p>`;
    }
  });
})();
