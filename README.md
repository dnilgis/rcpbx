# rcpbx Complete Update Package

All changes from our sessions compiled into one deployment.

## What's Included

### New Features
- ✅ **Animated logo**: `>rcpbx` expands to `>recipebox` on hover, vowels fall away on leave
- ✅ **Homepage redesign**: Two-panel layout with sidebar reference
- ✅ **Kitchen reference PDF**: Full-page 3-column print that fits on 2 pages
- ✅ **Recipe 3x5 print**: Print recipes as index cards
- ✅ **Mobile padding fix**: Prep data no longer clips edge on iPhone
- ✅ **iOS safe areas**: Proper padding for notched devices
- ✅ **Easter eggs**: Search responses, Konami code
- ✅ **View counter**: Real counter in footer via counterapi.dev
- ✅ **Google Analytics**: Ready to configure (replace G-XXXXXXXXXX)

---

## Files to Deploy

### Replace These Files

| Your File | Replace With |
|-----------|--------------|
| `index.html` (root) | `index.html` from this package |
| `reference/index.html` | `reference/index.html` from this package |

### Update All Recipe Pages

For every recipe HTML file, make these changes:

#### 1. Replace the logo HTML

Find:
```html
<a class="logo" href="/">rcpbx</a>
```
or similar, and replace with:
```html
<a href="/" class="logo-container" tabindex="0">
  <span class="logo-text">
    <span class="logo-prefix">&gt;</span><span class="logo-char">r</span><span class="logo-vowel v-e1">e</span><span class="logo-char">c</span><span class="logo-vowel v-i">i</span><span class="logo-char">p</span><span class="logo-vowel v-e2">e</span><span class="logo-char">b</span><span class="logo-vowel v-o">o</span><span class="logo-char">x</span>
  </span>
</a>
```

#### 2. Add the CSS

Either add `css/additions.css` to your CSS folder and link it:
```html
<link rel="stylesheet" href="/css/additions.css">
```

Or copy the contents into your existing `style.css`.

#### 3. Add the JS

Add `js/rcpbx.js` to your JS folder and include it:
```html
<script src="/js/rcpbx.js"></script>
```

#### 4. Fix prep data padding (recipe pages)

Make sure your `.prep-data` has this CSS:
```css
.prep-data {
  padding: 1rem 1.25rem;
}
@media (max-width: 700px) {
  .prep-data {
    padding: 1rem;
    margin: 0;
  }
}
```

---

## Google Analytics Setup

In `index.html` and `reference/index.html`, find:
```
G-XXXXXXXXXX
```
Replace with your actual GA4 Measurement ID (looks like `G-ABC123XYZ`).

---

## Quick Checklist

- [ ] Replace `index.html`
- [ ] Replace `reference/index.html`
- [ ] Add `css/additions.css` (or merge into style.css)
- [ ] Add `js/rcpbx.js`
- [ ] Update logo HTML on all recipe pages
- [ ] Update logo HTML on all category pages
- [ ] Replace `G-XXXXXXXXXX` with your GA4 ID
- [ ] Test animated logo on desktop (hover)
- [ ] Test animated logo on mobile (tap)
- [ ] Test Print/PDF on kitchen reference
- [ ] Test 3x5 print on a recipe page

---

## File Structure

```
rcpbx-complete/
├── index.html              ← New homepage
├── reference/
│   └── index.html          ← Kitchen reference with PDF print
├── recipes/
│   └── template.html       ← Recipe template with 3x5 print
├── css/
│   └── additions.css       ← New CSS to add
├── js/
│   └── rcpbx.js            ← Interactive features
└── README.md               ← This file
```

---

## Logo Animation Details

**Resting state**: `>rcpbx`
**Hover/tap state**: `>recipebox` (vowels fill in with staggered timing)
**Leave state**: Vowels fall down and fade, letters squeeze back together

The `>` prefix uses your accent color (green) to match section headers.

---

## Notes

- The view counter uses [counterapi.dev](https://counterapi.dev) - free, no signup required
- Easter eggs trigger on exact search matches (try: hello, bacon, 42, ramsay)
- Konami code: ↑↑↓↓←→←→BA
- 3x5 print works best in Chrome/Edge (Safari may need manual page size)
