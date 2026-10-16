# Shellwork

A reference manual for choosing chicken breeds by egg shell color, shape and size.
Standalone Django project (Django 6.1.2, Unfold admin). Everything is served under
`/shellwork/`, including static (`/shellwork/static/`) and media (`/shellwork/media/`),
and it is published as a static freeze to https://frank-dixon.github.io/shellwork/.

The static-zine version that used to live in this repo is kept on the `legacy-zine`
branch and tag.

## Local dev (port 8040)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # DEBUG=true for local dev
python manage.py migrate
python manage.py load_shellwork   # breeds, photos, citations, glossary, pairings from shellwork/data/
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8040
```

- Site: http://127.0.0.1:8040/shellwork/ (`/` redirects there)
- Admin: http://127.0.0.1:8040/admin/

All content is edited in the admin. The SQLite db (`db.sqlite3`) and `media/` are the
source of truth for publishing. `load_shellwork` wipes and reloads the seed, so don't
run it after making admin edits you want to keep.

Port 8040 avoids the personal site's ports (Caddy on 8000, frank-dixon-site on 8030).

## Tests

```bash
DEBUG=true python manage.py test shellwork
```

## Publish

`bin/publish` freezes every public page (index, every published breed, the
breed-for-a-colour helper, compare, glossary, sources, offline, manifest and sw.js) plus
static (without admin assets) and media. It writes them into the `shellwork/` folder of a
frank-dixon.github.io checkout. It deletes and replaces only that folder. It refuses to
start on a dirty checkout, and it aborts without committing if any path outside
`shellwork/` changed.

```bash
bin/publish --dry-run                                   # build to a temp dir only
bin/publish --repo ../frank-dixon.github.io             # replace shellwork/ and commit locally
bin/publish --repo ../frank-dixon.github.io --push      # ...push and wait for the Pages build
```

You can set `SHELLWORK_PAGES_REPO` instead of passing `--repo`. `--push` pulls first
(fast-forward only) and waits for the build using `gh api .../pages/builds/latest`.

To preview a build with the root layout:
`python -m http.server 8765 -d <dir containing shellwork/>`. Then run
`python tools/check_frozen.py http://127.0.0.1:8765` for the Playwright smoke test
(pages, filters, compare, service worker scope, offline mode and images at 390 and 1280).
