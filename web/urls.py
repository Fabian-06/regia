"""Rutas de la interfaz. Responsable: persona 5."""
from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
]
