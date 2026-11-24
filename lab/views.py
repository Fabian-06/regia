"""Vistas del Laboratorio A*. Responsable: persona 6."""
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie  # deja la cookie "csrftoken" que necesitan los POST a /api/
def index(request):
    """Página del laboratorio: A* paso a paso y comparación con Dijkstra."""
    return render(request, "lab/lab.html")
