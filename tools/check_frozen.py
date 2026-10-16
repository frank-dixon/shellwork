"""Playwright smoke test of a frozen build served with the Pages root layout.

    python -m http.server 8765 -d <dir containing shellwork/>   # e.g. a frank-dixon.github.io checkout
    python tools/check_frozen.py http://127.0.0.1:8765
"""
import sys
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765").rstrip("/")
fails = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in (390, 1280):
        ctx = browser.new_context(viewport={"width": width, "height": 844 if width == 390 else 900},
                                  is_mobile=width == 390, has_touch=width == 390)
        page = ctx.new_page()
        bad = []
        page.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 and BASE in r.url else None)
        page.on("pageerror", lambda e: bad.append(f"js: {e}"))
        tag = f"[{width}]"
        slugs = []
        for path in ["/shellwork/", "/shellwork/breed/welsummer/", "/shellwork/breed-for-a-colour/",
                     "/shellwork/compare/", "/shellwork/glossary/", "/shellwork/sources/", "/shellwork/offline/"]:
            r = page.goto(BASE + path, wait_until="networkidle")
            check(r.status == 200, f"{tag} {path} 200")
            if path == "/shellwork/":
                slugs = sorted(set(page.eval_on_selector_all("a[href*='/shellwork/breed/']",
                                   "as=>as.map(a=>new URL(a.href).pathname)")))
        check(len(slugs) == 17, f"{tag} 17 breed links on index ({len(slugs)})")
        for s in slugs:
            check(page.goto(BASE + s).status == 200, f"{tag} {s}")
        page.goto(BASE + "/shellwork/breed/welsummer/", wait_until="networkidle")
        imgs = page.eval_on_selector_all("img", "is=>is.map(i=>[i.currentSrc,i.complete&&i.naturalWidth>0])")
        check(imgs and all(ok for _, ok in imgs), f"{tag} breed images load ({len(imgs)})")
        check(all("/shellwork/" in src for src, _ in imgs), f"{tag} images served from /shellwork/")
        page.goto(BASE + "/shellwork/breed-for-a-colour/?colour=blue", wait_until="networkidle")
        vis = page.eval_on_selector_all(".paircard", "cs=>cs.filter(c=>c.offsetParent).map(c=>c.dataset.cat)")
        check(vis and set(vis) == {"blue"}, f"{tag} ?colour=blue filters client-side {vis}")
        page.goto(BASE + "/shellwork/compare/?b=marans,welsummer", wait_until="networkidle")
        vis = page.eval_on_selector_all(".cmp__col", "cs=>cs.filter(c=>c.offsetParent).map(c=>c.dataset.slug)")
        check(sorted(vis) == ["marans", "welsummer"], f"{tag} compare ?b= shows {vis}")
        page.goto(BASE + "/shellwork/", wait_until="networkidle")
        scope = page.evaluate("""async()=>{const r=await navigator.serviceWorker.ready;return r.scope}""")
        check(scope == BASE + "/shellwork/", f"{tag} SW scope {scope}")
        man = page.evaluate("fetch(document.querySelector('link[rel=manifest]').href).then(r=>r.json())")
        check(man["scope"] == "/shellwork/", f"{tag} manifest scope {man['scope']}")
        page.reload(wait_until="networkidle")
        ctx.set_offline(True)
        page.goto(BASE + "/shellwork/", wait_until="domcontentloaded")
        check("Shellwork" in page.title(), f"{tag} index works offline")
        page.goto(BASE + "/shellwork/never-visited/", wait_until="domcontentloaded")
        check("offline" in page.content().lower(), f"{tag} offline fallback page")
        ctx.set_offline(False)
        check(not bad, f"{tag} no 4xx or JS errors {bad[:5]}")
        ctx.close()
    browser.close()
print("PASS" if not fails else f"{len(fails)} FAILED")
sys.exit(1 if fails else 0)
