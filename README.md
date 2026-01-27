# rcpbx v2 — Complete Package

Mobile-first redesign, 3x5 print, easter eggs, indie footer with real counter.

---

## Files

```
rcpbx-final/
├── index.html           ← New homepage
├── css-additions.css    ← Add to your style.css
├── reference/
│   └── index.html       ← Kitchen reference page
└── js/
    ├── easter-eggs.js   ← Easter eggs + real counter
    └── kitchen-hints.js ← Contextual hints (optional)
```

---

## The View Counter (REAL DATA)

Uses **counterapi.dev** — free, no signup, tracks actual visits.

### How it works:
- First visit in a session → increments counter
- Same session, different pages → just shows current count
- Data persists on their servers forever
- Shows "..." while loading, "—" if API fails

### Setup:

1. Open `js/easter-eggs.js`
2. Find the CONFIG at the top:

```javascript
const CONFIG = {
  counterNamespace: 'rcpbx-com',  // ← YOUR unique name here
  counterKey: 'visits',
};
```

3. Change `counterNamespace` to something unique for your site

That's it. Counter auto-creates on first visit. No signup, no API keys, no bullshit.

---

## Deployment (GitHub Browser)

### 1. Replace Homepage
- Edit `index.html` → delete all → paste from this package
- Commit: "Redesign homepage"

### 2. Add CSS
- Edit `css/style.css` → scroll to bottom → paste `css-additions.css`
- Commit: "Add mobile + print styles"

### 3. Upload Reference
- Add file → Upload → drag `reference` folder
- Commit: "Add kitchen reference"

### 4. Upload JS
- Go to `js` folder → Upload both JS files
- Commit: "Add easter eggs"

### 5. Add Print Button to Recipes
In `.recipe-controls`:
```html
<button class="print-btn" onclick="window.print()">
  <span>🗃️</span> 3×5
</button>
```

---

## What You Get

### Footer
```
rcpbx · 1,247 meals inspired · $0 raised · never acquired
        ↑ real number
```

### Easter Eggs
| Trigger | Result |
|---------|--------|
| Hover logo | Expands to "recipe box" |
| Search "life story" | 🙄 Not here. Just recipes. |
| Search "ads" | 🚫 Nope. Never. |
| ↑↑↓↓←→←→BA | Achievement Unlocked |
| Check all ingredients | Confetti 🎉 |
| Hover "never acquired" | Snarky tooltip |
| Click footer | Escalating messages |

### Mobile
- 48px touch targets
- iOS safe areas
- Fixed thumb-zone controls

### 3x5 Print
- Fits index cards
- Cute ♨ icon

---

No build step. No dependencies. Real data.

*Now go cook something.*
