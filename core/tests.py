"""Tests del esqueleto. Responsable: persona 6.

Comprueban que todos los módulos se pueden importar y que las funciones de
entrada existen con el nombre acordado. Si alguien renombra una de ellas sin
avisar, este test falla antes de que el error llegue a los demás.
"""
import importlib
from unittest import TestCase

ENTRY_POINTS = {
    "network.graph": ["build_graph"],
    "routing.astar": ["find_route"],
    "routing.dijkstra": ["find_route"],
    "routing.costs": ["edge_cost", "initial_wait"],
    "routing.heuristics": ["estimate"],
    "conditions.context": ["get_context"],
    "conditions.clock": ["now_monterrey", "is_service_open", "headways"],
    "conditions.weather": ["fetch_weather"],
    "assistant.llm": ["is_available", "complete"],
    "assistant.parser": ["parse_query"],
    "assistant.explainer": ["explain"],
}


class TestSkeleton(TestCase):
    def test_los_puntos_de_entrada_existen(self):
        for module_name, functions in ENTRY_POINTS.items():
            module = importlib.import_module(module_name)
            for function in functions:
                with self.subTest(function=f"{module_name}.{function}"):
                    self.assertTrue(callable(getattr(module, function, None)))

    def test_routing_no_depende_de_django(self):
        """routing debe poder probarse y explicarse sin el resto del proyecto."""
        import pathlib

        import routing

        folder = pathlib.Path(routing.__file__).parent
        for path in folder.glob("*.py"):
            if path.name == "tests.py":
                continue
            with self.subTest(file=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertNotIn("import django", source)
                self.assertNotIn("from django", source)
