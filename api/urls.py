"""Rutas de la API. Responsable: persona 6.

Estas direcciones son parte del contrato con el frontend: no las cambiéis sin
avisar a las personas 5 y 4.
"""
from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("stations/", views.stations, name="stations"),
    path("context/", views.context, name="context"),
    path("route/", views.route, name="route"),
    path("assistant/", views.assistant, name="assistant"),
]
