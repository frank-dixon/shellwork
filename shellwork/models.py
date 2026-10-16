from types import SimpleNamespace

from django.db import models
from django.urls import reverse


class Breed(models.Model):
    COLOR_CATEGORIES = [
        ("white", "White"), ("cream", "Cream / tinted"), ("light-brown", "Light brown"),
        ("brown", "Brown"), ("dark-brown", "Dark brown"), ("blue", "Blue"),
        ("green", "Green / olive"), ("variable", "Variable (blue/green/other)"),
    ]
    SIZES = [("S", "Small"), ("M", "Medium"), ("L", "Large"), ("XL", "Extra large")]
    SHAPE_CONFIDENCE = [("sourced", "Sourced"), ("unsourced", "Not sourced: varies by hen")]
    FINISHES = [("matte", "Matte / chalky bloom"), ("satin", "Satin"), ("gloss", "Glossy")]
    TRISTATE = [("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")]

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    is_cross = models.BooleanField(default=False, help_text="Hybrid/cross rather than a standardized breed.")
    origin = models.CharField(max_length=160, blank=True, help_text="Leave blank unless a citation supports it.")
    egg_color_name = models.CharField(max_length=120)
    egg_color_category = models.CharField(max_length=20, choices=COLOR_CATEGORIES)
    egg_hex = models.CharField("egg colour hex", max_length=7, default="#E8DCC8", help_text="Approximate on-screen colour, not measured.")
    speckle_density = models.FloatField(default=0, help_text="0 = none, 1 = heavy (drives CSS egg speckles).")
    speckle_hex = models.CharField(max_length=7, default="#4A2A1A")
    shell_finish = models.CharField(max_length=10, choices=FINISHES, default="satin")
    egg_size = models.CharField(max_length=2, choices=SIZES)
    egg_size_note = models.CharField(max_length=200, blank=True)
    egg_shape = models.CharField(max_length=120, default="Varies by hen")
    shape_confidence = models.CharField(max_length=10, choices=SHAPE_CONFIDENCE, default="unsourced")
    lay_rate_min = models.PositiveIntegerField(null=True, blank=True, help_text="Eggs per year")
    lay_rate_max = models.PositiveIntegerField(null=True, blank=True)
    temperament = models.CharField(max_length=200, blank=True)
    broodiness = models.CharField(max_length=120, blank=True)
    autosexing = models.CharField(max_length=8, choices=TRISTATE, default="unknown")
    genetics_notes = models.TextField(blank=True)
    breeding_notes = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shellwork:breed", args=[self.slug])

    @property
    def size_scale(self):
        return {"S": 0.8, "M": 0.9, "L": 1.0, "XL": 1.07}.get(self.egg_size, 1.0)

    @property
    def lay_rate(self):
        if self.lay_rate_min and self.lay_rate_max:
            return f"{self.lay_rate_min}–{self.lay_rate_max}"
        return "Not sourced"

    def photo(self, kind):
        return next((p for p in self.photos.all() if p.kind == kind), None)

    @property
    def hen_photo(self):
        return self.photo("hen")

    @property
    def egg_photo(self):
        return self.photo("egg")


class Citation(models.Model):
    KINDS = [("conservancy", "Conservation body"), ("hatchery", "Hatchery / vendor"),
             ("peer-reviewed", "Peer-reviewed"), ("other", "Other")]
    breed = models.ForeignKey(Breed, null=True, blank=True, on_delete=models.CASCADE, related_name="citations",
                              help_text="Blank for general sources (e.g. genetics papers).")
    title = models.CharField(max_length=300)
    publisher = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    accessed = models.DateField()
    kind = models.CharField(max_length=20, choices=KINDS, default="other")
    supports = models.CharField(max_length=300, help_text="Comma-separated field names this source backs, e.g. egg_color_name,egg_size")
    excerpt = models.TextField(blank=True, help_text="Short quote/paraphrase of what the source says.")

    class Meta:
        ordering = ["breed__name", "publisher"]

    def __str__(self):
        return f"{self.publisher}: {self.title}"

    FIELD_LABELS = {"egg_color_name": "egg color", "egg_size": "egg size", "lay_rate": "eggs per year", "temperament": "temperament",
                    "broodiness": "broodiness", "autosexing": "autosexing", "origin": "origin", "genetics_notes": "genetics",
                    "breeding_notes": "breeding notes", "glossary": "glossary", "status": "conservation status"}

    @property
    def supports_labels(self):
        return [self.FIELD_LABELS.get(f, f.replace("_", " ")) for f in self.supports_list]

    @property
    def supports_list(self):
        return [s.strip() for s in self.supports.split(",") if s.strip()]


class Photo(models.Model):
    KINDS = [("hen", "Hen"), ("egg", "Egg")]
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name="photos")
    kind = models.CharField(max_length=4, choices=KINDS, default="hen")
    image = models.ImageField(upload_to="shellwork/photos/")
    caption = models.CharField(max_length=300, blank=True)
    author = models.CharField(max_length=200)
    source_url = models.URLField(max_length=500)
    license_name = models.CharField(max_length=80)
    license_url = models.URLField(max_length=300, blank=True)
    attribution_text = models.CharField(max_length=400)
    permission_note = models.TextField(blank=True, help_text="For non-open images (e.g. hatchery photos): record written permission here before use.")

    class Meta:
        ordering = ["breed__name", "kind"]

    def __str__(self):
        return f"{self.breed} ({self.kind})"


class GlossaryTerm(models.Model):
    term = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    definition = models.TextField()
    citation = models.ForeignKey(Citation, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["term"]

    def __str__(self):
        return self.term


class BreedingPairing(models.Model):
    CONFIDENCE = [("sourced", "Stated by source"), ("inferred", "Inferred from genetics")]
    parent_a = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name="pairings_as_a")
    parent_b = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name="pairings_as_b")
    target_color_category = models.CharField(max_length=20, choices=Breed.COLOR_CATEGORIES)
    expected_egg_color = models.CharField(max_length=160)
    explanation = models.TextField()
    confidence = models.CharField(max_length=10, choices=CONFIDENCE, default="sourced")
    source = models.ForeignKey(Citation, null=True, blank=True, on_delete=models.SET_NULL)
    parent_b_label = models.CharField(max_length=120, blank=True, help_text="Shown instead of parent B's name when the source used another variety.")
    variety_note = models.CharField(max_length=200, blank=True, help_text="E.g. when the source used a different variety of a parent breed.")
    offspring_hex = models.CharField("offspring egg hex", max_length=7, default="#9AA66A", help_text="Approximate color of the expected offspring egg (drives the CSS egg).")
    offspring_speckle_density = models.FloatField(default=0, help_text="0 = none, 1 = heavy")
    offspring_speckle_hex = models.CharField(max_length=7, default="#4A3A1C")
    offspring_finish = models.CharField(max_length=10, choices=Breed.FINISHES, default="satin")

    def __str__(self):
        return f"{self.parent_a} × {self.parent_b} → {self.expected_egg_color}"

    @property
    def offspring(self):
        """Duck-types the Breed fields the CSS egg tag reads."""
        return SimpleNamespace(egg_hex=self.offspring_hex, speckle_density=self.offspring_speckle_density,
                               speckle_hex=self.offspring_speckle_hex, shell_finish=self.offspring_finish,
                               size_scale=1.0, egg_color_name=self.expected_egg_color)
