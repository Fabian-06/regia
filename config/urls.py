"""Rutas principales. Cada módulo define las suyas en su propio urls.py."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),   # persona 6
    path("lab/", include("lab.urls")),   # persona 6
    path("", include("web.urls")),       # persona 5
]
