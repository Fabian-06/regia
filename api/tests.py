"""Tests de la API. Responsable: persona 6.

Los tests de TestPendingEndpoints describen el esqueleto recién creado.
Cuando implementéis un endpoint, su test de "pendiente" fallará: es la señal
para sustituirlo por tests del comportamiento real.
"""
from django.test import TestCase
from django.urls import reverse


class TestHealth(TestCase):
    def test_health_responde_ok(self):
        response = self.client.get(reverse("api:health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")


class TestPendingEndpoints(TestCase):
    def test_get_pendientes_devuelven_501(self):
        for name in ("api:stations", "api:context"):
            with self.subTest(endpoint=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 501)
                self.assertEqual(response.json()["error"], "pendiente")

    def test_post_pendientes_devuelven_501(self):
        for name in ("api:route", "api:assistant"):
            with self.subTest(endpoint=name):
                response = self.client.post(
                    reverse(name), data="{}", content_type="application/json"
                )
                self.assertEqual(response.status_code, 501)
                self.assertEqual(response.json()["error"], "pendiente")


class TestMethods(TestCase):
    def test_route_no_admite_get(self):
        response = self.client.get(reverse("api:route"))
        self.assertEqual(response.status_code, 405)
