"""PWA endpoints, modelled on frank-dixon-site pages/pwa.py: the shell list is
fingerprinted so the cache name changes whenever a shell file changes."""
import hashlib
import json
from functools import lru_cache

from django.contrib.staticfiles import finders
from django.http import HttpResponse, JsonResponse
from django.templatetags.static import static
from django.urls import reverse

SHELL_FILES = ["shellwork/css/shellwork.css", "shellwork/js/rolodex.js", "shellwork/js/compare.js", "shellwork/js/helper.js", "shellwork/js/compare-page.js",
               "shellwork/icons/icon-192.png", "shellwork/icons/icon-512.png"]


@lru_cache(maxsize=1)
def shell_fingerprint():
    h = hashlib.sha256()
    for f in SHELL_FILES:
        p = finders.find(f)
        if p:
            with open(p, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()[:12]


def manifest(request):
    return JsonResponse({
        "name": "Shellwork: breed reference by egg", "short_name": "Shellwork",
        "start_url": reverse("shellwork:index"), "scope": reverse("shellwork:index"),
        "display": "standalone", "background_color": "#18191B", "theme_color": "#18191B",
        "icons": [{"src": static("shellwork/icons/icon-192.png"), "sizes": "192x192", "type": "image/png"},
                  {"src": static("shellwork/icons/icon-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
    }, content_type="application/manifest+json")


SW = """const CACHE='shellwork-%(fp)s';
const SHELL=%(shell)s;
const OFFLINE='%(offline)s';
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL.concat([OFFLINE,'%(index)s']))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('shellwork-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
 if(r.mode==='navigate'){e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res}).catch(()=>caches.match(r).then(m=>m||caches.match(OFFLINE))));return}
 if(u.origin===location.origin||u.host.endsWith('gstatic.com')||u.host.endsWith('googleapis.com')){
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok||res.type==='opaque'){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp))}return res})))}});
"""


def service_worker(request):
    body = SW % {"fp": shell_fingerprint(), "shell": json.dumps([static(f) for f in SHELL_FILES]),
                 "offline": reverse("shellwork:offline"), "index": reverse("shellwork:index")}
    resp = HttpResponse(body, content_type="application/javascript")
    resp["Service-Worker-Allowed"] = reverse("shellwork:index")
    resp["Cache-Control"] = "no-cache"
    return resp
