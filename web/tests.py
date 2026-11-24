"""Tests de la interfaz. Responsable: persona 5."""
from django.test import TestCase
from django.urls import reverse


class TestPlanner(TestCase):
    def test_la_pagina_principal_carga(self):
        response = self.client.get(reverse("web:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/planner.html")

    def test_la_pagina_deja_la_cookie_csrf(self):
        response = self.client.get(reverse("web:index"))
        self.assertIn("csrftoken", response.cookies)
