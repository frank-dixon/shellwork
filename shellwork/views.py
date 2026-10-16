from django.shortcuts import get_object_or_404, render

from .models import Breed, BreedingPairing, Citation, GlossaryTerm

TAB = {"white": "mint", "cream": "mint", "light-brown": "pink", "brown": "pink", "dark-brown": "pink",
       "blue": "lav", "green": "lav", "variable": "lav"}
SWATCH = {"white": "#F3F0E8", "cream": "#E1C8A6", "light-brown": "#D2A67A", "brown": "#B37B52",
          "dark-brown": "#6A3A26", "blue": "#A8CCD3", "green": "#8E9A5C", "variable": "#B7CBA6"}


def _breeds():
    return Breed.objects.filter(published=True).prefetch_related("photos", "citations")


def _cats():
    used = set(Breed.objects.filter(published=True).values_list("egg_color_category", flat=True))
    return [(k, v, SWATCH[k]) for k, v in Breed.COLOR_CATEGORIES if k in used]


def index(request):
    breeds = list(_breeds())
    for b in breeds:
        b.tab = TAB[b.egg_color_category]
    return render(request, "shellwork/index.html", {
        "breeds": breeds, "cats": _cats(), "sizes": Breed.SIZES,
        "shapes": sorted({b.egg_shape for b in breeds}),
        "pairings": BreedingPairing.objects.select_related("parent_a", "parent_b")[:3],
    })


def breed_detail(request, slug):
    b = get_object_or_404(_breeds(), slug=slug)
    b.tab = TAB[b.egg_color_category]
    pairings = BreedingPairing.objects.select_related("parent_a", "parent_b", "source").filter(parent_a=b) | \
        BreedingPairing.objects.filter(parent_b=b)
    cites = list(b.citations.all())
    return render(request, "shellwork/breed.html", {"b": b, "cites": cites, "pairings": pairings.distinct()})


def helper(request):
    target = request.GET.get("colour", "")
    pairs = BreedingPairing.objects.select_related("parent_a", "parent_b", "source")
    targets = [(k, v, SWATCH[k]) for k, v in Breed.COLOR_CATEGORIES if pairs.filter(target_color_category=k).exists()]
    # Every pairing and every "already lays it" list is rendered; the chosen colour is shown and the rest
    # are hidden. helper.js re-applies ?colour= in the browser, so a static freeze of this one page works.
    layers = [(k, list(Breed.objects.filter(published=True, egg_color_category=k))) for k, _, _ in targets]
    return render(request, "shellwork/helper.html", {"targets": targets, "target": target, "pairs": pairs, "layers": layers})


def compare(request):
    # All breeds are rendered as hidden columns; compare.js shows the ?b= ones in order, so the page also
    # works as a static file. The server marks the requested ones visible for no-JS readers.
    slugs = [s for s in request.GET.get("b", "").split(",") if s][:3]
    return render(request, "shellwork/compare.html", {"breeds": list(_breeds()), "slugs": slugs})


def glossary(request):
    return render(request, "shellwork/glossary.html", {"terms": GlossaryTerm.objects.select_related("citation")})


def sources(request):
    return render(request, "shellwork/sources.html", {"cites": Citation.objects.select_related("breed").order_by("kind", "publisher", "breed__name")})


def offline(request):
    return render(request, "shellwork/offline.html")
