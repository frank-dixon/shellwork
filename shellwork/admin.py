from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Breed, BreedingPairing, Citation, GlossaryTerm, Photo


def thumb(obj, size=72):
    if obj and obj.image:
        return format_html('<img src="{}" style="height:{}px;width:auto;border-radius:6px;object-fit:cover" alt="">', obj.image.url, size)
    return "—"


class PhotoInline(StackedInline):
    model = Photo
    extra = 0
    readonly_fields = ["preview"]
    fields = [("kind", "image", "preview"), "caption", ("author", "license_name", "license_url"), "source_url", "attribution_text", "permission_note"]

    @admin.display(description="Preview")
    def preview(self, obj):
        return thumb(obj, 120)


class CitationInline(TabularInline):
    model = Citation
    extra = 0
    fields = ["publisher", "title", "url", "accessed", "kind", "supports"]


@admin.register(Breed)
class BreedAdmin(ModelAdmin):
    list_display = ["swatch", "name", "egg_color_name", "egg_color_category", "egg_size", "lay_rate", "hen_status", "egg_status", "n_citations", "published"]
    list_display_links = ["swatch", "name"]
    list_filter = ["published", "egg_color_category", "egg_size", "shape_confidence", "autosexing", "is_cross", "photos__kind"]
    search_fields = ["name", "slug", "origin", "egg_color_name", "temperament", "genetics_notes", "breeding_notes"]
    prepopulated_fields = {"slug": ["name"]}
    list_editable = ["published"]
    readonly_fields = ["egg_preview"]
    inlines = [PhotoInline, CitationInline]
    fieldsets = [
        (None, {"fields": [("name", "slug"), ("published", "is_cross", "sort_order"), "origin"]}),
        ("Egg", {"fields": ["egg_preview", ("egg_color_name", "egg_color_category"), ("egg_hex", "speckle_density", "speckle_hex", "shell_finish"),
                            ("egg_size", "egg_size_note"), ("egg_shape", "shape_confidence")]}),
        ("Hen", {"fields": [("lay_rate_min", "lay_rate_max"), "temperament", ("broodiness", "autosexing")]}),
        ("Notes", {"fields": ["genetics_notes", "breeding_notes"]}),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("photos", "citations")

    @admin.display(description="")
    def swatch(self, obj):
        return format_html('<span style="display:inline-block;width:18px;height:23px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:{};box-shadow:inset -3px -3px 5px rgba(0,0,0,.25)"></span>', obj.egg_hex)

    @admin.display(description="Egg render")
    def egg_preview(self, obj):
        if not obj.pk:
            return "Save to preview"
        return format_html(
            '<div style="display:flex;gap:16px;align-items:end"><span style="display:inline-block;width:56px;height:72px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;'
            'background:radial-gradient(ellipse 30% 20% at 36% 28%,rgba(255,255,255,.7),transparent 70%),radial-gradient(ellipse 90% 90% at 72% 82%,rgba(0,0,0,.35),transparent 60%),{}"></span>{}</div>',
            obj.egg_hex, thumb(obj.egg_photo, 90) if obj.egg_photo else "No egg photo")

    @admin.display(description="Hen photo")
    def hen_status(self, obj):
        p = next((p for p in obj.photos.all() if p.kind == "hen"), None)
        return thumb(p, 40) if p else mark_safe('<b style="color:#b00">missing</b>')

    @admin.display(description="Egg photo")
    def egg_status(self, obj):
        p = next((p for p in obj.photos.all() if p.kind == "egg"), None)
        return thumb(p, 40) if p else mark_safe('<b style="color:#b00">missing</b>')

    @admin.display(description="Sources")
    def n_citations(self, obj):
        return len(obj.citations.all())


@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
    list_display = ["preview", "breed", "kind", "author", "license_name", "source_link"]
    list_filter = ["kind", "license_name", "breed"]
    search_fields = ["breed__name", "author", "caption", "attribution_text"]
    readonly_fields = ["preview_large"]
    autocomplete_fields = ["breed"]

    @admin.display(description="")
    def preview(self, obj):
        return thumb(obj, 56)

    @admin.display(description="Preview")
    def preview_large(self, obj):
        return thumb(obj, 260)

    @admin.display(description="Source")
    def source_link(self, obj):
        return format_html('<a href="{}" target="_blank" rel="noopener">Commons page</a>', obj.source_url)


@admin.register(Citation)
class CitationAdmin(ModelAdmin):
    list_display = ["publisher", "title", "breed", "kind", "supports", "accessed"]
    list_filter = ["kind", "publisher", "breed"]
    search_fields = ["title", "publisher", "url", "supports", "excerpt"]


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(ModelAdmin):
    list_display = ["term", "citation"]
    search_fields = ["term", "definition"]
    prepopulated_fields = {"slug": ["term"]}


@admin.register(BreedingPairing)
class BreedingPairingAdmin(ModelAdmin):
    list_display = ["__str__", "target_color_category", "confidence", "source"]
    list_filter = ["target_color_category", "confidence"]
    search_fields = ["parent_a__name", "parent_b__name", "expected_egg_color", "explanation"]
    autocomplete_fields = ["parent_a", "parent_b"]
    readonly_fields = ["offspring_preview"]
    fieldsets = [
        (None, {"fields": [("parent_a", "parent_b"), "parent_b_label", "variety_note", ("target_color_category", "expected_egg_color"), "explanation", ("confidence", "source")]}),
        ("Offspring egg", {"fields": ["offspring_preview", ("offspring_hex", "offspring_speckle_density", "offspring_speckle_hex", "offspring_finish")]}),
    ]

    @admin.display(description="Egg render")
    def offspring_preview(self, obj):
        return format_html('<span style="display:inline-block;width:56px;height:72px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;'
                           'background:radial-gradient(ellipse 30% 20% at 36% 28%,rgba(255,255,255,.7),transparent 70%),radial-gradient(ellipse 90% 90% at 72% 82%,rgba(0,0,0,.35),transparent 60%),{}"></span>',
                           obj.offspring_hex if obj else "#ccc")

