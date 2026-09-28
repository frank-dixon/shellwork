# Shellwork

An immersive full-viewport **hen↔egg journey** — Phase 1 covers shell **color**, **shape**, and **size** only (no breeding calculator). Continuous ambient motion, parallax layers, and soft scene transitions; cream UI with turquoise accent.

Hub: [frank-dixon.github.io](https://frank-dixon.github.io/)

## Local edit

```bash
npm i
npm run watch   # or: npm start
```

One watcher does both:

- **Tailwind** — `src/input.css` → `docs/css/shellwork.css`
- **JS minify** — commented `src/js/experience.js` → `docs/js/experience.js`

Open `docs/index.html` (or serve `docs/`). Prefer Tailwind utilities in HTML.

```bash
npm run build   # css + js once before commit
```

## Live demo

**https://frank-dixon.github.io/shellwork/**

GitHub Pages serves `/docs` from `main`. Portfolio micro-projects always commit, push, and deploy Pages on update.
