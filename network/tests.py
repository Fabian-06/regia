"""Tests de la red. Responsable: persona 1."""
from collections import deque

from django.test import SimpleTestCase

from core.contracts import EdgeKind
from network.graph import build_graph


class NetworkGraphTests(SimpleTestCase):
    def setUp(self):
        self.graph = build_graph()

    def test_counts(self):
        """38 estaciones, 3 líneas (19, 13 y 9 estaciones) y 41 nodos."""
        self.assertEqual(len(self.graph.stations), 38)
        self.assertEqual(len(self.graph.lines), 3)
        self.assertEqual(len(self.graph.lines["L1"].station_ids), 19)
        self.assertEqual(len(self.graph.lines["L2"].station_ids), 13)
        self.assertEqual(len(self.graph.lines["L3"].station_ids), 9)
        self.assertEqual(len(self.graph.edges), 41)

    def test_terminals(self):
        """Las terminales coinciden con el plano del enunciado."""
        l1 = self.graph.lines["L1"].station_ids
        l2 = self.graph.lines["L2"].station_ids
        l3 = self.graph.lines["L3"].station_ids

        self.assertEqual((l1[0], l1[-1]), ("talleres", "exposicion"))
        self.assertEqual((l2[0], l2[-1]), ("sendero", "general-i-zaragoza"))
        self.assertEqual((l3[0], l3[-1]), ("general-i-zaragoza", "hospital-metropolitano"))

    def test_transfers(self):
        """Existen exactamente los 3 transbordos en ambos sentidos (6 aristas TRANSFER)."""
        transfer_edges = [
            (e.source, e.target)
            for edge_list in self.graph.edges.values()
            for e in edge_list
            if e.kind == EdgeKind.TRANSFER
        ]
        expected = {
            (("cuauhtemoc", "L1"), ("cuauhtemoc", "L2")),
            (("cuauhtemoc", "L2"), ("cuauhtemoc", "L1")),
            (("general-i-zaragoza", "L2"), ("general-i-zaragoza", "L3")),
            (("general-i-zaragoza", "L3"), ("general-i-zaragoza", "L2")),
            (("felix-u-gomez", "L1"), ("felix-u-gomez", "L3")),
            (("felix-u-gomez", "L3"), ("felix-u-gomez", "L1")),
        }
        self.assertEqual(set(transfer_edges), expected)

    def test_bidirectional_edges(self):
        """Toda arista tiene su arista de vuelta con el mismo tipo, tiempo y distancia."""
        for node, edge_list in self.graph.edges.items():
            for edge in edge_list:
                reverse_edges = self.graph.edges.get(edge.target, [])
                has_reverse = any(
                    rev.target == node
                    and rev.kind == edge.kind
                    and rev.minutes == edge.minutes
                    and rev.meters == edge.meters
                    for rev in reverse_edges
                )
                self.assertTrue(has_reverse, f"Falta arista de vuelta para {edge}")

    def test_positive_values(self):
        """Ningún tiempo ni distancia es cero o negativo."""
        for edge_list in self.graph.edges.values():
            for edge in edge_list:
                self.assertGreater(edge.minutes, 0, f"Tiempo inválido en {edge}")
                self.assertGreater(edge.meters, 0, f"Distancia inválida en {edge}")

    def test_connected_graph(self):
        """Desde cualquier nodo se puede llegar a cualquier otro."""
        nodes = list(self.graph.edges.keys())
        self.assertTrue(nodes, "El grafo no tiene nodos")

        visited = {nodes[0]}
        queue = deque([nodes[0]])
        while queue:
            current = queue.popleft()
            for edge in self.graph.edges[current]:
                if edge.target not in visited:
                    visited.add(edge.target)
                    queue.append(edge.target)

        self.assertEqual(visited, set(nodes), "Hay nodos desconectados en el grafo")