from django.urls import path

from . import pwa, views

app_name = "shellwork"
urlpatterns = [
    path("", views.index, name="index"),
    path("breed/<slug:slug>/", views.breed_detail, name="breed"),
    path("breed-for-a-colour/", views.helper, name="helper"),
    path("compare/", views.compare, name="compare"),
    path("glossary/", views.glossary, name="glossary"),
    path("sources/", views.sources, name="sources"),
    path("offline/", views.offline, name="offline"),
    path("manifest.webmanifest", pwa.manifest, name="manifest"),
    path("sw.js", pwa.service_worker, name="sw"),
]
