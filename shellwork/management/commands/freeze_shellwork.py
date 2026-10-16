"""Render Shellwork to static files for frank-dixon.github.io/shellwork/.

    DEBUG=false python manage.py freeze_shellwork --out build/shellwork

The output directory IS the shellwork/ folder: index.html, breed/<slug>/,
breed-for-a-colour/, compare/, glossary/, sources/, offline/,
manifest.webmanifest, sw.js, static/ (collectstatic, no admin assets) and
media/. Admin is never written. ?colour= and ?b= filtering runs client-side
on the static copy (helper.js, compare-page.js).
"""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test import Client, override_settings

from shellwork.models import Breed

PREFIX = "/shellwork/"
STATIC_SKIP = {"admin", "unfold"}  # top-level static dirs that only the admin uses


def pages():
    urls = [PREFIX, PREFIX + "breed-for-a-colour/", PREFIX + "compare/", PREFIX + "glossary/",
            PREFIX + "sources/", PREFIX + "offline/", PREFIX + "manifest.webmanifest", PREFIX + "sw.js"]
    urls += [f"{PREFIX}breed/{s}/" for s in Breed.objects.filter(published=True).values_list("slug", flat=True)]
    return urls


def target_for(url):
    rel = url[len(PREFIX):]
    return rel if rel and not rel.endswith("/") else rel + "index.html"


class Command(BaseCommand):
    help = "Freeze Shellwork into a static directory (the contents of /shellwork/)."

    def add_arguments(self, parser):
        parser.add_argument("--out", default="build/shellwork", help="Output directory (emptied first).")

    def handle(self, *args, out, **options):
        if settings.DEBUG:
            raise CommandError("Run with DEBUG=false so the frozen copy uses hashed static files.")
        if settings.STATIC_URL != PREFIX + "static/" or settings.MEDIA_URL != PREFIX + "media/":
            raise CommandError("STATIC_URL/MEDIA_URL must live under /shellwork/.")
        if not Breed.objects.filter(published=True).exists():
            raise CommandError("No published breeds. Run migrate and load_shellwork (or add breeds in admin) first.")
        out = Path(out).resolve()
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)

        call_command("collectstatic", interactive=False, verbosity=0, clear=True)

        with override_settings(ALLOWED_HOSTS=["testserver"], SECURE_SSL_REDIRECT=False):
            client = Client()
            urls = pages()
            for url in urls:
                r = client.get(url)
                if r.status_code != 200:
                    raise CommandError(f"{url} returned {r.status_code}")
                path = out / target_for(url)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(r.content)
                self.stdout.write(f"  {url} -> {path.relative_to(out)}")

        root = Path(settings.STATIC_ROOT)

        def skip(d, names):
            drop = [n for n in names if n.endswith((".gz", ".br"))]
            if Path(d) == root:
                drop += [n for n in names if n in STATIC_SKIP or n == "staticfiles.json"]
            return drop

        shutil.copytree(root, out / "static", ignore=skip)
        media = Path(settings.MEDIA_ROOT)
        if media.exists():
            shutil.copytree(media, out / "media")
        self.stdout.write(self.style.SUCCESS(f"Froze {len(urls)} pages plus static/ and media/ into {out}"))
