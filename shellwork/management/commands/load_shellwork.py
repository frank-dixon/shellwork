import json
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from shellwork.models import Breed, BreedingPairing, Citation, GlossaryTerm, Photo

DATA = Path(__file__).resolve().parents[2] / "data"


class Command(BaseCommand):
    help = "Load (or reload) Shellwork breeds, citations, photos, glossary and pairings from shellwork/data/seed.json."

    @transaction.atomic
    def handle(self, *args, **opts):
        seed = json.loads((DATA / "seed.json").read_text())
        BreedingPairing.objects.all().delete()
        GlossaryTerm.objects.all().delete()
        Citation.objects.all().delete()
        for p in Photo.objects.all():
            p.image.delete(save=False)
        Photo.objects.all().delete()

        general = {}
        for g in seed["general_citations"]:
            g = dict(g)
            key = g.pop("key")
            general[key] = Citation.objects.create(breed=None, **g)

        breeds = {}
        for b in seed["breeds"]:
            b = dict(b)
            cites, photos = b.pop("citations"), b.pop("photos")
            obj, _ = Breed.objects.update_or_create(slug=b["slug"], defaults=b)
            breeds[obj.slug] = obj
            for c in cites:
                Citation.objects.create(breed=obj, **c)
            for p in photos:
                p = dict(p)
                fn = p.pop("file")
                ph = Photo(breed=obj, **p)
                with open(DATA / "photos" / fn, "rb") as fh:
                    ph.image.save(fn, File(fh), save=False)
                ph.save()

        links = seed["genetic_links"]
        for slug in links["blue"]:
            for key in ("wang2013", "wragg2013"):
                g = general[key]
                Citation.objects.create(breed=breeds[slug], title=g.title, publisher=g.publisher, url=g.url, accessed=g.accessed,
                                        kind=g.kind, supports="genetics_notes", excerpt=g.excerpt)
        for slug in links["brown"]:
            g = general["samiullah2015"]
            Citation.objects.create(breed=breeds[slug], title=g.title, publisher=g.publisher, url=g.url, accessed=g.accessed,
                                    kind=g.kind, supports="genetics_notes", excerpt=g.excerpt)

        def resolve(ref):
            if ":" in ref:
                _, slug = ref.split(":", 1)
                return Citation.objects.filter(breed__slug=slug).first()
            return general[ref]

        for g in seed["glossary"]:
            GlossaryTerm.objects.create(term=g["term"], slug=slugify(g["term"]), definition=g["definition"], citation=resolve(g["cite"]))
        for p in seed["pairings"]:
            BreedingPairing.objects.create(parent_a=breeds[p["a"]], parent_b=breeds[p["b"]], target_color_category=p["cat"],
                                           expected_egg_color=p["color"], explanation=p["explanation"],
                                           confidence=p["confidence"], source=resolve(p["cite"]),
                                           variety_note=p.get("variety_note", ""), parent_b_label=p.get("parent_b_label", ""), **p.get("offspring", {}))
        self.stdout.write(self.style.SUCCESS(
            f"Loaded {Breed.objects.count()} breeds, {Photo.objects.count()} photos, {Citation.objects.count()} citations, "
            f"{GlossaryTerm.objects.count()} glossary terms, {BreedingPairing.objects.count()} pairings."))
