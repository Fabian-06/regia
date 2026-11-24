"""Vistas de la interfaz. Responsable: persona 5.

Las vistas solo entregan la página. Los datos (estaciones, rutas, clima) los
pide el JavaScript a /api/ con fetch.
"""
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie  # deja la cookie "csrftoken" que necesitan los POST a /api/
def index(request):
    """Página principal: el planificador de rutas."""
    return render(request, "web/planner.html")
