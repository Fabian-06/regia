"""Tests del Laboratorio A*. Responsable: persona 6."""
from django.test import TestCase
from django.urls import reverse


class TestLab(TestCase):
    def test_la_pagina_del_laboratorio_carga(self):
        response = self.client.get(reverse("lab:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lab/lab.html")
