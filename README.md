# Shellwork

An immersive full-viewport **hen↔egg journey** — Phase 1 covers shell **color**, **shape**, and **size** only (no breeding calculator). Searchable / filterable catalog of **30+ hen breeds** paired with egg color families (white, tinted, brown, dark chocolate, blue, green-olive), continuous ambient motion, parallax layers, and soft scene transitions; cream UI with turquoise accent (`#0B8A8F`).

Hub: [frank-dixon.github.io](https://frank-dixon.github.io/)

Primary sources cited on-page: [Koops Coops](https://www.koopscoops.com/), [Murray McMurray Hatchery](https://www.mcmurrayhatchery.com/), [Cackle Hatchery](https://www.cacklehatchery.com/chicken-breeds/).

## Local edit

```bash
npm i
npm run watch   # or: npm start
```

One watcher does both:

- **Tailwind** — `src/input.css` → `docs/css/shellwork.css`
- **JS bundle** — `src/js/experience.js` + `src/js/breeds.js` → `docs/js/experience.js`

Open `docs/index.html` (or serve `docs/`). Prefer Tailwind utilities in HTML.

```bash
npm run build   # css + js once before commit
```

## Live demo

**https://frank-dixon.github.io/shellwork/**

GitHub Pages serves `/docs` from `main`. Portfolio micro-projects always commit, push, and deploy Pages on update.
