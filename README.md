# Shellwork

A laying-hen egg **flip-zine** — Phase 1 covers shell **color**, **shape**, and **size** only (no breeding calculator).

Hub: [frank-dixon.github.io](https://frank-dixon.github.io/)

## Local edit

```bash
npm i
npm run watch   # or: npm start
```

One watcher does both:

- **Tailwind** — `src/input.css` → `docs/css/shellwork.css`
- **JS minify** — commented `src/js/zine.js` → `docs/js/zine.js`

Open `docs/index.html` (or serve `docs/`). Prefer Tailwind utilities in HTML.

```bash
npm run build   # css + js once before commit
```

## Deploy

GitHub Pages is **not** enabled yet. Push is for review only until Frank says deploy/ship.
