from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("shellwork/", include("shellwork.urls")),
    path("", RedirectView.as_view(url="/shellwork/", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += [re_path(r"^shellwork/media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})]
