# rcpbx v2 — Complete Package

Mobile-first redesign, 3x5 print, fridge reference, easter eggs, real counter.

---

## Files

```
rcpbx-final/
├── index.html           ← New homepage
├── recipe-template.html ← Recipe page with 3x5 print
├── css-additions.css    ← Add to your style.css
├── reference/
│   └── index.html       ← Kitchen reference (fridge print)
└── js/
    ├── easter-eggs.js   ← Easter eggs + real counter
    └── kitchen-hints.js ← Contextual hints (optional)
```

---

## Print Features

### Recipe → 3x5 Index Card
- Click "🗃️ 3×5 Card" button on recipe page
- Set printer to 3x5 or 4x6 index card size
- Or "Save as PDF" to see the compact layout
- Two-column: ingredients left, steps right

### Reference → Fridge Sheet
- Click "🧲 Print for Fridge" on reference page
- Prints to letter size, 3-column compact grid
- All sections visible

---

## View Counter (Real)

Uses counterapi.dev — free, no signup.

Edit `js/easter-eggs.js` line 13:
```javascript
counterNamespace: 'rcpbx-com',  // ← your unique name
```

---

## Deployment

1. Replace `index.html`
2. Add `css-additions.css` to end of `css/style.css`
3. Upload `reference/` folder
4. Upload `js/` files
5. Use `recipe-template.html` for recipe pages

---

## Easter Eggs

| Trigger | Result |
|---------|--------|
| Hover logo | Expands, vowels fall slowly |
| Search "life story" | Snarky response |
| ↑↑↓↓←→←→BA | Achievement Unlocked |
| Check all ingredients | Confetti 🎉 |
| Click footer | Escalating messages |

---

*Now go cook something.*
